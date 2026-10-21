# Validation record

Source review date: 21 October 2026. Automated checks: **passed**.

## What was checked

The checker validates unique function identifiers, group membership, required description fields, separation of availability from activation, official-source hosts, reference resolution, procedure-to-function links and demonstration timing. It verifies the synthetic calculation independently. These checks do not prove that prose is factually correct; source review remains a separate editorial activity.

Generated local links and anchors are checked. Browser tests exercise report search, group and preview filters, disclosures, print-state restoration, mobile page width, slide navigation, notes and elapsed timers. Wide data tables can scroll horizontally within their containers; the page itself must fit the mobile viewport.

PowerPoint files are checked for shape bounds and populated speaker notes. Bounds checks do not detect every text overflow. Rendering and visual inspection, when performed, are recorded separately in `qa/visual-review.json`; absence of that record means no rendered-review claim is made.

See [qa/validation.json](qa/validation.json) for machine-readable results. No live AWS workflow, billing query, scan, resource mutation or memory-recall experiment was executed. No operational improvement is measured.

## Documentation limits

Each product report contains a source register and explicit documentation qualifications. Feature-specific current pages and dated change history take precedence over stale general summaries. The references are not a specification of hidden implementation details or universal assurances about account-specific behavior.

## Publication

The workflow checks before committing each changed file or deletion. It does not make manual historical copies or distribution archives. Previous revisions remain in Git history. Publication to the repository is not deployment to GitHub Pages.
