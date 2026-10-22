# Repository integration

The release candidate is isolated at `applications/aws-validation-console/agent_lab/` on branch `feat/devops-agent-response-lab`, based on main commit `7ed9843ed35f6c78214dd2853df497b670a49995`. The legacy 0.2.1 workbench and unrelated repository content are unchanged. This is source publication, not a deployed service or a live AWS acceptance result.

The original README's final source-integration paragraph describes the earlier standalone delivery. It is historical context; this repository copy is committed. The original distribution manifest and screenshots are not retained as repository source.

From this directory, install `requirements.txt` and run `python build_assets.py` to reproduce the five schemas, the 12-panel Grafana JSON, and the empty offline preview. Generated assets need not be tracked. Runtime application startup needs none of the generated preview/report files.

`validation/review.json` preserves the previous delivery's measured counts and source hashes; it is not a claim that live AWS acceptance ran. Repository CI separately reruns the Python, native-browser and real-loopback worker checks without AWS credentials. AWS interactions in these tests are explicitly test doubles or botocore Stubber responses.

Next target: real two-account acceptance, beginning with read-only preflight. Configuration, approved targets and local AWS profiles must be supplied on the operator's host. A successful read does not authorize a write, demonstrate fault efficacy, or prove incident response. No branch merge or AWS operation is implicit in this publication.
