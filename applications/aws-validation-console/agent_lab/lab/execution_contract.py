"""Compare the immutable FIS execution snapshot with the approved definition.

A read of today's mutable template is not proof of what an earlier operation
ran. Runtime state/timestamps and action descriptions are not execution inputs.
The comparison is detective, not an IAM guard against the initial dispatch.
"""
from .util import Blocked, digest, iso


def execution_projection(value):
    actions = value.get('actions')
    targets = value.get('targets')
    if not isinstance(actions, dict) or not actions or not isinstance(targets, dict):
        raise Blocked('FIS snapshot is missing its action or target definition')
    projected_actions = {}
    for name, action in actions.items():
        if not isinstance(action, dict) or not action.get('actionId'):
            raise Blocked('FIS snapshot has an incomplete action definition')
        projected_actions[name] = {
            'actionId': action['actionId'],
            'parameters': action.get('parameters') or {},
            'targets': action.get('targets') or {},
            'startAfter': sorted(action.get('startAfter') or []),
        }
    options = value.get('experimentOptions') or {}
    return {
        'roleArn': value.get('roleArn'),
        'targets': targets,
        'actions': projected_actions,
        'stopConditions': sorted(value.get('stopConditions') or [], key=digest),
        'accountTargeting': options.get('accountTargeting', 'single-account'),
        'emptyTargetResolutionMode': options.get('emptyTargetResolutionMode', 'fail'),
    }


def verify_execution(template, execution, actions_mode):
    if execution.get('experimentTemplateId') != template.get('id'):
        raise Blocked('Executed FIS template identity differs from the approved definition')
    if execution.get('experimentOptions', {}).get('actionsMode') != actions_mode:
        raise Blocked('Executed FIS actions mode differs from the approved operation')
    expected = execution_projection(template)
    actual = execution_projection(execution)
    if digest(expected) != digest(actual):
        raise Blocked('Executed FIS definition differs from approval; stop and restore the owned experiment')
    return digest(actual)


def verify_captured_execution(store, fault, captured, actions_mode, owner):
    preview = store.record(fault.preview_record_id)
    definition = store.record(preview['data']['template_record_id'])
    if definition['kind'] != 'fis_template' or definition['data']['contract_sha256'] != fault.template_sha256:
        raise Blocked('Native execution definition provenance is inconsistent')
    execution = captured['experiment']
    fingerprint = verify_execution(definition['data']['template'], execution, actions_mode)
    source_id = captured.get('source_record_id')
    sources = {source_id: store.record(source_id)['sha256']} if source_id else {}
    return store.put_record('execution_contract_check', owner, {
        'experiment_id': execution['id'], 'actions_mode': actions_mode,
        'execution_contract_sha256': fingerprint, 'template_record_id': definition['id'],
        'input_hashes': {definition['id']: definition['sha256'], **sources},
        'checked_at': iso(), 'verdict': 'matching_definition',
        'limits': ['Post-dispatch comparison; not a preventive target lock or action-permission proof.'],
    })
