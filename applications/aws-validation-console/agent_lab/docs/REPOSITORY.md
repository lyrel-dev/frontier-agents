# Repository integration

Application path: `applications/aws-validation-console/agent_lab/`.
Baseline: `b9dc53939611cc32904b49e2447dbb7fd5e2ab35`.
Target branch: `feat/aws-fis-console-acceptance`.

Only this application and its matching GitHub Actions workflow are in scope.
Other documentation and `main` remain untouched. Generated previews, schemas,
reports, screenshots and dashboard JSON belong in CI/distribution artifacts, not
source-control snapshots. Local configuration, credentials and AWS evidence must
not be committed. A successful branch CI run is software acceptance, not the live
response/prevention acceptance described in DELIVERY_ACCEPTANCE.md.
