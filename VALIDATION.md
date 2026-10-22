# Validation and evidence boundary

Revision: 2026-10-22-canonical-guides.

The completed automated checks are recorded in [qa/checks.json](qa/checks.json). They cover 57 globally identified canonical sections, 272 local HTML links, 54 PowerPoint slides, note references and the explicit synthetic fixtures. Browser checks run at 390 and 1440 pixels when `--browser` is used; the JSON records whether they actually ran.

The source review is editorial work, separate from the automated checks. Each guide identifies its reviewed official sections, unresolved or conflicting source versions, and detailed versus linked/deferred coverage. A passing reference-ID check does not prove a source supports every claim. See [content review](qa/content-review.md).

The new presentation programme is 124 minutes including 28 minutes of prepared-result exercises. The evidence appendix in each deck is untimed. These are walkthrough budgets, not live service completion guarantees.

Presentation layout was rendered locally from the curated slide source and representative slides inspected; full canonical reference text was subsequently embedded into notes by the publication build. Automated bounds checks are not pixel-level assurance of every possible office renderer.

No live AWS workflow, credential provider, security test, memory-recall experiment or external destination publication was executed. No improvement, security coverage or saving is measured. The readiness-console application and its workflow are outside the documentation build and are checked for preservation.

Legacy HTML paths contain only navigation stubs to the canonical guides. They are not retained document editions. Git history holds prior content; no manual archives or ZIP distributions are generated.
