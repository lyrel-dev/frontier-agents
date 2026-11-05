#!/usr/bin/env python3
"""Offline consistency and selected semantic checks for the phase-one contracts.

This is not an API server, scheduler, provider adapter, authorization engine or CEL
evaluator. JSON numbers are read as Decimal. Source digests are checked only for
the documented fixture subset (ASCII JSON strings/keys, safe integers, booleans,
null, arrays and objects), plus exact UTF-8 artifact strings.
"""
from __future__ import annotations

import argparse
import copy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource as SchemaResource
except ImportError:
    raise SystemExit('Install jsonschema>=4.18,<5 to run the offline contract validator.')

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
EVIDENCE_KINDS = {'SOURCE_REVISION': 'SourceRevision', 'OBSERVATION': 'Observation',
                  'PROJECTION_REVISION': 'ProjectionRevision', 'SNAPSHOT': 'Snapshot'}
REF_FIELDS = {
    'connectionId': 'Connection', 'collectionId': 'Collection', 'readAttemptId': 'ReadAttempt',
    'sourceRevisionId': 'SourceRevision', 'requestSourceRevisionId': 'SourceRevision',
    'responseSourceRevisionId': 'SourceRevision', 'selectedSourceRevisionId': 'SourceRevision',
    'templateSourceRevisionId': 'SourceRevision', 'effectiveTargetSourceRevisionId': 'SourceRevision',
    'catalogSourceRevisionId': 'SourceRevision', 'observationId': 'Observation',
    'selectedObservationId': 'Observation', 'selectedTaskObservationId': 'Observation',
    'selectedSummaryObservationId': 'Observation', 'selectedDetailObservationId': 'Observation',
    'findingDetailObservationId': 'Observation', 'deploymentObservationId': 'Observation',
    'effectiveTargetObservationId': 'Observation', 'completionObservationId': 'Observation',
    'selectionObservationId': 'Observation', 'selectedPostureProjectionId': 'ProjectionRevision',
    'systemId': 'System', 'userJourneyId': 'UserJourney', 'serviceId': 'Service',
    'targetServiceId': 'Service', 'resourceId': 'Resource', 'targetResourceId': 'Resource',
    'eventContextId': 'EventContext', 'healthEventId': 'HealthEvent',
    'componentDeploymentId': 'ComponentDeployment', 'findingId': 'Finding',
    'agentSpaceId': 'AgentSpace', 'investigationId': 'Investigation', 'executionId': 'Execution',
    'scenarioId': 'Scenario', 'scenarioRevisionId': 'ScenarioRevision',
    'defaultRevisionId': 'ScenarioRevision', 'runId': 'Run', 'stepRunId': 'StepRun',
    'commandId': 'Command', 'catalogSnapshotId': 'Snapshot', 'policyContextSnapshotId': 'Snapshot',
    'policySnapshotId': 'Snapshot', 'inputSnapshotId': 'Snapshot',
}
ARRAY_REFS = {
    'resourceIds': 'Resource', 'userJourneyIds': 'UserJourney', 'recommendationIds': 'Recommendation',
    'sourceRevisionIds': 'SourceRevision', 'assignmentSourceRevisionIds': 'SourceRevision',
    'candidateSourceRevisionIds': 'SourceRevision', 'observationIds': 'Observation',
    'deliveryObservationIds': 'Observation', 'projectionRevisionIds': 'ProjectionRevision',
    'readAttemptIds': 'ReadAttempt', 'decisionCommandIds': 'Command', 'resumeCommandIds': 'Command',
    'serviceIds': 'Service', 'attentionServiceIds': 'Service',
    'currentCoverageServiceIds': 'Service', 'retainedEvidenceServiceIds': 'Service',
}
OPAQUE_FIELDS = {'identity', 'sourceIdentity', 'providerIdentity', 'parentExecutionIdentity',
                 'executionPointerIdentity', 'primaryTaskIdentity', 'registeredServiceIdentity',
                 'expectedSummaryIdentity', 'deploymentIdentity', 'payload', 'suggestion',
                 'inputSchema', 'inputValues', 'inputBindings', 'filters', 'allowedScopes'}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON member: {key}')
        result[key] = value
    return result


def load(path):
    return json.loads(Path(path).read_text(), parse_float=Decimal, object_pairs_hook=unique_object)


def plain(value):
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [plain(v) for v in value]
    return value


def canonical_fixture(value):
    """Fixed compact serialization for fixture hashes; not a general JCS library."""
    if isinstance(value, Decimal):
        return format(value, 'f').rstrip('0').rstrip('.') if '.' in format(value, 'f') else format(value, 'f')
    if isinstance(value, dict):
        return '{' + ','.join(json.dumps(k, ensure_ascii=False) + ':' + canonical_fixture(value[k]) for k in sorted(value)) + '}'
    if isinstance(value, list):
        return '[' + ','.join(canonical_fixture(x) for x in value) + ']'
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def digest(value):
    return 'sha256:' + hashlib.sha256(canonical_fixture(value).encode()).hexdigest()


def safe_source_subset(value):
    if value is None or isinstance(value, bool):
        return True
    if isinstance(value, str):
        return value.isascii()
    if isinstance(value, int):
        return abs(value) <= 9007199254740991
    if isinstance(value, list):
        return all(safe_source_subset(x) for x in value)
    if isinstance(value, dict):
        return all(k.isascii() and safe_source_subset(v) for k, v in value.items())
    return False


def primary(kind):
    return kind[0].lower() + kind[1:] + 'Id'


def issue(code, location, message):
    return {'code': code, 'location': location, 'message': message}


def walk(value, path=()):
    """Walk modeled values without interpreting arbitrary retained native JSON."""
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            if key not in OPAQUE_FIELDS:
                yield from walk(child, path + (key,))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from walk(child, path + (i,))


def schema_errors(schema, examples):
    errors = []
    if set(examples['records']) != set(schema['x-entities']):
        errors.append(issue('ENTITY_EXAMPLE_COVERAGE', 'model/examples.json', 'Examples must cover exactly the declared entity registry.'))
    for kind, rows in examples['records'].items():
        if kind not in schema['$defs']:
            continue
        if not rows:
            errors.append(issue('ENTITY_EXAMPLE_COVERAGE', kind, 'At least one worked record is required.'))
        validator = Draft202012Validator({'$ref': '#/$defs/' + kind, '$defs': schema['$defs']})
        for i, row in enumerate(rows):
            for error in validator.iter_errors(row):
                errors.append(issue('SCHEMA', f'{kind}[{i}]/' + '/'.join(map(str, error.absolute_path)), error.message))
    return errors


def semantic_errors(examples, schema):
    errors = []
    records, ws = examples['records'], examples['workspaceId']
    idx = {kind: {} for kind in records}
    for kind, rows in records.items():
        for row in rows:
            ident = row.get(primary(kind))
            loc = f'{kind}:{ident}'
            if row.get('workspaceId') != ws:
                errors.append(issue('WORKSPACE_MISMATCH', loc, 'Record escapes the containing workspace.'))
            if ident in idx[kind]:
                errors.append(issue('DUPLICATE_ID', loc, 'Canonical entity identity is duplicated.'))
            idx[kind][ident] = row

    def get(kind, ident):
        return idx.get(kind, {}).get(ident)

    def err(code, loc, msg):
        errors.append(issue(code, loc, msg))

    def resolve(kind, ident, loc):
        found = get(kind, ident)
        if found is None or found.get('workspaceId') != ws:
            err('REFERENCE_SCOPE', loc, f'{kind}:{ident} is absent from this workspace.')
        return found

    def observation_source(oid):
        o = get('Observation', oid)
        return get('SourceRevision', o['sourceRevisionId']) if o else None

    def identity_key(ident):
        return canonical_fixture({k: v for k, v in ident.items() if k != 'aliases'})

    # Resolve typed references, including owned values. Native payloads and source
    # identities are deliberately opaque here: their fields are not console IDs.
    for kind, rows in records.items():
        for row in rows:
            loc = f'{kind}:{row[primary(kind)]}'
            # Only three snapshot kinds currently have typed contents. Other
            # retained contents remain arbitrary JSON and may legitimately use
            # native field names such as serviceId without naming console IDs.
            modeled = row
            if kind == 'Snapshot' and row['kind'] not in ('TOPOLOGY', 'POLICY_CONTEXT', 'RUN_INPUT'):
                modeled = {key: value for key, value in row.items() if key != 'contents'}
            for path, value in walk(modeled):
                where = loc + '/' + '/'.join(map(str, path))
                if 'kind' in value and 'id' in value:
                    target = EVIDENCE_KINDS.get(value['kind'], value['kind'])
                    if target in idx:
                        resolve(target, value['id'], where)
                for key, target in REF_FIELDS.items():
                    if key in value and value[key] is not None:
                        if key == 'serviceId' and path and path[0] == 'associations':
                            continue  # Native RegisteredService ID; often built-in "aws".
                        resolve(target, value[key], where + '/' + key)
                for key, target in ARRAY_REFS.items():
                    if isinstance(value.get(key), list):
                        for ident in value[key]:
                            resolve(target, ident, where + '/' + key)

    seen_revisions = set()
    for source in records['SourceRevision']:
        loc = 'SourceRevision:' + source['sourceRevisionId']
        key = (identity_key(source['identity']), source['representation'], source['profile'],
               source['profileVersion'], source['providerVersion'], source['contentDigest'])
        if key in seen_revisions:
            err('DUPLICATE_SOURCE_REVISION', loc, 'The same identity/representation/profile/version/content is retained twice.')
        seen_revisions.add(key)
        if source['digestProfile'] == 'RFC8785_SHA256':
            if not safe_source_subset(source['payload']):
                err('FIXTURE_DIGEST_SUBSET', loc, 'Fixture JSON digest checking intentionally supports only the documented safe subset.')
            elif digest(source['payload']) != source['contentDigest']:
                err('SOURCE_DIGEST', loc, 'Retained payload does not match its content digest.')
        elif not isinstance(source['payload'], str):
            err('FIXTURE_DIGEST_SUBSET', loc, 'Raw-byte fixture checking needs an inline UTF-8 string.')
        else:
            actual = 'sha256:' + hashlib.sha256(source['payload'].encode()).hexdigest()
            if actual != source['contentDigest']:
                err('SOURCE_DIGEST', loc, 'Artifact bytes do not match the retained digest.')
            if source['artifact'] and (source['artifact']['digest'] != actual or source['artifact']['byteLength'] != len(source['payload'].encode())):
                err('ARTIFACT_DIGEST', loc, 'Artifact length/digest must cover the same exact UTF-8 bytes.')

    for collection in records['Collection']:
        keys = [q['queryKey'] for q in collection['queries']]
        if len(keys) != len(set(keys)):
            err('QUERY_IDENTITY', collection['collectionId'], 'Query keys must be unique within a collection.')
    attempts = set()
    for read in records['ReadAttempt']:
        loc = 'ReadAttempt:' + read['readAttemptId']
        parent = get('Collection', read['collectionId'])
        query = next((q for q in parent['queries'] if q['queryKey'] == read['queryKey']), None) if parent else None
        key = (read['collectionId'], read['queryKey'], read['attemptNo'])
        if key in attempts:
            err('READ_ATTEMPT_IDENTITY', loc, 'Collection/query/attempt number is duplicated.')
        attempts.add(key)
        if not query or query['requestDigest'] != read['requestDigest']:
            err('READ_QUERY_SCOPE', loc, 'Read must resolve its reserved query and exact request digest.')
        request = get('SourceRevision', read['requestSourceRevisionId'])
        if request and request['contentDigest'] != read['requestDigest']:
            err('REQUEST_EVIDENCE', loc, 'Request digest must match retained request evidence.')
        if read['state'] == 'FAILED' and read['error'] is None:
            err('READ_STATE', loc, 'Failed read requires an explicit observed error.')
        if read['state'] == 'SUCCEEDED' and (read['error'] is not None or read['returnedCount'] is None):
            err('READ_STATE', loc, 'Successful read needs a known count and no request error.')
        if read['endedAt'] is not None and read['endedAt'] < read['startedAt']:
            err('TIME_ORDER', loc, 'Read ended before it started.')
        if read['state'] != 'STARTED' and read['endedAt'] is None:
            err('READ_STATE', loc, 'A settled read must retain its end time.')
    for observation in records['Observation']:
        loc = 'Observation:' + observation['observationId']
        read = get('ReadAttempt', observation['readAttemptId']) if observation['readAttemptId'] else None
        if read:
            collection = get('Collection', read['collectionId'])
            if collection and collection['connectionId'] != observation['connectionId']:
                err('OBSERVATION_SCOPE', loc, 'Read and observation use different connection scopes.')
            if read['authorizationContextKey'] != observation['authorizationContextKey']:
                err('OBSERVATION_SCOPE', loc, 'Read and observation must pin the same authorization context.')
            if observation['observedAt'] < read['startedAt'] or (read['endedAt'] is not None and observation['observedAt'] > read['endedAt']):
                err('TIME_ORDER', loc, 'Observed response falls outside its read attempt.')

    for service in records['Service']:
        for membership in service['memberships']:
            for jid in membership['userJourneyIds']:
                journey = get('UserJourney', jid)
                if journey and journey['systemId'] != membership['systemId']:
                    err('MEMBERSHIP_PARENT', service['serviceId'], 'A journey must belong to the selected system.')
    contexts = set()
    for context in records['EventContext']:
        key = (context['healthEventId'], context['kind'], context['contextKey'])
        if key in contexts:
            err('CONTEXT_IDENTITY', context['eventContextId'], 'Health context identity is duplicated.')
        contexts.add(key)
        expected = context['accountId'] if context['kind'] == 'ACCOUNT' else context['organizationId']
        if context['kind'] != 'PUBLIC' and context['contextKey'] != expected:
            err('CONTEXT_KEY', context['eventContextId'], 'Non-null context key must equal its actual account/organization identity.')
    for impact in records['EntityImpact']:
        context = get('EventContext', impact['eventContextId'])
        source = observation_source(impact['selectedObservationId'])
        if context and context['kind'] == 'ORG_SUMMARY':
            err('ORG_SUMMARY_IMPACT', impact['entityImpactId'], 'Organization summaries cannot own entity impacts.')
        if context and source and context['kind'] == 'ACCOUNT':
            account = source['payload'].get('awsAccountId') if isinstance(source['payload'], dict) else None
            if account is not None and account != context['accountId']:
                err('IMPACT_ACCOUNT', impact['entityImpactId'], 'Supplied source account contradicts its account context.')
    for communication in records['Communication']:
        pages = communication['pages']
        if communication['assemblyState'] == 'COMPLETE':
            totals = {p['totalPages'] for p in pages}
            expected = set(range(1, next(iter(totals)) + 1)) if len(totals) == 1 else set()
            payloads = {(p['pageNumber'], p['payloadDigest']) for p in pages}
            if not expected or {p['pageNumber'] for p in pages} != expected or len(payloads) != len(expected):
                err('COMMUNICATION_COMPLETENESS', communication['communicationId'], 'Complete assembly requires every consistent logical page, with no conflict.')

    for finding in records['Finding']:
        loc = finding['findingId']
        if finding['recommendationPresence'] in ('UNAVAILABLE', 'NOT_REQUESTED') and finding['recommendationIds'] is not None:
            err('RECOMMENDATION_PRESENCE', loc, 'Unobserved suggestions cannot be converted to an empty list.')
        if finding['recommendationPresence'] == 'EMPTY' and finding['recommendationIds'] != []:
            err('RECOMMENDATION_PRESENCE', loc, 'Known empty suggestions need an explicit empty list.')
        if finding['recommendationPresence'] == 'PRESENT' and not finding['recommendationIds']:
            err('RECOMMENDATION_PRESENCE', loc, 'Present suggestions require retained identities.')
        for rid in finding['recommendationIds'] or []:
            recommendation = get('Recommendation', rid)
            if recommendation and recommendation['findingDetailObservationId'] != finding['selectedDetailObservationId']:
                err('CURRENT_DETAIL_SCOPE', loc, 'Current suggestions must come from the selected detail observation.')
    for recommendation in records['Recommendation']:
        finding = get('Finding', recommendation['findingId'])
        observation = get('Observation', recommendation['findingDetailObservationId'])
        source = get('SourceRevision', recommendation['sourceRevisionId'])
        if finding and finding['serviceId'] != recommendation['serviceId']:
            err('RECOMMENDATION_PARENT', recommendation['recommendationId'], 'Finding and suggestion must share service scope.')
        if observation and observation['sourceRevisionId'] != recommendation['sourceRevisionId']:
            err('RECOMMENDATION_PROVENANCE', recommendation['recommendationId'], 'Suggestion pins a different payload from its detail observation.')
        if source and source['representation'] != 'DETAIL':
            err('RECOMMENDATION_PROVENANCE', recommendation['recommendationId'], 'Suggestion must originate in retained detail, not a summary.')

    for kind in ('Investigation', 'Execution', 'JournalRecord', 'ApprovalRequest', 'Asset'):
        for row in records[kind]:
            space = get('AgentSpace', row['agentSpaceId'])
            ident = row.get('identity')
            if ident and space and ident['scope']['parentKeys'].get('agentSpaceId') != space['identity']['nativeId']:
                err('AGENT_SPACE_SCOPE', row[primary(kind)], 'Native identity contradicts the owning Agent Space.')
            execution = get('Execution', row.get('executionId'))
            if kind in ('JournalRecord', 'ApprovalRequest') and execution and execution['agentSpaceId'] != row['agentSpaceId']:
                err('EXECUTION_PARENT', row[primary(kind)], 'Execution and child are in different Agent Spaces.')
            if kind == 'JournalRecord' and execution and ident['scope']['parentKeys'].get('executionId') != execution['identity']['nativeId']:
                err('JOURNAL_PARENT', row['journalRecordId'], 'Native journal identity contradicts its execution.')
    for investigation in records['Investigation']:
        seen = set()
        for membership in investigation['executionMemberships']:
            execution = get('Execution', membership['executionId'])
            observation = get('Observation', membership['observationId'])
            source = observation_source(membership['observationId'])
            if membership['investigationId'] != investigation['investigationId'] or (execution and execution['agentSpaceId'] != investigation['agentSpaceId']):
                err('EXECUTION_MEMBERSHIP_SCOPE', investigation['investigationId'], 'Observed execution membership crosses task/Agent Space scope.')
            if execution and source and identity_key(source['identity']) != identity_key(execution['identity']):
                err('EXECUTION_MEMBERSHIP_EVIDENCE', investigation['investigationId'], 'Membership must cite the observed execution identity.')
            if observation and observation['readAttemptId']:
                read = get('ReadAttempt', observation['readAttemptId'])
                collection = get('Collection', read['collectionId']) if read else None
                query = next((q for q in collection['queries'] if q['queryKey'] == read['queryKey']), None) if collection else None
                if query and query['subject'] != {'kind': 'Investigation', 'id': investigation['investigationId']}:
                    err('EXECUTION_MEMBERSHIP_EVIDENCE', investigation['investigationId'], 'Task relationship must retain the ListExecutions request association.')
            if membership['executionId'] in seen:
                err('DUPLICATE_MEMBERSHIP', investigation['investigationId'], 'Current execution memberships must be deduplicated.')
            seen.add(membership['executionId'])
    for journal in records['JournalRecord']:
        observation = get('Observation', journal['selectedObservationId'])
        if observation and observation['sourceRevisionId'] != journal['selectedSourceRevisionId']:
            err('SELECTED_REVISION', journal['journalRecordId'], 'Inspector must use the exact selected source revision.')

    # The only modeled assertion reducer here checks declared evidence/coverage
    # prerequisites and required-denominator consistency, never executes a predicate.
    def check_result(check, loc):
        conclusive = check['verdict'] in ('PASS', 'FAIL')
        c = check['coverage']
        if conclusive and not check['evidenceRefs']:
            err('CHECK_EVIDENCE', loc, 'A conclusive assertion requires retained evidence.')
        witness = check['claimType'] == 'EXISTENTIAL' and check['verdict'] == 'PASS'
        if conclusive and not witness and c['claim'] != 'SUFFICIENT':
            err('CHECK_COVERAGE', loc, 'Conclusive non-witness assertion needs sufficient bounded coverage.')
        if check['claimType'] == 'ABSENCE' and conclusive and (c['windowState'] != 'CLOSED' or c['pagination'] != 'EXHAUSTED' or c['detail'] != 'COMPLETE' or c['identity'] != 'COMPLETE' or c['resolution'] not in ('FINISHED', 'NOT_APPLICABLE') or c['knownGaps']):
            err('ABSENCE_COVERAGE', loc, 'Absence cannot be inferred from open, partial, unresolved or gapped collection.')
    for attempt in records['StepAttempt']:
        step = get('StepRun', attempt['stepRunId'])
        if step and attempt['runId'] != step['runId']:
            err('ATTEMPT_PARENT', attempt['stepAttemptId'], 'Attempt belongs to a different Run than its step.')
        if attempt['settledAt'] is not None and attempt['settledAt'] < attempt['startedAt']:
            err('TIME_ORDER', attempt['stepAttemptId'], 'Attempt settled before it started.')
        if attempt['checkResult']:
            check_result(attempt['checkResult'], attempt['stepAttemptId'])
        for _, value in walk(attempt):
            evidence = []
            if value.get('kind') == 'OBSERVATION' and 'id' in value:
                evidence.append(value['id'])
            evidence.extend(value.get('observationIds', []))
            for oid in evidence:
                obs = get('Observation', oid)
                if obs and attempt['settledAt'] is not None and obs['observedAt'] > attempt['settledAt']:
                    err('SEALED_ATTEMPT_FUTURE_EVIDENCE', attempt['stepAttemptId'], 'Later reconciliation cannot rewrite a settled attempt.')

    def verdict(required, values):
        if not required:
            return 'NOT_EVALUATED'
        statuses = [values.get(key, 'INCONCLUSIVE') for key in required]
        return 'FAIL' if 'FAIL' in statuses else ('PASS' if all(s == 'PASS' for s in statuses) else 'INCONCLUSIVE')

    def dag(steps, loc):
        lookup = {s['stepKey']: s for s in steps}
        if len(lookup) != len(steps):
            err('STEP_IDENTITY', loc, 'Step keys must be unique.')
        visiting, done = set(), set()
        def visit(key):
            if key in visiting:
                err('STEP_CYCLE', loc, 'Step dependencies contain a cycle.'); return
            if key in done:
                return
            visiting.add(key)
            for dependency in lookup[key]['needs']:
                if dependency not in lookup or lookup[dependency]['phase'] != lookup[key]['phase']:
                    err('STEP_DEPENDENCY_SCOPE', loc, 'Dependency must resolve within its main/finalizer graph.')
                else:
                    visit(dependency)
            visiting.remove(key); done.add(key)
        for key in lookup:
            visit(key)

    for revision in records['ScenarioRevision']:
        definition = revision['definition']; loc = revision['scenarioRevisionId']
        dag(definition['steps'], loc)
        if digest(definition) != revision['digest'] or digest(definition['inputSchema']) != definition['inputSchemaDigest']:
            err('REVISION_DIGEST', loc, 'Published definition/input schema digest is inconsistent.')
        try:
            Draft202012Validator.check_schema(definition['inputSchema'])
        except Exception as exc:
            err('INPUT_SCHEMA', loc, str(exc))
        if definition['inputSchema'].get('type') != 'object' or definition['inputSchema'].get('additionalProperties') is not False:
            err('INPUT_SCHEMA', loc, 'Published input schema must be a closed top-level object.')
        locks = {x['alias']: x for x in definition['operationLocks']}
        if len(locks) != len(definition['operationLocks']) or any(s['operationAlias'] not in locks for s in definition['steps']):
            err('OPERATION_LOCK', loc, 'Each step must have one resolved immutable operation lock.')
    for scenario in records['Scenario']:
        revision = get('ScenarioRevision', scenario['defaultRevisionId'])
        if revision and revision['scenarioId'] != scenario['scenarioId']:
            err('DEFAULT_REVISION_PARENT', scenario['scenarioId'], 'Default revision belongs to another Scenario.')
    for run in records['Run']:
        revision = get('ScenarioRevision', run['scenarioRevisionId'])
        snapshot_record = get('Snapshot', run['inputSnapshotId'])
        if not revision or not snapshot_record:
            continue
        admission = snapshot_record['contents']
        if snapshot_record['kind'] != 'RUN_INPUT' or admission.get('scenarioRevisionId') != run['scenarioRevisionId'] or admission.get('revisionDigest') != revision['digest']:
            err('RUN_ADMISSION', run['runId'], 'Run must pin its exact admitted revision and digest.'); continue
        definition = revision['definition']; enabled = set(admission['enabledStepKeys'])
        definitions = {s['stepKey']: s for s in definition['steps']}
        required = {s['stepKey'] for s in definition['steps'] if s['required'] and s['checkRole'] == 'CRITERION' and s['stepKey'] in enabled}
        if not enabled <= set(definitions) or set(admission['requiredCriterionKeys']) != required:
            err('CRITERION_DENOMINATOR', run['runId'], 'Admission must freeze all enabled required criteria.')
        if len(admission['requiredCriterionKeys']) != len(required):
            err('CRITERION_DENOMINATOR', run['runId'], 'Required criteria cannot be duplicated.')
        declared = {b['bindingKey'] for b in definition['bindings']}
        resolved = [b['bindingKey'] for b in admission['resolvedBindings']]
        if set(resolved) != declared or len(resolved) != len(set(resolved)):
            err('BINDING_CLOSURE', run['runId'], 'Admission must resolve each declared binding exactly once.')
        for error in Draft202012Validator(definition['inputSchema']).iter_errors(admission['inputValues']):
            err('ADMISSION_INPUT', run['runId'], error.message)
        step_rows = [s for s in records['StepRun'] if s['runId'] == run['runId']]
        if {s['stepKey'] for s in step_rows} != set(definitions):
            err('STEP_RUN_COVERAGE', run['runId'], 'All declared steps, including zero-attempt/skipped ones, need a retained StepRun.')
        values = {}
        for step in step_rows:
            selected = [a for a in records['StepAttempt'] if a['stepRunId'] == step['stepRunId'] and a['attemptNo'] == step['selectedAttemptNo']]
            if step['selectedAttemptNo'] is not None and len(selected) != 1:
                err('ATTEMPT_SELECTION', step['stepRunId'], 'Selected attempt must resolve exactly once.')
            if step['stepKey'] in required:
                values[step['stepKey']] = selected[0]['checkResult']['verdict'] if selected and selected[0]['checkResult'] else 'INCONCLUSIVE'
        if run['assessmentVerdict'] != verdict(admission['requiredCriterionKeys'], values):
            err('RUN_VERDICT', run['runId'], 'Verdict must retain failed/missing/skipped required checks in its denominator.')
        if run['phase'] == 'TERMINAL' and run['terminalAt'] is None:
            err('RUN_STATE', run['runId'], 'Terminal Run requires a terminal timestamp.')
        latest = {}
        for attempt in sorted((a for a in records['StepAttempt'] if a['runId'] == run['runId']), key=lambda a: a['settledAt'] or a['startedAt']):
            for effect in attempt['externalOperations']:
                latest[effect['originEffectKey']] = effect['remoteDisposition']
        if run['finalizationState'] == 'COMPLETE' and any(s in ('ACTIVE', 'UNKNOWN') for s in latest.values()):
            err('UNRESOLVED_FINALIZATION', run['runId'], 'Complete finalization cannot hide an active or unknown tracked effect.')

    for projection in records['ProjectionRevision']:
        value, loc, profile = projection['value'], projection['projectionRevisionId'], projection['profile']
        if projection['generatedAt'] < projection['asOf']:
            err('TIME_ORDER', loc, 'Projection generation precedes its as-of cutoff.')
        if profile == 'EVALUATION':
            results = {c['criterionKey']: c['result']['verdict'] for c in value['criteria']}
            for criterion in value['criteria']:
                check_result(criterion['result'], loc + '/' + criterion['criterionKey'])
            if len(results) != len(value['criteria']) or value['verdict'] != verdict(value['requiredCriterionKeys'], results):
                err('EVALUATION_VERDICT', loc, 'Evaluation must preserve its required criterion denominator.')
        elif profile == 'SERVICE_STATUS':
            context = get('Snapshot', value['policyContextSnapshotId'])
            if context and (context['kind'] != 'POLICY_CONTEXT' or context['contents']['serviceId'] != value['serviceId']):
                err('POLICY_CONTEXT_SCOPE', loc, 'Status must use the retained policy context of the same service.')
            for dimension in ('runtimeHealth', 'resiliencePosture', 'assessmentExecution'):
                if value[dimension]['state'] not in ('UNKNOWN', 'UNAVAILABLE', 'NOT_OBSERVED') and not value[dimension]['evidenceRefs']:
                    err('STATUS_EVIDENCE', loc, f'{dimension} cannot become known without independent evidence.')
                expiry = value[dimension]['expiresAt']
                if expiry is not None and expiry <= projection['asOf'] and value[dimension]['state'] not in ('UNKNOWN', 'STALE', 'UNAVAILABLE', 'NOT_OBSERVED'):
                    err('EXPIRED_CURRENT_STATUS', loc, f'{dimension} has expired; retained raw evidence cannot remain a current known state.')
        elif profile == 'INVESTIGATION_RESULT':
            source = get('SourceRevision', value['selectedSourceRevisionId'])
            completion = observation_source(value['completionObservationId'])
            if value['availability'] == 'AVAILABLE' and source is None:
                err('RESULT_SELECTION', loc, 'Available result requires a retained source revision.')
            if value['selectionBasis'] == 'EXPLICIT_COMPLETION_REFERENCE' and (not completion or not value['expectedSummaryIdentity']):
                err('RESULT_SELECTION', loc, 'Explicit selection needs completion evidence and its exact expected identity.')
            if source and value['expectedSummaryIdentity'] and identity_key(source['identity']) != identity_key(value['expectedSummaryIdentity']):
                err('RESULT_SELECTION', loc, 'Selected summary differs from the exact completion reference.')
            # Fixture completion profile has an explicit normalized phase. Real
            # adapters must derive this from channel-specific type/profile evidence.
            if completion and isinstance(completion['payload'], dict) and completion['payload'].get('phase') not in (None, value['phase']):
                err('RESULT_PHASE', loc, 'A different result phase cannot replace this phase selection.')
        elif profile == 'LIFECYCLE_EXPOSURE':
            deployment = get('ComponentDeployment', value['componentDeploymentId'])
            if deployment and deployment['observationId'] != value['deploymentObservationId']:
                err('DEPLOYMENT_PROVENANCE', loc, 'Exposure must use the exact observed component deployment.')
            entries = [e for e in records['LifecycleEntry'] if e['sourceRevisionId'] == value['catalogSourceRevisionId']]
            if not any(value['milestoneKey'] in {m['milestoneKey'] for m in entry['milestones']} for entry in entries):
                err('MILESTONE_SCOPE', loc, 'Milestone must resolve in the selected catalogue revision.')
        elif profile == 'WORKSPACE_SUMMARY':
            population = set(value['serviceIds'])
            for field in ('serviceIds', 'attentionServiceIds', 'currentCoverageServiceIds', 'retainedEvidenceServiceIds'):
                if len(value[field]) != len(set(value[field])) or not set(value[field]) <= population:
                    err('SUMMARY_DENOMINATOR', loc, 'Service populations must be distinct and scoped to the same denominator.')
            expected = Decimal(100) * len(set(value['currentCoverageServiceIds'])) / len(population) if population else None
            if value['currentCoveragePercent'] != expected:
                err('SUMMARY_DENOMINATOR', loc, 'Coverage percentage must use the distinct service population; empty denominator is null.')

    for assessment in records['ResilienceAssessment']:
        snapshot_record = get('Snapshot', assessment['policyContextSnapshotId'])
        posture = get('ProjectionRevision', assessment['selectedPostureProjectionId'])
        if snapshot_record and (snapshot_record['kind'] != 'POLICY_CONTEXT' or snapshot_record['contents']['serviceId'] != assessment['serviceId']):
            err('ASSESSMENT_POLICY_SCOPE', assessment['resilienceAssessmentId'], 'Assessment context must stay within its service.')
        if posture and (posture['profile'] != 'SERVICE_STATUS' or posture['value']['serviceId'] != assessment['serviceId'] or (snapshot_record and posture['value']['policyContextSnapshotId'] != snapshot_record['snapshotId'])):
            err('ASSESSMENT_POLICY_SCOPE', assessment['resilienceAssessmentId'], 'Selected posture must resolve the same captured policy context.')

    for snapshot_record in records['Snapshot']:
        loc = snapshot_record['snapshotId']; source_ids = set(snapshot_record['sourceRevisionIds']); obs_ids = set(snapshot_record['observationIds'])
        read_ids = {r['readAttemptId'] for r in snapshot_record['readAttempts']}
        if digest({k: v for k, v in snapshot_record.items() if k != 'manifestDigest'}) != snapshot_record['manifestDigest']:
            err('SNAPSHOT_DIGEST', loc, 'Snapshot manifest does not match its retained content.')
        for read in snapshot_record['readAttempts']:
            if get('ReadAttempt', read['readAttemptId']) != read:
                err('SNAPSHOT_READ_COPY', loc, 'Snapshot must retain the exact immutable read attempt, not a reconstructed current version.')
            for key in ('requestSourceRevisionId', 'responseSourceRevisionId'):
                if read[key] is not None and read[key] not in source_ids:
                    err('SNAPSHOT_CLOSURE', loc, 'Retained read request/response revision is missing from the manifest.')
        for oid in obs_ids:
            observation = get('Observation', oid)
            if observation and (observation['sourceRevisionId'] not in source_ids or (observation['readAttemptId'] and observation['readAttemptId'] not in read_ids)):
                err('SNAPSHOT_CLOSURE', loc, 'Observed source/read provenance is not closed within the capture.')
            if observation and observation['observedAt'] > snapshot_record['capturedAt']:
                err('SNAPSHOT_FUTURE_EVIDENCE', loc, 'Capture cannot include a future observation.')
        for pid in snapshot_record['projectionRevisionIds']:
            projection_record = get('ProjectionRevision', pid)
            if not projection_record:
                continue
            for evidence in projection_record['inputRefs']:
                if (evidence['kind'] == 'SOURCE_REVISION' and evidence['id'] not in source_ids) or (evidence['kind'] == 'OBSERVATION' and evidence['id'] not in obs_ids):
                    err('SNAPSHOT_CLOSURE', loc, 'A retained projection depends on unpinned source/observation input.')
            if projection_record['generatedAt'] > snapshot_record['capturedAt']:
                err('SNAPSHOT_FUTURE_EVIDENCE', loc, 'Capture cannot include a future projection.')
        if snapshot_record['captureStartedAt'] > snapshot_record['capturedAt'] or (snapshot_record['captureFinishedAt'] is not None and not snapshot_record['captureStartedAt'] <= snapshot_record['captureFinishedAt'] <= snapshot_record['capturedAt']):
            err('TIME_ORDER', loc, 'Capture start/finish/assembly times are inconsistent.')
        if snapshot_record['kind'] == 'POLICY_CONTEXT':
            context = snapshot_record['contents']; observation = get('Observation', context['effectiveTargetObservationId'])
            if observation and observation['sourceRevisionId'] != context['effectiveTargetSourceRevisionId']:
                err('POLICY_TARGET_SELECTION', loc, 'Captured effective target revision and observation do not match.')
            if context['effectiveTargetSourceRevisionId'] not in source_ids or context['effectiveTargetObservationId'] not in obs_ids:
                err('POLICY_TARGET_SELECTION', loc, 'Effective targets must be pinned in this same policy capture.')
        elif snapshot_record['kind'] == 'TOPOLOGY':
            graph = snapshot_record['contents']; nodes = {n['nodeKey'] for n in graph['nodes']}
            if len(nodes) != len(graph['nodes']):
                err('GRAPH_IDENTITY', loc, 'Snapshot node keys must be unique.')
            for edge in graph['edges']:
                if edge['fromNodeKey'] not in nodes or edge['toNodeKey'] not in nodes:
                    err('GRAPH_ENDPOINT_SCOPE', loc, 'Graph endpoints must exist in this snapshot.')

    for experiment in records['Experiment']:
        names = {a['actionName'] for a in experiment['actions']}
        if len(names) != len(experiment['actions']):
            err('FIS_ACTION_IDENTITY', experiment['experimentId'], 'Named action values are unique within their experiment.')
        for action in experiment['actions']:
            if any(dep not in names or dep == action['actionName'] for dep in action['startAfter']):
                err('FIS_ACTION_SCOPE', experiment['experimentId'], 'Action dependencies must refer to another action in this experiment.')
        for target in experiment['targetMemberships']:
            if target['identityCompleteness'] == 'IDENTIFIED' and target['sourceIdentity'] is None:
                err('TARGET_IDENTITY', experiment['experimentId'], 'Identified target needs an explicit source identity.')
            resource = get('Resource', target['resourceId'])
            if resource and target['sourceIdentity'] and identity_key(resource['identity']) != identity_key(target['sourceIdentity']):
                err('TARGET_IDENTITY', experiment['experimentId'], 'Selected target is not the referenced inventory identity.')
    return errors


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True)


def check_inventory(model):
    manifest = load(ROOT / 'inventory.json'); sha = manifest['sourceCommit']; actual = {}
    for line in git('ls-tree', '-r', '-l', sha, '--', 'aws').splitlines():
        meta, path = line.split('\t', 1)
        if re.match(r'^aws/[^/]+/analysis/', path):
            _, _, blob, size = meta.split(); actual[path] = (blob, int(size))
    expected = {f['path']: (f['blobSha'], f['sizeBytes']) for f in manifest['files']}
    assert expected == actual, 'Inventory paths, blobs or byte sizes differ from the pinned tree.'
    assert len(expected) == len(manifest['files']) == manifest['fileCount'], 'Inventory count/uniqueness mismatch.'
    assert sha == model['x-sourceCommit'], 'Model and inventory source commits disagree.'
    for service, count in manifest['services'].items():
        assert sum(p.split('/')[1] == service for p in expected) == count, f'Incorrect {service} file count.'
    return manifest


def check_crosswalk(model, inventory, examples):
    registry = load(ROOT / 'model/adapter-profiles.json'); entities = set(model['x-entities'])
    assert registry['sourceCommit'] == inventory['sourceCommit'], 'Crosswalk source commit drift.'
    assert set(sum(registry['canonicalEntitiesByModule'].values(), [])) == entities, 'Crosswalk entity coverage drift.'
    aliases = set(); profiles = {p['profileId']: p for p in registry['profiles']}
    assert len(profiles) == len(registry['profiles']), 'Duplicate adapter profile.'
    for mapping in registry['mappings']:
        assert set(mapping['canonicalEntities']) <= entities, 'Unknown crosswalk target entity.'
        if mapping.get('profileId'):
            assert mapping['profileId'] in profiles, 'Unresolved crosswalk profile.'
        for concept in mapping['sourceConcepts']:
            key = (mapping['sourceService'], concept)
            assert key not in aliases, f'Duplicate source concept mapping: {key}'
            aliases.add(key)
    for profile in profiles.values():
        assert set(profile['canonicalEntities']) <= entities, 'Unknown profile target entity.'
        binding = profile.get('normalizedBinding')
        if binding:
            shape = binding['schemaRef'].split('/')[-1]
            assert shape in model['$defs'], f'Unknown normalized profile shape: {shape}'
            if binding.get('projectionProfile'):
                assert model['x-projectionProfiles'][binding['projectionProfile']] == shape, 'Projection profile shape drift.'
    for row in examples['records']['SourceRevision']:
        assert row['profile'] in profiles, f'Unregistered fixture source profile: {row["profile"]}'
        assert row['profileVersion'] == profiles[row['profile']]['sourceRevisionBinding']['profileVersion'], 'Source profile version drift.'
    sha = inventory['sourceCommit']; concepts = set()
    for file in inventory['files']:
        path = file['path']
        if '/diagrams/' not in path or not path.endswith(('.mmd', '.md')):
            continue
        content = git('show', sha + ':' + path)
        if 'erDiagram' not in content and 'classDiagram' not in content:
            continue
        service = 'workflow' if '/fis/analysis/workflow/' in path else file['service']
        names = set(re.findall(r'^\s*class\s+([A-Za-z][A-Za-z0-9_]*)\b', content, re.M))
        names |= set(re.findall(r'^\s*([A-Za-z][A-Za-z0-9_]*)\s*\{\s*$', content, re.M))
        for left, right in re.findall(r'^\s*(\w+)\s+[|}o{]+--[|}o{]+\s+(\w+)\s*:', content, re.M):
            names.update((left, right))
        concepts |= {(service, name) for name in names}
    # The 52 selected native DevOps shapes are an additional explicit source
    # surface; they are not inferred to be 52 business entities.
    catalog = git('show', sha + ':aws/devops-agent/analysis/annexes/Investigation_API_Catalog.md')
    selected = catalog.split('## 3. Returned entities and nested value objects', 1)[1].split('## 4.', 1)[0]
    concepts |= {('devops-agent', name) for name in re.findall(r'^### ([A-Za-z][A-Za-z0-9_]*)\s*$', selected, re.M)}
    assert concepts <= aliases, 'Unmapped source concepts: ' + repr(sorted(concepts - aliases))
    paths = {x['sourcePath'] for x in registry['mappings'] + registry['profiles']}
    for path in paths:
        git('cat-file', '-e', sha + ':' + path)
    return {'mappings': len(registry['mappings']), 'sourceAliases': len(aliases), 'sourceConceptsChecked': len(concepts), 'adapterProfiles': len(profiles)}


def check_diagrams(model):
    complete = (ROOT / 'diagrams/complete-model.mmd').read_text()
    names = re.findall(r'^class (\w+)\s*\{', complete, re.M)
    assert len(names) == len(set(names)) and set(names) == set(model['x-entities']), 'Complete class diagram entity coverage mismatch.'
    manifest = load(ROOT / 'diagrams/manifest.json')
    assert manifest['schemaSha256'] == hashlib.sha256((ROOT / 'model/schema.json').read_bytes()).hexdigest(), 'Diagram schema provenance is stale.'
    for diagram in manifest['diagrams']:
        for kind in ('mmd', 'dot', 'svg'):
            item = diagram[kind]; path = ROOT / item['path']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], 'Stale diagram hash: ' + item['path']
        ET.parse(ROOT / diagram['svg']['path'])
    return len(manifest['diagrams'])


def check_api(model):
    path = ROOT / 'api/operations.json'
    if not path.exists():
        raise AssertionError('API operation catalog has not been produced.')
    catalog = load(path); schema = load(ROOT / 'api/rpc.schema.json'); examples = load(ROOT / 'api/examples.json')
    Draft202012Validator.check_schema(schema)
    registry = Registry().with_resources([(model['$id'], SchemaResource.from_contents(model)), (schema['$id'], SchemaResource.from_contents(schema))])
    operations = {o['name']: o for o in catalog['operations']}
    assert len(operations) == len(catalog['operations']) == catalog['operationCount'], 'API operation count/uniqueness drift.'
    assert set(catalog['entityCoverage']) == set(model['x-entities']), 'API does not cover all model entities.'
    for entity, names in catalog['entityCoverage'].items():
        assert names and all(n in operations and entity in operations[n]['entities'] for n in names), f'Bad operation coverage for {entity}.'
    supplied = {e['operation'] for e in examples['examples']}
    assert supplied == set(operations), 'Every operation needs an input/output example.'
    count = 0
    for example in examples['examples']:
        op = operations[example['operation']]
        assert op['target'] == catalog['namespace'] + '.' + op['name'], 'RPC namespace/target drift.'
        for member, refkey in (('request', 'inputSchemaRef'), ('response', 'outputSchemaRef')):
            name = op[refkey].split('/')[-1]
            validator = Draft202012Validator({'$ref': schema['$id'] + '#/$defs/' + name}, registry=registry)
            found = list(validator.iter_errors(example[member]))
            assert not found, f'{op["name"]} {member}: ' + '; '.join(e.message for e in found[:3])
            count += 1
        request = schema['$defs'][op['inputSchemaRef'].split('/')[-1]]
        assert request.get('additionalProperties') is False, 'Request root must be closed: ' + op['name']
        assert 'workspaceId' not in request.get('properties', {}), 'Caller must not select workspace scope.'
        if op['mutating']:
            assert 'clientToken' in request.get('required', []), 'Mutation needs an explicit idempotency token.'
    validator = Draft202012Validator({'$ref': schema['$id'] + '#/$defs/RpcError'}, registry=registry)
    for example in examples['errors']:
        validator.validate(example['response'])
        assert catalog['errors'][example['response']['__type']]['status'] == example['status'], 'Error status mismatch.'
    return {'operations': len(operations), 'requestResponseExamples': count, 'errorExamples': len(examples['errors'])}


def check_links():
    checked = 0
    for path in ROOT.rglob('*.md'):
        content = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        targets = re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', content)
        targets += re.findall(r'^\[[^\]]+\]:\s*(\S+)', content, re.M)
        for target in targets:
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            resolved = (path.parent / unquote(parts.path)).resolve()
            assert resolved.exists(), f'Broken relative link in {path.relative_to(ROOT)}: {target}'
            checked += 1
    return checked


def apply_cases(base, schema):
    cases = load(ROOT / 'examples/semantic-cases.json')['cases']
    for case in cases:
        candidate = copy.deepcopy(base)
        for mutation in case.get('mutations', []):
            rows = candidate['records'][mutation['entity']]
            record = next(r for r in rows if r[primary(mutation['entity'])] == mutation['id'])
            parts = [p.replace('~1', '/').replace('~0', '~') for p in mutation['path'].split('/')[1:]]
            parent = record
            for part in parts[:-1]:
                parent = parent[int(part)] if isinstance(parent, list) else parent[part]
            key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
            if mutation.get('op') == 'remove':
                del parent[key]
            else:
                parent[key] = mutation['value']
        for addition in case.get('appendRecords', []):
            candidate['records'][addition['entity']].append(copy.deepcopy(addition['record']))
        for target in case.get('rehash', []):
            row = next(r for r in candidate['records'][target['entity']] if r[primary(target['entity'])] == target['id'])
            if target['entity'] == 'Snapshot':
                row['manifestDigest'] = digest({k: v for k, v in row.items() if k != 'manifestDigest'})
            elif target['entity'] == 'SourceRevision':
                row['contentDigest'] = digest(row['payload'])
        result = schema_errors(schema, candidate)
        if not result:
            result += semantic_errors(candidate, schema)
        codes = {e['code'] for e in result}
        if case['expect'] == 'VALID':
            assert not result, f'Case {case["id"]} unexpectedly rejected: {result[:3]}'
        else:
            assert set(case['expectedCodes']) <= codes, f'Case {case["id"]} missed expected violations {case["expectedCodes"]}; got {sorted(codes)}'
        for assertion in case.get('assertions', []):
            row = next(r for r in candidate['records'][assertion['entity']] if r[primary(assertion['entity'])] == assertion['id'])
            value = row
            for part in assertion['path'].split('/')[1:]:
                value = value[int(part)] if isinstance(value, list) else value[part]
            assert value == assertion['equals'], f'Case {case["id"]} failed its stated fixture assertion.'
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Print a machine-readable validation summary.')
    parser.add_argument('--model-only', action='store_true', help='Check model/examples/cases while other package artifacts are still being authored.')
    args = parser.parse_args()
    report = {'status': 'PASS', 'scope': 'OFFLINE_CONTRACTS_ONLY', 'checks': {}, 'limitations': [
        'No API server, authentication, persistence, scheduler, provider call, expression evaluation or adapter is executed.',
        'Semantic checks cover declared invariants and adversarial examples, not all possible domain behavior.',
        'Fixture digest checking is a restricted subset, not a complete RFC 8785 conformance implementation.',
        'Source/profile coverage checks verify named inventories and mappings, not full native SDK payload conformance.',
        'Diagram checks establish entity coverage, XML validity and provenance; visual review and Mermaid syntax are separate gates.',
    ]}
    try:
        schema = load(ROOT / 'model/schema.json'); examples = load(ROOT / 'model/examples.json')
        Draft202012Validator.check_schema(schema)
        assert set(schema['x-entities']) == {name for name, shape in schema['$defs'].items() if shape.get('x-entity')}, 'Schema entity registry drift.'
        errors = schema_errors(schema, examples)
        if not errors:
            errors = semantic_errors(examples, schema)
        if errors:
            report['errors'] = errors
            raise AssertionError(f'{len(errors)} model example violation(s).')
        report['checks']['entities'] = len(schema['x-entities'])
        report['checks']['modelRecords'] = sum(map(len, examples['records'].values()))
        report['checks']['semanticCases'] = apply_cases(examples, schema)
        if not args.model_only:
            inventory = check_inventory(schema)
            report['checks']['inventoryFiles'] = inventory['fileCount']
            report['checks'].update(check_crosswalk(schema, inventory, examples))
            report['checks']['classDiagrams'] = check_diagrams(schema)
            report['checks'].update(check_api(schema))
            report['checks']['relativeLinks'] = check_links()
    except Exception as exc:
        report['status'] = 'FAIL'; report['failure'] = str(exc)
    if args.json or report['status'] != 'PASS':
        print(json.dumps(plain(report), indent=2))
    else:
        print('PASS — offline model, provenance, scope, semantic cases and cross-artifact contracts.')
        print(json.dumps(report['checks'], sort_keys=True))
        print('No runtime, live AWS, authorization, scheduler or production guarantees were tested.')
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
