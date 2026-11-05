---
id: fis-revised-package-checks
title: Revised package checks
type: validation-guide
service: aws-fis
status: maintained
version: "1.0"
created: "2026-11-05"
updated: "2026-11-05"
tags: [aws, fis, validation, obsidian]
aliases: [FIS revised package validation tools]
related: [../README.md, ../VALIDATION.md, ../docs/README.md]
---

# Revised package checks

The package checker validates the maintained files without rewriting them. It checks YAML headers and unique note IDs, local Markdown and property links, all eight diagram notes and their sources, embedded diagram parity, SVG XML/title/description structure, the official FIS source register, literal HTML assets, the documentation inventory and import hashes, and the preserved initial interface's hashes.

From the repository root, with Node.js, Python 3.10 or later, `PyYAML` and `jsonschema` available. The latter validates the suggested UI's recorded operation DTOs; the browser application has no runtime dependencies.

```bash
python3 aws/fis/analysis/revised/tools/check_package.py
node --test aws/fis/analysis/revised/initial/app/tests/model.test.cjs
node --test aws/fis/analysis/revised/suggested/app/tests/model.test.cjs
```

The checker does not claim that Obsidian itself, a browser, AWS or an API server was exercised. [VALIDATION.md](../VALIDATION.md) records the actual validation scope and results. The initial source manifest fixes the reviewed baseline and explicitly identifies the two files with adapted navigation URLs.
