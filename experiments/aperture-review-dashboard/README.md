# Aperture review dashboard D1

An **experimental, offline review workspace** for Aperture Documentation Baseline C2, dated 21 October 2026. This branch's addition is independent of the three AWS agent guides currently maintained at the root of frontier-agents. It does not alter their scope, root manifest, build process or validation claims.

## Open the dashboard

Download or clone the branch and open [index.html](index.html) in a browser. The application includes all record data, styles and JavaScript inline. It requires **no backend, external asset, account or build step**. GitHub file previews do not execute HTML.

For a stable local origin, from this directory use `python -m http.server 8765 --bind 127.0.0.1` and open http://127.0.0.1:8765/. Keep it on loopback.

## Included files

- `index.html`: interactive review app with ten views, search, evidence drill-down, proposed decisions, local annotations and exports.
- `src/dashboard.js`, `src/shell.html`, `data/snapshot.json`: readable source, template and embedded C2-derived dataset.
- `documentation/`: current C2 handbook, operational review and unchanged full proposed-decision register.
- `evidence/validation-results.json`: the original D1 validation receipt, tied to the full D1 distribution and its stated testing limitations.
- `tools/`: reproducible offline build and source-integrity checks.

**Source-document coverage:** The full D1 distribution has hundreds of historical files from the C2 archive. This Git branch intentionally excludes those historical assets and does not commit distribution ZIP files, consistent with frontier-agents publishing policy. Some historical source links inside the dashboard therefore will not resolve in this branch. Their metadata and embedded record content remain searchable. Obtain the full C2 distribution separately to open every original source file. This branch is not a full C2 mirror.

## Rebuild and check

```sh
python tools/build_dashboard.py --check
python tools/check_dashboard.py
```

Running `python tools/build_dashboard.py` regenerates `index.html` from the tracked source and recomputes its inline-script CSP hash. Do not edit compiled source manually. The dashboard uses no external connections.

## Evidence boundary

The reports are dated documentation snapshots. R14 model execution remains synthetic and the restricted LiteLLM adapter is not integrated into Aperture authority. Metric and alarm definitions are proposed, not installed monitoring. Notes and review labels are unverified personal annotations, not production approvals or permissions.

Saving notes to browser storage is optional and unencrypted. Avoid secrets or sensitive incident data. This branch neither certifies production readiness nor reruns historical validation suites.
