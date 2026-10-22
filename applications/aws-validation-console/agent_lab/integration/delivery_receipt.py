"""Call ONLY after the existing incident sender receives actual acceptance.

This helper formats a receipt for your existing structured logging destination.
It sends no incident, does not call AWS, and never substitutes for native delivery.
Fields must come from the original alarm and the sender's actual result.
"""
from datetime import datetime, timezone
import json

def receipt(*, alarm_arn: str, alarm_transition_at: str, source_event_id: str,
            agent_account_id: str, workload_account_id: str, agent_space_id: str,
            reference_system: str, reference_id: str, accepted_at: str,
            accepted: bool) -> dict:
    if accepted is not True:raise ValueError('Do not emit an acceptance receipt for an unaccepted incident')
    values=locals()
    if any(not isinstance(v,str) or not v for k,v in values.items() if k!='accepted'):
        raise ValueError('Every identity, timestamp and reference must come from the actual event/result')
    for key in ('alarm_transition_at','accepted_at'):
        parsed=datetime.fromisoformat(values[key].replace('Z','+00:00'))
        if parsed.tzinfo is None:raise ValueError('Timezone-aware timestamps required')
    return {'schema':'agent-validation.delivery/v1',**values}

def log_receipt(**kwargs) -> None:
    """Use a logger routed to the configured CloudWatch log group in deployment."""
    print(json.dumps(receipt(**kwargs),sort_keys=True),flush=True)


def final_failure(*, alarm_arn: str, alarm_transition_at: str, source_event_id: str,
                  agent_account_id: str, workload_account_id: str, agent_space_id: str,
                  reference_system: str, reference_id: str, attempted_at: str,
                  reason_code: str) -> dict:
    """Format only a final, actually observed sender rejection after its retries.

    Do not infer rejection from a missing task. A later positive acceptance receipt
    supersedes this negative route result; inconsistent source IDs are ambiguous.
    """
    values=locals()
    if any(not isinstance(v,str) or not v for v in values.values()):
        raise ValueError('All fields must identify the actual source incident and sender result')
    for key in ('alarm_transition_at','attempted_at'):
        if datetime.fromisoformat(values[key].replace('Z','+00:00')).tzinfo is None:
            raise ValueError('Timezone-aware timestamps required')
    return {'schema':'agent-validation.delivery/v1','accepted':False,'final':True,**values}
