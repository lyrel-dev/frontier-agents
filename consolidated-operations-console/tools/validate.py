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
EVIDENCE_KINDS = {'Source': 'Source', 'Observation': 'Observation',
                  'Projection': 'Projection', 'Snapshot': 'Snapshot'}
REF_FIELDS = {
    'connection': 'Connection', 'collectionId': 'Collection', 'readAttempt': 'ReadAttempt',
    'source': 'Source', 'requestSource': 'Source',
    'responseSource': 'Source', 'selectedSource': 'Source',
    'templateSource': 'Source', 'effectiveTargetSource': 'Source',
    'catalogSource': 'Source', 'observation': 'Observation',
    'selectedObservation': 'Observation', 'selectedTaskObservation': 'Observation',
    'selectedSummaryObservation': 'Observation', 'selectedDetailObservation': 'Observation',
    'findingDetailObservation': 'Observation', 'deploymentObservation': 'Observation',
    'effectiveTargetObservation': 'Observation', 'completionObservation': 'Observation',
    'selectionObservation': 'Observation', 'selectedPostureProjection': 'Projection',
    'systemId': 'System', 'userJourneyId': 'UserJourney', 'serviceId': 'Service',
    'targetServiceId': 'Service', 'resourceId': 'Resource', 'targetResourceId': 'Resource',
    'eventContextId': 'EventContext', 'healthEventId': 'HealthEvent',
    'componentDeploymentId': 'ComponentDeployment', 'findingId': 'Finding',
    'agentSpaceId': 'AgentSpace', 'investigationId': 'Investigation', 'executionId': 'Execution',
    'scenarioId': 'Scenario', 'scenario': 'Scenario',
    'runId': 'Run', 'stepRunId': 'StepRun',
    'commandId': 'Command', 'catalogSnapshot': 'Snapshot', 'policyContextSnapshot': 'Snapshot',
    'policySnapshot': 'Snapshot', 'inputSnapshot': 'Snapshot',
}
ARRAY_REFS = {
    'resourceIds': 'Resource', 'userJourneyIds': 'UserJourney', 'recommendationIds': 'Recommendation',
    'sources': 'Source', 'assignmentSources': 'Source',
    'candidateSources': 'Source', 'observations': 'Observation',
    'deliveryObservations': 'Observation', 'projections': 'Projection',
    'readAttempts': 'ReadAttempt', 'decisionCommandIds': 'Command', 'resumeCommandIds': 'Command',
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
    history = {kind: {} for kind in records}
    groups = {}
    for kind, rows in records.items():
        shape = schema['$defs'][kind]
        if not {'version', 'createdAt', 'updatedAt'} <= set(shape['required']):
            errors.append(issue('UNIFORM_VERSION_CONTRACT', kind, 'Every entity requires the same version metadata.'))
        if kind.endswith(('Revision', 'Version')) or any(k in shape['properties'] for k in ('projectionVersion', 'localUpdatedAt')):
            errors.append(issue('VERSION_ENTITY', kind, 'History must not create another entity type or a competing version clock.'))
        for row in rows:
            ident, version = row.get(primary(kind)), row.get('version')
            loc = f'{kind}:{ident}@{version}'
            if row.get('workspaceId') != ws:
                errors.append(issue('WORKSPACE_MISMATCH', loc, 'Record escapes the containing workspace.'))
            key = (ident, version)
            if key in history[kind]:
                errors.append(issue('DUPLICATE_ENTITY_VERSION', loc, 'The same entity version occurs more than once; versions are immutable.'))
            history[kind][key] = row
            if ident not in idx[kind] or version > idx[kind][ident]['version']:
                idx[kind][ident] = row
            groups.setdefault((kind, ident), []).append(row)
            if row['updatedAt'] < row['createdAt']:
                errors.append(issue('VERSION_TIME_ORDER', loc, 'A version cannot predate entity creation.'))
    for (kind, ident), rows in groups.items():
        ordered = sorted(rows, key=lambda x: x['version'])
        if len({r['createdAt'] for r in ordered}) != 1:
            errors.append(issue('ENTITY_CREATION_STABLE', f'{kind}:{ident}', 'Entity creation time must remain stable across versions.'))
        if any(a['updatedAt'] > b['updatedAt'] for a, b in zip(ordered, ordered[1:])):
            errors.append(issue('VERSION_TIME_ORDER', f'{kind}:{ident}', 'Later versions cannot have earlier publication time.'))
        def sealed(row):
            return ((kind == 'ReadAttempt' and row['state'] != 'STARTED') or
                    (kind == 'StepAttempt' and row['settledAt'] is not None) or
                    (kind == 'Run' and row['phase'] == 'TERMINAL'))
        if any(sealed(row) for row in ordered[:-1]):
            errors.append(issue('SEALED_ENTITY_VERSION', f'{kind}:{ident}', 'A settled execution fact cannot acquire a later reopened representation; reconciliation is new evidence.'))
        fixed_fields = {'Run': ('scenario', 'inputSnapshot', 'admittedAt'),
                        'Collection': ('connection', 'queries', 'startedAt'),
                        'ReadAttempt': ('collectionId', 'queryKey', 'attemptNo', 'requestDigest', 'requestSource', 'startedAt'),
                        'StepRun': ('runId', 'stepKey'),
                        'StepAttempt': ('runId', 'stepRunId', 'attemptNo', 'dispatchKey', 'startedAt')}.get(kind, ())
        for field in fixed_fields:
            if any(r.get(field) != ordered[0].get(field) for r in ordered):
                errors.append(issue('EXECUTION_IDENTITY_STABLE', f'{kind}:{ident}', f'Immutable {field} cannot change across lifecycle versions.'))
        for field in ('workspaceId', 'agentSpaceId', 'eventContextId', 'healthEventId', 'runId', 'stepRunId'):
            if field in ordered[0] and any(r.get(field) != ordered[0][field] for r in ordered):
                errors.append(issue('IDENTITY_SCOPE_STABLE', f'{kind}:{ident}', 'An entity cannot move to another ownership scope through a new version.'))

    def get(kind, ident):
        if ident is None:
            return None
        if isinstance(ident, dict):
            if ident.get('kind') != kind or 'version' not in ident:
                return None
            return history.get(kind, {}).get((ident['id'], ident['version']))
        return idx.get(kind, {}).get(ident)

    def err(code, loc, msg):
        errors.append(issue(code, loc, msg))

    def resolve(kind, ident, loc):
        found = get(kind, ident)
        if found is None or found.get('workspaceId') != ws:
            err('REFERENCE_SCOPE', loc, f'{kind}:{ident} is absent from this workspace; exact references never fall back to latest.')
        return found

    def ref_key(value):
        return value['kind'], value['id'], value['version']

    def exact_refs(value):
        for _, item in walk(value):
            if {'kind', 'id', 'version'} <= set(item) and item['kind'] in history:
                yield {'kind': item['kind'], 'id': item['id'], 'version': item['version']}

    def observation_source(oid):
        o = get('Observation', oid)
        return get('Source', o['source']) if o else None

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
                        resolve(target, value if 'version' in value else value['id'], where)
                        selected = get(target, value) if 'version' in value else None
                        if selected and selected['updatedAt'] > row['updatedAt']:
                            err('REFERENCE_FUTURE_VERSION', where, 'A retained representation cannot reference an entity version published after it.')
                for key, target in REF_FIELDS.items():
                    if key in value and value[key] is not None:
                        if key == 'serviceId' and path and path[0] == 'associations':
                            continue  # Native RegisteredService ID; often built-in "aws".
                        resolve(target, value[key], where + '/' + key)
                for key, target in ARRAY_REFS.items():
                    if isinstance(value.get(key), list):
                        for ident in value[key]:
                            resolve(target, ident, where + '/' + key)

    seen_sources = {}
    source_keys = {}
    for source in records['Source']:
        loc = 'Source:' + source['sourceId'] + '@' + str(source['version'])
        key = (identity_key(source['identity']), source['representation'], source['profile'], source['sourceOperation'])
        if source['sourceId'] in source_keys and source_keys[source['sourceId']] != key:
            err('SOURCE_IDENTITY_STABLE', loc, 'Versions of one Source must preserve the same logical source identity.')
        source_keys[source['sourceId']] = key
        if key in seen_sources and seen_sources[key] != source['sourceId']:
            err('SOURCE_LOGICAL_IDENTITY', loc, 'Content changes must append versions under the same logical source identity.')
        seen_sources[key] = source['sourceId']
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

    for kind, key_fields, code in (
        ('Projection', ('projectionKey', 'profile'), 'PROJECTION_LOGICAL_IDENTITY'),
        ('Recommendation', ('serviceId', 'findingId', 'source', 'groupKey', 'ordinal'), 'RECOMMENDATION_LOGICAL_IDENTITY'),
    ):
        seen_keys, seen_ids = {}, {}
        for row in records[kind]:
            ident = row[primary(kind)]
            values = [row[field] for field in key_fields]
            if kind == 'Projection':
                values.append(sorted({(ref['kind'], ref['id']) for ref in row['subjectRefs']}))
            key = canonical_fixture(values)
            if (key in seen_keys and seen_keys[key] != ident) or (ident in seen_ids and seen_ids[ident] != key):
                err(code, kind + ':' + ident, 'Versions must preserve one logical identity; repeated capture cannot create duplicate identities.')
            seen_keys[key], seen_ids[ident] = ident, key

    for collection in records['Collection']:
        keys = [q['queryKey'] for q in collection['queries']]
        if len(keys) != len(set(keys)):
            err('QUERY_IDENTITY', collection['collectionId'], 'Query keys must be unique within a collection.')
    attempts = {}
    for read in records['ReadAttempt']:
        loc = 'ReadAttempt:' + read['readAttemptId']
        parent = get('Collection', read['collectionId'])
        query = next((q for q in parent['queries'] if q['queryKey'] == read['queryKey']), None) if parent else None
        key = (read['collectionId'], read['queryKey'], read['attemptNo'])
        if key in attempts and attempts[key] != read['readAttemptId']:
            err('READ_ATTEMPT_IDENTITY', loc, 'Collection/query/attempt number is duplicated.')
        attempts[key] = read['readAttemptId']
        if not query or query['requestDigest'] != read['requestDigest']:
            err('READ_QUERY_SCOPE', loc, 'Read must resolve its reserved query and exact request digest.')
        request = get('Source', read['requestSource'])
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
        read = get('ReadAttempt', observation['readAttempt']) if observation['readAttempt'] else None
        if read:
            collection = get('Collection', read['collectionId'])
            if collection and collection['connection'] != observation['connection']:
                err('Observation_SCOPE', loc, 'Read and observation use different connection scopes.')
            if read['authorizationContextKey'] != observation['authorizationContextKey']:
                err('Observation_SCOPE', loc, 'Read and observation must pin the same authorization context.')
            if observation['observedAt'] < read['startedAt'] or (read['endedAt'] is not None and observation['observedAt'] > read['endedAt']):
                err('TIME_ORDER', loc, 'Observed response falls outside its read attempt.')

    for service in records['Service']:
        for membership in service['memberships']:
            for jid in membership['userJourneyIds']:
                journey = get('UserJourney', jid)
                if journey and journey['systemId'] != membership['systemId']:
                    err('MEMBERSHIP_PARENT', service['serviceId'], 'A journey must belong to the selected system.')
    contexts = {}
    for context in records['EventContext']:
        key = (context['healthEventId'], context['kind'], context['contextKey'])
        if key in contexts and contexts[key] != context['eventContextId']:
            err('CONTEXT_IDENTITY', context['eventContextId'], 'Health context identity is duplicated.')
        contexts[key] = context['eventContextId']
        expected = context['accountId'] if context['kind'] == 'ACCOUNT' else context['organizationId']
        if context['kind'] != 'PUBLIC' and context['contextKey'] != expected:
            err('CONTEXT_KEY', context['eventContextId'], 'Non-null context key must equal its actual account/organization identity.')
    for impact in records['EntityImpact']:
        context = get('EventContext', impact['eventContextId'])
        source = observation_source(impact['selectedObservation'])
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
            detail = get('Observation', finding['selectedDetailObservation'])
            if recommendation and (not detail or recommendation['source'] != detail['source']):
                err('CURRENT_DETAIL_SCOPE', loc, 'Current suggestions must come from the exact selected detail Source version; a repeated receipt may reuse that suggestion identity.')
    for recommendation in records['Recommendation']:
        finding = get('Finding', recommendation['findingId'])
        observation = get('Observation', recommendation['findingDetailObservation'])
        source = get('Source', recommendation['source'])
        if finding and finding['serviceId'] != recommendation['serviceId']:
            err('RECOMMENDATION_PARENT', recommendation['recommendationId'], 'Finding and suggestion must share service scope.')
        if observation and observation['source'] != recommendation['source']:
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
            observation = get('Observation', membership['observation'])
            source = observation_source(membership['observation'])
            if membership['investigationId'] != investigation['investigationId'] or (execution and execution['agentSpaceId'] != investigation['agentSpaceId']):
                err('EXECUTION_MEMBERSHIP_SCOPE', investigation['investigationId'], 'Observed execution membership crosses task/Agent Space scope.')
            if execution and source and identity_key(source['identity']) != identity_key(execution['identity']):
                err('EXECUTION_MEMBERSHIP_EVIDENCE', investigation['investigationId'], 'Membership must cite the observed execution identity.')
            if observation and observation['readAttempt']:
                read = get('ReadAttempt', observation['readAttempt'])
                collection = get('Collection', read['collectionId']) if read else None
                query = next((q for q in collection['queries'] if q['queryKey'] == read['queryKey']), None) if collection else None
                if query and {k:v for k,v in query['subject'].items() if k != 'version'} != {'kind': 'Investigation', 'id': investigation['investigationId']}:
                    err('EXECUTION_MEMBERSHIP_EVIDENCE', investigation['investigationId'], 'Task relationship must retain the ListExecutions request association.')
            if membership['executionId'] in seen:
                err('DUPLICATE_MEMBERSHIP', investigation['investigationId'], 'Current execution memberships must be deduplicated.')
            seen.add(membership['executionId'])
    for journal in records['JournalRecord']:
        observation = get('Observation', journal['selectedObservation'])
        if observation and observation['source'] != journal['selectedSource']:
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
            if value.get('kind') == 'Observation' and 'id' in value:
                evidence.append(value)
            evidence.extend(value.get('observations', []))
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

    for scenario in records['Scenario']:
        definition = scenario['definition']; loc = scenario['scenarioId'] + '@' + str(scenario['version'])
        dag(definition['steps'], loc)
        if scenario['state'] == 'DRAFT':
            continue
        if 'operationLocks' not in definition:
            continue  # An archived draft has no invented publication locks.
        if digest(definition) != scenario['digest'] or digest(definition['inputSchema']) != definition['inputSchemaDigest']:
            err('SCENARIO_DIGEST', loc, 'Published definition/input schema digest is inconsistent.')
        try:
            Draft202012Validator.check_schema(definition['inputSchema'])
        except Exception as exc:
            err('INPUT_SCHEMA', loc, str(exc))
        if definition['inputSchema'].get('type') != 'object' or definition['inputSchema'].get('additionalProperties') is not False:
            err('INPUT_SCHEMA', loc, 'Published input schema must be a closed top-level object.')
        locks = {x['alias']: x for x in definition['operationLocks']}
        if len(locks) != len(definition['operationLocks']) or any(s['operationAlias'] not in locks for s in definition['steps']):
            err('OPERATION_LOCK', loc, 'Each step must have one resolved immutable operation lock.')
    for run in records['Run']:
        revision = get('Scenario', run['scenario'])
        snapshot_record = get('Snapshot', run['inputSnapshot'])
        if not revision or not snapshot_record:
            continue
        if revision['state'] != 'PUBLISHED':
            err('RUN_SCENARIO_PUBLICATION', run['runId'], 'A Run must pin an exact published Scenario version.'); continue
        admission = snapshot_record['contents']
        if snapshot_record['kind'] != 'RUN_INPUT' or admission.get('scenario') != run['scenario'] or admission.get('scenarioDigest') != revision['digest']:
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
        step_rows = [get('StepRun', ref) for ref in run['steps']]
        step_rows = [s for s in step_rows if s is not None]
        if len(step_rows) != len(run['steps']) or len({s['stepRunId'] for s in step_rows}) != len(step_rows) or any(s['runId'] != run['runId'] for s in step_rows):
            err('STEP_RUN_REFERENCE', run['runId'], 'Run must select exact versions of its own distinct steps.')
        if {s['stepKey'] for s in step_rows} != set(definitions):
            err('STEP_RUN_COVERAGE', run['runId'], 'All declared steps, including zero-attempt/skipped ones, need a retained StepRun.')
        values = {}
        for step in step_rows:
            selected = get('StepAttempt', step['selectedAttempt']) if step['selectedAttempt'] else None
            if step['selectedAttempt'] and (not selected or step['selectedAttempt'] not in step['attempts'] or selected['stepRunId'] != step['stepRunId']):
                err('ATTEMPT_SELECTION', step['stepRunId'], 'Selected attempt must be one exact known version owned by this step.')
            if step['stepKey'] in required and selected and selected['checkResult']:
                values[step['stepKey']] = selected['checkResult']['verdict']
        expected_verdict = verdict(admission['requiredCriterionKeys'], values)
        if run['phase'] != 'TERMINAL' and not values:
            expected_verdict = 'NOT_EVALUATED'
        if run['assessmentVerdict'] != expected_verdict:
            err('RUN_VERDICT', run['runId'], 'Verdict must use pinned child versions and retain missing/skipped required criteria.')
        if run['phase'] == 'TERMINAL' and run['terminalAt'] is None:
            err('RUN_STATE', run['runId'], 'Terminal Run requires a terminal timestamp.')
        latest = {}
        for attempt in sorted((get('StepAttempt', r) for step in step_rows for r in step['attempts'] if get('StepAttempt', r)), key=lambda a: a['settledAt'] or a['startedAt']):
            for effect in attempt['externalOperations']:
                latest[effect['originEffectKey']] = effect['remoteDisposition']
        if run['finalizationState'] == 'COMPLETE' and any(s in ('ACTIVE', 'UNKNOWN') for s in latest.values()):
            err('UNRESOLVED_FINALIZATION', run['runId'], 'Complete finalization cannot hide an active or unknown tracked effect.')

    for projection in records['Projection']:
        value, loc, profile = projection['value'], projection['projectionId'], projection['profile']
        def subject_version(kind, ident):
            selected = [r for r in projection['subjectRefs'] if r['kind'] == kind and r['id'] == ident]
            if len(selected) != 1:
                err('PROJECTION_SUBJECT', loc, 'Profile subject must select one exact entity representation.')
                return None
            return get(kind, selected[0])
        if projection['generatedAt'] < projection['asOf']:
            err('TIME_ORDER', loc, 'Projection generation precedes its as-of cutoff.')
        if profile == 'EVALUATION':
            if value['subject'] not in projection['subjectRefs']:
                err('PROJECTION_SUBJECT', loc, 'Evaluation subject must match its exact published subject reference.')
            results = {c['criterionKey']: c['result']['verdict'] for c in value['criteria']}
            for criterion in value['criteria']:
                check_result(criterion['result'], loc + '/' + criterion['criterionKey'])
            if len(results) != len(value['criteria']) or value['verdict'] != verdict(value['requiredCriterionKeys'], results):
                err('EVALUATION_VERDICT', loc, 'Evaluation must preserve its required criterion denominator.')
        elif profile == 'SERVICE_STATUS':
            subject_version('Service', value['serviceId'])
            context = get('Snapshot', value['policyContextSnapshot'])
            if context and (context['kind'] != 'POLICY_CONTEXT' or context['contents']['serviceId'] != value['serviceId']):
                err('POLICY_CONTEXT_SCOPE', loc, 'Status must use the retained policy context of the same service.')
            for dimension in ('runtimeHealth', 'resiliencePosture', 'assessmentExecution'):
                if value[dimension]['state'] not in ('UNKNOWN', 'UNAVAILABLE', 'NOT_OBSERVED') and not value[dimension]['evidenceRefs']:
                    err('STATUS_EVIDENCE', loc, f'{dimension} cannot become known without independent evidence.')
                expiry = value[dimension]['expiresAt']
                if expiry is not None and expiry <= projection['asOf'] and value[dimension]['state'] not in ('UNKNOWN', 'STALE', 'UNAVAILABLE', 'NOT_OBSERVED'):
                    err('EXPIRED_CURRENT_STATUS', loc, f'{dimension} has expired; retained raw evidence cannot remain a current known state.')
        elif profile == 'INVESTIGATION_RESULT':
            subject_version('Investigation', value['investigationId'])
            source = get('Source', value['selectedSource'])
            completion = observation_source(value['completionObservation'])
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
            deployment = subject_version('ComponentDeployment', value['componentDeploymentId'])
            if deployment and deployment['observation'] != value['deploymentObservation']:
                err('DEPLOYMENT_PROVENANCE', loc, 'Exposure must use the exact observed component deployment.')
            entries = [e for e in records['LifecycleEntry'] if e['source'] == value['catalogSource']]
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
        snapshot_record = get('Snapshot', assessment['policyContextSnapshot'])
        posture = get('Projection', assessment['selectedPostureProjection'])
        if snapshot_record and (snapshot_record['kind'] != 'POLICY_CONTEXT' or snapshot_record['contents']['serviceId'] != assessment['serviceId']):
            err('ASSESSMENT_POLICY_SCOPE', assessment['resilienceAssessmentId'], 'Assessment context must stay within its service.')
        if posture and (posture['profile'] != 'SERVICE_STATUS' or posture['value']['serviceId'] != assessment['serviceId'] or (snapshot_record and posture['value']['policyContextSnapshot'] != {'kind':'Snapshot','id':snapshot_record['snapshotId'],'version':snapshot_record['version']})):
            err('ASSESSMENT_POLICY_SCOPE', assessment['resilienceAssessmentId'], 'Selected posture must resolve the same captured policy context.')

    for snapshot_record in records['Snapshot']:
        loc = snapshot_record['snapshotId'] + '@' + str(snapshot_record['version'])
        own = ('Snapshot', snapshot_record['snapshotId'], snapshot_record['version'])
        members = {ref_key(r) for r in snapshot_record['members']}
        if len(members) != len(snapshot_record['members']):
            err('SNAPSHOT_MEMBER_UNIQUENESS', loc, 'An exact entity representation can occur only once in a manifest.')
        if digest({k: v for k, v in snapshot_record.items() if k != 'manifestDigest'}) != snapshot_record['manifestDigest']:
            err('SNAPSHOT_DIGEST', loc, 'Snapshot manifest does not match its retained content.')
        modeled = {k:v for k,v in snapshot_record.items() if k not in ('members', 'contents')}
        if snapshot_record['kind'] in ('TOPOLOGY', 'POLICY_CONTEXT', 'RUN_INPUT'):
            modeled['contents'] = snapshot_record['contents']
        required = list(exact_refs(modeled))
        for ref in snapshot_record['members']:
            row = get(ref['kind'], ref)
            if row is None:
                continue
            if row['updatedAt'] > snapshot_record['capturedAt']:
                err('SNAPSHOT_FUTURE_EVIDENCE', loc, 'Capture cannot pin an entity version published after its cutoff.')
            item = row
            if ref['kind'] == 'Snapshot' and row['kind'] not in ('TOPOLOGY','POLICY_CONTEXT','RUN_INPUT'):
                item = {k:v for k,v in row.items() if k != 'contents'}
            required.extend(exact_refs(item))
        if any(ref_key(r) not in members and ref_key(r) != own for r in required):
            err('SNAPSHOT_CLOSURE', loc, 'Capture lacks an exact transitive entity reference; latest substitution is prohibited.')
        if snapshot_record['captureStartedAt'] > snapshot_record['capturedAt'] or (snapshot_record['captureFinishedAt'] is not None and not snapshot_record['captureStartedAt'] <= snapshot_record['captureFinishedAt'] <= snapshot_record['capturedAt']):
            err('TIME_ORDER', loc, 'Capture start/finish/assembly times are inconsistent.')
        if snapshot_record['kind'] == 'RUN_INPUT' and any(r['kind'] in ('Run','StepRun','StepAttempt') for r in snapshot_record['members']):
            err('ADMISSION_FUTURE_STATE', loc, 'Admission captures inputs, not its own later execution state.')
        if snapshot_record['kind'] == 'POLICY_CONTEXT':
            context = snapshot_record['contents']; observation = get('Observation', context['effectiveTargetObservation'])
            if observation and observation['source'] != context['effectiveTargetSource']:
                err('POLICY_TARGET_SELECTION', loc, 'Captured effective target Source and Observation versions do not match.')
            if ref_key(context['effectiveTargetSource']) not in members or ref_key(context['effectiveTargetObservation']) not in members:
                err('POLICY_TARGET_SELECTION', loc, 'Effective targets must be pinned in this policy capture.')
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
    for row in examples['records']['Source']:
        assert row['profile'] in profiles, f'Unregistered fixture source profile: {row["profile"]}'
        assert row['profileVersion'] == profiles[row['profile']]['sourceBinding']['profileVersion'], 'Source profile version drift.'
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
    manifest = load(ROOT / 'diagrams/manifest.json')
    assert manifest['format'] == 'drawio-atlas/1', 'All maintained diagrams must use the Draw.io atlas.'
    assert manifest['schemaSha256'] == hashlib.sha256((ROOT / 'model/schema.json').read_bytes()).hexdigest(), 'Diagram schema provenance is stale.'
    atlas = ROOT / manifest['drawio']['path']
    assert hashlib.sha256(atlas.read_bytes()).hexdigest() == manifest['drawio']['sha256'], 'Draw.io source hash mismatch.'
    document = ET.parse(atlas).getroot()
    assert document.tag == 'mxfile', 'Diagram source is not an editable Draw.io document.'
    pages = {p.attrib['id']: p for p in document.findall('diagram')}
    assert len(pages) == len(manifest['diagrams']), 'Diagram page count mismatch.'
    entities = set(model['x-entities']); detailed_entities = set(); detailed_edges = set()
    for diagram in manifest['diagrams']:
        page = pages[diagram['id']]
        root = page.find('mxGraphModel/root')
        assert root is not None, 'Draw.io page lacks native editable cells.'
        classes = {o.attrib['entity']: o for o in root.findall('object') if 'entity' in o.attrib}
        assert set(classes) == set(diagram['entities']) <= entities, 'Draw.io class coverage mismatch.'
        boxes = []
        for name, obj in classes.items():
            cell = obj.find('mxCell'); geom = cell.find('mxGeometry')
            field_cell = root.find(f"mxCell[@id='{obj.attrib['id']}-fields']")
            assert field_cell is not None and 'version: Version' in field_cell.attrib['value'], 'Every displayed entity needs its uniform version.'
            assert set(obj.attrib['displayFields'].split(',')) <= set(model['$defs'][name]['properties']), 'Diagram shows an obsolete field.'
            x,y,w,h = (float(geom.attrib[k]) for k in ('x','y','width','height'))
            boxes.append((name,x,y,x+w,y+h))
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                assert not (max(a[1],b[1]) < min(a[3],b[3]) and max(a[2],b[2]) < min(a[4],b[4])), 'Overlapping Draw.io classes: ' + repr((a[0],b[0]))
        edge_ids = set()
        for obj in root.findall('object'):
            if 'relationshipIndex' not in obj.attrib:
                continue
            index = int(obj.attrib['relationshipIndex']); edge_ids.add(index)
            relation = model['x-relationships'][index]; cell = obj.find('mxCell')
            assert obj.attrib['fromEntity'] == relation['from'] and obj.attrib['toEntity'] == relation['to'], 'Draw.io relationship direction drift.'
            assert cell.attrib['source'] == classes[relation['from']].attrib['id'] and cell.attrib['target'] == classes[relation['to']].attrib['id'], 'Draw.io edge is attached to the wrong class.'
            for suffix, cardinality in (('from','fromCardinality'),('to','toCardinality')):
                label = root.find(f"mxCell[@id='{obj.attrib['id']}-{suffix}']")
                assert label is not None and label.attrib['value'] == relation[cardinality], 'Draw.io cardinality drift.'
        assert edge_ids == set(diagram['relationshipIds']), 'Draw.io relationship manifest differs from actual edges.'
        if diagram['kind'] == 'overview':
            assert set(classes) == entities, 'Overview must include every entity.'
        else:
            detailed_entities.update(diagram['primaryEntities']); detailed_edges.update(edge_ids)
        for kind in ('svg', 'png'):
            item = diagram[kind]; path = ROOT / item['path']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], 'Stale diagram hash: ' + item['path']
        ET.parse(ROOT / diagram['svg']['path'])
    assert detailed_entities == entities, 'Detailed sheets must cover every entity.'
    assert detailed_edges == set(range(len(model['x-relationships']))), 'Detailed sheets must cover every relationship.'
    assert not list((ROOT/'diagrams').glob('*.mmd')) and not list((ROOT/'diagrams').glob('*.dot')), 'Obsolete diagram pipelines remain in the maintained package.'
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


def select_case_record(rows, entity, selector):
    matches = [r for r in rows if r[primary(entity)] == selector['id'] and ('version' not in selector or r['version'] == selector['version'])]
    if not matches:
        raise AssertionError('Case references an unavailable exact entity version: ' + repr(selector))
    return max(matches, key=lambda x: x['version'])


def apply_cases(base, schema):
    cases = load(ROOT / 'examples/semantic-cases.json')['cases']
    for case in cases:
        candidate = copy.deepcopy(base)
        for mutation in case.get('mutations', []):
            rows = candidate['records'][mutation['entity']]
            record = select_case_record(rows, mutation['entity'], mutation)
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
            row = select_case_record(candidate['records'][target['entity']], target['entity'], target)
            if target['entity'] == 'Snapshot':
                row['manifestDigest'] = digest({k: v for k, v in row.items() if k != 'manifestDigest'})
            elif target['entity'] == 'Source':
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
            row = select_case_record(candidate['records'][assertion['entity']], assertion['entity'], assertion)
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
        'Diagram checks establish Draw.io entity/relationship coverage and export provenance; visual review is a separate recorded gate.',
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
