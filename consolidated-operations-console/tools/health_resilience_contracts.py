"""Cross-record invariants for optional Health/Resilience normalized evidence.

The schemas check shape. These checks prove exact local reference/scope and time
relationships for fixture records; they do not implement an AWS adapter.
"""
from __future__ import annotations
import json


def validate_health_resilience(records):
    errors = []
    history = {}
    for kind, rows in records.items():
        key = kind[0].lower() + kind[1:] + 'Id'
        for row in rows:
            history[(kind, row.get(key), row.get('version'))] = row

    def err(code, where, message):
        errors.append({'code': code, 'location': where, 'message': message})

    def get(reference):
        if not isinstance(reference, dict):
            return None
        return history.get((reference.get('kind'), reference.get('id'), reference.get('version')))

    def identity(value):
        if not isinstance(value, dict):
            return None
        return json.dumps({k: v for k, v in value.items() if k != 'aliases'}, sort_keys=True)

    def identities(entity):
        if entity is None:
            return []
        return [entity.get('identity')] + [p.get('identity') for p in entity.get('providerBindings', [])]

    def scope(reference, where):
        entity = get(reference.get('entity'))
        native = reference.get('sourceIdentity')
        if reference.get('entity') is not None and entity is None:
            err('HR_SUBJECT_REFERENCE', where, 'Subject entity must resolve to its exact version.')
        if entity is not None and native is not None and identity(native) not in {identity(x) for x in identities(entity) if x is not None}:
            err('HR_SUBJECT_IDENTITY', where, 'Resolved subject contradicts its scoped provider identity.')

    def correlation(value, expected_service, where):
        if not isinstance(value, dict):
            return
        service = get(value.get('service'))
        assessment = get(value.get('assessment'))
        service_id = value.get('service', {}).get('id')
        if service is None or assessment is None:
            err('HR_CORRELATION_REFERENCE', where, 'Correlation references must resolve exactly.')
        if (expected_service is not None and service_id != expected_service) or (assessment is not None and assessment.get('serviceId') != service_id):
            err('HR_ASSESSMENT_SCOPE', where, 'A correlation and its assessment must name the same enclosing service.')

    def service_source(value, source, where):
        service = get(value.get('service'))
        if service is None:
            err('HR_EFFECTIVE_SERVICE_REFERENCE', where, 'Normalized service evidence must resolve its exact Service version.')
        elif identity(source.get('identity')) not in {identity(x) for x in identities(service) if x is not None}:
            err('HR_EFFECTIVE_SERVICE_SCOPE', where, 'Source identity does not match an observed provider binding of the referenced Service.')

    for context in records.get('EventContext', []):
        descriptions = context.get('descriptions', [])
        locales = [x['locale'] for x in descriptions]
        where = 'EventContext:' + context['eventContextId']
        if len(locales) != len(set(locales)):
            err('HR_DESCRIPTION_LOCALE', where, 'Each context version has at most one current description per locale.')
        event_candidates = [v for (kind, ident, version), v in history.items() if kind == 'HealthEvent' and ident == context['healthEventId']]
        event = max(event_candidates, key=lambda v: v['version']) if event_candidates else None
        for value in descriptions:
            source = get(value.get('source'))
            if source is None:
                err('HR_DESCRIPTION_SOURCE', where, 'Description Source must resolve exactly.')
                continue
            if event is not None and source.get('identity', {}).get('nativeId') != event['eventArn']:
                err('HR_DESCRIPTION_SCOPE', where, 'Localized text belongs to a different Health event.')
            if context['kind'] == 'ACCOUNT' and source.get('identity', {}).get('scope', {}).get('accountId') != context['accountId']:
                err('HR_DESCRIPTION_SCOPE', where, 'Localized text belongs to a different account context.')

    for attempt in records.get('ReadAttempt', []):
        keys = [(x['eventArn'], x['accountId']) for x in attempt.get('itemErrors', [])]
        if len(keys) != len(set(keys)):
            err('HR_ITEM_FAILURE_IDENTITY', 'ReadAttempt:' + attempt['readAttemptId'], 'The response contains duplicate event/account failure identities.')

    for collection in records.get('Collection', []):
        for query in collection.get('queries', []):
            value = query.get('assessmentCorrelation')
            if value is not None:
                subject = query.get('subject')
                where = 'Collection:' + collection['collectionId'] + '/' + query['queryKey']
                if not isinstance(subject, dict) or subject.get('kind') != 'Service':
                    err('HR_CAPTURE_SUBJECT', where, 'A finding capture correlation requires an exact Service query subject.')
                correlation(value, subject.get('id') if isinstance(subject, dict) else None, where)

    for recommendation in records.get('Recommendation', []):
        content = recommendation.get('normalizedSuggestion', {})
        groups = {'INFRASTRUCTURE_AND_CODE': {'infrastructureAndCode', 'infrastructureAndCodeRecommendations', 'INFRASTRUCTURE_AND_CODE'}, 'OBSERVABILITY': {'observability', 'observabilityRecommendations', 'OBSERVABILITY'}, 'TESTING': {'testing', 'testingRecommendations', 'TESTING'}}
        if content.get('category') in groups and recommendation.get('groupKey') not in groups[content['category']]:
            err('HR_RECOMMENDATION_CATEGORY', 'Recommendation:' + recommendation['recommendationId'], 'Category must identify the owner source array, independently of the finding failure category.')

    for policy in records.get('ResiliencePolicy', []):
        for component in policy.get('components', []):
            normalized = component.get('normalized')
            if normalized is None:
                continue
            where = 'ResiliencePolicy:' + policy['resiliencePolicyId'] + '/' + component['kind']
            for key, value in normalized['targets'].items():
                if component['targets'].get(key) != value or component['units'].get(key) != normalized['units'].get(key):
                    err('HR_POLICY_NORMALIZATION', where, 'Validated metrics and units must agree with the observed read fields; retained unknown native keys are not discarded.')
            if normalized.get('disasterRecoveryApproach') is not None and normalized['disasterRecoveryApproach'] != component.get('disasterRecoveryApproach'):
                err('HR_POLICY_NORMALIZATION', where, 'A validated DR approach must equal the observed raw approach.')

    for source in records.get('Source', []):
        where = 'Source:' + source['sourceId'] + '@' + str(source['version'])
        normalization = source.get('normalization')
        if normalization is not None:
            if normalization['inputContentDigest'] != source['contentDigest']:
                err('HR_NORMALIZATION_INPUT', where, 'Source normalization must pin the containing raw payload digest; its digest does not cover normalized output.')
            if normalization['normalizedAt'] > source['updatedAt']:
                err('HR_NORMALIZATION_TIME', where, 'Normalized fields cannot be produced after the containing immutable Source version was published.')
        targets = source.get('effectiveTargets')
        if targets is not None:
            service_source(targets, source, where)
            for metric, value in targets.get('values', {}).items():
                provenance = value.get('provenance', {})
                if provenance.get('resolvedPolicy') is not None and get(provenance['resolvedPolicy']) is None:
                    err('HR_POLICY_REFERENCE', where + '/' + metric, 'Resolved policy must name its exact retained version.')
        for subject in source.get('eventSubjects', []):
            scope(subject['subject'], where)
        if source.get('subjectState') is not None:
            scope(source['subjectState']['subject'], where)
            if source['subjectState']['observedAt'] > source['updatedAt']:
                err('HR_SUBJECT_STATE_TIME', where, 'Subject state cannot be observed after its Source version was published.')
        signal = source.get('healthSignal')
        if signal is not None:
            scope(signal['subject'], where)
            if not signal['windowStart'] <= signal['windowEnd'] <= signal['measuredAt'] <= signal['receivedAt'] <= source['updatedAt']:
                err('HR_SIGNAL_TIME', where, 'Health signal measurement window, measurement, receipt and publication times are inconsistent.')
            if signal['expiresAt'] is not None and signal['expiresAt'] < signal['measuredAt']:
                err('HR_SIGNAL_EXPIRY', where, 'A signal cannot expire before it was measured; delivery after expiry is permitted.')
            names = [m['name'] for m in signal['measurements']]
            if len(names) != len(set(names)):
                err('HR_SIGNAL_MEASUREMENT', where, 'Named measurements must be unique in one signal observation.')
        posture = source.get('postureEvidence')
        if posture is not None:
            if not posture['captureStartedAt'] <= posture['captureEndedAt'] <= source['updatedAt']:
                err('HR_POSTURE_TIME', where, 'Posture capture cannot finish before it starts or after publication.')
            if posture['kind'] == 'AWS_SERVICE':
                service_source(posture, source, where)
                correlation(posture.get('assessmentCorrelation'), posture['service']['id'], where)
                outcomes = [v['component'] for v in posture['componentOutcomes']]
                if len(outcomes) != len(set(outcomes)):
                    err('HR_POSTURE_COMPONENT', where, 'One native posture observation has at most one outcome per component.')
                if posture.get('policyContext') is not None:
                    context = get(posture['policyContext'])
                    if context is None or context.get('kind') != 'POLICY_CONTEXT' or context.get('contents', {}).get('serviceId') != posture['service']['id']:
                        err('HR_POSTURE_POLICY_CONTEXT', where, 'Observed policy context must be a same-service POLICY_CONTEXT snapshot.')
            else:
                services = posture['contributorServices']; findings = posture['contributorFindings']
                service_ids = [v['id'] for v in services]
                finding_ids = [v['id'] for v in findings]
                if len(service_ids) != len(set(service_ids)) or len(finding_ids) != len(set(finding_ids)):
                    err('HR_POSTURE_CONTRIBUTOR', where, 'Derived counts use distinct logical contributor identities, not multiple versions of one contributor.')
                subject = posture['subject']; resolved_subject = get(subject)
                if resolved_subject is None:
                    err('HR_POSTURE_SUBJECT', where, 'Derived attention subject must resolve to its exact System/UserJourney version.')
                for reference in services:
                    service = get(reference)
                    if service is None:
                        err('HR_POSTURE_CONTRIBUTOR', where, 'Contributor Service must resolve exactly.')
                        continue
                    memberships = service.get('memberships', [])
                    belongs = any((subject['kind'] == 'System' and m['systemId'] == subject['id']) or (subject['kind'] == 'UserJourney' and subject['id'] in m['userJourneyIds']) for m in memberships)
                    if not belongs:
                        err('HR_POSTURE_MEMBERSHIP', where, 'Contributor Service version lacks the asserted subject membership; current membership cannot substitute for captured evidence.')
                for reference in findings:
                    finding = get(reference)
                    if finding is None or finding.get('serviceId') not in set(service_ids):
                        err('HR_POSTURE_FINDING_SCOPE', where, 'A contributor finding must resolve exactly and belong to a contributor service.')

    for snapshot in records.get('Snapshot', []):
        where = 'Snapshot:' + snapshot['snapshotId']
        if snapshot.get('kind') == 'POLICY_CONTEXT':
            context = snapshot['contents']; target = get(context.get('effectiveTargetSource'))
            if target and target.get('effectiveTargets') is not None and target['effectiveTargets']['service']['id'] != context['serviceId']:
                err('HR_POLICY_TARGET_SCOPE', where, 'PolicyContext and effective-target source must have the same service scope.')
        if snapshot.get('kind') == 'TOPOLOGY':
            edges = snapshot['contents'].get('edges', [])
            keys = [edge['edgeKey'] for edge in edges]
            if len(keys) != len(set(keys)):
                err('HR_GRAPH_EDGE_IDENTITY', where, 'Edge keys are unique within a captured topology; preserve native property grouping on that edge.')
    return errors


def validate_traversal_pages(responses):
    """Check recorded response pages within one authenticated fixture scope.

    These are local contract invariants, not a pagination server or proof that
    every page/provider object was collected. An omitted count stays unknown.
    """
    errors = []
    traversals = {}

    def err(code, where, message):
        errors.append({'code': code, 'location': where, 'message': message})

    for response in responses:
        if not isinstance(response, dict) or not isinstance(response.get('page'), dict):
            continue
        page = response['page']; traversal = page.get('traversalId')
        where = 'Page:' + str(traversal)
        metadata = (page.get('asOfSequence'), page.get('createdAt'), page.get('expiresAt'))
        previous = traversals.setdefault(traversal, {'metadata': metadata, 'count': None})
        if previous['metadata'] != metadata:
            err('HR_PAGE_PUBLICATION', where, 'A retained traversal cannot change its publication or creation/expiry metadata across pages.')
        count = page.get('totalResults')
        if not isinstance(count, int) or isinstance(count, bool):
            continue  # Type/absence is checked by the Page schema.
        if previous['count'] is not None and previous['count'] != count:
            err('HR_PAGE_TOTAL_STABILITY', where, 'Exact authorized totalResults must remain stable within one retained traversal.')
        previous['count'] = count
        items = response.get('items', [])
        if isinstance(items, list) and len(items) > count:
            err('HR_PAGE_TOTAL_BOUND', where, 'Total result cardinality cannot be smaller than the current page.')
        if count == 0 and 'nextToken' in response:
            err('HR_PAGE_EMPTY_TRAVERSAL', where, 'An established empty local result set cannot advertise another result page.')
    return errors
