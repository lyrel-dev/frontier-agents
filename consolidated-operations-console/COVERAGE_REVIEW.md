# Review of commit 3521b93 and coverage amendments

## Verdict

**Request changes on [3521b93](https://github.com/lyrel-dev/frontier-agents/commit/3521b93e026a2db9d0edab0c4d6d2700762f1b7e) as the completed response to model-coverage verification.** The commit is a useful, reproducible source audit and already acknowledges substantial gaps. It does not itself close them. Its substantive-source count omits an identity-bearing FIS child, several crosswalks imply values that have no concrete owner, and the audit accepts insufficient proof for some normalized claims.

The amendments close the identified gaps within the existing contract scope and make the remaining scope explicit. The resulting audit has **41 findings: 36 resolved, five retained-scope decisions, and no unassigned open-review finding**. This means every identified item has a concrete correction or a documented boundary. It does **not** mean every AWS capability is normalized: the broader catalog still contains **one partial and 42 retained-only concepts**.

The original analyses and their 226-file inventory remain unchanged. The audit is about those pinned solution designs, not an independently verified inventory of every current AWS API or live account resource. The amended contract remains a design specification: collectors, storage, authorization enforcement, dispatch, scheduling and evaluation are not implemented by these changes.

## The entity count the original request needed

The four original AWS solution catalogs contain **64 substantive source entity concepts: 30 provider-owned and 34 application-defined**. The shared workflow contributes five additional substantive identities, giving **69 including workflow**. They map many-to-many into **36 uniformly versioned target entities**.

| Source | Provider-owned | Application-defined | Substantive source entities | Normalized | Partial | Retained only |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AWS Health | 3 | 9 | 12 | 11 | 0 | 1 |
| AWS Resilience Hub | 9 | 8 | 17 | 15 | 0 | 2 |
| AWS DevOps Agent | 11 | 10 | 21 | 15 | 1 | 5 |
| AWS FIS | 7 | 7 | 14 | 8 | 0 | 6 |
| Shared assessment workflow | 0 | 5 | 5 | 5 | 0 | 0 |
| **Four AWS solutions** | **30** | **34** | **64** | **49** | **1** | **14** |

The correction from **63 to 64** is `fis:ActionExecution`. The [original FIS report](../aws/fis/analysis/report.md) gives it the scoped key `(experimentKey, actionName)` and separate runtime state/timestamps. Under the audit's identity-and-lifecycle policy it is a source entity concept. Its correct target remains an owned `FISAction` under `Experiment.actions`; this correction does not justify another target entity or a revision-only class. Pure source history constructs remain separate from substantive entities and map to ordinary owner versions.

“Represented” therefore needs a qualifier. All 64 source entity concepts have a declared representation, but only 49 have reviewed normalized core meaning, one is partial, and 14 are inspectable retained evidence. The target's 36 entities are an application design count, not a preservation percentage. Registry lineage names 31 target entities from the four AWS packages and 35 including workflow; Workspace is the shared application boundary. These lineage sets overlap and cannot be summed by service.

## Coverage change, with denominators preserved

The fixed AWS diagram benchmark remains **119 declarations**, with **11** more in the shared workflow. The broader catalog grows from 190 to 193 because the review adds `AssessmentCost`, `PageSnapshot` and `NormalizationDiagnostic` as named dictionary supplements. Those three additions change neither the entity count nor the diagram denominator. The 52 selected DevOps returned/nested SDK types remain a separate overlapping population.

| Population | Total, original → amended | Normalized | Partial | Retained only | Unmapped |
| --- | ---: | ---: | ---: | ---: | ---: |
| Four AWS diagram models | 119 → 119 | 74 → 101 | 22 → 1 | 22 → 17 | 1 → 0 |
| Including shared workflow diagrams | 130 → 130 | 83 → 112 | 24 → 1 | 22 → 17 | 1 → 0 |
| Broader semantic catalog | 190 → 193 | 103 → 150 | 29 → 1 | 57 → 42 | 1 → 0 |
| Selected DevOps SDK types | 52 → 52 | 10 → 13 | 1 → 1 | 41 → 38 | 0 → 0 |

The fixed four-AWS benchmark improves from **74/119 (62.2%) to 101/119 (84.9%) normalized**. Including workflow, it becomes **112/130 (86.2%)**. The original unmapped `ExperimentMetricBinding` now has an executable schema binding and cross-record checks. Zero unmapped concepts means a concrete representation was established; it does not turn retained-only content into normalized capabilities.

The [generated audit](COVERAGE.md), [catalog](coverage/CATALOG.md) and [machine report](coverage/report.json) provide all individual judgments and exact source/target evidence. They are the authoritative counts. [MAPPING.md](MAPPING.md) is now generated from the registry and reviewed judgments, preventing its tables from drifting independently.

## Contract corrections

### Health and Resilience Hub — COV-HR-01 through COV-HR-16

Localized Health descriptions now belong to EventContext and cite their exact Source. Their requested-locale versus stream-language basis is explicit. Batch item errors retain the event/account scope independently of transport success: an HTTP-successful response can contain partial or wholly failed items without pretending the request transport failed. Resource matching preserves method/confidence, and the original application's lifecycle `CANDIDATE` qualifier is retained separately from the conservative application applicability result.

Source can carry typed effective targets, event-subject linkage, deletion/visibility evidence, health measurements and posture evidence. Effective targets distinguish percentages, integer-minute durations and string DR approaches, with per-metric provenance. Native source-account ownership does not imply policy inheritance. Optional normalized PolicyComponent and Recommendation values preserve valid native content while enforcing known family/unit/category constraints. Finding-capture correlation pins an exact same-service assessment and temporal basis without inventing an assessment ownership relationship. Ordered native topology properties remain available.

Normalization itself now has provenance: input content digest, rule digest and normalization time, plus optional diagnostics containing path, raw value, normalized/fallback value and reason. A changed normalized result or rule creates a new Source version even if the raw bytes are unchanged. Raw `contentDigest` is not repurposed as a digest of the derived view. Native JSON values remain opaque to console identity walking.

The three supplements address missed crosswalk claims. AssessmentCost is explicitly retained at the assessment profile's `$.cost`; no typed cost object is claimed. PageSnapshot maps to the actual RPC Page response value, including optional `totalResults`. That count means the exact authorized, filtered cardinality of the retained local traversal publication; absence means unknown. It is not a page length, hidden-resource count or AWS completeness claim. NormalizationDiagnostic has an actual Source owner. Permission/discovery/DNS configuration and other native administration objects receive concrete retained profile/member paths instead of nonexistent typed-value names.

### DevOps Agent — DEVOPS-COV-01 through DEVOPS-COV-11

Two new typed Projection profiles bind investigation timelines and published assertions to exactly one Investigation. They preserve subjects, attribution, confidence evidence, derivation, publication/observation times, grouping and supersession. Findings, hypotheses, root-cause assessments, mitigation proposals, review results and action-stage observations are explicit typed envelopes. Their published content stays opaque; this contract neither exposes private model reasoning nor invents unpublished assertions.

Exact evidence must appear among the projection inputs. Scoped subjects and referenced commands/approvals agree with the Investigation's AgentSpace. Parent links are local and acyclic; supersession targets the current rendition or an explicitly cited older version of the same logical Projection. Independent source clocks may be out of order, so grouping is not promoted into causal or timestamp order. Native journal attribution remains distinct from a trusted console actor, and artifact references preserve their channel and selected Asset version without claiming cross-channel absence or historical consumption.

Graph provenance now distinguishes provider evidence, application inference, operator statements and independent observations. A provider edge cannot disguise application inference; an execution hierarchy cannot manufacture causality. Collection and coverage metadata retain exact collector/selection/evaluation policy identities where supplied.

Approval invocation distinguishes validated context from unsupported or incomplete native context. Decision receipts retain the exact request Source, action pattern/digest, ApprovalRequest, Execution and AgentSpace. Resume receipts also retain the successful decision Command. Their version guards have different owners: decision guards ApprovalRequest, resume guards Execution. Approval, resume, observed action execution and operational recovery remain independent facts.

### FIS and shared workflow — COV-FIS-01 through COV-FIS-05; COV-FW-01 through COV-FW-04

Selectors remain represented even when they resolve to no resources. Memberships and action slots use explicit target names instead of parsing opaque keys. Selector and action-map completeness are separate. Known duplicate names/edges, self-edges and multi-node cycles fail for all captures. `COMPLETE` action maps require every endpoint. Explicit `PARTIAL`/`UNKNOWN` allows unloaded endpoints. Unmarked legacy records retain the former closed-reference validation; this preserves the original negative cases without claiming that their provider collection was complete.

`ExperimentMetricBinding` now belongs to a typed EVALUATION_INPUT Snapshot value under `console.telemetry.evaluation-input/v1`. Four application Source profiles bind query definitions, numeric metric observations, criteria and workflow observation envelopes. Exact experiment/query/criterion versions, units, period, event windows, action anchors, cutoff evidence and capture closure are checked. Standalone FIS experiments need no fabricated workflow Run. Raw CloudWatch profiles remain retained native evidence until explicitly normalized.

StepAttempt recovery retains once-resolved input pins, checkpoint history and technical execution errors. Run citations distinguish produced, consumed and imported evidence and keep producer/consumer attempts within the same Run. Workflow observations preserve declared value availability and schema identity, while their arbitrary value remains opaque. CheckResult includes optional evaluator identity and actual/expected summaries; a false criterion remains different from a technical execution error. The obsolete evaluation/version terminology and profile descriptions are corrected.

## Audit and reproducibility corrections — COV-AUD-01 through COV-AUD-05

The coverage check now requires real target ownership and schema evidence. A reachable entity name, generic EntityRef or opaque JSON payload cannot by itself prove an owned normalized value. Supporting raw/constraint paths are labeled separately from normalization-proof paths. Normalized profile metadata must name the correct owner, admitted discriminator and a live direct typed binding in the supported schema pattern. A foreign schema-document prefix is rejected instead of silently resolved against the current model.

Transport DTOs use a separate proof route: their typed definition must be reachable from an actual declared operation request/response. PageSnapshot therefore has an RPC response owner, with no invented domain entity. The 52 native SDK judgments now validate their source heading, semantic kind, shape role, mapped source concept, profile IDs, owner binding and consistency with that concept's coverage level.

Every finding has a unique ID, explicit status, affected-construct references, resolution and validation evidence. A resolved status alone does not award normalized credit. Static duplicated input summaries and cached registry/diagram snapshots are removed. Counts, crosswalk tables, value/profile totals and status narratives are derived. Inventory metadata is pinned to the frozen source tree; review findings name the exact reviewed commit. Catalog bytes are hashed into the report, and HTML verifies the catalog/report hashes and common source/target pins before combining individual cards with totals.

The full validation gate also exposed a packaging defect: the documented renderer dependency installation made Markdown link checks scan ignored third-party documentation. The checker now limits that gate to maintained Git files, including new review files before staging.

The [mapping rulebook](MAPPING_RULES.md) now has **25 rules**, including explicit recovery provenance, approval authority, selector joins, falsifiable coverage proof and completeness-aware relationship validation. The existing entity/value/reference/version/retention rules remain intact.

## Compatibility and review boundaries

No target entity, operation or revision-only class is added. The 36 entity names, 108 operation names and V2 namespace remain stable. The original 215 model examples and 216 RPC request/response examples are tested directly from the reviewed Git commit against the amended contracts; existing fixtures are not rewritten to make them pass. All 79 original semantic cases continue to pass.

Most new content is optional or selected through a new explicit profile. Omitted historical metadata remains unknown or retained-only; it is never backfilled by choosing today's normalizer, collector or policy. Existing broad native values remain available beside narrower normalized views. A client opting into the new profiles needs their new schemas. The compatibility evidence covers the original corpus and stated invariants; it is not a proof that every malformed record accepted by a formerly permissive schema remains accepted. Duplicate/cyclic action graphs and contradictory new provenance are deliberately rejected.

The five retained-scope decisions are concrete boundaries:

| Decision | Boundary and review trigger |
| --- | --- |
| COV-HR-13 | Health event-type/aggregate evidence and Resilience configuration, discovery, permissions and DNS administration remain retained. Add typed administration only for a specified consumer/workflow and field-authority model. |
| COV-HR-14 | AssessmentCost remains an exact retained cost observation. Review before typed cost comparison, units/currency assumptions or remediation budgeting. |
| DEVOPS-COV-09 | Registered services, goals, recommendations, triggers, private connections and peripheral native DTOs remain retained. Normalize when an application workflow requires their independent lifecycle. |
| DEVOPS-COV-11 | Investigation normalizes Task's INVESTIGATION facet. Other native Task discriminators remain partial/retained until concrete workflows define their ownership and lifecycle. |
| COV-FIS-01 | Template/catalog/target-account/stop-condition and other native FIS configuration breadth remains retained. Runtime selectors are now typed; a full authoring/control plane is outside this contract amendment. |

These decisions do not conceal open implementation work. Before production use, require real adapter fixtures for pagination, partial/empty reads, locale and unknown native values; immutable version storage and concurrency; current authorization over exact evidence closure; durable idempotency/dispatch/reconciliation; normalization reprocessing policy; evaluator and checkpoint recovery conformance; retention behavior; and actual UI integration. [VALIDATION.md](VALIDATION.md) records those implementation gates. No live AWS call or production service behavior was verified by this amendment.

## Validation and reviewer navigation

Reproduce from the repository root:

```sh
python consolidated-operations-console/tools/validate.py --json
python -m unittest discover -s consolidated-operations-console/tools -p 'test_*coverage.py'
python consolidated-operations-console/api/generate.py --check
python consolidated-operations-console/tools/render_model.py --check
python consolidated-operations-console/tools/build_coverage.py --check
python consolidated-operations-console/tools/build_reference.py --check
```

The new regression suite contains **130 tests**, covering original-fixture compatibility, positive domain bindings and adversarial scope/time/ownership/provenance cases. The model/API generator, source inventory, semantic fixtures, editable Draw.io atlas and offline HTML reference are checked separately. A dedicated CI workflow runs these gates on pull requests with read-only repository permissions. Executed results and the remaining limits are recorded in [VALIDATION.md](VALIDATION.md), [validation.json](validation.json) and [reference/build-report.json](reference/build-report.json).

For review, start with [schema.json](model/schema.json), [adapter-profiles.json](model/adapter-profiles.json), [the API generator](api/generate.py), the three domain contract helpers under [tools](tools/), and the service-specific review inputs under [coverage](coverage/). The large generated reference/catalog changes follow from those sources. Original source analyses are untouched.

### Complete finding register

Original finding titles are preserved as history. The full source evidence, amended paths and resolutions are in [COVERAGE.md](COVERAGE.md).

| Finding | Disposition | Original issue |
| --- | --- | --- |
| `COV-HR-01` | RESOLVED | Localized EventDescription is declared but unbound |
| `COV-HR-02` | RESOLVED | Health failedSet item scope is absent from normalized errors |
| `COV-HR-03` | RESOLVED | OrganizationHealthAccess registry targets omit its actual owner |
| `COV-HR-04` | RESOLVED | Match confidence and lifecycle candidate semantics need an explicit disposition |
| `COV-HR-05` | RESOLVED | Effective target values remain retained rather than normalized |
| `COV-HR-06` | RESOLVED | Policy component read-shape validation can be tightened |
| `COV-HR-07` | RESOLVED | Finding capture assessment correlation lacks a typed basis |
| `COV-HR-08` | RESOLVED | Recommendation identity is normalized but its content is arbitrary JSON |
| `COV-HR-09` | RESOLVED | Native topology edge property collections are not normalized |
| `COV-HR-10` | RESOLVED | Operational event subject linkage remains untyped |
| `COV-HR-11` | RESOLVED | Source reference tombstone semantics have no explicit target field |
| `COV-HR-12` | RESOLVED | Runtime-health and component-posture evidence are retained profiles |
| `COV-HR-13` | RETAINED_SCOPE | Native administration and auxiliary configuration are intentional retention boundaries |
| `COV-HR-14` | RETAINED_SCOPE | AssessmentCost registry implied a typed value that did not exist |
| `COV-HR-15` | RESOLVED | Original PageSnapshot totalResults lacked a bound response field |
| `COV-HR-16` | RESOLVED | NormalizationDiagnostic had no bound target despite registry claims |
| `DEVOPS-COV-01` | RESOLVED | Registry rows and aliases do not count independent entities |
| `DEVOPS-COV-02` | RESOLVED | Timeline and richer investigation assertions are retained, not normalized projections |
| `DEVOPS-COV-03` | RESOLVED | Native journal attribution is not an ActorRef binding |
| `DEVOPS-COV-04` | RESOLVED | Graph structure exists but required graph meaning and provenance are incomplete |
| `DEVOPS-COV-05` | RESOLVED | Approval context is pinned but invocation and scope values remain raw |
| `DEVOPS-COV-06` | RESOLVED | Collector and coverage-policy identity are not retained as typed metadata |
| `DEVOPS-COV-07` | RESOLVED | Generic artifact storage descriptors do not fully normalize cross-channel artifact references |
| `DEVOPS-COV-08` | RESOLVED | The decision Command receipt does not expose a reconstructable decision input |
| `DEVOPS-COV-09` | RETAINED_SCOPE | Peripheral native resources are represented only by retained source profiles |
| `DEVOPS-COV-10` | RESOLVED | SnapshotProjection crosswalk wording uses obsolete target field names |
| `DEVOPS-COV-11` | RETAINED_SCOPE | Native Task normalization selects one task discriminator |
| `COV-FIS-01` | RETAINED_SCOPE | Retained provider configuration is mislabeled as normalized owned values |
| `COV-FIS-02` | RESOLVED | Resolved memberships lack a typed selector join |
| `COV-FIS-03` | RESOLVED | Telemetry binding and experiment-assessment linkage are not concretely mapped |
| `COV-FW-01` | RESOLVED | Attempt recovery facts have no declared value contract |
| `COV-FW-02` | RESOLVED | Evidence ownership and production/import roles need an explicit consolidation rule |
| `COV-FW-03` | RESOLVED | A normalized profile advertises fields absent from its bound value |
| `COV-FW-04` | RESOLVED | Evaluation profile identity wording retains removed revision-resource names |
| `COV-FIS-04` | RESOLVED | FIS substantive entity count omitted the identity-bearing action execution child |
| `COV-FIS-05` | RESOLVED | Action dependencies lack complete graph validation and hydration-aware endpoint rules |
| `COV-AUD-01` | RESOLVED | Normalized path checks do not establish the declared owner binding |
| `COV-AUD-02` | RESOLVED | The separate native SDK shape audit accepts incomplete proof |
| `COV-AUD-03` | RESOLVED | Generated coverage prose hard-codes unresolved findings and model counts |
| `COV-AUD-04` | RESOLVED | Review inputs duplicate unchecked summaries and registry snapshots |
| `COV-AUD-05` | RESOLVED | The documented renderer setup makes link validation scan ignored dependency documentation |
