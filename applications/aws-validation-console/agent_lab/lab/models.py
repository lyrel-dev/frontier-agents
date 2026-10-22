"""Strict administrator configuration and immutable experiment contracts.

Execution definitions reference approved instruments by ID. Operator onboarding
can propose network/verifier/runbook configuration, activated only by a separate
approval. No contract accepts credential material or unrestricted operations.
"""
from __future__ import annotations
import ipaddress
from typing import Annotated, Any, Literal
from urllib.parse import urlsplit
import jmespath
from pydantic import BaseModel, ConfigDict, Field, model_validator

ID = Annotated[str, Field(pattern=r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$')]
HASH = Annotated[str, Field(pattern=r'^[a-f0-9]{64}$')]
MODEL = Literal['ec2','eks-ec2','eks-fargate','ecs-ec2','ecs-fargate','lambda','shared','docker','podman','kubernetes']
READS = {
    'ec2': {'describe_instances','describe_volumes','describe_instance_status','describe_network_acls'},
    'ecs': {'describe_services','describe_tasks'},
    'eks': {'describe_cluster','describe_nodegroup'},
    'lambda': {'get_function_configuration','get_function_concurrency'},
    'rds': {'describe_db_instances','describe_db_clusters'},
    'autoscaling': {'describe_auto_scaling_groups'},
    'elbv2': {'describe_target_health'},
    'ssm': {'get_parameter'},
    'cloudwatch': {'describe_alarms','get_metric_data'},
    'elasticache': {'describe_cache_clusters','describe_replication_groups'},
    'dynamodb': {'describe_table','describe_continuous_backups'},
    'kinesis': {'describe_stream_summary'},
    's3': {'get_bucket_replication','get_bucket_versioning'},
    'directconnect': {'describe_virtual_interfaces','describe_connections'},
    'cloudformation': {'describe_stacks'},
}


class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)


class Account(Strict):
    account_id: str = Field(pattern=r'^\d{12}$')
    region: str = Field(pattern=r'^[a-z]{2}(?:-[a-z]+)+-\d$')
    profile: str = Field(min_length=1, max_length=150)


class Probe(Strict):
    id: ID
    title: str = Field(min_length=1, max_length=150)
    url: str = Field(min_length=1, max_length=2048)
    allowed_networks: list[str] = Field(min_length=1, max_length=20)
    requests_per_second: float = Field(default=1, gt=0, le=5)
    timeout_seconds: float = Field(default=3, gt=0, le=5)
    expected_status: list[int] = Field(default_factory=lambda:[200], min_length=1, max_length=10)
    json_expression: str | None = Field(default=None, max_length=300)
    expected_json_value: Any = None
    header_environment: dict[str, str] = Field(default_factory=dict, max_length=10)
    allow_loopback_http: bool = False

    @model_validator(mode='after')
    def bounded(self):
        u = urlsplit(self.url)
        if u.username or u.password or u.fragment or not u.hostname:
            raise ValueError('Probe URL cannot contain credentials or fragments')
        loopback = u.hostname in ('127.0.0.1','::1','localhost')
        if u.scheme != 'https' and not (self.allow_loopback_http and u.scheme == 'http' and loopback):
            raise ValueError('HTTPS required except an explicitly enabled loopback development target')
        for network in self.allowed_networks:
            ipaddress.ip_network(network)
        if self.json_expression:
            jmespath.compile(self.json_expression)
        for header, env in self.header_environment.items():
            if '\n' in header or '\r' in header or header.lower() in ('host','connection','content-length'):
                raise ValueError('Reserved or invalid probe header')
            if not env or not env.replace('_','').isalnum():
                raise ValueError('Header secret must name a local environment variable')
        return self


class ReadCheck(Strict):
    account_id: str | None = Field(default=None, pattern=r'^\d{12}$')
    id: ID
    service: str
    operation: str
    parameters: dict[str, Any] = Field(default_factory=dict, max_length=30)
    expression: str = Field(min_length=1, max_length=500)
    operator: Literal['eq','gte','lte','contains'] = 'eq'
    expected: Any
    purpose: str = Field(min_length=10, max_length=1500)

    @model_validator(mode='after')
    def allowlisted(self):
        if self.operation not in READS.get(self.service, set()):
            raise ValueError('Read operation not supported by the bounded verifier')
        if not self.parameters:
            raise ValueError('Explicit resource selectors required; account-wide verifier calls are not allowed')
        if self.service == 'ssm' and self.parameters.get('WithDecryption') is not False:
            raise ValueError('Parameter verification must explicitly set WithDecryption=false')
        if not self.expression[0].isalpha():
            raise ValueError('Verification expression must select a response field')
        jmespath.compile(self.expression)
        return self


class Metric(Strict):
    account_id: str | None = Field(default=None, pattern=r'^\d{12}$')
    id: ID
    title: str
    namespace: str
    metric_name: str
    dimensions: dict[str, str] = Field(default_factory=dict, max_length=30)
    statistic: str = Field(pattern=r'^(Sum|Average|Minimum|Maximum|SampleCount|p\d+(?:\.\d+)?)$')
    unit: str
    period_seconds: int = Field(default=60, ge=60, le=3600)

    @model_validator(mode='after')
    def period(self):
        if self.period_seconds % 60:
            raise ValueError('CloudWatch periods must be whole minutes')
        return self


class Runbook(Strict):
    id: ID
    title: str
    document_arn: str
    document_version: str = Field(pattern=r'^[1-9][0-9]*$')
    content_sha256: HASH
    parameters: dict[str, list[str]] = Field(min_length=1, max_length=30)
    timeout_seconds: int = Field(ge=10, le=1800)
    before_checks: list[ID] = Field(default_factory=list, max_length=20)
    after_checks: list[ID] = Field(min_length=1, max_length=20)
    rollback_runbook_id: ID | None = None
    implementation_artifact: str = Field(min_length=1, max_length=2000)
    implementation_diff_sha256: HASH


class Fault(Strict):
    native_fis: bool = False
    preview_record_id: str | None = None
    target_accounts_sha256: str | None = None
    resolved_targets: list[dict[str, Any]] = Field(default_factory=list, max_length=1000)
    target_match: Literal['exact','subset'] = 'exact'
    minimum_targets: int = Field(default=1, ge=1, le=1000)
    independent_recovery: str = Field(default='', max_length=6000)
    action_review: str = Field(default='', max_length=6000)
    id: ID
    title: str
    template_id: str = Field(pattern=r'^[A-Za-z0-9-]{1,64}$')
    template_sha256: HASH
    target_arns: list[str] = Field(min_length=1, max_length=1000)
    allowed_action_ids: list[str] = Field(min_length=1, max_length=30)
    max_fault_seconds: int = Field(ge=1, le=86400)
    baseline_checks: list[ID] = Field(min_length=1, max_length=20)
    fault_checks: list[ID] = Field(min_length=1, max_length=20)
    cleanup_checks: list[ID] = Field(min_length=1, max_length=20)
    cleanup_runbook_id: ID | None = None
    safety_alarm_arns: list[str] = Field(min_length=1, max_length=5)
    safety_review: str = Field(min_length=20, max_length=4000)


class Route(Strict):
    receipt_expression: str | None = Field(default=None, max_length=4000)
    alarm_name: str = Field(min_length=1, max_length=255)
    reference_system: str = Field(min_length=1, max_length=200)
    # Must match the real incident integration; alarm_arn is not universal.
    reference_id_format: str = Field(min_length=1, max_length=500)
    receipt_log_group: str | None = None
    receipt_account: Literal['agent','workload'] = 'agent'
    lifecycle_log_group: str | None = None
    route_contract: str = Field(min_length=20, max_length=4000)

    @model_validator(mode='after')
    def format_contract(self):
        if self.receipt_expression:jmespath.compile(self.receipt_expression)
        allowed = {'alarm_arn','alarm_name','source_event_id'}
        import string
        names = {f for _, f, _, _ in string.Formatter().parse(self.reference_id_format) if f}
        if not names or not names.issubset(allowed):
            raise ValueError('Reference format must use alarm_arn, alarm_name or source_event_id')
        if 'source_event_id' in names and not self.receipt_log_group:
            raise ValueError('A dynamic external ID requires the delivery-receipt adapter')
        return self


class TargetAccount(Account):
    association_id: str = Field(min_length=1, max_length=255)


class Binding(Strict):
    orchestrator: Account | None = None
    target_accounts: list[TargetAccount] = Field(default_factory=list, max_length=100)
    id: ID
    name: str
    agent: Account
    workload: Account
    agent_space_id: str = Field(pattern=r'^[A-Za-z0-9-]{1,128}$')
    association_id: str = Field(min_length=1, max_length=255)
    service_id: ID
    deployment_model: MODEL
    environment: Literal['nonproduction']
    fault_profile: str | None = None
    change_profile: str | None = None
    requester_profile: str | None = None
    route: Route
    probes: list[Probe] = Field(min_length=1, max_length=10)
    checks: list[ReadCheck] = Field(min_length=1, max_length=100)
    faults: list[Fault] = Field(min_length=1, max_length=20)
    runbooks: list[Runbook] = Field(default_factory=list, max_length=30)
    metrics: list[Metric] = Field(default_factory=list, max_length=20)
    max_pages: int = Field(default=10, ge=1, le=20)

    @model_validator(mode='after')
    def references(self):
        if self.agent.account_id == self.workload.account_id:
            raise ValueError('Agent and workload accounts must be distinct')
        for rows in [self.probes,self.checks,self.faults,self.runbooks,self.metrics]:
            if len({r.id for r in rows}) != len(rows):
                raise ValueError('Duplicate instrument ID')
        if len({a.account_id for a in self.target_accounts}) != len(self.target_accounts):
            raise ValueError('Duplicate target account')
        if any(a.account_id == self.workload.account_id or a.region != self.workload.region for a in self.target_accounts):
            raise ValueError('Additional target accounts must be unique and share the workload Region')
        if self.orchestrator and self.orchestrator.region != self.workload.region:
            raise ValueError('FIS orchestrator and target accounts must share a Region')
        permitted_accounts = {self.workload.account_id, *[a.account_id for a in self.target_accounts]}
        if any(c.account_id and c.account_id not in permitted_accounts for c in [*self.checks, *self.metrics]):
            raise ValueError('Verifier/metric account is not a configured target account')
        checks = {x.id for x in self.checks}
        books = {x.id for x in self.runbooks}
        for f in self.faults:
            if not set(f.baseline_checks+f.fault_checks+f.cleanup_checks) <= checks:
                raise ValueError('Fault references an unregistered verifier')
            if f.cleanup_runbook_id and f.cleanup_runbook_id not in books:
                raise ValueError('Unregistered cleanup runbook')
            if f.native_fis:
                if not f.preview_record_id or not f.target_accounts_sha256 or not f.resolved_targets:
                    raise ValueError('Native FIS needs a retained preview and account-configuration fingerprint')
                if len(f.independent_recovery) < 20 or len(f.action_review) < 20:
                    raise ValueError('Document action prerequisites and independent recovery before execution')
                for phase in [f.baseline_checks, f.fault_checks, f.cleanup_checks]:
                    covered = {c.account_id or self.workload.account_id for c in self.checks if c.id in phase}
                    if not permitted_accounts <= covered:
                        raise ValueError('Baseline, effect and cleanup checks must cover every target account')
                for arn in f.safety_alarm_arns:
                    a = arn.split(':',5)
                    if len(a)!=6 or a[4]!=(self.orchestrator or self.workload).account_id or a[3]!=self.workload.region or a[2]!='cloudwatch':
                        raise ValueError('Stop alarms must belong to the FIS orchestrator account/Region')
            else:
                for arn in f.target_arns+f.safety_alarm_arns:
                    self._arn(arn)
        for r in self.runbooks:
            self._arn(r.document_arn)
            if not set(r.before_checks+r.after_checks) <= checks:
                raise ValueError('Runbook references an unregistered verifier')
            if r.rollback_runbook_id and (r.rollback_runbook_id not in books or r.rollback_runbook_id == r.id):
                raise ValueError('Invalid rollback runbook')
            roles = r.parameters.get('AutomationAssumeRole', [])
            if len(roles) != 1 or not roles[0].startswith(f'arn:aws:iam::{self.workload.account_id}:role/'):
                raise ValueError('Runbooks require an explicit workload-account AutomationAssumeRole')
        return self

    def _arn(self, value: str):
        parts = value.split(':',5)
        if len(parts) != 6 or parts[0:2] != ['arn','aws'] or parts[4] != self.workload.account_id:
            raise ValueError('Instrument ARN is outside the workload account or aws partition')
        if parts[3] and parts[3] != self.workload.region:
            raise ValueError('Instrument ARN is outside the workload Region')


class FISAccount(Strict):
    """Administrator-owned SDK profile. Discovery never accepts browser credentials."""
    id: ID
    name: str = Field(min_length=1, max_length=150)
    account_id: str = Field(pattern=r'^\d{12}$')
    profile: str = Field(min_length=1, max_length=150)
    execution_profile: str | None = Field(default=None, max_length=150)
    regions: list[str] = Field(min_length=1, max_length=30)

    @model_validator(mode='after')
    def validate_regions(self):
        import re
        if len(set(self.regions)) != len(self.regions):
            raise ValueError('Duplicate discovery Region')
        if any(not re.fullmatch(r'[a-z]{2}(?:-[a-z]+)+-\d', r) for r in self.regions):
            raise ValueError('Invalid discovery Region')
        return self


class Configuration(Strict):
    enable_aws_writes: bool = False
    bindings: list[Binding] = Field(default_factory=list, max_length=100)
    fis_accounts: list[FISAccount] = Field(default_factory=list, max_length=100)
    fis_discovery_max_pages: int = Field(default=1000, ge=1, le=10000)
    poll_seconds: int = Field(default=10, ge=2, le=60)
    approval_ttl_seconds: int = Field(default=900, ge=60, le=3600)
    probe_gap_seconds: int = Field(default=15, ge=5, le=60)
    @model_validator(mode='after')
    def unique(self):
        if len({b.id for b in self.bindings}) != len(self.bindings):
            raise ValueError('Duplicate binding ID')
        if len({a.id for a in self.fis_accounts}) != len(self.fis_accounts):
            raise ValueError('Duplicate discovery account ID')
        scopes = [(a.account_id, region) for a in self.fis_accounts for region in a.regions]
        if len(set(scopes)) != len(scopes):
            raise ValueError('Duplicate account/Region discovery scope')
        return self


class Oracle(Strict):
    mechanism_code: ID
    mechanism_description: str = Field(min_length=20, max_length=4000)
    affected_resource_arns: list[str] = Field(min_length=1, max_length=100)
    required_checks: list[ID] = Field(min_length=1, max_length=20)
    rubric: str = Field(min_length=20, max_length=4000)


class BusinessRequirement(Strict):
    id: ID
    metric_id: ID
    category: Literal['data_correctness','collateral_regression','application']
    aggregation: Literal['maximum','minimum','sum','last']
    operator: Literal['lte','gte','eq']
    threshold: float
    minimum_samples: int = Field(default=1, ge=1, le=1000000)
    interpretation: str = Field(min_length=20, max_length=2000)


class Experiment(Strict):
    business_requirements: list[BusinessRequirement] = Field(default_factory=list, max_length=30)
    schema_version: Literal['1.0'] = '1.0'
    id: ID
    revision: int = Field(default=1, ge=1)
    title: str = Field(min_length=1, max_length=200)
    binding_id: ID
    fault_id: ID
    probe_id: ID
    mode: Literal['native','assisted'] = 'native'
    baseline_seconds: int = Field(default=60, ge=30, le=600)
    observation_seconds: int = Field(default=600, ge=60, le=172800)
    ingestion_wait_seconds: int = Field(default=120, ge=0, le=600)
    response_deadline_seconds: int = Field(default=300, ge=10, le=1800)
    max_error_ratio: float = Field(ge=0, lt=1)
    max_latency_ms: float = Field(gt=0, le=120000)
    stable_seconds: int = Field(default=30, ge=10, le=300)
    bucket_seconds: int = Field(default=10, ge=5, le=60)
    minimum_delivery_ratio: float = Field(default=.9, ge=.8, le=1)
    oracle: Oracle
    hypotheses: str = Field(min_length=20, max_length=5000)
    intervention_runbook_ids: list[ID] = Field(default_factory=list, max_length=20)

    @model_validator(mode='after')
    def durations(self):
        if len({r.id for r in self.business_requirements}) != len(self.business_requirements):
            raise ValueError('Business requirement IDs must be unique')
        if self.response_deadline_seconds > self.observation_seconds:
            raise ValueError('Response deadline exceeds the observation window')
        if self.stable_seconds % self.bucket_seconds or self.observation_seconds % self.bucket_seconds:
            raise ValueError('Stability and observation durations must align to probe buckets')
        return self


class ComparisonPlan(Strict):
    claim: Literal['prevent_recurrence','reduce_impact','detect_earlier']
    minimum_improvement: float = Field(default=.25, gt=0, le=1)
    traffic_tolerance: float = Field(default=.1, ge=0, le=.2)
    maximum_latency_regression_ratio: float = Field(default=.1, ge=0, le=.5)
    minimum_pairs: int = Field(default=1, ge=1, le=20)
    maximum_benign_investigations: int = Field(default=0, ge=0, le=10)
    knowledge_history_note: str = Field(min_length=20, max_length=4000)


class CampaignRequest(Strict):
    title: str = Field(min_length=1, max_length=200)
    experiment_ref: str
    comparison: ComparisonPlan


class TrialRequest(Strict):
    experiment_ref: str
    campaign_id: str | None = None
    arm: Literal['baseline','treatment','benign'] = 'baseline'


class Approval(Strict):
    expected_digest: HASH
    confirmation: str = Field(min_length=1, max_length=600)
    approver: str = Field(min_length=1, max_length=150)
    rationale: str = Field(min_length=10, max_length=4000)


class Citation(Strict):
    record_id: str
    quote: str = Field(min_length=5, max_length=3000)


class Diagnosis(Strict):
    reviewer: str = Field(min_length=1, max_length=150)
    finding_record_id: str
    finding_quote: str = Field(min_length=5, max_length=6000)
    asserted_resource_arns: list[str] = Field(min_length=1, max_length=100)
    asserted_mechanism_code: ID
    citations: list[Citation] = Field(min_length=1, max_length=10)
    rationale: str = Field(min_length=20, max_length=6000)
    material_unsupported_claims: list[str] = Field(default_factory=list, max_length=20)


class ChangeProposal(Strict):
    runbook_id: ID
    source_record_id: str
    source_quote: str = Field(min_length=5, max_length=6000)
    rationale: str = Field(min_length=20, max_length=6000)
    proposer: str = Field(min_length=1, max_length=150)
