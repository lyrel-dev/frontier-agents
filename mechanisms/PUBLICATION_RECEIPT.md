# Publication receipt: mechanism documentation v2

Date: 21 October 2026. Status: published and downloaded output verified.

## Published revision

- Repository: `lyrel-dev/frontier-agents`
- Branch: `main`
- Content revision: `2026-10-21-mechanisms-v2`
- Workflow: [39590540403](https://github.com/lyrel-dev/frontier-agents/actions/runs/39590540403)
- Trigger commit: `cfa370676fb78441a209e869b6e314f0f171dd56`
- Workflow job: `119190098654`, completed successfully, including generation, structural validation, per-document commits and artifact upload.
- Repository visibility: private; unchanged.
- GitHub Pages: not deployed by this workflow.

## Package identity

The GitHub Actions artifact was downloaded through the connected repository integration. Its nested document ZIP is identical to the repository file `dist/frontier-agents-document-suite.zip`.

| Item | Verified value |
|---|---|
| Artifact ID | `12341691323` |
| Artifact SHA-256 | `9d67df960012bbd960ef58bf78d78caf685d16845d9a66cf1972694e3764cd04` |
| Document ZIP bytes | `2097939` |
| Document ZIP SHA-256 | `5b56846172e79425897a161f28e94cb9eb8f4f624503da7d2204d40328ab7eae` |
| Document ZIP Git blob SHA | `c864f87d0c3320cada7cc17fefca463e3df1864b` |
| Manifest entries verified | 119 |
| Manifest mismatches | 0 |

This receipt was committed after the package was verified. It is intentionally outside the package whose checksum it records.

## Checks on a fresh extraction

`python tools/build_suite.py --check` passed without creating a local `dist` directory: 14 active HTML files, 2,104 local links/anchors and all five core presentation schedules; no recorded errors.

The browser regression suite was rerun against a copy of the downloaded files. Four mechanism guides, the index and comparison overview passed desktop and mobile checks at 1440 and 390 pixels. Search, filters, disclosures, six-step reading mode, presentation navigation, exports, keyboard controls and print restoration passed where applicable. No JavaScript page errors or horizontal page overflow were recorded. Another 329 mechanism-companion local links were checked. Inline mechanism sections in all five main reports passed mobile layout checks. The test loaded self-contained HTML with Playwright `set_content`; it did not navigate a deployed website.

Ten downloaded PowerPoint decks contained 232 slides. Shape-bound and nonempty-speaker-note checks passed. All 14 DevOps mechanism slides were rendered again; the new corrective-feedback slide and shortened exercise page were visually inspected. This is not a new pixel-level review of every slide.

The editorial validator passed with no recorded errors. The published source contains 32 mechanism records and 46 official source references. The 88 timed core slides still total 160 minutes, including 48 demonstration minutes. Reference slides are untimed; four separately selectable prepared-result exercises add 44 minutes if delivered.

## Evidence boundary

See [CONTINUATION_VALIDATION.md](CONTINUATION_VALIDATION.md) for the corrections and source-check scope. Selected critical memory, feedback, setup and lifecycle sources were rechecked, and two references were added; not every historical product claim was freshly audited. The source count is not a claim that every page was re-fetched in this continuation.

No live AWS workflow, account change, penetration test, cost action or memory-recall experiment was performed. No performance, accuracy, savings or productivity result is measured. Proposed verification procedures remain labeled as proposed.
