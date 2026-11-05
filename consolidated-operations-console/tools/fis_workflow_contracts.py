"""Offline invariants for the FIS/workflow review additions.

These checks validate captured contracts, not adapters, persistence, scheduler
behavior, metric evaluation or a source-completeness guarantee.
"""
from collections import defaultdict

QUERY = 'console.telemetry.metric-query/v1'
METRIC = 'console.telemetry.metric-observation/v1'
CRITERION = 'console.telemetry.criterion/v1'
WORKFLOW_OBSERVATION = 'console.workflow.observation/v1'
EVALUATION_INPUT = 'console.telemetry.evaluation-input/v1'
NORMALIZED = {QUERY, METRIC, CRITERION, WORKFLOW_OBSERVATION}
TERMINAL = {'SUCCEEDED', 'FAILED', 'CANCELED', 'TIMED_OUT', 'INDETERMINATE'}
# These are native identities, adapter JSON or explanatory values, matching the
# core validator's opaque boundaries. Their property names do not acquire
# console reference semantics when included in a captured entity.
_OPAQUE_REFERENCE_FIELDS = {
    'identity', 'sourceIdentity', 'providerIdentity', 'parentExecutionIdentity',
    'executionPointerIdentity', 'primaryTaskIdentity', 'registeredServiceIdentity',
    'expectedSummaryIdentity', 'deploymentIdentity', 'payload', 'suggestion',
    'inputSchema', 'inputValues', 'inputBindings', 'filters', 'allowedScopes',
    'actualSummary', 'expectedSummary', 'importedFrom',
}


def reference_key(value):
    return value.get('kind'), value.get('id'), value.get('version')


def exact_references(value):
    """Walk a value already known to contain only modeled console fields.

    Arbitrary native JSON is not a console-reference namespace. In particular,
    normalized Source payloads must go through normalized_payload_references.
    """
    if isinstance(value, dict):
        if {'kind', 'id', 'version'} <= value.keys():
            yield value
        else:
            for field, child in value.items():
                if field not in _OPAQUE_REFERENCE_FIELDS:
                    yield from exact_references(child)
    elif isinstance(value, list):
        for child in value:
            yield from exact_references(child)


def normalized_payload_references(source):
    """Yield only explicitly typed reference slots of the normalized profiles.

    WorkflowObservationValue.value is arbitrary native/adapter JSON, even when
    a body happens to have kind/id/version fields. valueSchemaDigest does not
    turn those fields into console references. Keep this same boundary for
    both direct validation and transitive capture closure.
    """
    if source.get('payloadStorage') != 'INLINE':
        return
    payload = source.get('payload')
    if not isinstance(payload, dict):
        return
    profile = source.get('profile')
    if profile == METRIC and 'querySource' in payload:
        yield 'querySource', payload['querySource']
    fields = ('nativeEvidence',) if profile in {QUERY, METRIC} else ('evidenceRefs',) if profile == WORKFLOW_OBSERVATION else ()
    for field in fields:
        for index, reference in enumerate(payload.get(field, [])):
            yield field + '/' + str(index), reference
    if profile in {METRIC, WORKFLOW_OBSERVATION}:
        for index, reference in enumerate(payload.get('coverage', {}).get('readAttempts', [])):
            yield 'coverage/readAttempts/' + str(index), reference


def _primary(kind):
    return kind[0].lower() + kind[1:] + 'Id'


def _closed_action_references(experiment):
    # Preserve the earlier contract's closed-reference validation when the new
    # field is absent. That legacy validation policy is not provider-hydration
    # evidence. Only an explicit incomplete mode permits unloaded endpoints.
    return experiment.get('actionCompleteness') not in {'PARTIAL', 'UNKNOWN'}


def contract_errors(examples):
    """Return structured errors for a grouped model examples/records document."""
    records = examples.get('records', examples)
    errors = []
    index = {}
    for kind, rows in records.items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and _primary(kind) in row and 'version' in row:
                index[(kind, row[_primary(kind)], row['version'])] = row

    def fail(code, where, message):
        errors.append({'code': code, 'location': where, 'message': message})

    def resolve(ref, where, expected=None, profile=None, owner=None):
        if not isinstance(ref, dict) or not {'kind', 'id', 'version'} <= ref.keys():
            fail('REVIEW_EXACT_REFERENCE', where, 'An exact entity kind, ID and version is required.')
            return None
        row = index.get(reference_key(ref))
        if row is None:
            fail('REVIEW_EXACT_REFERENCE', where, 'The exact referenced entity version is unavailable; latest substitution is prohibited.')
        elif expected and ref['kind'] != expected:
            fail('REVIEW_REFERENCE_KIND', where, 'Referenced entity kind does not match the declared owner/value contract.')
            return None
        elif profile and row.get('profile') != profile:
            fail('TELEMETRY_PROFILE', where, 'The referenced Source has a different profile from the required normalized contract.')
            return None
        if row is not None and owner is not None:
            if row.get('workspaceId') != owner.get('workspaceId'):
                fail('REFERENCE_SCOPE', where, 'A typed normalized reference must resolve within its owning record workspace.')
                return None
            if row['updatedAt'] > owner['updatedAt']:
                fail('REFERENCE_FUTURE_VERSION', where, 'A typed normalized reference cannot name a version published after its owning record.')
                return None
        return row

    def window(value, where):
        if isinstance(value, dict) and 'start' in value and 'end' in value and value['start'] > value['end']:
            fail('EVIDENCE_WINDOW_ORDER', where, 'Event-time window start must not follow its end.')

    def source_payload(ref, where, profile, owner=None):
        source = resolve(ref, where, 'Source', profile, owner)
        if source is None:
            return None
        if source.get('payloadStorage') != 'INLINE':
            fail('NORMALIZED_ARTIFACT_UNVERIFIED', where, 'Materialize and validate artifact content before using it as normalized input.')
            return None
        return source.get('payload')

    # FIS dependency edges belong to one captured Experiment version. A cycle
    # in observed edges is conclusive even when other children remain unloaded;
    # missing endpoints fail a COMPLETE or legacy closed-reference contract.
    # Explicit PARTIAL/UNKNOWN permits unloaded endpoints; legacy validation
    # policy must not be mistaken for proof of provider population completeness.
    for experiment in records.get('Experiment', []):
        where = experiment['experimentId'] + '@' + str(experiment['version'])
        actions = experiment.get('actions', [])
        action_names = {action['actionName'] for action in actions}
        if len(action_names) != len(actions):
            fail('FIS_ACTION_IDENTITY', where, 'Named action values must be unique within this Experiment version.')
        successors = {name: set() for name in action_names}
        for action in actions:
            name = action['actionName']
            predecessors = action.get('startAfter', [])
            if len(predecessors) != len(set(predecessors)):
                fail('FIS_ACTION_DEPENDENCY_DUPLICATE', where + '/actions/' + name, 'An experiment-local predecessor/successor edge cannot occur more than once.')
            for predecessor in set(predecessors):
                if predecessor == name:
                    fail('FIS_ACTION_SCOPE', where + '/actions/' + name, 'An action cannot depend on itself.')
                elif predecessor not in action_names and _closed_action_references(experiment):
                    fail('FIS_ACTION_SCOPE', where + '/actions/' + name, 'COMPLETE and unmarked legacy action captures require experiment-local endpoints; explicit PARTIAL/UNKNOWN permits unloaded children.')
                if predecessor in action_names:
                    successors[predecessor].add(name)
        incoming = dict.fromkeys(action_names, 0)
        for children in successors.values():
            for child in children:
                incoming[child] += 1
        ready = [name for name, count in incoming.items() if count == 0]
        visited = 0
        while ready:
            name = ready.pop()
            visited += 1
            for child in successors[name]:
                incoming[child] -= 1
                if incoming[child] == 0:
                    ready.append(child)
        if visited != len(action_names):
            fail('FIS_ACTION_CYCLE', where, 'The observed same-experiment dependency edges contain a cycle.')

        # Membership identity is independent of selector identity. No parsing.
        if 'targetSelections' not in experiment:
            continue  # historical captures did not record this normalized join
        names = [selector['targetName'] for selector in experiment['targetSelections']]
        if len(names) != len(set(names)):
            fail('FIS_SELECTOR_IDENTITY', where, 'Target names must be unique within this Experiment version.')
        membership_keys = [item.get('selectionKey') for item in experiment.get('targetMemberships', [])]
        if len(membership_keys) != len(set(membership_keys)):
            fail('FIS_MEMBERSHIP_IDENTITY', where, 'Resolved membership keys must be unique within this Experiment version.')
        complete = experiment.get('targetSelectionCompleteness') == 'COMPLETE'
        for item in experiment.get('targetMemberships', []):
            if 'targetName' not in item:
                fail('FIS_SELECTOR_JOIN', where, 'Every normalized membership needs its explicit targetName.')
            elif complete and item['targetName'] not in names:
                fail('FIS_SELECTOR_JOIN', where, 'Membership references a selector absent from the complete experiment-local selector set.')
        for action in experiment.get('actions', []):
            if complete and any(name not in names for name in action.get('targetBindings', {}).values()):
                fail('FIS_SELECTOR_JOIN', where, 'Action target slot references a selector outside this Experiment version.')

    # Bound normalized Source profiles have exact reference and numerical scope checks.
    for source in records.get('Source', []):
        if source.get('profile') not in NORMALIZED or source.get('payloadStorage') != 'INLINE':
            continue
        where = source['sourceId'] + '@' + str(source['version'])
        payload = source.get('payload', {})
        if not isinstance(payload, dict):
            continue  # JSON Schema reports a malformed payload
        for path, ref in normalized_payload_references(source):
            resolve(ref, where + '/payload/' + path, owner=source)
        if source['profile'] == QUERY:
            if source.get('identity', {}).get('scope') != payload.get('scope'):
                fail('TELEMETRY_SCOPE', where, 'Metric query scope must equal the qualified Source owning scope.')
        elif source['profile'] == METRIC:
            query = source_payload(payload.get('querySource'), where, QUERY, source)
            window(payload.get('window'), where)
            if query:
                for key in ('unit', 'periodSeconds', 'normalizationDigest'):
                    if query.get(key) != payload.get(key):
                        fail('TELEMETRY_QUERY_PIN', where, 'Metric sample '+key+' differs from its exact query definition.')
                if source.get('identity', {}).get('scope') != query.get('scope'):
                    fail('TELEMETRY_SCOPE', where, 'Metric samples and query use different owning scopes.')
            times = [x['timestamp'] for x in payload.get('samples', []) if 'timestamp' in x]
            if times != sorted(set(times)):
                fail('TELEMETRY_SAMPLE_ORDER', where, 'Samples for one query series must have distinct, increasing timestamps.')
            interval = payload.get('window', {})
            if 'start' in interval and 'end' in interval and any(not interval['start'] <= t < interval['end'] for t in times):
                fail('TELEMETRY_SAMPLE_WINDOW', where, 'A sample falls outside its declared half-open event-time window.')
            coverage = payload.get('coverage', {})
            if interval and (coverage.get('windowStart'), coverage.get('windowEnd')) != (interval.get('start'), interval.get('end')):
                fail('TELEMETRY_COVERAGE_WINDOW', where, 'Sample coverage must describe the same event-time window.')
            if payload.get('collectionState') == 'UNAVAILABLE' and coverage.get('claim') == 'SUFFICIENT':
                fail('TELEMETRY_UNAVAILABLE_COVERAGE', where, 'Unavailable collection cannot claim sufficient numeric evidence.')
        elif source['profile'] == WORKFLOW_OBSERVATION:
            window(payload.get('window'), where)
            if payload.get('scope') != payload.get('source', {}).get('scope') or payload.get('scope') != source.get('identity', {}).get('scope'):
                fail('WORKFLOW_OBSERVATION_SCOPE', where, 'Observation scope differs from its qualified source scope.')
            interval = payload.get('window', {})
            coverage = payload.get('coverage', {})
            if interval and (coverage.get('windowStart'), coverage.get('windowEnd')) != (interval.get('start'), interval.get('end')):
                fail('WORKFLOW_OBSERVATION_WINDOW', where, 'Observation coverage must describe the same event-time window.')
            if payload.get('collection') == 'UNAVAILABLE' and coverage.get('claim') == 'SUFFICIENT':
                fail('WORKFLOW_OBSERVATION_COVERAGE', where, 'Unavailable collection cannot claim sufficient observation evidence.')

    # Snapshot owns the experiment/query/criterion/window relation without a Run.
    typed_snapshots = {}
    for snap in records.get('Snapshot', []):
        contents = snap.get('contents')
        if snap.get('kind') != 'EVALUATION_INPUT' or not isinstance(contents, dict) or contents.get('contractProfile') != EVALUATION_INPUT:
            continue
        where = snap['snapshotId'] + '@' + str(snap['version'])
        typed_snapshots[('Snapshot', snap['snapshotId'], snap['version'])] = contents
        for ref in exact_references(contents):
            resolve(ref, where + '/contents', owner=snap)
        if contents.get('subject') not in snap.get('subjectRefs', []):
            fail('TELEMETRY_SUBJECT', where, 'Captured telemetry subject must be an exact Snapshot subject.')
        resolve(contents.get('subject'), where, 'Experiment')
        cutoff = contents.get('evidenceCutoffAt')
        if cutoff is not None and cutoff > snap.get('capturedAt', cutoff):
            fail('TELEMETRY_CUTOFF', where, 'Evidence cutoff cannot be later than capture assembly.')
        criterion_keys = []
        for binding in contents.get('telemetryBindings', []):
            if binding.get('experiment') != contents.get('subject'):
                fail('TELEMETRY_SUBJECT', where, 'Every binding belongs to the exact Experiment version under evaluation.')
            experiment = resolve(binding.get('experiment'), where, 'Experiment')
            query = source_payload(binding.get('querySource'), where, QUERY, snap)
            criterion = source_payload(binding.get('criterionSource'), where, CRITERION, snap)
            window(binding.get('window'), where)
            if criterion:
                criterion_keys.append(criterion.get('criterionKey'))
                if query and criterion.get('unit') != query.get('unit'):
                    fail('TELEMETRY_UNIT', where, 'Criterion and query units differ; conversion cannot be inferred.')
                if criterion.get('timingAnchor') == 'ACTION_START' and experiment and _closed_action_references(experiment) and criterion.get('actionName') not in {x['actionName'] for x in experiment.get('actions', [])}:
                    fail('TELEMETRY_ANCHOR', where, 'An action anchor must name an action in the captured Experiment version.')
            accepted = binding.get('acceptedEvidence', [])
            for ref in [binding.get('anchorEvidence')] + accepted:
                evidence = resolve(ref, where)
                if evidence and cutoff is not None:
                    known = evidence.get('observedAt', evidence.get('updatedAt', cutoff))
                    if known > cutoff or evidence.get('updatedAt', cutoff) > cutoff:
                        fail('TELEMETRY_CUTOFF', where, 'Accepted evidence was not known by the sealed evaluation cutoff.')
            for ref in accepted:
                evidence = resolve(ref, where)
                if evidence and ref['kind'] == 'Observation':
                    evidence = resolve(evidence.get('source'), where, 'Source')
                if not evidence:
                    continue
                if evidence.get('profile') != METRIC or evidence.get('payloadStorage') != 'INLINE':
                    fail('TELEMETRY_ACCEPTED_EVIDENCE', where, 'Numeric evaluation requires verified normalized metric evidence, not an arbitrary retained payload.')
                    continue
                value = evidence.get('payload', {})
                if cutoff is not None and (evidence.get('updatedAt', cutoff) > cutoff or value.get('observedAt', cutoff) > cutoff):
                    fail('TELEMETRY_CUTOFF', where, 'Accepted normalized values and their Source versions must be known by the sealed evaluation cutoff.')
                if value.get('querySource') != binding.get('querySource'):
                    fail('TELEMETRY_BINDING_PIN', where, 'Accepted observations must reference the exact captured query version.')
                observed, intended = value.get('window', {}), binding.get('window', {})
                if observed and intended and not intended['start'] <= observed['start'] <= observed['end'] <= intended['end']:
                    fail('TELEMETRY_BINDING_WINDOW', where, 'Accepted metric observation lies outside the association event window.')
        if len(criterion_keys) != len(set(criterion_keys)):
            fail('TELEMETRY_CRITERION_IDENTITY', where, 'Each criterion key must occur once in a captured experiment evaluation.')
        # Include transitive typed payload references in the capture closure.
        members = {reference_key(r) for r in snap.get('members', [])}
        pending = list(exact_references(contents)); seen = set()
        while pending:
            reference = pending.pop(); key = reference_key(reference)
            if key in seen:
                continue
            seen.add(key)
            if key not in members:
                fail('TELEMETRY_CAPTURE_CLOSURE', where, 'Capture lacks an exact reference required by its typed evaluation context.')
            value = resolve(reference, where)
            if value is None:
                continue
            modeled = dict(value)
            if reference['kind'] == 'Source':
                modeled.pop('payload', None)
                pending.extend(ref for _, ref in normalized_payload_references(value))
            if reference['kind'] == 'Snapshot' and key != ('Snapshot',snap['snapshotId'],snap['version']):
                modeled.pop('contents', None)
            pending.extend(exact_references(modeled))
    for projection in records.get('Projection', []):
        if projection.get('profile') != 'EVALUATION':
            continue
        value = projection.get('value', {})
        capture = typed_snapshots.get(reference_key(value.get('inputSnapshot', {})))
        if capture and (value.get('subject') != capture.get('subject') or value.get('evidenceCutoffAt') != capture.get('evidenceCutoffAt')):
            fail('TELEMETRY_EVALUATION_CONTEXT', projection['projectionId'], 'Projection subject and cutoff must match the exact typed input capture.')

    # Recovery checks run on all retained versions, not only the current head.
    histories = defaultdict(list)
    for attempt in records.get('StepAttempt', []):
        histories[attempt['stepAttemptId']].append(attempt)
        recovery = attempt.get('recovery')
        if not recovery:
            continue
        where = attempt['stepAttemptId'] + '@' + str(attempt['version'])
        values = [recovery['resolvedInputs']]
        checkpoint = recovery.get('checkpoint')
        if checkpoint:
            values.append(checkpoint['value'])
            if not attempt.get('startedAt', 0) <= checkpoint['recordedAt'] <= attempt.get('updatedAt', checkpoint['recordedAt']):
                fail('ATTEMPT_CHECKPOINT_TIME', where, 'Checkpoint time must lie within the recorded attempt lifecycle.')
        for value in values:
            source = resolve(value.get('source'), where, 'Source')
            if source and source.get('contentDigest') != value.get('contentDigest'):
                fail('ATTEMPT_VALUE_DIGEST', where, 'Resolved-input/checkpoint digest must match its exact retained Source.')
        if recovery.get('error') and attempt.get('outcome') == 'SUCCEEDED':
            fail('ATTEMPT_ERROR_OUTCOME', where, 'A successful technical attempt cannot carry a terminal execution error.')
        run_versions = [r for r in records.get('Run', []) if r.get('runId') == attempt.get('runId')]
        step_versions = [s for s in records.get('StepRun', []) if s.get('stepRunId') == attempt.get('stepRunId') and s.get('runId') == attempt.get('runId')]
        if not run_versions or not step_versions:
            fail('ATTEMPT_RECOVERY_CONTEXT', where, 'Recovery validation requires the owning Run and StepRun context.')
        elif len({reference_key(r.get('scenario', {})) for r in run_versions}) != 1 or len({s.get('stepKey') for s in step_versions}) != 1:
            fail('ATTEMPT_RECOVERY_CONTEXT', where, 'A stable Run and StepRun cannot change the pinned Scenario or step key used for recovery.')
        else:
            scenario = resolve(run_versions[0].get('scenario'), where, 'Scenario')
            if scenario:
                definition = scenario.get('definition', {})
                step = next((s for s in definition.get('steps', []) if s.get('stepKey') == step_versions[0].get('stepKey')), None)
                lock = next((l for l in definition.get('operationLocks', []) if step and l.get('alias') == step.get('operationAlias')), None)
                if not lock:
                    fail('ATTEMPT_RECOVERY_CONTEXT', where, 'Recovery requires the step operation lock from the admitted Scenario version.')
                else:
                    if recovery['resolvedInputs'].get('schemaDigest') != lock.get('inputSchemaDigest'):
                        fail('ATTEMPT_INPUT_SCHEMA', where, 'Resolved inputs must use the admitted operation lock input schema.')
                    if checkpoint and checkpoint['value'].get('schemaDigest') != lock.get('checkpointSchemaDigest'):
                        fail('ATTEMPT_CHECKPOINT_SCHEMA', where, 'Resume checkpoint must use the pinned operation checkpoint schema.')
    for identity, versions in histories.items():
        versions.sort(key=lambda a:a['version'])
        for previous, current in zip(versions, versions[1:]):
            before, after = previous.get('recovery'), current.get('recovery')
            if before and (not after or before['resolvedInputs'] != after['resolvedInputs']):
                fail('ATTEMPT_INPUT_RESEALED', identity, 'Once evaluated, resolved inputs cannot change or disappear across versions of the same attempt.')
            old_checkpoint = (before or {}).get('checkpoint'); new_checkpoint = (after or {}).get('checkpoint')
            if old_checkpoint and (not new_checkpoint or new_checkpoint['sequence'] < old_checkpoint['sequence'] or (new_checkpoint['sequence'] == old_checkpoint['sequence'] and new_checkpoint != old_checkpoint)):
                fail('ATTEMPT_CHECKPOINT_REWIND', identity, 'Checkpoint sequences advance monotonically; one sequence cannot name different contents.')
            if previous.get('outcome') in TERMINAL and before != after:
                fail('ATTEMPT_RECOVERY_AFTER_SEAL', identity, 'Settled recovery facts cannot be reopened; late reconciliation adds evidence.')
    for run in records.get('Run', []):
        where = run['runId'] + '@' + str(run['version'])
        for citation in run.get('evidenceCitations', []):
            resolve(citation.get('evidence'), where)
            attempts = citation.get('consumerAttempts', []) + ([citation['producerAttempt']] if citation.get('producerAttempt') else [])
            for reference in attempts:
                attempt = resolve(reference, where, 'StepAttempt')
                if attempt and attempt.get('runId') != run['runId']:
                    fail('RUN_EVIDENCE_SCOPE', where, 'Producer/consumer attempts in a Run evidence manifest must belong to that Run.')
    return errors
