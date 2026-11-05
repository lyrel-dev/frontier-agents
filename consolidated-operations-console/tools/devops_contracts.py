"""Offline invariants for the optional typed DevOps normalization bindings.

Historical v2 records without newly recorded metadata remain valid and unknown.
These checks assess proposed contracts/fixtures, not an implemented AWS adapter.
"""
from decimal import Decimal


def semantic_errors(examples, digest):
    records = examples.get('records', {})
    index = {}
    for kind, rows in records.items():
        field = kind[0].lower() + kind[1:] + 'Id'
        for row in rows:
            index.setdefault((kind, row.get(field), row.get('version')), []).append(row)
    errors = []

    def err(code, at, message):
        errors.append({'code': code, 'location': at, 'message': message})

    def key(ref):
        return (ref.get('kind'), ref.get('id'), ref.get('version')) if isinstance(ref, dict) else None

    def get(ref, owner=None):
        matches = index.get(key(ref), [])
        if owner is not None:
            matches = [row for row in matches if row.get('workspaceId') == owner.get('workspaceId')]
        return matches[0] if len(matches) == 1 else None

    def after(left, right):
        return left is not None and right is not None and Decimal(str(left)) > Decimal(str(right))

    def assertion(value, at, generated_at=None):
        if after(value.get('validFrom'), value.get('validUntil')):
            err('ASSERTION_VALIDITY_ORDER', at, 'Assertion validity end must not precede its start.')
        if after(value.get('observedAt'), generated_at):
            err('PROJECTION_OBSERVATION_TIME', at, 'A projection cannot include an observation received after its generation.')
        derivation = value.get('derivation') or {}
        expected = {'APPLICATION_INFERENCE': 'APPLICATION_INFERENCE', 'DETERMINISTIC_PARSE': 'DETERMINISTIC_PARSE'}
        if value.get('origin') in expected and derivation.get('method') != expected[value['origin']]:
            err('ASSERTION_ORIGIN', at, 'An inferred or parsed assertion must retain its matching derivation method.')

    def artifact(value, at, space=None, owner=None):
        resolved = get(value.get('asset'), owner)
        if value.get('asset') and resolved is None:
            err('ARTIFACT_RESOLUTION', at, 'An Asset resolution must pin a retained exact Asset version in the owner workspace.')
        if resolved:
            if space is not None and resolved.get('agentSpaceId') != space:
                err('ARTIFACT_SCOPE', at, 'Resolved Asset must belong to the investigation Agent Space.')
            if value.get('nativeAssetIdentity') != resolved.get('identity'):
                err('ARTIFACT_RESOLUTION', at, 'Resolved native Asset identity must match the pinned Asset record.')
            if value.get('nativeAssetVersion') is not None and str(value['nativeAssetVersion']) != str(resolved.get('nativeVersion')):
                err('ARTIFACT_RESOLUTION', at, 'The claimed native Asset version must match the exact resolved representation.')

    def evidence_scope(reference, at, owner, investigation):
        record = get(reference, owner)
        if record is None:
            err('PROJECTION_EVIDENCE_SCOPE', at, 'Evidence must resolve its exact retained version in the projection workspace.')
            return
        source = record if reference['kind'] == 'Source' else None
        if reference['kind'] == 'Observation':
            source = get(record.get('source'), owner)
            if source is None:
                err('PROJECTION_EVIDENCE_SCOPE', at, 'An observation citation must resolve its exact retained Source.')
        if not source or not investigation:
            return
        native_scope = source.get('identity', {}).get('scope', {})
        owning_scope = investigation.get('identity', {}).get('scope', {})
        native_space = native_scope.get('parentKeys', {}).get('agentSpaceId')
        owning_space = owning_scope.get('parentKeys', {}).get('agentSpaceId')
        # External telemetry may have no Agent Space parent. Compare only
        # explicitly supplied native scope; never equate native and console IDs.
        if native_space is not None and owning_space is not None:
            if native_space != owning_space or any(
                native_scope.get(field) != owning_scope.get(field)
                for field in ('partition', 'accountId', 'region', 'organizationId')
            ):
                err('PROJECTION_EVIDENCE_SCOPE', at, 'Evidence declares a different native Agent Space scope.')

    def command_owner(command, request_ref, request, at):
        subjects = command.get('subjectRefs', [])
        execution = None
        for kind, identity in [('ApprovalRequest', request['approvalRequestId']),
                               ('Execution', request.get('executionId')),
                               ('AgentSpace', request.get('agentSpaceId'))]:
            refs = [ref for ref in subjects if ref.get('kind') == kind]
            if len(refs) != 1 or refs[0].get('id') != identity:
                err('APPROVAL_SUBJECT', at, 'Approval commands must pin one matching ApprovalRequest, Execution and AgentSpace subject.')
                continue
            selected = refs[0]
            if kind == 'ApprovalRequest' and key(selected) != key(request_ref):
                err('APPROVAL_SUBJECT', at, 'The ApprovalRequest subject must equal the exact request version in the intent.')
            resolved = get(selected, command)
            if resolved is None:
                err('APPROVAL_OWNER_SCOPE', at, 'Approval command subjects must resolve exact versions in the command workspace.')
                continue
            if kind == 'Execution':
                execution = resolved
                if resolved.get('agentSpaceId') != request.get('agentSpaceId'):
                    err('APPROVAL_OWNER_SCOPE', at, 'ApprovalRequest and its selected Execution must share the Agent Space.')
        return execution

    for investigation in records.get('Investigation', []):
        for i, value in enumerate(investigation.get('artifactReferences', [])):
            artifact(value, f"Investigation:{investigation.get('investigationId')}/artifactReferences/{i}",
                     investigation.get('agentSpaceId'), investigation)

    for command in records.get('Command', []):
        at = f"Command:{command.get('commandId')}@{command.get('version')}"
        intent = command.get('approvalDecision')
        if intent:
            request = get(intent['approvalRequest'], command)
            if request is None:
                err('APPROVAL_CONTEXT', at, 'Decision must resolve the exact retained ApprovalRequest version in its workspace.')
            else:
                command_owner(command, intent['approvalRequest'], request, at)
                if command.get('expectedVersion') != intent['approvalRequest']['version']:
                    err('APPROVAL_VERSION_GUARD', at, 'Decision expectedVersion guards the pinned ApprovalRequest version.')
                if key(intent['requestSource']) not in {key(ref) for ref in command.get('subjectRefs', [])}:
                    err('APPROVAL_SUBJECT', at, 'Decision subjects must include the exact observed request Source.')
                invocation = request.get('invocation', {})
                if invocation.get('validation') != 'VALIDATED':
                    err('APPROVAL_INVOCATION', at, 'Unsupported or incomplete approval context cannot authorize dispatch.')
                if intent['requestSource'] != request.get('requestSource') or intent['expectedActionDigest'] != request.get('actionDigest'):
                    err('APPROVAL_CONTEXT', at, 'Decision input must match the pinned observed request Source and action digest.')
                if intent['decision'] == 'APPROVED' and intent['finalPattern'] != invocation.get('requestedPattern'):
                    err('APPROVAL_SCOPE', at, 'The console permits exactly the requested single-use pattern; never widen, reinterpret, or silently narrow pins.')
        resume = command.get('approvalResume')
        if resume:
            request = get(resume['approvalRequest'], command)
            decision = get(resume['decisionCommand'], command)
            if request is None or decision is None or not decision.get('approvalDecision'):
                err('APPROVAL_RESUME_CONTEXT', at, 'Resume must resolve its exact request and reconstructable decision in its workspace.')
            else:
                execution = command_owner(command, resume['approvalRequest'], request, at)
                if execution and command.get('expectedVersion') != execution.get('version'):
                    err('APPROVAL_VERSION_GUARD', at, 'Resume expectedVersion guards the selected Execution version, not the approval or decision version.')
                decision_subjects = [ref for ref in command.get('subjectRefs', []) if ref.get('kind') == 'Command']
                if len(decision_subjects) != 1 or key(decision_subjects[0]) != key(resume['decisionCommand']):
                    err('APPROVAL_SUBJECT', at, 'Resume must pin its exact decision Command among its subjects.')
                invocation = request.get('invocation', {})
                original = decision['approvalDecision']
                action = resume['action']
                if original['approvalRequest'] != resume['approvalRequest'] or decision.get('state') != 'SUCCEEDED' or decision.get('operation') != 'DecideApproval':
                    err('APPROVAL_RESUME_CONTEXT', at, 'Resume must use the successful decision for this exact request.')
                expected = {'approvalId': request.get('nativeApprovalId'), 'interruptId': invocation.get('interruptId'),
                            'toolUseId': invocation.get('toolUseId'), 'action': original['decision']}
                if invocation.get('validation') != 'VALIDATED' or any(action.get(k) != v or v is None for k, v in expected.items()):
                    err('APPROVAL_RESUME_CONTEXT', at, 'Resume action must preserve observed invocation identifiers and the recorded decision.')

    for snapshot in records.get('Snapshot', []):
        if snapshot.get('kind') != 'TOPOLOGY':
            continue
        graph = snapshot.get('contents', {})
        at = f"Snapshot:{snapshot.get('snapshotId')}@{snapshot.get('version')}"
        for kind in ['nodes', 'edges']:
            for i, element in enumerate(graph.get(kind, [])):
                loc = f'{at}/{kind}/{i}'
                metadata = element.get('assertion') or {}
                if metadata:
                    assertion(metadata, loc)
                if graph.get('derivation') and (not metadata or (kind == 'nodes' and not {'nodeKind', 'resolution', 'resolutionReason'} <= set(element))):
                    err('GRAPH_METADATA', loc, 'A graph with explicit derivation must keep assertion metadata and node type/resolution for every element.')
                if kind != 'edges':
                    continue
                origins = {'OPERATOR_ASSERTED': {'OPERATOR_STATEMENT', 'OPERATOR_CONFIRMED'},
                           'INDEPENDENTLY_OBSERVED': {'INDEPENDENTLY_OBSERVED'}}
                claim = element.get('claimKind')
                if claim in origins and metadata.get('origin') not in origins[claim]:
                    err('GRAPH_ASSERTION_ORIGIN', loc, 'New explicit claim kinds require matching retained assertion origin and evidence.')
                inferred = metadata.get('origin') == 'APPLICATION_INFERENCE' or (metadata.get('derivation') or {}).get('method') == 'APPLICATION_INFERENCE'
                if claim == 'PROVIDER' and inferred:
                    err('GRAPH_ASSERTION_ORIGIN', loc, 'An application inference cannot be represented as a provider claim.')
                if graph.get('graphKind') == 'EXECUTION_HIERARCHY' and element.get('relationKind') in ['asserted_cause_of', 'causes']:
                    err('GRAPH_VIEW_MEANING', loc, 'Execution parentage cannot be emitted as a causal edge.')

    def links(items, available, field, at, code):
        """Validate explicit relationships, independently of source timestamp order."""
        done = set()
        for ident, item in items.items():
            target = item.get(field)
            if target == ident:
                err(code + '_SELF', at + '/' + ident, 'An item cannot link to itself; same-item corrections use the next Projection version.')
            elif target is not None and target not in available:
                err(code + '_SCOPE', at + '/' + ident, 'The linked item is absent from the allowed retained rendition scope.')
            chain = set()
            current = ident
            while current in available and current not in done:
                if current in chain:
                    err(code + '_CYCLE', at + '/' + ident, 'Explicit parent/supersession relationships must be acyclic.')
                    break
                chain.add(current)
                current = available[current].get(field)
            done.update(chain)

    for projection in records.get('Projection', []):
        profile = projection.get('profile')
        if profile not in ['INVESTIGATION_TIMELINE', 'INVESTIGATION_ASSERTIONS']:
            continue
        at = f"Projection:{projection.get('projectionId')}@{projection.get('version')}"
        value = projection['value']
        items = value['items']
        inputs = {key(ref) for ref in projection['inputRefs']}
        owner_refs = [ref for ref in projection.get('subjectRefs', []) if ref.get('kind') == 'Investigation']
        investigation = None
        if len(owner_refs) != 1 or owner_refs[0]['id'] != value['investigationId']:
            err('INVESTIGATION_PROJECTION_SCOPE', at, 'The profile must select exactly one Investigation subject matching its investigationId.')
        else:
            investigation = get(owner_refs[0], projection)
            if investigation is None:
                err('INVESTIGATION_PROJECTION_SCOPE', at, 'The Investigation subject must resolve its exact version in the projection workspace.')
        if projection.get('outputDigest') != digest(value):
            err('PROJECTION_OUTPUT_DIGEST', at, 'Typed output digest must match the immutable projection value.')
        by_id = {item['itemId']: item for item in items}
        if len(by_id) != len(items):
            err('PROJECTION_ITEM_ID', at, 'Item IDs must be unique within a projection rendition.')

        # A prior superseded item is available only through an exact earlier
        # Projection input from the same logical stream. Do not look up a head.
        previous = {}
        for reference in sorted(projection['inputRefs'], key=lambda ref: ref['version']):
            if reference['kind'] != 'Projection' or reference['id'] != projection['projectionId'] or reference['version'] >= projection['version']:
                continue
            prior = get(reference, projection)
            if prior and prior.get('profile') == profile and prior.get('value', {}).get('investigationId') == value['investigationId']:
                previous.update({item['itemId']: item for item in prior['value']['items']})
        links(by_id, {**previous, **by_id}, 'supersedesItemId', at, 'PROJECTION_SUPERSESSION')
        if profile == 'INVESTIGATION_TIMELINE':
            links(by_id, by_id, 'parentItemId', at, 'TIMELINE_PARENT')

        for i, item in enumerate(items):
            loc = f'{at}/items/{i}'
            citations = list(item['sourceRefs'] if profile == 'INVESTIGATION_TIMELINE' else item['assertion']['evidenceRefs'])
            subjects = [item['execution']] if profile == 'INVESTIGATION_TIMELINE' and item.get('execution') else list(item.get('subjectRefs', []))
            if profile == 'INVESTIGATION_TIMELINE':
                if after(item.get('observedAt'), projection.get('generatedAt')):
                    err('PROJECTION_OBSERVATION_TIME', loc, 'A projection cannot include an observation received after its generation.')
                if item.get('assertionOrigin') in ['APPLICATION_INFERENCE', 'DETERMINISTIC_PARSE'] and item['derivation'].get('method') != item['assertionOrigin']:
                    err('ASSERTION_ORIGIN', loc, 'Timeline inferred/parsed origin must match its derivation method.')
            else:
                assertion(item['assertion'], loc, projection.get('generatedAt'))
                confidence = item['assertion'].get('publishedConfidence')
                if confidence:
                    citations.append(confidence['evidence'])
                action = item.get('actionObservation') or {}
                if action.get('approvalRequest'):
                    subjects.append(action['approvalRequest'])
                if action.get('command'):
                    command = get(action['command'], projection)
                    if command is None:
                        err('INVESTIGATION_ITEM_SCOPE', loc, 'An action observation must resolve its exact Command version in the projection workspace.')
                    else:
                        subjects.extend(ref for ref in command.get('subjectRefs', []) if ref['kind'] in
                                        ('Investigation', 'Execution', 'AgentSpace', 'ApprovalRequest'))
            for reference in subjects:
                subject = get(reference, projection)
                if subject is None:
                    err('INVESTIGATION_ITEM_SCOPE', loc, 'Item subjects must resolve exact versions in the projection workspace.')
                    continue
                if reference['kind'] == 'Investigation' and (len(owner_refs) != 1 or key(reference) != key(owner_refs[0])):
                    err('INVESTIGATION_ITEM_SCOPE', loc, 'An item Investigation subject must match the exact profile owner.')
                if investigation and 'agentSpaceId' in subject and subject['agentSpaceId'] != investigation.get('agentSpaceId'):
                    err('INVESTIGATION_ITEM_SCOPE', loc, 'An item Execution or other scoped subject cannot cross the investigation Agent Space.')
            for entry in item.get('artifactReferences', []):
                artifact(entry, loc, investigation.get('agentSpaceId') if investigation else None, projection)
                citations.append(entry['source'])
                if entry.get('resolutionEvidence'):
                    citations.append(entry['resolutionEvidence'])
            if any(key(reference) not in inputs for reference in citations):
                err('PROJECTION_CITATION', loc, 'Every source, confidence and artifact citation must occur among the exact projection inputs.')
            for reference in citations:
                evidence_scope(reference, loc, projection, investigation)
    return errors
