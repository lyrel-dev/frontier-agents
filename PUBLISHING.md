# Publishing documentation

Edit guide prose in `guides/*.md`, use-case narratives in `catalog/use-cases.json`, chapter membership in `tools/docs/structure.py`, slide content in `tools/docs/presentation.py`, and figures in `tools/docs/diagrams.py`.

Run `python tools/docs/build.py` and `python tools/docs/check.py --browser`. Inspect rendered prose, diagrams, and slides as well as the recorded checks. Trigger the documentation workflow through `documentation-build.json`; generated documentation changes are committed separately on the checked-out branch. Promote a tested branch without overwriting intervening changes.

Do not maintain compressed distributions, historical copies, old forwarding pages, or alternate renderers. Git is the revision history. Preserve `applications/` and its workflow. Repository publication is not website hosting.
