# AWS agents — engineering reference

This is a replacement of the earlier narrative-led collection, not a format patch. The current scope is AWS DevOps Agent, AWS Security Agent and AWS FinOps Agent.

Open `index.html` after cloning the repository. The reports and browser presentations are self-contained and require no server. GitHub previews display source; this is not a GitHub Pages deployment.

| Product | Total allocation | Demo included | Reference | Editable deck |
|---|---|---|---|---|
| AWS DevOps Agent | [35:00 presentation](devops/presentation.html) | 8:00 | [Report](devops/validated-report.html) | [PowerPoint](presentations/aws-devops-agent-presentation.pptx) |
| AWS Security Agent | [33:30 presentation](security/presentation.html) | 10:00 | [Report](security/report.html) | [PowerPoint](presentations/aws-security-agent-presentation.pptx) |
| AWS FinOps Agent | [31:30 presentation](finops/presentation.html) | 8:00 | [Report](finops/report.html) | [PowerPoint](presentations/aws-finops-agent-presentation.pptx) |

## Structure

`reference/` holds the canonical product descriptions and teaching material. Each product directory contains a grouped function reference, configuration mechanisms, proposed procedures, browser presentation and Markdown transcript. `comparison.html` compares concrete product boundaries; it does not invent a common agent runtime.

The function catalogue is organized by product responsibility. Setup mechanisms are not counted as capabilities, and operational examples are not presented as executed results. Each material product assertion links to an official source; proposed checks, synthetic arithmetic and documentation qualifications are labeled separately. See [METHOD.md](METHOD.md).

## Build and validate

```sh
python -m pip install python-pptx==1.0.2 beautifulsoup4==4.13.4 playwright==1.57.0
python -m playwright install chromium
python tools/build_reference.py
python tools/check_reference.py
```

The publication workflow validates before committing each changed file or deletion separately. Earlier revisions remain in Git history. No archive directory, distribution ZIP, encoded import package or historical copy is generated.

## Evidence boundary

Source review: 21 October 2026. Documents can change after that date. The references state what the official pages document, not an independently observed service implementation. No live product execution or measured accuracy, security coverage, cost saving or productivity benefit is claimed. Browser and presentation checks are recorded in [VALIDATION.md](VALIDATION.md); they do not establish factual or operational correctness.
