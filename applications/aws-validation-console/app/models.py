"""Versioned, non-executable interchange contracts. Unknown fields are rejected."""
from __future__ import annotations
from typing import Annotated, Literal, Union
from pydantic import (BaseModel, ConfigDict, Field, AwareDatetime, StrictBool,
                      StrictInt, StrictStr, model_validator)

ID = Annotated[str, Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$")]
REF = Annotated[str, Field(pattern=r"^(scenario|execution_run|evidence|snapshot|validation_run|report):[A-Za-z0-9][A-Za-z0-9_.-]{0,99}@[1-9][0-9]*$")]
Value = Union[StrictBool, Annotated[int, Field(strict=True, ge=-9007199254740991, le=9007199254740991)], Annotated[float, Field(strict=True, allow_inf_nan=False, ge=-9007199254740991, le=9007199254740991)]]
Model = Literal['ec2', 'eks-ec2', 'eks-fargate', 'ecs-ec2', 'ecs-fargate', 'lambda', 'docker', 'podman', 'kubernetes', 'shared']
Outcome = Literal['pass', 'fail', 'inconclusive', 'not_assessed']

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

class Assertion(StrictModel):
    id: ID
    title: str = Field(min_length=1, max_length=300)
    metric: ID
    operator: Literal['lte', 'gte', 'eq']
    threshold: Value
    unit: str = Field(min_length=1, max_length=40)
    category: Literal['collection', 'application', 'recovery', 'data', 'detection', 'response', 'safety']
    required: StrictBool = True
    min_samples: int = Field(default=1, ge=1, le=1_000_000_000, strict=True)
    max_collection_lag_seconds: int = Field(default=300, ge=0, le=604800, strict=True)
    @model_validator(mode='after')
    def validate_bool(self):
        if isinstance(self.threshold, bool) and self.operator != 'eq':
            raise ValueError('Boolean assertions support eq only')
        return self

class ScenarioData(StrictModel):
    status: Literal['draft', 'specified'] = 'draft'
    models: list[Model] = Field(min_length=1, max_length=10)
    domain: str = Field(min_length=1, max_length=100)
    hypothesis: str = Field(min_length=1, max_length=3000)
    procedure: str = Field(min_length=1, max_length=12000)
    fault_mode: Literal['none', 'fis', 'external', 'local'] = 'external'
    action: str = Field(default='', max_length=500)
    evidence_required: list[str] = Field(default_factory=list, max_length=50)
    acceptance: str = Field(default='', max_length=6000)
    recovery: str = Field(default='', max_length=6000)
    limitations: list[str] = Field(default_factory=list, max_length=50)
    source_urls: list[str] = Field(default_factory=list, max_length=20)
    assertions: list[Assertion] = Field(default_factory=list, max_length=50)
    @model_validator(mode='after')
    def unique_assertions(self):
        if len({a.id for a in self.assertions}) != len(self.assertions):
            raise ValueError('Assertion IDs must be unique within a scenario')
        if self.status == 'specified' and not self.assertions:
            raise ValueError('A specified scenario needs at least one assertion')
        return self

class RunData(StrictModel):
    scenario_ref: REF
    snapshot_ref: REF | None = None
    execution_type: Literal['observation', 'external', 'simulated']
    execution_state: Literal['planned', 'running', 'completed', 'failed', 'aborted']
    scope_id: str = Field(min_length=1, max_length=300)
    targets: list[str] = Field(default_factory=list, max_length=1000)
    started_at: AwareDatetime
    ended_at: AwareDatetime | None = None
    fault_confirmed: StrictBool | None = None
    external_id: str | None = Field(default=None, max_length=300)
    notes: str = Field(default='', max_length=12000)
    @model_validator(mode='after')
    def dates(self):
        if self.execution_state in ('completed', 'failed', 'aborted') and self.ended_at is None:
            raise ValueError('A terminal execution state needs ended_at')
        if self.ended_at is not None and self.ended_at < self.started_at:
            raise ValueError('ended_at precedes started_at')
        return self

class EvidenceData(StrictModel):
    run_ref: REF
    scope_id: str = Field(min_length=1, max_length=300)
    metric: ID
    value: Value
    unit: str = Field(min_length=1, max_length=40)
    sample_count: int = Field(ge=1, le=1_000_000_000, strict=True)
    window_start: AwareDatetime
    window_end: AwareDatetime
    collected_at: AwareDatetime
    source: str = Field(min_length=1, max_length=2000)
    notes: str = Field(default='', max_length=6000)
    @model_validator(mode='after')
    def dates(self):
        if self.window_end < self.window_start:
            raise ValueError('Evidence window is reversed')
        if self.collected_at < self.window_end:
            raise ValueError('collected_at precedes the end of its measurement window')
        return self

class Resource(StrictModel):
    id: str = Field(min_length=1, max_length=2000)
    name: str = Field(max_length=1000)
    provider: Literal['aws', 'docker', 'podman', 'kubernetes']
    model: Model
    kind: str = Field(max_length=100)
    location: str = Field(default='', max_length=500)
    state: str = Field(default='unknown', max_length=150)
    facts: dict[str, Union[StrictStr, StrictInt, StrictBool, list[StrictStr], None]] = Field(default_factory=dict)

class Coverage(StrictModel):
    scope: str = Field(max_length=300)
    status: Literal['complete', 'denied', 'error', 'truncated', 'not_requested']
    resource_count: int = Field(ge=0)
    error_code: str = Field(default='', max_length=200)
    detail: str = Field(default='', max_length=3000)

class SnapshotData(StrictModel):
    connection_id: ID
    connector: Literal['aws', 'docker', 'podman', 'kubernetes']
    scope_id: str = Field(min_length=1, max_length=300)
    identity: dict[str, str] = Field(default_factory=dict)
    started_at: AwareDatetime
    ended_at: AwareDatetime
    requested_scope: list[str] = Field(default_factory=list, max_length=100)
    coverage: list[Coverage] = Field(default_factory=list, max_length=500)
    resources: list[Resource] = Field(default_factory=list, max_length=20000)
    limitations: list[str] = Field(default_factory=list, max_length=50)
    @model_validator(mode='after')
    def dates(self):
        if self.ended_at < self.started_at:
            raise ValueError('Snapshot time interval is reversed')
        return self

class CheckResult(StrictModel):
    assertion_id: str
    title: str
    category: str
    required: bool
    outcome: Outcome
    reason: str
    expected: str
    observed: Value | None = None
    evidence_ref: str | None = None

class ValidationData(StrictModel):
    run_ref: REF
    scenario_ref: REF
    evaluator_version: str = Field(max_length=80)
    evaluated_at: AwareDatetime
    outcome: Outcome
    checks: list[CheckResult] = Field(default_factory=list, max_length=50)
    gates: list[str] = Field(default_factory=list, max_length=50)
    input_hashes: dict[str, str] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list, max_length=50)

class ReportData(StrictModel):
    validation_ref: REF | None = None
    outcome: Outcome
    body: str = Field(max_length=40000)
    limitations: list[str] = Field(default_factory=list, max_length=50)
    generated_at: AwareDatetime

class BaseRecord(StrictModel):
    id: ID
    revision: int = Field(default=1, ge=1, le=1_000_000, strict=True)
    title: str = Field(min_length=1, max_length=300)
    simulated: StrictBool = False

class ScenarioRecord(BaseRecord):
    kind: Literal['scenario']
    data: ScenarioData
class RunRecord(BaseRecord):
    kind: Literal['execution_run']
    data: RunData
class EvidenceRecord(BaseRecord):
    kind: Literal['evidence']
    data: EvidenceData
class SnapshotRecord(BaseRecord):
    kind: Literal['snapshot']
    data: SnapshotData
class ValidationRecord(BaseRecord):
    kind: Literal['validation_run']
    data: ValidationData
class ReportRecord(BaseRecord):
    kind: Literal['report']
    data: ReportData

Record = Annotated[Union[ScenarioRecord, RunRecord, EvidenceRecord, SnapshotRecord, ValidationRecord, ReportRecord], Field(discriminator='kind')]

class Bundle(StrictModel):
    schema_version: Literal['1.0'] = '1.0'
    kind: Literal['validation_bundle'] = 'validation_bundle'
    records: list[Record] = Field(min_length=1, max_length=5000)
    manifest: dict[str, str] | None = None

class InspectRequest(StrictModel):
    connection_id: ID
class EvaluateRequest(StrictModel):
    run_ref: REF
    evidence_refs: list[REF] | None = Field(default=None, max_length=200)
class ObserveRequest(StrictModel):
    snapshot_ref: REF
class ReportRequest(StrictModel):
    validation_ref: REF
