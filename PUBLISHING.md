# Publishing this revision

This package contains the complete 21 October 2026 editorial-format revision. It does not change the GitHub repository until a user with write access publishes it.

To update `lyrel-dev/frontier-agents` while retaining one changed document per Git commit:

```bash
git clone git@github.com:lyrel-dev/frontier-agents.git
unzip -o aws-frontier-agents-format-standardized.zip -d frontier-agents
cd frontier-agents
python -m pip install beautifulsoup4==4.13.4 python-pptx==1.0.2
python tools/assemble_content.py
python tools/build_suite.py
python tools/build_suite.py --check
python tools/editorial_lint.py
python tools/build_suite.py --commit
git push origin main
```

`tools/build_suite.py --commit` creates a separate commit for each changed document; it does not run without an explicit invocation. The existing GitHub Actions workflow will also run after the `documentation-build.json` change reaches `main`. Review results and source claims before distributing externally. It does not change repository visibility or configure Pages hosting.

Validation does not include live AWS executions, external-source revalidation or measured business outcomes. `qa/editorial-lint.json` and `qa/editorial-interaction-validation.json` record format checks and interactive controls.
