# Publishing documentation

Edit the canonical guide, chapter map or lesson plan, rebuild, then run `python tools/docs_check.py --browser`. Review the generated HTML before committing. The documentation workflow is triggered by `documentation-build.json`; it validates before committing each changed documentation file separately.

The report and presentation are both HTML. No compressed distributions or retained historical document copies are produced. Git holds prior revisions. The separate application and its workflow must remain unchanged. Repository publication is not website hosting.
