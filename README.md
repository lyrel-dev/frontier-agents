# Frontier agents — engineering field guides

Detailed, source-linked interactive reports and timed presentations. Download or clone the repository and open `index.html` in a browser. No server, build step or external JavaScript is needed to read the generated reports. GitHub file previews do not execute the report HTML; repository publication is not a GitHub Pages deployment.

| Guide | Interactive report | Presentation | Timing |
|---|---|---|---|
| AWS DevOps Agent | [Report](devops/validated-report.html) | [PowerPoint](presentations/aws-devops-agent-presentation.pptx) | 35 min / 12 min demo |
| Kiro | [Report](kiro/report.html) | [PowerPoint](presentations/kiro-presentation.pptx) | 32 min / 13 min demo |
| AWS Security Agent | [Report](security/report.html) | [PowerPoint](presentations/aws-security-agent-presentation.pptx) | 30 min / 8 min demo |
| AWS FinOps Agent | [Report](finops/report.html) | [PowerPoint](presentations/aws-finops-agent-presentation.pptx) | 27 min / 7 min demo |
| Common architectural patterns | [Report](architecture/common-patterns.html) | [PowerPoint](presentations/aws-frontier-agents-common-architecture-presentation.pptx) | 36 min / 8 min demo |

Each guide includes a six-step narrative, use-case scope, a detailed capability inventory, controls, examples, timed demos, readiness worksheet and official sources. The entire programme is 160 minutes including 48 minutes of demonstrations; questions and breaks are additional.

## Format and editorial standard

See [EDITORIAL_STANDARD.md](EDITORIAL_STANDARD.md) and [FORMAT_IMPLEMENTATION.md](FORMAT_IMPLEMENTATION.md). Every capability now has an untimed reference slide for detailed discussion; timing applies only to the core.

## Documents

- `*/report.md`: narrative and capability report in Markdown.
- `*/presentation-transcript.md`: speaker transcript, timing and demo runbooks.
- `presentations/`: five editable PowerPoint decks generated from the same slide source as the HTML presentations; one untimed evidence appendix per deck.
- `*/validation-record.md`: retained original capability audits, unchanged.
- `archive/2026-10-20/`: original HTML reports preserved for provenance.
- `content/`: versioned narrative, presentation and evidence source data.
- `demo-assets/`: product-neutral contract and explicitly synthetic cost fixture.
- `MANIFEST.json`, `VALIDATION.md`: file integrity and validation scope.

## Rebuild

```sh
python -m pip install beautifulsoup4==4.13.4 python-pptx==1.0.2
python tools/build_suite.py
python tools/build_suite.py --check
```

The documentation workflow builds and checks the suite and commits each generated file separately. Existing Git history and unrelated repository files are not replaced. The historical PowerPoint edition is superseded by the report-aligned, editable publication edition; it is not a byte-for-byte copy of the earlier image-led decks.

## Evidence boundary

Independent analysis, not an AWS publication. The original audits are 20 October 2026 snapshots; the presentation source and narrative revision are dated 21 October. Selected critical product boundaries were rechecked, not every source page. Examples and gates are recommendations. No live AWS account or agent workflow was exercised, and no productivity, diagnostic accuracy, security coverage or cost savings are claimed.

## Mechanisms and enablement

[Open the mechanism guide index](mechanisms/index.html), or read the [comparison](mechanisms/overview.md). Four platform guides contain 32 documented mechanism records, official enablement procedures, proposed checks and lifecycle controls. Five reference PowerPoints are untimed. Optional prepared-result exercises total 44 minutes, separate from the unchanged 160-minute core programme.

Build source: `content/mechanisms.json` and `tools/build_mechanisms.py`. See [mechanism validation](mechanisms/VALIDATION.md) for source qualifications and test boundaries.
