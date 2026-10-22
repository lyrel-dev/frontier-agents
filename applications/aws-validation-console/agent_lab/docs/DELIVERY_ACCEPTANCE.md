# Delivery acceptance: implemented software versus live Definition of Done

Source baseline: `b9dc53939611cc32904b49e2447dbb7fd5e2ab35`.
Implementation version: **0.5.1-dev**. No live AWS result or remote publication is implied by this document.

## Component gates

| Gate | Implementation and executable coverage | Live obligation |
|---|---|---|
| Account onboarding | Versioned profiles/accounts/Regions, source reads, Agent Space/association discovery, separate approval, stale-revision and active-work rejection; `tests/test_delivery_components.py`, `tests/setup_browser_checks.py`. | Actual role/SSO refresh, expected identities, Region availability and least-privilege efficacy. |
| FIS discovery | Paginated resumable catalogue, raw captures and explicit incomplete coverage; `tests/test_fis_fleet.py`. | Enumerate the authorized account set and compare with independent AWS inventory. |
| Native preparation | Approved skip-all preview, target/account map, guided typed checks and compound local activation; delivery, native workflow and SDK contract tests. | Actual selector/resource types, complete target resolution and safe IAM envelope. |
| Actual orchestration path | Fresh dispatch preview, separately journaled run-all, drift detection, per-account verification and cleanup; `tests/test_native_workflow.py`, inherited lifecycle/safety tests. | Approved non-production fault through AWS, reliable cloud-side stopping, observed effect in every target account. |
| Response evidence | Native correlation, captured receipts/tasks/journals, no-response/collection distinctions, cited diagnosis and independent recovery; inherited response tests. | Existing route delivery, agent behavior and independent diagnosis review. |
| Business and collateral checks | Required closed-window metrics; pass/fail/missing outcomes, graphs, CSV and prevention gating; native workflow tests. | Independently accepted metric/reconciliation producers and meaningful limits. |
| Prevention | Versioned recommendation, exact implementation, independent after-state and qualified replay; inherited campaign tests plus business requirement gating. | A real recommendation, deployed change and comparable real replay, with benign and failed controls. |
| Operational packaging | Empty runtime, source-derived schemas/previews, deployment definitions, native/browser scripts and restart harnesses. | Current source deployed on the intended Docker/Podman/Kubernetes/local host, credentials, volume durability, backup/recovery and native browser acceptance. |

The machine-readable `validation/acceptance-traceability.json` records the updated requirements. `validation/delivery-validation.json` in the package records the tests actually run, without reusing old CI results. Provider fixtures are test-only. Runtime fixtures and passing examples are not installed.

## Required live workflow

1. Preserve reviewed source/image hashes. Install approved credentials and independently review roles, recovery and target scope.
2. Use Guided setup to connect the account set, select the real Agent Space and every target association, discover templates, perform approved skip-all previews and register a complete measurement plan.
3. Run one approved native-response trial, then a repeated campaign. Compare actual target/operation IDs, incident references, source receipts, agent findings and workload measurements with AWS evidence.
4. Exercise wrong account, denied evidence, no response after proven delivery, ambiguous reference, changed targets, expired approval, worker interruption, stopping and failed restoration. Do not disable the only independent recovery path.
5. Obtain an actual recommendation, implement the reviewed change, verify state, replay under comparable challenge, and evaluate business/data and collateral requirements. Retain unsuccessful/unmatched attempts.
6. Independently audit all pinned evidence and the test's scope. Require native UI and intended-host acceptance for the exact revision. Record unresolved issues rather than converting missing evidence into approval.

Passing unit, SDK, HTTP or DOM tests is not closure of these live gates. Credentials cannot be manufactured for acceptance. Until the real environment is authorized and observed, **the full product Definition of Done is not met**. Deliberate boundaries in COVERAGE.md also remain visible; they are not silently waived as successful requirements.

## Publication

The delivery branch retains the reviewed source and required CI. See REPOSITORY.md for integration boundaries and RELEASE_0_5_1.md for this increment. Actual publication and current-source CI results must be verified; no live AWS claim follows from source publication.
