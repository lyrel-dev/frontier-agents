<!-- USE-CASE-VALIDATION -->
## Use case catalog and presentation structure

The published catalog contains **54** use cases grouped by platform, operational family, delivery mode, cadence and availability. Browser checks cover the standalone catalog and embedded report catalogs. Presentation titles are checked against the editorial marketing-language list, and non-exercise slides must meet minimum information-density rules. These checks validate documentation structure and controls, not successful AWS execution.
<!-- /USE-CASE-VALIDATION -->

# Structured HTML validation

Results are in [qa/checks.json](qa/checks.json). The checks compare every canonical section body and official source register with the pinned previous publication, check chapter membership, nested navigation, links, speaker notes and slide budgets, and verify that no binary presentation outputs remain.

Browser tests use real local HTML navigation at 390 and 1440 pixels. They exercise search, chapter and type filters, chapter expansion, section links, all slides, agendas, keyboard navigation, notes, paused/reset timers, persistent slide links and print-state restoration. These tests do not establish product-documentation correctness or successful AWS operation.

The separate application and its workflow are checked for unchanged content. The current presentation duration and prepared-result exercise allocation are recorded in `qa/checks.json`. Git holds prior revisions; no manual archives are created.
