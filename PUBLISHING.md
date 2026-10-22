# Publishing documentation

Edit guide prose outside the delimited generated blocks in `guides/*.md`; edit detailed mechanism prose and its claim references in the `review` fields of `catalog/mechanisms.json`. The build synchronizes those blocks before rendering. Edit cases in `catalog/use-cases.json`, mechanism and feature relationships in `catalog/mechanisms.json` and `catalog/features.json`, recipes in `catalog/profiles.json`, product entities and relationships in `catalog/resource-models.json`, chapter membership in `tools/docs/structure.py`, slide content in `tools/docs/presentation.py`, and figures in `tools/docs/diagrams.py`.

Run `python tools/docs/build.py` and `python tools/docs/check.py --browser`. Inspect rendered prose, diagrams, and slides as well as the recorded checks. Trigger the documentation workflow through `documentation-build.json`; generated documentation changes are committed separately on the checked-out branch. Promote a tested branch without overwriting intervening changes.

Do not maintain compressed distributions, historical copies, old forwarding pages, or alternate renderers. Git is the revision history. Preserve `applications/` and its workflow. Repository publication is not website hosting.
