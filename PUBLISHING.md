# Publishing and rebuilding

The editorial-format revision was published through the successful [approved editorial import](https://github.com/lyrel-dev/frontier-agents/actions/runs/39575904010). The mechanism extension is generated from `content/mechanisms.json`; verify its publication by the latest successful documentation workflow and the presence of `mechanisms/index.html` on `main`.

Repository visibility is preserved. Repository storage is not a GitHub Pages deployment. The source and generated files are committed one changed document per commit; unrelated history is retained.

## Rebuild

```sh
python tools/assemble_content.py
python tools/build_suite.py
python tools/build_suite.py --check
python tools/editorial_lint.py
```

The existing documentation workflow runs when `documentation-build.json` is updated. Workflow permissions and definitions are not changed by the mechanism extension. The build checks references, local links and core timing; browser and rendered-slide checks are recorded separately. No live AWS execution or measured benefit is claimed.
