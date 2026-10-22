# Repository delivery

Repository: `lyrel-dev/frontier-agents`. Delivery branch: `feat/aws-fis-console-delivery`. Source changes are restricted to `applications/aws-validation-console/agent_lab/` and its CI workflow. The source baseline is `b9dc53939611cc32904b49e2447dbb7fd5e2ab35`. Neither `main` nor the earlier benchmark branch is changed.

The previously local 0.5.0 increment is included along with the 0.5.1 publication fixes. Commit and CI identifiers must be checked against GitHub; a local source build is not evidence of remote publication. Generated previews, schemas and dashboard JSON are rebuilt from source. No account configuration, credential, experiment measurement, distribution archive or runtime database is committed.

Repository CI performs credential-free software, native browser, local-worker, Docker and monitoring-server checks. No workflow receives AWS credentials or performs an incident test in a customer account. Live acceptance remains a separate authorized workflow.
