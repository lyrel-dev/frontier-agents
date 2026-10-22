# Editorial and technical acceptance standard

The documentation distinguishes five layers:

1. **Product function** — a broad supported area such as incident response, penetration testing or cost inquiry.
2. **Platform capability** — a reusable ability exposed by the product.
3. **Operation** — an action on a named configuration, execution or evidence object.
4. **Mechanism** — the documented process that connects trigger, state, execution and output.
5. **Use case** — an engineering problem that applies functions, capabilities and mechanisms.

A use case must never be relabeled as a platform capability merely because it is common. The use-case catalog classifies every record as a built-in function, configured workflow, controlled action or team-composed procedure.

## Report structure

Each report follows this order:

- product functions and resource model;
- grouped and searchable day-to-day use cases;
- access, context and configuration;
- mechanisms and operations;
- worked evidence example;
- troubleshooting, limits and failure modes;
- coverage and source notes.

Use cases are grouped by operational family and contain inputs, reviewable output, cadence, availability, constraints, canonical sections and official sources. Duplicated use cases are consolidated; variations belong in fields or examples rather than additional records.

## Presentation structure

Presentation titles are descriptive book-style section headings, not slogans, promises or conclusions. Examples include **Incident Operations Use Cases**, **Memory, Instructions and Skills**, and **Finding Lineage, Remediation and Revalidation**.

The presentation sequence is:

- resource and function model;
- grouped use-case catalog;
- supporting configuration and mechanisms;
- operating lifecycle and controls;
- worked evidence exercise;
- troubleshooting and limits.

Every non-exercise slide must contain a complete mechanism flow, a comparison with at least three substantive items, or a table with enough rows to establish structure. Decorative title-only or takeaway-only slides are not accepted. A takeaway may summarize the slide, but it cannot substitute for content.

## Procedures and evidence

Every procedure states meaningful prerequisites, configuration decisions, expected confirmation and failure interpretation. Lifecycle instructions distinguish disable, cancel, soft delete, forget and permanent deletion where the product does. Steps and diagrams use as many elements as the subject requires.

Cite the official source near the product claim. Source registers identify reviewed topics and conflicts between retrieved page versions. Missing documented implementation details remain unknown. Synthetic examples identify invented inputs, supply enough evidence to support their conclusion and include a failure branch.

Use direct descriptive prose. Do not replace product explanation with generic cautions or speculative benefits. Present recommendations as engineering guidance, not native features.

Automated checks establish link, schema, fixture, browser, catalog and presentation-layout properties only. They cannot certify factual completeness, successful AWS setup, diagnostic correctness, security coverage or savings. Coverage maps state detailed, linked and deferred areas.

One canonical guide per platform. Globally unique section and use-case identifiers. Presentations and catalog records link to canonical sections. No manual archive directories or committed distribution packages; Git history is the version record.
