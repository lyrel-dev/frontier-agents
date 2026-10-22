# Structured HTML validation

Results are in [qa/checks.json](qa/checks.json). The checks compare every canonical section body and official source register with the pinned previous publication, check chapter membership, nested navigation, links, speaker notes and slide budgets, and verify that no binary presentation outputs remain.

Browser tests use real local HTML navigation at 390 and 1440 pixels. They exercise search, chapter and type filters, chapter expansion, section links, all slides, agendas, keyboard navigation, notes, paused/reset timers, persistent slide links and print-state restoration. These tests do not establish product-documentation correctness or successful AWS operation.

The separate application and its workflow are checked for unchanged content. The existing 124-minute programme and 28-minute prepared-result exercise allocation are retained. Git holds prior revisions; no manual archives are created.
