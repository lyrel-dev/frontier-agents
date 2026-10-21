# Publishing and rebuilding

Only current source and generated documents are tracked. Git history is the version record. Do not create snapshot directories, compressed import payloads, or committed distribution ZIP files. Clone the repository and open index.html locally. Repository publication is not a Pages deployment.

```sh
python tools/assemble_content.py
python tools/build_suite.py
python tools/build_suite.py --check
python tools/editorial_lint.py
python tools/validate_scope.py
```

Update documentation-build.json to request publication. Changed documents and deletions are committed individually. Repository visibility is unchanged.
