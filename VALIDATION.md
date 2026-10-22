# Documentation validation

The current [machine-readable results](qa/checks.json) distinguish source structure, rendered behavior, and synthetic examples. The [content revision record](qa/content-review.json) identifies cleanup and editorial changes; the [source review record](qa/source-review.json) identifies new and selectively rechecked official material.

The [product resource checks](qa/resource-models.json) verify entity ownership, qualified relationships, all feature/resource bindings and unchanged approved catalog sources. [Product-source evidence](qa/product-source-review.json) identifies the exact reviewed claims and version qualifications.

The [relationship checks](qa/relationships.json) additionally validate all 54 former-record mappings, 30 outcome definitions, workflow dependency types, feature configuration references, implementation profiles, reverse impact links and semantic regression cases. These are modeled dependencies, not live availability tests.

Checks cover stable section identifiers, source mapping, use-case narratives, local links, unique SVG identifiers and accessibility descriptions, report and catalog filtering, chapter and slide navigation, notes, timers, hash links, and print-state restoration at desktop and mobile widths. The synthetic cost arithmetic and incident/security evidence relationships are checked separately.

These are not live AWS tests, an exhaustive upstream-documentation audit, or a claim that passing structural checks alone establishes good technical writing. The diagrams are logical explanatory models. No productivity, accuracy, security coverage, or savings result has been measured.

The application tree and its workflow are compared with the pinned baseline and must remain unchanged. Superseded document entry points and generators are removed rather than archived.
