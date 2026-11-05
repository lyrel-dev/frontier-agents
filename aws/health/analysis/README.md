# AWS Health: reviewed model and operator UI prototype

This package contains the reviewed AWS Health API analysis, four entity relationship diagrams, and **Pulse**, a single-page operator application that makes the initial model tangible with a realistic fictional scenario.

**Open [index.html](index.html) to run the prototype.** The generated page contains its JavaScript, styles, mock data, and diagram SVGs. It runs offline in a modern browser without a package installation, application server, or runtime dependencies. Keep the adjacent report and diagram files to use the document links in the application.

The model separates **AWS-reported evidence**, **collection coverage**, **derived lifecycle posture**, and **local operator workflow**. A completed task can coexist with a provider-pending entity and an older inventory observation. A public advisory can remain relevant without establishing an affected account. The reasons for these boundaries, the full operation inventory, and official AWS citations are in [report.md](report.md).

## Deliverables

| Deliverable | Purpose |
|---|---|
| [index.html](index.html) | Self-contained, generated application entry point |
| [report.md](report.md) | Canonical reviewed API analysis, model, entity dictionary, constraints, and official source index |
| [report.pdf](report.pdf) | Readable report containing all four diagrams and the source index |
| [REVIEW.md](REVIEW.md) | Review findings, incorporated clarifications, and documentation verification |
| [tools/README.md](tools/README.md) | Report and diagram generation instructions and supported source format |

### Entity relationship diagrams

Each diagram has editable Mermaid source and a standalone SVG. The SVGs are also embedded in the application and PDF.

| Diagram | Editable source | Rendered diagram |
|---|---|---|
| Event and account impact | [01-core-model.mmd](diagrams/01-core-model.mmd) | [01-core-model.svg](diagrams/01-core-model.svg) |
| Source history and delivery | [02-history-delivery.mmd](diagrams/02-history-delivery.mmd) | [02-history-delivery.svg](diagrams/02-history-delivery.svg) |
| Lifecycle posture | [03-lifecycle-posture.mmd](diagrams/03-lifecycle-posture.mmd) | [03-lifecycle-posture.svg](diagrams/03-lifecycle-posture.svg) |
| Operator workflow | [04-operator-workflow.mmd](diagrams/04-operator-workflow.mmd) | [04-operator-workflow.svg](diagrams/04-operator-workflow.svg) |

## Run and rebuild

Open `index.html` directly, or serve this directory for a consistent browser origin and storage behavior:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/>. This optional server only serves the checked-in files; it does not collect AWS data.

From this `analysis` directory, rebuild the generated application with Python 3:

```bash
python3 app/build.py
```

The application build uses only the Python standard library. It reads the source files and the four reviewed SVGs, then writes `index.html`. Make changes in `app/src/` and rebuild; direct edits to the generated HTML are overwritten.

To regenerate diagrams using the Python standard library:

```bash
python3 tools/render_diagrams.py
python3 app/build.py
```

To regenerate the PDF and diagrams, follow [tools/README.md](tools/README.md). The documentation build uses the dependencies in [tools/requirements.txt](tools/requirements.txt); those are not application runtime dependencies.

```bash
python3 -m pip install -r tools/requirements.txt
python3 tools/build_report.py
python3 app/build.py
```

### Source layout

| Path | Responsibility |
|---|---|
| [app/src/shell.html](app/src/shell.html) | Page shell, navigation, dialogs, and bundle placeholders |
| [app/src/styles.css](app/src/styles.css) | Layout, responsive presentation, and visual states |
| [app/src/mock-data.js](app/src/mock-data.js) | Normalized fictional records, fixed scenario metadata, expected counts, and replay event |
| [app/src/model.js](app/src/model.js) | Pure joins, filters, counters, lifecycle calculations, coverage assessment, and relational validation |
| [app/src/app.js](app/src/app.js) | Views, detail panels, browser-local work, simulated controls, and JSON export |
| [app/build.py](app/build.py) | Standard-library bundler for the offline HTML |
| [app/tests/model.test.cjs](app/tests/model.test.cjs) | Node semantic tests against the normalized scenario |
| [tools/build_report.py](tools/build_report.py) | PDF generation from the canonical report and diagrams |
| [tools/render_diagrams.py](tools/render_diagrams.py) | Report-specific SVG generation from the Mermaid source semantics |

`mock-data.js` and `model.js` expose browser globals and CommonJS exports. The model exports `eventRows`, `metrics`, `lifecycleRows`, `coverageSummary`, `workRows`, `serviceMatrix`, and `validateData`, allowing the same semantic rules to drive the interface and tests.

## Explore the six application areas

| Area | What to inspect |
|---|---|
| **Overview** | Open issue and pending-action counts, resources approaching lifecycle milestones, collection completeness, service/region activity, and prioritized team work |
| **Event feed** | Account and public contexts, category/actionability/state filters, event details, entity states, source history, and normalized model records |
| **Action center** | Team assignments, acknowledgements, work progress, completion, verification, and response notes; these are local application records |
| **Lifecycle posture** | Catalog milestones joined to separately observed deployments, explicit matching evidence, planning horizons, and unmatched inventory |
| **Coverage** | Complete, partial, and stale collection scopes; provider time versus collection time; the intentionally missing communication page |
| **Model & report** | All four ERDs, model principles, the reviewed PDF, canonical Markdown, and editable diagram sources |

### Controls and state ownership

- **Search, account, and region filters** narrow the relevant model records. The Event feed adds category, scope, actionability, and AWS event-state controls. Event-only filters reset when navigating to other areas. A public event stays visible under account selection while contributing zero reported affected accounts.
- **Assignments, workflow changes, and notes** persist in this browser when local storage is available. They do not change AWS event/entity state or replace an inventory observation. If browser storage is unavailable, the session stays usable in memory and export preserves a copy.
- **Replay AWS update** applies one predefined mock provider update: `payment-webhook` changes from `PENDING` to `RESOLVED`. The other payment function remains pending, the event stays open, and the completed local work item and older lifecycle inventory assessment remain separate. Reset permits another replay.
- **Refresh observations** simulates collecting the same evidence again. It advances successful collection timestamps while preserving provider update timestamps and the known stale/partial gaps. It does not invent missing pages or mark a workload healthy.
- **Planning horizon** changes the lifecycle list between 30, 60, 90, and 365 days. Overdue milestones remain visible; unmatched applicability remains unknown.
- **Export snapshot** downloads JSON containing the fictional scenario, current filters, and local operator work. It does not upload data or export live AWS information.
- **Reset demo scenario** asks for confirmation before restoring the original fixture and clearing the saved demo changes. Cancel preserves the current session.

## Fixed fictional scenario

The initial snapshot is **5 November 2026 at 13:30 UTC / 14:30 CET**, displayed in the `Europe/Zurich` time zone. Calculations use the scenario clock, not today's wall clock. Explicit replay and refresh controls advance the simulation.

All organization names, account IDs, resource IDs and ARNs, event IDs and ARNs, incidents, descriptions, and milestone dates are **synthetic demonstration data**. Familiar AWS service names, source-field names, and enum values illustrate the documented contract. The fixture's version schedules must not be used as AWS support guidance; native AWS claims and their official citations belong to the reviewed report.

### Baseline counts

These values apply after reset with no filters. A saved session, selected scope, or replay can change visible totals.

| Counting unit | Initial value | Interpretation |
|---|---:|---|
| Health events | 10 | 7 open, 2 upcoming, and 1 closed; counted by event identity |
| Open issue events | **3** | Includes the public S3 advisory |
| Reported affected accounts | 5 | Established by ACCOUNT contexts; public recipients add none |
| Regions | 4 | Frankfurt, Ireland, Northern Virginia, and Oregon |
| Contexts | 15 | 13 ACCOUNT, 1 PUBLIC, and 1 ORG_SUMMARY |
| Observed entity-impact records | 21 | Event-relative observations, including one broader impact marker |
| Impaired entity records | 4 | Explicit source `IMPAIRED` |
| Pending entity records | **5** | Explicit source `PENDING`, independent of local completion |
| Unknown / unsupplied entity status | 5 / 1 | Explicit `UNKNOWN` and a missing status are distinct |
| Unimpaired / resolved entity records | 3 / 3 | Retained source states, not inferred from work completion |
| Mapped impact rows / distinct affected resources | 20 / 19 | The warehouse writer participates in two events but is one inventory resource |
| Inventory resources | 20 | Includes proactive inventory without an associated Health event |
| Confirmed lifecycle exposures | 7 | Deployment-to-milestone assessments |
| Resources with future milestones within 30 days | **4** | Excludes the two overdue exposures; counts distinct resources |
| Unmatched deployments | 1 | Catalog applicability stays unknown |
| Complete collection scopes | **3 of 5** | One additional scope is stale and another has only 2 of 3 communication pages |
| Local work items | 9 | 4 new, 1 acknowledged, 3 in progress, 1 completed, and 0 verified |

The Oregon example uses a deliberately reduced number of rows to demonstrate incomplete page assembly; it does not claim that these small payloads reached an AWS transport size limit. Its two EventBridge-only impacts have no supplied Health entity ARN before API hydration. Their local, context-specific impact identities remain usable without inventing a provider identifier.

### Model invariants made visible

The operational core is `HealthEvent → EventContext → EntityImpact`. ACCOUNT contexts establish account attribution; ORG_SUMMARY observations do not own entity impacts. A Health entity can be a resource, a group, or a broader construct, so entity count and distinct inventory-resource count use different units.

A mixed context status is a **local rollup**, not an AWS event-state enum. Source `UNKNOWN`, an unsupplied field, stale collection, partial pagination, and unmatched lifecycle applicability retain separate meanings. A quiet service/region cell means no matching open event was observed within the available coverage; the application does not infer workload health from silence.

Lifecycle exposure is a derived catalog-to-inventory relationship. Local completion and a later AWS entity update do not rewrite the earlier inventory scan. A new inventory observation is needed to establish a changed deployment. The report describes the corresponding ownership, identity, provenance, and matching rules in detail.

## Validation record

### Automated semantic checks: passed

Run the dependency-free Node test suite from this directory with a recent Node.js release supporting `node:test` and `structuredClone`:

```bash
node --test app/tests/model.test.cjs
```

**Recorded result: 10 tests passed, 0 failed.** The checks cover:

1. Relational validity and distinct baseline counting units.
2. Public visibility without affected-account attribution; repeated deliveries without duplicate events.
3. Account, region, category, search, and actionability filtering with consistent counts.
4. Per-context status matching and an explicitly local mixed-state rollup.
5. Explicit unknown versus unsupplied state, with unfamiliar provider values preserved.
6. Operator completion and verification remaining independent of provider impact and lifecycle exposure.
7. One verified resource participating in two events without double-counting the resource.
8. Incomplete or absent coverage remaining uncertain even when no event is returned.
9. Fixed-clock lifecycle calculations and the unmatched deployment remaining unknown.
10. Invalid references, duplicate identities, contradictory account routing, and work targets with multiple target types being rejected.

The documentation review and report/diagram verification are recorded separately in [REVIEW.md](REVIEW.md).

### Browser QA: verified flows and remaining limit

The generated application was exercised in Chrome through the managed preview. Desktop presentation and a **390-pixel-wide iframe viewport** were visually inspected. This is a narrow-layout check, not physical-device testing.

| Check | Observed result |
|---|---|
| Six application areas | Overview, Event feed, Action center, Lifecycle posture, Coverage, and Model & report rendered successfully. |
| Public advisory | S3 detail showed zero affected accounts and zero entities despite notification recipients. |
| Account and state filters | Development → Lambda showed only its one entity and no Payments task; Closed state returned the recovered ELB event. Public-scope filtering also worked. |
| Event and exposure details | Event summary/entity panels and lifecycle milestone/resource evidence opened successfully. |
| Lifecycle population | Seven confirmed exposures, two overdue assessments, four future assessments within 30 days, and exactly one unmatched deployment were displayed. |
| Local response | Acknowledgement, team reassignment, response note, and completion worked. The AWS entity remained pending; reassignment and completed workflow survived reload. |
| Provider replay | Pending entities decreased from five to four. The payment-webhook entity became resolved, the shared event stayed open, and lifecycle exposure remained unchanged. |
| Collection refresh | Complete scopes received a newer collection time. Provider update times, stale reconciliation, and missing communication page remained unchanged. |
| Diagrams | All four embedded diagrams rendered with their accessible titles and descriptions. |
| Responsive navigation | The 390-pixel layout stacked metrics and panels, and the navigation drawer opened and navigated to Event feed. |
| Console inspection | No application-origin errors were observed during the exercised flows; browser-extension metadata errors were excluded. |

A final browser pass was rejected by the browser URL policy. **Browser verification remains incomplete** for text search and region controls, alternate planning horizons, the timeline and model-data tabs, JSON download, reset cancellation/confirmation, document-link navigation, and a full keyboard/focus audit. The semantic suite covers filtering, matching, and state boundaries independently. The final changes to responsive focus handling and replay summary text were syntax-checked and bundled after the main UI exercise; they were not fully re-exercised after that browser limitation.

A static audit confirms that the generated HTML embeds all application scripts, CSS, mock data, and diagram SVGs and requires no external runtime assets. A separate network-disabled browser run was not performed. File-origin storage behavior remains browser-dependent; the application catches storage failures and preserves the in-memory session.

## Production boundary and delivery scope

This is a model demonstrator. It implements no authentication, tenant authorization, backend persistence, live AWS API collector, EventBridge subscription, actual event stream, inventory connector, or resource remediation. Browser storage is local demo state, not a shared operational record.

The source evidence is read-only from the operator workflow. The only provider-state transition offered here is the clearly labeled mock replay. The reviewed AWS Health operation inventory contains two native organization integration mutations—`EnableHealthServiceAccessForOrganization` and `DisableHealthServiceAccessForOrganization`—and **neither is implemented by this prototype**. Acknowledgements, assignments, notes, completion, and verification belong to the local application model; see the report's [API capability inventory and writable boundary](report.md#1-api-capability-inventory).

A production implementation would need authenticated collection, tenant-scoped identities, durable raw evidence and revision storage, idempotent page/delivery assembly, reconciliation and freshness policies, audited workflow persistence, and verified inventory matching. The [reviewed report](report.md) provides the initial model and design constraints for that work.

The requested delivery target is the **`main` branch** of the `frontier-agents` repository. This package is scoped to **`aws/health/analysis/`**; the existing service documents and applications outside this directory are outside this change.
