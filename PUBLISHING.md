# Publication

Edit canonical Markdown and the curated lesson plan. Rebuild and validate before changing `documentation-build.json` to request a publication run. The workflow renders the guides and slides, runs the documented checks, and commits each changed document or deletion separately. It does not create ZIP distributions or snapshot directories.

The documentation-owned paths are isolated from `applications/` and `.github/workflows/validation-console.yml`. Review the final Git diff and preservation check. No force push or history rewrite is part of publication.
