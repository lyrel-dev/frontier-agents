# Draw.io model atlas

[model.drawio](model.drawio) is the editable eight-page source for every diagram in this package. It contains native Draw.io class shapes, attribute compartments, connector waypoints, cardinality labels and page links. Geometry and styling belong to this file; the schema owns entity and relationship text.

## Reading the model

The overview shows all **36 entities**, grouped by module, with each entity's own `version`. It deliberately shows selected associations. The seven detailed sheets collectively show **all 45 declared relationships**, using boundary proxies where the same entity is defined on another sheet. A proxy has a dashed outline and a link to its home sheet; it does not introduce another entity.

| Page | Purpose | SVG | PNG |
| --- | --- | --- | --- |
| 01 · Complete model | Every entity and module, with selected associations | [SVG](complete-model.svg) | [PNG](complete-model.png) |
| 02 · Scope and operator work | Workspace, access, resource identity, work and command ownership | [SVG](foundation.svg) | [PNG](foundation.png) |
| 03 · Collection, evidence and history | Collection, reads, stable Source identity, observations, projections and snapshots | [SVG](evidence.svg) | [PNG](evidence.png) |
| 04 · Workload catalogue | Systems, journeys, services, dependencies and resource links | [SVG](workload.svg) | [PNG](workload.png) |
| 05 · Health events and lifecycle | Event context, impacts, communication, deployments and lifecycle evidence | [SVG](health.svg) | [PNG](health.png) |
| 06 · Resilience context and findings | Service scope, policy capture, assessment and recommendations | [SVG](resilience.svg) | [PNG](resilience.png) |
| 07 · Investigation and execution | AgentSpace scope, observed membership, journal, approval and assets | [SVG](investigation.svg) | [PNG](investigation.png) |
| 08 · Published scenarios and execution | Scenario versions, admission, step lifecycle and separate provider effects | [SVG](workflow.svg) | [PNG](workflow.png) |

Every class uses the same `version`, `createdAt` and `updatedAt` contract. All entities other than Workspace also carry `workspaceId`. The diagrams show selected attributes; [the generated reference](../model/REFERENCE.md) contains every field. An exact historical input is an `EntityRef` value `{kind, id, version}`. The reference value has no independent entity lifecycle.

## Editing and regeneration

Open `model.drawio` in [Draw.io](https://app.diagrams.net/) or [Draw.io Desktop](https://github.com/jgraph/drawio-desktop). Each sheet has its own canvas and can be edited independently. Page links are available on classes and boundary proxies. Save the atlas after changing positions, waypoints or styling.

`tools/render_model.py` synchronizes schema-owned class text, relationship labels and cardinalities while preserving the Draw.io geometry. It also generates the complete entity reference. Adding an entity or relationship requires an intentional layout change; the check rejects incomplete coverage rather than adding it to an arbitrary automatic grid.

From `consolidated-operations-console/`:

```sh
python tools/render_model.py --check
```

This check is offline and reads committed artifacts. To regenerate, install the pinned JavaScript dependencies and Inkscape, then acquire the pinned official Draw.io source outside this repository:

```sh
npm ci --prefix tools --ignore-scripts
git clone --no-checkout --filter=blob:none --sparse https://github.com/jgraph/drawio.git /tmp/console-drawio-runtime
git -C /tmp/console-drawio-runtime sparse-checkout set src/main/webapp
git -C /tmp/console-drawio-runtime checkout c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3
DRAWIO_RUNTIME=/tmp/console-drawio-runtime python tools/render_model.py
```

For text-only schema synchronization before rendering:

```sh
python tools/render_model.py --sync-only
```

The SVG/PNG outputs and manifest remain stale until the full rendering command runs. For an existing dependency installation, `CONSOLE_DIAGRAM_NODE_MODULES` accepts module search paths separated by the platform path separator.

## Rendering and inspection evidence

The SVGs are produced by the official **Draw.io 32.6.10** `render` and `Graph.getSvg` implementation at the pinned source commit. [The runtime pin](../tools/drawio-runtime.json) records the executable source-file hashes. Its DOM environment uses JSDOM 26.1.0 and native canvas font metrics. Labels are plain SVG text, with explicit line breaks and fixed class geometry. Inkscape rasterizes the Draw.io SVGs to the PNG previews.

[manifest.json](manifest.json) ties the schema, atlas, reference, resolved geometry report, SVGs and PNGs together by hash. [render-report.json](render-report.json) records Draw.io's actual class bounds and routed connector points. It checks for overlapping classes, connectors crossing unrelated classes, relationship labels intruding into class boxes and class text exceeding its bounds. Deliberately overlapping and crossing fixtures verify the geometry checks. Every page also passes a native Draw.io codec round trip with entity and relationship metadata preserved. XML coverage is checked against the schema, including class version fields, endpoints and cardinalities.

All eight PNGs were inspected after rendering. Layout checks and image inspection establish this atlas's geometry and readability; they are separate from model semantics and from application runtime behavior. The file remains native editable Draw.io XML; no installed-desktop certification is implied.
