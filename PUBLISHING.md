# Publishing documentation

The six catalog JSON registers (use-cases, mechanisms, features, profiles, aliases, resource-models) are frozen at dace05a3ce6aaae02470a817584b8ca3a4cc95be. Do not change their definitions, identifiers, relationships, or use-case semantics during reader revisions.

Authored product prose lives in guides/*.md. Detailed mechanism blocks are generated from the frozen register. Chapter membership remains in tools/docs/structure.py; reader layout is in reader.py, reading.css, and reading.js; presentation content remains in presentation.py. Update rendered navigation without introducing another parallel guide or record-type index.

Run python tools/docs/build.py and python tools/docs/check.py --browser. The reading checks compare frozen records byte-for-byte and test complete task-to-procedure reading journeys. Trigger the existing workflow through documentation-build.json and publish only after validation.

Git retains previous versions. Do not create manual archives, migration copies, or forwarding editions. Preserve the independent application and its workflow. Repository publication does not deploy a website.
