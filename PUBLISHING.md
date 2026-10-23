# Publishing documentation

Edit canonical Markdown under `content/`. YAML front matter identifies each document, section, slide, diagram, or approved record. The compiler regenerates the existing HTML routes and supporting projections. Do not edit generated HTML, SVG, assembled guide Markdown, or catalog JSON.

## Approved records

The entity model and use cases are frozen. Their Markdown representation reconstructs the approved JSON values without changing identities, relationships, objectives, workflow conditions, or completion criteria. Preservation tests continue to compare these projections against the approved revision. Neither a review comment nor a model-produced patch authorizes a change to frozen records.

## Validation and publication

Run `python tools/docs/build.py`, `python tools/docs/check.py --browser`, and `python tools/docs/review_check.py`. Inspect the generated documents and any source diff. Verify a second build produces identical content outputs and leaves all `content/` files unchanged. Publish only after the checks complete successfully. The source-editing and review contracts are documented in [AUTHORING.md](AUTHORING.md).

The documentation workflow builds the branch being changed. Generated files are committed separately. Do not change the independent application or its workflow. Repository publication is not deployment of a hosted website.

## History and private review data

Use Git history for previous versions; do not create manual archives or replacement editions. Review exports contain the reviewer's comments and selected source excerpts. Keep them local unless their publication has been explicitly reviewed. Exporting or copying an LLM request does not send it to a provider automatically.
