# Reading-structure review

## Defects addressed

The previous primary navigation exposed internal record categories rather than reading tasks. Each product guide embedded another complete catalog with a second search, and configuration and mechanism details required navigation through separate indexes. The presentation index repeated the entire home page.

## Reader paths

The home page introduces the cross-service overview and the three product books. A book starts with its overview chapter, offers chapter navigation and a single search, and links to relevant use cases without repeating the full catalog. The use-case directory contains grouped summaries and search; each selected case includes its workflow, applicable configuration, completion criteria and direct technical references. The resource model remains a technical dictionary. Presentations retain their slide content and timings and have their own index.

## Frozen scope

No definitions, cases, variants, dependency semantics, profiles, source claims or relationship multiplicities were changed. All six JSON registers are compared byte-for-byte with dace05a3ce6aaae02470a817584b8ca3a4cc95be. Historical identifiers remain lookup metadata; retired HTML index pages are removed, not archived. Internal references are rewritten. External bookmarks to removed index URLs are not maintained as duplicate editions.

## Validation

See reading-structure.json for chapter/search/deep-link/print tests, all 30 use-case pages, and a complete task-to-configuration-to-procedure navigation test. Existing source, relationship, entity and presentation checks remain. Browser checks are not a live AWS test or a claim of prose quality.
