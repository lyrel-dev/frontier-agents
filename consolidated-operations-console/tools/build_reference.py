#!/usr/bin/env python3
"""Build the offline HTML model/API reference from the reviewed repository contracts.

The two reference/*-notes.json files hold editorial use cases and source history.
Schemas, examples, relationships, mappings and operation metadata are read directly.
No network access or third-party Python dependency is required to build or check.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKAGE = "consolidated-operations-console/"
REPO_URL = "https://github.com/lyrel-dev/frontier-agents"
BASELINE = "31980a1b7540b1ad74274b0edfc7fc1f08f6a396"
SOURCE_COMMIT = "d926a81c584b6b69f41bfb9641532c4f8f2d7cb3"
V1_COMMIT = "db142c84bcfd691d5c71071681731cac81a52c7b"
OUTPUT = ROOT / "reference.html"
REPORT = ROOT / "reference/build-report.json"
MODULES = {
    "foundation": ("Foundation", "Shared identity, access, evidence, history, operator work and durable command intent."),
    "workload": ("Workload", "Systems, journeys, services and dependency context."),
    "health": ("Health", "Provider events, scoped impact, communications and lifecycle exposure."),
    "resilience": ("Resilience", "Policy context, assessments, findings and recommendations."),
    "investigation": ("Investigation", "Agent spaces, tasks, executions, journals, approvals and assets."),
    "workflow": ("Workflow", "Scenario authoring, publication, admitted runs and execution history."),
    "fis": ("FIS", "Observed fault-injection experiments and the explicit stop command."),
}


def read_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


MODEL = read_json("model/schema.json")
RPC = read_json("api/rpc.schema.json")
CATALOG = read_json("api/operations.json")
ADAPTERS = read_json("model/adapter-profiles.json")
MODEL_EXAMPLES = read_json("model/examples.json")
API_EXAMPLES = read_json("api/examples.json")
DIAGRAMS = read_json("diagrams/manifest.json")
INVENTORY = read_json("inventory.json")
ENTITY_NAMES = [name for name, schema in MODEL["$defs"].items() if schema.get("x-entity")]
OPERATIONS = {op["name"]: op for op in CATALOG["operations"]}
EXAMPLES = {example["operation"]: example for example in API_EXAMPLES["examples"]}
MODEL_VALUES = [name for name in MODEL["$defs"] if name not in ENTITY_NAMES]
RPC_VALUES = [name for name in RPC["$defs"] if not name.endswith(("Request", "Response"))]
ENTITY_NOTES = {}
OPERATION_NOTES = {}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def code(value) -> str:
    return f"<code>{esc(value)}</code>"


def prose(value) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, list):
        return "".join(prose(item) for item in value)
    if isinstance(value, dict):
        return "".join(f"<p><strong>{esc(k)}.</strong> {esc(v)}</p>" for k, v in value.items())
    return "".join(f"<p>{esc(paragraph)}</p>" for paragraph in str(value).split("\n\n") if paragraph.strip())


def bullet(items) -> str:
    if not items:
        return ""
    if isinstance(items, str):
        return prose(items)
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def raw_json(value) -> str:
    return "<pre><code>" + esc(json.dumps(value, indent=2, ensure_ascii=False)) + "</code></pre>"


def disclosure(title, body, *, css="", opened=False, ident="") -> str:
    attrs = (f' class="{esc(css)}"' if css else "") + (" open" if opened else "")
    attrs += f' id="{esc(ident)}"' if ident else ""
    return f"<details{attrs}><summary>{esc(title)}</summary><div class=\"detail-body\">{body}</div></details>"


def anchor(kind, name, label=None) -> str:
    return f'<a href="#{esc(kind)}-{esc(name)}">{esc(label or name)}</a>'


def source_link(path, commit=BASELINE, label=None, heading=None, source_anchor=None, directory=False) -> str:
    path = str(path).lstrip("./")
    fragment = source_anchor
    if not fragment and heading:
        fragment = re.sub(r"[^\w\- ]", "", str(heading).lower()).replace(" ", "-")
    url = f"{REPO_URL}/{'tree' if directory else 'blob'}/{commit}/{quote(path, safe='/@')}"
    if fragment:
        url += "#" + quote(str(fragment).lstrip("#"), safe="-_")
    return f'<a class="source-link" href="{esc(url)}">{esc(label or path)}</a>'


def canonical_source(path, label=None) -> str:
    return source_link(PACKAGE + path, label=label)


def table(headers, rows, css="") -> str:
    if not rows:
        return ""
    return (f'<div class="table-wrap"><table class="{esc(css)}"><thead><tr>'
            + "".join(f"<th scope=\"col\">{esc(header)}</th>" for header in headers)
            + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
            + "</tbody></table></div>")


def metadata(rows) -> str:
    return '<dl class="metadata">' + "".join(f"<dt>{esc(k)}</dt><dd>{v}</dd>" for k, v in rows if v) + "</dl>"


def ref_target(ref, context):
    name = ref.rsplit("/", 1)[-1]
    if "model.json#" in ref or context == "model":
        collection = "model"
    else:
        collection = "rpc"
    if collection == "model" and name in ENTITY_NAMES:
        return f"entity-{name}", name
    return f"value-{collection}-{name}", name


def type_html(schema, context="model") -> str:
    if isinstance(schema, bool):
        return "Any JSON value" if schema else "No valid value"
    if "$ref" in schema:
        target, name = ref_target(schema["$ref"], context)
        rendered = f'<a href="#{esc(target)}"><code>{esc(name)}</code></a>'
        restrictions = []
        for field_name, field in schema.get("properties", {}).items():
            if "const" in field:
                restrictions.append(f"{code(field_name)} = {code(json.dumps(field['const']))}")
            elif "enum" in field:
                restrictions.append(f"{code(field_name)} ∈ " + " / ".join(code(json.dumps(value)) for value in field["enum"]))
        if restrictions:
            rendered += " (" + "; ".join(restrictions) + ")"
        return rendered
    if "const" in schema:
        return code(json.dumps(schema["const"], ensure_ascii=False))
    if "enum" in schema:
        return " · ".join(code(json.dumps(v, ensure_ascii=False)) for v in schema["enum"])
    for union, label in [("oneOf", "One of"), ("anyOf", "Any of")]:
        if union in schema:
            return f'<span class="bound">{label}:</span> ' + " | ".join(type_html(x, context) for x in schema[union])
    if "allOf" in schema:
        refs = [part for part in schema["allOf"] if "$ref" in part]
        constants = [(name, spec["const"]) for part in schema["allOf"]
                     for name, spec in part.get("properties", {}).items() if "const" in spec]
        rendered = " &amp; ".join(type_html(part, context) for part in refs)
        if constants:
            rendered += " " + "; ".join(f"{code(name)} = {code(json.dumps(value))}" for name, value in constants)
        if rendered:
            return rendered
    typ = schema.get("type", "object" if "properties" in schema else "JSON value")
    if isinstance(typ, list):
        return " | ".join(code(t) for t in typ)
    if typ == "array":
        return "Array of " + type_html(schema.get("items", {}), context)
    if typ == "object" and isinstance(schema.get("additionalProperties"), dict) and not schema.get("properties"):
        return "Map&lt;string, " + type_html(schema["additionalProperties"], context) + "&gt;"
    if "properties" in schema:
        return "Object { " + ", ".join(code(k) for k in schema["properties"]) + " }"
    return code(typ)


def constraint_lines(schema):
    if not isinstance(schema, dict):
        return []
    out = []
    names = {
        "minLength": "Minimum length", "maxLength": "Maximum length",
        "minimum": "Minimum", "maximum": "Maximum", "exclusiveMinimum": "Exclusive minimum",
        "exclusiveMaximum": "Exclusive maximum", "multipleOf": "Multiple of",
        "minItems": "Minimum items", "maxItems": "Maximum items",
        "minProperties": "Minimum properties", "maxProperties": "Maximum properties",
        "format": "Format", "pattern": "Pattern", "uniqueItems": "Unique items",
    }
    for key, label in names.items():
        if key in schema:
            out.append(f"{label}: {code(schema[key])}")
    if schema.get("additionalProperties") is False:
        out.append("Unknown properties are rejected.")
    if "propertyNames" in schema:
        out.append("Map keys: " + "; ".join(constraint_lines(schema["propertyNames"])))
    if "items" in schema:
        nested = constraint_lines(schema["items"])
        if nested:
            out.append("Each item: " + "; ".join(nested))
    for union in ("anyOf", "oneOf"):
        for part in schema.get(union, []):
            out += constraint_lines(part)
    return list(dict.fromkeys(out))


COMMON_FIELDS = {
    "workspaceId": "Trusted application scope. Request bodies cannot select a tenant.",
    "version": "Immutable representation number. In a getter request, omission selects the current head once.",
    "createdAt": "Local creation time of the logical entity; constant across its entity versions.",
    "updatedAt": "Local publication time of this entity representation; nondecreasing across versions.",
    "expectedVersion": "Optimistic precondition on the named entity head; never a nested value's own clock.",
    "clientToken": "Opaque mutation-intent token. Exact replay requires the same operation, payload and preconditions.",
    "maxResults": "Requested page bound; default 20, maximum 100. A response may contain fewer rows.",
    "nextToken": "Opaque continuation for the same fixed traversal and query. Absence ends traversal.",
    "page": "Publication metadata for the selected traversal; it is not a domain Snapshot.",
    "clearFields": "Explicitly clears listed nullable local fields. A field cannot be assigned and cleared together.",
    "selectedObservation": "Exact observation selected for this representation; historical reads do not retarget it.",
    "command": "Durable intent receipt. An accepted external command is not proof of provider completion.",
    "items": "The operation's typed result collection. Parent/version and ordering semantics are specified below.",
    "profile": "Registered profile selecting the source or interpretation contract for this record.",
    "profileVersion": "Version of the registered profile/schema; separate from the containing entity's version.",
    "sourceOperation": "Named source operation retained with the representation; it participates in Source identity.",
    "contentDigest": "Digest of the retained content under the declared digest profile; digest equality alone does not establish entity identity.",
    "providerUpdatedAt": "Provider-reported update time, when available; separate from local publication and observation time.",
    "providerVersion": "Native provider version, when available; it does not replace the entity version.",
    "fieldPresence": "Explicit presence information preserving omission, null, unknown, unavailable and known values.",
    "payload": "Retained source JSON. Its known fields are validated by the registered profile; it is not a patch to canonical state.",
    "payloadStorage": "Selects inline JSON or a managed artifact. INLINE may contain legitimate JSON null; ARTIFACT requires its artifact reference.",
    "digestProfile": "Declared algorithm/canonicalization used to compute the content digest.",
    "inputRefs": "Exact retained inputs used by this interpretation; later input versions do not change this representation.",
    "observedAt": "Time the evidence was observed; distinct from provider event/update time and local entity publication.",
    "generatedAt": "Time the derived result was generated; recomputation does not make its input evidence newer.",
    "capturedAt": "Capture cutoff used to interpret the retained historical context.",
}


def fields_table(schema, context, subject="") -> str:
    props = schema.get("properties", {})
    if not props:
        if schema.get("type") == "object" and schema.get("additionalProperties") is False:
            return "<p>This object has no members. Send <code>{}</code> for an empty request.</p>"
        return "<p>Value type: " + type_html(schema, context) + ".</p>" + bullet_plain_html(constraint_lines(schema))
    rows = []
    for name, field in props.items():
        required = name in schema.get("required", [])
        desc = field.get("description", "")
        if not desc:
            own_id = subject[0].lower() + subject[1:] + "Id" if subject else ""
            # Publication metadata such as Page.createdAt is not entity creation metadata.
            if subject in ENTITY_NAMES and name == own_id:
                desc = f"Stable logical identity of this {subject}; the entity version selects a retained representation."
            elif subject in ENTITY_NAMES and name == "version":
                desc = "Positive server-assigned version of this immutable entity representation."
            elif name in ("createdAt", "updatedAt") and subject not in ENTITY_NAMES:
                desc = "Timestamp with the meaning assigned by this containing value."
            elif subject.endswith("Response") and name == "version":
                desc = "The actual selected entity representation version."
            else:
                desc = COMMON_FIELDS.get(name, "")
        bounds = constraint_lines(field)
        description = (f"<p>{esc(desc)}</p>" if desc else "")
        description += "<br>".join(f'<span class="bound">{text}</span>' for text in bounds)
        if not description:
            description = '<span class="bound">Uses the declared type and containing contract.</span>'
        req = '<span class="required">Required</span>' if required else '<span class="optional">Optional</span>'
        rows.append([f'<code class="field-name">{esc(name)}</code>', req, type_html(field, context), description])
    result = table(["Field", "Presence", "Type / allowed values", "Meaning and constraints"], rows, "fields")
    if schema.get("additionalProperties") is False:
        result += '<p class="source-note">Closed object: undeclared members are rejected by this schema. Required means present; a permitted null remains a value.</p>'
    inline = []
    for name, field in props.items():
        child = field.get("items", field)
        if isinstance(child, dict) and "properties" in child and "$ref" not in child:
            suffix = "[]" if "items" in field else ""
            inline.append(f"<h5>{esc(name + suffix)}</h5>" + fields_table(child, context, subject + "." + name))
    if inline:
        result += disclosure("Inline owned structures", "".join(inline))
    structural = {k: schema[k] for k in ["allOf", "oneOf", "anyOf", "if", "then", "else", "dependentRequired", "dependentSchemas", "not"] if k in schema}
    if structural:
        result += disclosure("Conditional and cross-field schema rules", raw_json(structural), css="schema-rules")
    return result


def bullet_plain_html(items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>" if items else ""


def schema_details(schema, ident=""):
    return disclosure("Full JSON Schema definition", raw_json(schema), css="raw-schema", ident=ident)


def entity_use_cases(notes):
    rendered = []
    for case in notes.get("useCases", []):
        if isinstance(case, str):
            rendered.append('<div class="use-case">' + prose(case) + "</div>")
            continue
        body = f"<h5>{esc(case.get('title', 'Use case'))}</h5>"
        for key, label in [("scenario", "Context"), ("howEntityIsUsed", "Use"), ("outcome", "Result")]:
            if case.get(key):
                body += f'<p><span class="label">{label}.</span> {esc(case[key])}</p>'
        rendered.append('<div class="use-case">' + body + "</div>")
    return "".join(rendered)


def relationship_rows(entity=None):
    rows = []
    for index, rel in enumerate(MODEL["x-relationships"]):
        if entity and entity not in (rel["from"], rel["to"]):
            continue
        rows.append([
            anchor("entity", rel["from"]), code(rel["fromCardinality"]), esc(rel["label"]),
            code(rel["toCardinality"]), anchor("entity", rel["to"]),
        ])
    return table(["Entity A", "A end", "Relationship", "B end", "Entity B"], rows)


def mapping_table(mappings):
    rows = []
    for mapping in mappings:
        source = source_link(mapping["sourcePath"], SOURCE_COMMIT)
        targets = ", ".join(anchor("entity", n) for n in mapping.get("canonicalEntities", [])) or "No new entity"
        profile = mapping.get("profileId")
        if profile:
            targets += "<br>" + anchor("profile", profile)
        rows.append([
            "<strong>" + esc(mapping["sourceService"]) + "</strong><br>" + "<br>".join(code(n) for n in mapping["sourceConcepts"]),
            code(mapping["disposition"]) + "<br>" + esc(mapping["representation"]) + "<br>" + targets,
            esc(mapping["preservedSemantics"]) + "<p>" + source + "</p>",
        ])
    return table(["Earlier package / concept", "Consolidated representation", "Preserved meaning / source"], rows)


def historical_origins(notes):
    parts = []
    for origin in notes.get("historicalOrigins", []):
        title = ", ".join(origin.get("sourceConcepts", [])) or origin.get("kind", "Earlier definition")
        body = f"<h5>{esc(title)}</h5>"
        if origin.get("kind"):
            body += f'<p class="source-note">Origin type: {esc(origin["kind"])}.</p>'
        if origin.get("previousUse"):
            body += "<p><strong>Previous use.</strong> " + esc(origin["previousUse"]) + "</p>"
        if origin.get("consolidation"):
            body += "<p><strong>Consolidation decision.</strong> " + esc(origin["consolidation"]) + "</p>"
        if origin.get("sourcePath"):
            commit = origin.get("sourceCommit") or (BASELINE if origin["sourcePath"].startswith(PACKAGE) else SOURCE_COMMIT)
            body += "<p>" + source_link(origin["sourcePath"], commit, heading=origin.get("heading"), source_anchor=origin.get("anchor")) + "</p>"
        parts.append('<div class="provenance">' + body + "</div>")
    return "".join(parts)


def select_entity_example(name, notes):
    rows = MODEL_EXAMPLES["records"][name]
    field = name[0].lower() + name[1:] + "Id"
    selector = notes.get("preferredExample", notes.get("example", {}))
    if isinstance(selector, dict) and selector.get("id"):
        match = [row for row in rows if row[field] == selector["id"] and row["version"] == selector.get("version", row["version"])]
        if match:
            return match[-1]
    if name == "Scenario":
        return next(row for row in rows if row["state"] == "PUBLISHED")
    if name == "Source":
        match = [row for row in rows if row[field] == "src-health-impact"]
        if match:
            return max(match, key=lambda row: row["version"])
    return max(rows, key=lambda row: row["version"])


def card_header(kind, name, module, badges):
    return (f'<div class="card-heading"><div><p class="eyebrow">{esc(MODULES[module][0])} · {esc(kind)}</p>'
            f'<h3>{esc(name)}</h3></div><a class="permalink" href="#{esc(kind)}-{esc(name)}" aria-label="Link to {esc(name)}">#</a></div>'
            + '<div class="badges">' + "".join(f'<span class="badge">{esc(badge)}</span>' for badge in badges) + "</div>")


def search_terms(value):
    if isinstance(value, dict):
        return " ".join(str(k) + " " + search_terms(v) for k, v in value.items())
    if isinstance(value, list):
        return " ".join(search_terms(v) for v in value)
    return str(value)


def entity_card(name):
    schema = MODEL["$defs"][name]
    notes = ENTITY_NOTES[name]
    module = schema["x-module"]
    mappings = [m for m in ADAPTERS["mappings"] if name in m.get("canonicalEntities", [])]
    profiles = [p for p in ADAPTERS["profiles"] if name in p.get("canonicalEntities", [])]
    ops = CATALOG["entityCoverage"][name]
    terms = search_terms([name, module, notes, list(schema["properties"]), mappings])
    body = card_header("entity", name, module, ["Versioned entity", schema["x-writeAuthority"], f"{len(schema['properties'])} fields"])
    body += prose(notes["purpose"])
    body += metadata([
        ("Logical identity", code(schema["x-identity"])),
        ("Retained record", code(schema["x-recordIdentity"])),
        ("Logical key", " + ".join(code(x) for x in schema.get("x-logicalKey", []))),
        ("Owner / authority", esc(notes.get("ownership", schema["x-owner"]))),
        ("Lifecycle", esc(notes.get("lifecycle", schema["x-sealingRule"]))),
        ("Sealing rule", esc(schema["x-sealingRule"])),
        ("Field authorities", "; ".join(f"{code(k)}: {code(v)}" for k, v in schema.get("x-fieldAuthorities", {}).items())),
        ("Authoritative contract", canonical_source("model/schema.json", f"model/schema.json · {name}")),
    ])
    if schema["x-writeAuthority"] == "MIXED":
        body += '<p class="notice">Field authority is partitioned, but the containing entity has one version. Owned governance or enrichment values have no independent version counter.</p>'
    body += "<h4>Use cases</h4>" + entity_use_cases(notes)
    body += "<h4>Fields</h4>" + fields_table(schema, "model", name)
    if notes.get("invariants"):
        body += "<h4>Invariants and interpretation</h4>" + bullet(notes["invariants"])
    rels = relationship_rows(name)
    if rels:
        body += "<h4>Relationships</h4><p class=\"source-note\">Multiplicity is shown at each class-diagram end. Exact references and live identities remain distinct in the field definitions.</p>" + rels
    body += "<h4>Where it was defined and how it was used</h4>" + historical_origins(notes)
    if mappings:
        body += disclosure(f"Source crosswalk · {len(mappings)} mapping rows", mapping_table(mappings))
    else:
        body += '<p class="source-note">This shared entity is introduced by consolidation. Its origin notes identify the earlier concerns it unifies; it is not presented as a native AWS resource.</p>'
    if profiles:
        body += "<p><strong>Related source profiles.</strong> " + "; ".join(anchor("profile", p["profileId"]) for p in profiles) + ".</p>"
    body += "<h4>API operations</h4><div class=\"link-list\">" + "".join(anchor("operation", n) for n in ops) + "</div>"
    example = select_entity_example(name, notes)
    field = name[0].lower() + name[1:] + "Id"
    body += disclosure(f"Synthetic entity example · {example[field]} · version {example['version']}",
                       '<p class="source-note">Copied from the checked model fixtures. This is a selected representation, which may be historical.</p>' + raw_json(example), css="entity-example")
    history = [row for row in MODEL_EXAMPLES["records"][name] if row[field] == example[field]]
    if len(history) > 1:
        body += disclosure("Version history for this fixture identity", table(["Version", "State / interpretation", "Published at (epoch seconds)"], [
            [code(row["version"]), esc(row.get("state", "Immutable retained representation")), code(row["updatedAt"])]
            for row in sorted(history, key=lambda row: row["version"])
        ]))
    body += schema_details(schema)
    return f'<article class="reference-card" id="entity-{esc(name)}" data-kind="entity" data-name="{esc(name)}" data-module="{esc(module)}" data-search="{esc(terms)}">{body}</article>'


def predecessor_source(mapping):
    package = mapping["sourcePackage"]
    if "@" in package:
        path, commit = package.rsplit("@", 1)
    else:
        path, commit = package, SOURCE_COMMIT
    # Link to the real earlier package rather than guessing an operation-heading anchor.
    return source_link(path, commit, label=package, directory=True)


def predecessor_table(mappings):
    return table(["Earlier operation / package", "Disposition", "Current operations / meaning"], [
        [code(m["sourceOperation"]) + "<br>" + predecessor_source(m), code(m["disposition"]),
         ", ".join(anchor("operation", n) for n in m["newOperations"]) + "<p>" + esc(m["notes"]) + "</p>"]
        for m in mappings
    ])


def operation_case(notes):
    case = notes["useCase"]
    body = f'<h5>{esc(case.get("title", "Use case"))}</h5>'
    for key, label in [("actor", "Actor"), ("scenario", "Context"), ("whenToUse", "When to use"), ("intendedResult", "Intended result")]:
        if case.get(key):
            body += f'<p><span class="label">{label}.</span> {esc(case[key])}</p>'
    if case.get("steps"):
        body += "<ol>" + "".join(f"<li>{esc(step)}</li>" for step in case["steps"]) + "</ol>"
    return '<div class="use-case">' + body + "</div>"


def operation_card(name):
    op = OPERATIONS[name]
    notes = OPERATION_NOTES[name]
    example = EXAMPLES[name]
    request = RPC["$defs"][name + "Request"]
    response = RPC["$defs"][name + "Response"]
    predecessors = [m for m in CATALOG["predecessorMappings"] if name in m["newOperations"]]
    terms = search_terms([op, notes, list(request.get("properties", {})), list(response.get("properties", {})), predecessors])
    body = card_header("operation", name, op["module"], [op["kind"], op["maturity"], op["deliveryPhase"]])
    body += prose(notes["purpose"])
    body += metadata([
        ("Wire target", code("POST /") + "<br>" + code("X-Amz-Target: " + op["target"])),
        ("Media type", code(CATALOG["transport"]["contentType"])),
        ("Permission", code(op["permission"]) + " · proposed application capability"),
        ("Entity scope", ", ".join(anchor("entity", entity) for entity in op["entities"])),
        ("Scope members", ", ".join(code(field) for field in op.get("scopeFields", [])) or "Trusted workspace / operation context"),
        ("Effect", "Mutating intent; a durable Command receipt is returned." if op["mutating"] else "Read-only selection of retained data; no implicit fresh provider collection."),
        ("Provider dispatch", ", ".join(code(n) for n in op["nativeOperations"]) + " · adapter target, not a wire-compatible console alias" if op["nativeOperations"] else "No direct native dispatch declared by this operation."),
        ("Contract source", canonical_source("api/operations.json", "Operation metadata") + " · " + canonical_source("api/rpc.schema.json", "Request / response schemas")),
    ])
    body += "<h4>Use case</h4>" + operation_case(notes)
    if notes.get("preconditions"):
        body += "<h4>Preconditions</h4>" + bullet(notes["preconditions"])
    body += f'<h4 id="request-{esc(name)}">Request · {esc(name)}Request</h4>' + fields_table(request, "rpc", name + "Request")
    body += f'<h4 id="response-{esc(name)}">Response · {esc(name)}Response</h4>' + fields_table(response, "rpc", name + "Response")
    body += "<h4>Operation semantics</h4>" + bullet(op["semantics"])
    if notes.get("pitfalls"):
        body += "<h4>Interpretation and recovery</h4>" + bullet(notes["pitfalls"])
    body += "<p><strong>Declared errors.</strong> " + ", ".join(anchor("error", n) for n in op["errors"]) + ".</p>"
    body += '<p class="source-note">Transport rejection also uses the shared size and media-type errors. The <a href="#errors">error reference</a> describes HTTP status, retryability and recovery.</p>'
    if example.get("preconditions"):
        body += disclosure("Example admission preconditions", raw_json(example["preconditions"]))
    request_wire = "POST / HTTP/1.1\nHost: console.example.invalid\nContent-Type: application/x-amz-json-1.1\nX-Amz-Target: " + op["target"] + "\n\n" + json.dumps(example["request"], indent=2, ensure_ascii=False)
    body += disclosure("Synthetic request example", "<pre><code>" + esc(request_wire) + "</code></pre>", css="request-example")
    body += disclosure("Synthetic response example · HTTP 200", raw_json(example["response"]), css="response-example")
    body += "<h4>Earlier operations and consolidation</h4>" + prose(notes.get("historicalInterpretation"))
    if predecessors:
        body += predecessor_table(predecessors)
    else:
        body += '<p class="source-note">No predecessor facade operation is recorded for this operation. It is introduced in the current consolidated contract; native operations, if any, are listed separately above.</p>'
    next_ops = notes.get("nextSteps", [])
    if next_ops:
        body += "<p><strong>Related next operations.</strong> " + ", ".join(anchor("operation", n) for n in next_ops) + ".</p>"
    if notes.get("nextStep"):
        body += prose(notes["nextStep"])
    body += disclosure("Full request and response JSON Schemas", "<h5>Request</h5>" + raw_json(request) + "<h5>Response</h5>" + raw_json(response), css="raw-schema")
    return f'<article class="reference-card" id="operation-{esc(name)}" data-kind="operation" data-name="{esc(name)}" data-module="{esc(op["module"])}" data-search="{esc(terms)}">{body}</article>'


def chapter(ident, number, title, body, intro=""):
    return f'<section class="chapter" id="{ident}"><p class="eyebrow">{esc(number)}</p><h2>{esc(title)}</h2>' + (f'<p class="chapter-intro">{esc(intro)}</p>' if intro else "") + body + "</section>"


def overview():
    counts = Counter(MODEL["$defs"][name]["x-module"] for name in ENTITY_NAMES)
    op_counts = Counter(op["module"] for op in OPERATIONS.values())
    rows = [[anchor("entity-module", module, title), code(counts[module]), code(op_counts[module]), esc(desc)] for module, (title, desc) in MODULES.items()]
    principles = [
        ("One entity, one version contract", "Every entity carries version, createdAt and updatedAt. A material change appends the next immutable representation of the same identity. Owned values share their owner's version; no Version or Revision resource is introduced."),
        ("Exact history, explicit live navigation", "EntityRef pins kind, id and version. EntityIdentity intentionally follows a continuing identity. Historical reads never substitute current content, and current authorization still applies."),
        ("Evidence has a clear owner", "Source retains a scoped native representation. Observation records seeing it. Projection records a versioned interpretation with exact inputs and coverage. Snapshot closes a historical capture over exact entity versions."),
        ("Operations express intent", "Closed request DTOs expose deliberate edits or commands. Server metadata, provider state and derived conclusions are not arbitrary writable fields. Provider dispatch, observed effects and local operator work retain separate meanings."),
    ]
    body = ('<p>The application brings workload, Health, resilience, investigation and fault-injection work into one workspace. '
            'The first phase establishes a common model and operation contract before implementing persistence, collectors, authorization, command dispatch, orchestration or a console UI.</p>'
            '<p>This reference describes contract revision 2, based on main at ' + source_link(PACKAGE + "README.md", BASELINE, BASELINE[:7]) +
            '. It incorporates the explicit correction that all entities are versioned and all diagrams use Draw.io. '
            'The previous AWS analyses remain pinned independently to ' + source_link("aws", SOURCE_COMMIT, SOURCE_COMMIT[:7], directory=True) + '.</p>')
    body += '<div class="principles">' + "".join('<div class="principle"><h3>' + esc(title) + "</h3><p>" + esc(text) + "</p></div>" for title, text in principles) + "</div>"
    body += table(["Module", "Entities", "Operations", "Responsibility"], rows)
    body += '<div class="notice"><strong>Contract and examples, not a running service.</strong><p>All 108 operations are marked CONTRACT_ONLY. Examples are synthetic, independently valid situations with their own prior-head assumptions; they are not one chronological transaction log and no provider call was made to produce this document.</p></div>'
    body += '<p>Source-backed design guidance is recorded in ' + canonical_source("DESIGN_PRINCIPLES.md", "Design principles") + '. This document uses repository evidence and the user’s explicit correction; it does not claim knowledge of inaccessible past conversations.</p>'
    body += '<p><strong>Consolidation path.</strong> Review the unified model and exact contracts first; implement retained reads and trusted ingestion (P2), durable commands and replay (P3), then workflow execution and its effect-reconciliation gates (P4). The application shell composes those verified capabilities. ' + canonical_source("CONSOLIDATION_PLAN.md", "Implementation gates and acceptance evidence") + '.</p>'
    return chapter("context", "01 · Context", "A modular, consolidated model", body)


def protocol():
    rows = [
        ("Transport", "POST /; application/x-amz-json-1.1; PascalCase operation names and lowerCamelCase JSON members."),
        ("Target", "X-Amz-Target: " + CATALOG["namespace"] + ".<Operation>"),
        ("Success", "HTTP 200 with the operation-specific output. For an asynchronous command, this means admission or receipt replay, not provider completion."),
        ("Scope", "Workspace and actor come from trusted authenticated context. Parent IDs and Connection references select scoped objects; they confer no authority."),
        ("Versions", "Get<Entity>(version?) selects an exact immutable representation when supplied, or the current head once when omitted. ListEntityVersions returns exact references in descending version order."),
        ("Concurrency", "expectedVersion guards the named entity, including owned values. Provider commands also require exact source context where declared. A conflict admits no new mutation."),
        ("Replay", "Every mutation requires a clientToken. Same scoped operation/token with identical intent replays its exact receipt before current-head checks. Changed intent with the same token conflicts."),
        ("Lists", "maxResults is 1–100, default 20. Tokens bind the initial 15-minute publication, principal, query and selected parents. An empty page alone does not end traversal."),
        ("Bounds", "Request body ≤ 1 MiB, response budget ≤ 8 MiB, plus each schema's field and collection bounds. Large content uses managed artifact references."),
        ("Time", "Finite epoch seconds, maximum millisecond precision. Local publication, provider update, observation, derivation and capture times remain distinct."),
        ("Presence", "Omitted, null, known empty, known zero, unavailable and not requested retain distinct meanings. clearFields is an explicit local clearing operation."),
        ("Compatibility", "V2 is an explicit breaking correction of the proposed V1 contract. Reused operation names do not imply wire compatibility."),
    ]
    body = table(["Concern", "Shared rule"], [[esc(k), esc(v)] for k, v in rows])
    body += '<p>Authentication, authorization enforcement and SDK compatibility remain implementation work. The selector/media-type pattern is an AWS RPC style facade; catalog permissions are proposed console capabilities, not AWS IAM action names. ' + canonical_source("api/PROTOCOL.md", "Complete protocol and its primary references") + '.</p>'
    body += "<h3>Write authority and effect</h3>" + table(["Category", "Meaning"], [[code(k), esc(v)] for k, v in [
        ("READ", "Read retained records, exact history or a documented current selector."),
        ("LOCAL_COMMAND", "Change application-owned state or create a capture/publication and durable receipt."),
        ("INGEST", "Record collector-owned collection, source and observation facts."),
        ("DERIVE", "Compute a projection from exact authorized inputs and trusted rule identity."),
        ("PROVIDER_COMMAND", "Admit a narrow external intent; dispatch and reconciliation establish later outcomes."),
        ("EXECUTION_COMMAND", "Admit or cancel an application Run; execution, acceptance and cleanup remain separate."),
    ]])
    body += "<h3>Reference and ownership rules</h3>" + table(["Value", "Use"], [
        [anchor("value-model", "EntityRef"), "Exact kind/id/version for retained evidence, command results, admission bindings and snapshot members."],
        [anchor("value-model", "EntityIdentity"), "Explicit live navigation or a continuing WorkItem target; never substitute it for a historical pin."],
        [anchor("value-model", "EvidenceRef"), "Exact Source, Observation, Projection or Snapshot reference, optionally with a typed locator."],
        ["Owned value", "No independent identity, version counter or CRUD endpoint. A change is a change to the containing entity."],
    ])
    body += '<p>Versioning does not create write access. Collector and workflow entities advance under their authority; sealed facts retain immutable history. A Source A → B → A content sequence publishes versions 1 → 2 → 3, while an unchanged consecutive poll may reuse the current Source version in a new Observation. A Run pins one PUBLISHED Scenario representation even when the current Scenario head is a later draft.</p>'
    body += '<p>Snapshot members close over declared exact references. Structural parent identities do not silently pull current parent fields into history. Access to any historical evidence closure is re-authorized at read time.</p>'
    return chapter("protocol", "02 · Shared contract", "How the model and API behave", body)


CROSS_CASES = [
    {
        "title": "Build the workload catalog without implying a provider edit",
        "context": "A platform owner registers a checkout system and its customer journey, then attaches a service to those local catalog identities.",
        "entities": ["System", "UserJourney", "Service", "Resource", "Command"],
        "operations": ["CreateSystem", "CreateUserJourney", "CreateService", "UpdateService", "GetCommand"],
        "steps": ["Create the System and UserJourney with separate intent tokens; use returned canonical IDs.", "Create the Service with its owned membership set. Read before editing and guard the Service head with expectedVersion.", "Use the durable receipt and exact returned versions. A catalog edit does not rename or create a native AWS service."],
        "outcome": "One local catalog writer owns service membership, while verified provider bindings preserve the distinction between application and native identities.",
    },
    {
        "title": "Explain whether a Health impact is current, stale or unsupported",
        "context": "An operator needs a qualified impact view for a service after receiving an account-scoped Health event.",
        "entities": ["HealthEvent", "EventContext", "EntityImpact", "Collection", "ReadAttempt", "Source", "Observation", "Projection"],
        "operations": ["StartCollection", "RecordReadAttempt", "IngestObservation", "CompleteCollection", "ListHealthEvents", "ListEventContexts", "ListEntityImpacts", "GetServiceStatus", "GetSource"],
        "steps": ["The trusted collector starts a fixed collection and records read-attempt settlement and observed source evidence.", "Complete the collection with independent pagination, detail, identity and claim-coverage dimensions; a quiet or empty response is not enough to establish absence.", "Navigate event → context → impacts, then inspect the service-status projection and its exact inputs. Preserve account/public/organization context instead of multiplying one event by delivery count."],
        "outcome": "The operator can trace a displayed impact to its native evidence and see what the collection actually established.",
    },
    {
        "title": "Investigate a resilience finding and record remediation work",
        "context": "An assessment reveals a service-scoped finding; the operator needs the recommendation context and a separately owned work lifecycle.",
        "entities": ["Service", "ResilienceAssessment", "Finding", "Recommendation", "Snapshot", "WorkItem", "Command"],
        "operations": ["StartResilienceAssessment", "GetCommand", "ListResilienceAssessments", "ListFindings", "ListRecommendations", "GetSnapshot", "UpdateRecommendationEnrichment", "CreateWorkItem", "RecordWorkItemVerification"],
        "steps": ["Admit an assessment against the exact service/source context, then reconcile Command and collected assessment evidence.", "Read the finding under its Service parent and inspect recommendation and captured assessment context. Add estimates through Recommendation enrichment using the Recommendation version.", "Create a WorkItem for assignment and completion. Record verification with exact supporting evidence; technical assessment completion or local closure alone does not prove remediation."],
        "outcome": "Assessment posture, recommendation metadata and operator work state remain independently intelligible.",
    },
    {
        "title": "Decide an investigation approval and resume deliberately",
        "context": "A DevOps execution pauses on a specific tool approval request while its task memberships and journal continue to be observed.",
        "entities": ["AgentSpace", "Investigation", "Execution", "JournalRecord", "ApprovalRequest", "Command"],
        "operations": ["StartInvestigation", "ListInvestigations", "ListExecutions", "ListJournalRecords", "GetApprovalRequest", "DecideApproval", "GetCommand", "ResumeExecution"],
        "steps": ["Start the investigation in the selected AgentSpace and obtain its observed task/execution context from retained reads.", "Inspect the exact ApprovalRequest, source and action digest. Submit a deliberate decision with the relevant head and source preconditions.", "Resume only with the exact definitive successful decision Command version and matching approval context. Reconcile uncertain decision or resume effects instead of blindly resending."],
        "outcome": "Approval intent, provider decision, resume and actual tool effects retain separate evidence and authority.",
    },
    {
        "title": "Publish a scenario, run that version and inspect exact attempts",
        "context": "A reliability engineer authors a workflow that performs an experiment and evaluates explicit criteria.",
        "entities": ["Scenario", "Run", "StepRun", "StepAttempt", "Snapshot", "Experiment", "Projection"],
        "operations": ["CreateScenario", "UpdateScenario", "PublishScenario", "StartRun", "GetRun", "ListRunSteps", "ListStepAttempts", "GetExperiment", "GetProjection"],
        "steps": ["Edit a draft under Scenario.expectedVersion and publish it to resolve trusted operation/schema locks.", "Admit a Run with the exact PUBLISHED Scenario, subject and Connection versions. Inspect the atomic Run, Snapshot and StepRun response.", "Read children through the selected parent version. Preserve skipped zero-attempt steps and the admitted required-criterion denominator when interpreting evaluation."],
        "outcome": "Later scenario edits, child transitions or evaluator knowledge cannot silently change the historical admitted run.",
    },
    {
        "title": "Cancel a run while an external experiment may still be active",
        "context": "An operator requests cancellation during execution and needs to distinguish the local fence from remote cessation and cleanup.",
        "entities": ["Run", "StepRun", "StepAttempt", "Experiment", "Command"],
        "operations": ["RequestRunCancellation", "GetCommand", "GetRun", "ListRunSteps", "ListStepAttempts", "StopExperiment", "GetExperiment"],
        "steps": ["Request cancellation against the Run head with a stable intent token. Replay the original receipt before considering a new intent.", "Inspect exact attempts and known external-effect references. Use the explicit StopExperiment contract only when authorized and its target/source preconditions are established.", "Observe terminal native state and required finalization independently. Non-creating reconciliation handles uncertain effects; cancellation cannot reissue a creating Start merely to discover a lost handle."],
        "outcome": "A cancellation request remains visible without being mistaken for completed remote cleanup or proven recovery.",
    },
    {
        "title": "Reconstruct a past decision after the current state changes",
        "context": "An auditor wants the service, source and interpretation used for an earlier operational decision.",
        "entities": ["Service", "Source", "Observation", "Projection", "Snapshot", "WorkItem"],
        "operations": ["CaptureSnapshot", "GetSnapshot", "ListEntityVersions", "GetService", "GetSource", "GetObservation", "GetProjection", "GetWorkItem"],
        "steps": ["Capture a closed set of exact authorized members and their declared evidence closure at the chosen cutoff.", "Retrieve the Snapshot and resolve exact references through the normal typed getters, or enumerate an entity's history before selecting a specific version.", "Recheck current authority. Unknown or unavailable versions remain explicit outcomes; a getter never substitutes the current head for missing history."],
        "outcome": "The historical explanation remains tied to the representations available at the decision, with unavailable evidence made visible.",
    },
]


def use_case_chapter():
    body = '<p>These illustrative journeys combine the declared operations. They describe the intended application behavior; provider dispatch and runtime guarantees still require the implementation gates above.</p>'
    for index, case in enumerate(CROSS_CASES, 1):
        body += f'<section class="use-case" id="use-case-{index}"><h3>{index:02d} · {esc(case["title"])}</h3>' + prose(case["context"])
        body += "<p><strong>Entities.</strong> " + ", ".join(anchor("entity", n) for n in case["entities"]) + ".</p>"
        body += "<ol>" + "".join(f"<li>{esc(step)}</li>" for step in case["steps"]) + "</ol>"
        body += "<p><strong>Operations.</strong> " + ", ".join(anchor("operation", n) for n in case["operations"]) + ".</p>"
        body += "<p><strong>Result.</strong> " + esc(case["outcome"]) + "</p></section>"
    return chapter("use-cases", "03 · Use cases", "Follow the work across modules", body)


def diagrams():
    parts = ['<p>These eight diagrams are embedded from the reviewed Draw.io exports. The editable source is ' + canonical_source("diagrams/model.drawio", "model.drawio") + '. The overview contains all 36 entities; the focused pages collectively cover all 45 declared relationships. Class boxes select fields for legibility; the entity reference below contains every field.</p>']
    for diagram in DIAGRAMS["diagrams"]:
        ident = diagram["id"]
        svg = (ROOT / diagram["svg"]["path"]).read_text(encoding="utf-8")
        # Prefix SVG IDs before inlining multiple independently rendered Draw.io pages.
        ids = set(re.findall(r'(?<![\w:-])id="([^"]+)"', svg))
        for old in sorted(ids, key=len, reverse=True):
            new = "svg-" + ident + "-" + old
            svg = re.sub(r'(?<![\w:-])id="' + re.escape(old) + '"', f'id="{new}"', svg)
            svg = svg.replace(f'url(#{old})', f'url(#{new})').replace(f'href="#{old}"', f'href="#{new}"')
        def replace_aria(match):
            return 'aria-labelledby="' + " ".join("svg-" + ident + "-" + token if token in ids else token for token in match.group(1).split()) + '"'
        svg = re.sub(r'aria-labelledby="([^"]+)"', replace_aria, svg)
        if re.search(r"<script|<foreignObject|onload=|<image", svg, re.I):
            raise ValueError(f"Unexpected active/external diagram content: {ident}")
        diagram_body = ('<div class="diagram-toolbar"><button type="button" class="button" data-diagram-zoom="frame-' + ident + '" aria-pressed="false">View at full size</button>'
                        '<p>' + canonical_source(diagram["svg"]["path"], "Original SVG") + ' · ' + canonical_source("diagrams/model.drawio", "Editable Draw.io atlas") + '</p></div>'
                        '<div class="diagram-frame" id="frame-' + ident + '">' + svg + '</div>'
                        '<p class="diagram-caption">' + esc(diagram["title"]) + ' · ' + str(len(diagram["entities"])) + ' entity appearances · '
                        + str(len(diagram["relationshipIds"])) + ' relationships on this page. Horizontal scrolling preserves detail on small screens.</p>')
        parts.append(disclosure(diagram["title"], diagram_body, css="diagram", opened=ident == "complete-model", ident="diagram-" + ident))
    return chapter("diagrams", "04 · Draw.io atlas", "Read the model visually", "".join(parts))


def filters():
    options = '<option value="all">All modules</option>' + "".join(f'<option value="{key}">{esc(title)}</option>' for key, (title, _) in MODULES.items())
    return ('<section class="chapter" id="catalog-search"><p class="eyebrow">Reference navigator</p><h2>Find an entity or operation</h2>'
            '<p>Search names, fields, earlier concepts, source packages and use-case terms. Filters apply to the two catalogs; shared rules, diagrams and appendices remain available.</p>'
            '<div class="filters"><div class="filter-controls"><label for="reference-search">Search the reference<input id="reference-search" type="search" placeholder="Try expectedVersion, approval, or Health" autocomplete="off"></label>'
            '<label for="module-filter">Module<select id="module-filter">' + options + '</select></label>'
            '<label for="kind-filter">Entry type<select id="kind-filter"><option value="all">All entries</option><option value="entity">Entities</option><option value="operation">Operations</option></select></label>'
            '<button type="button" class="button" id="reset-filters">Clear filters</button></div><p id="result-count" role="status" aria-live="polite"></p><div class="search-results" id="search-results" hidden></div></div>'
            '<noscript><p>JavaScript is disabled. All entries remain visible; use the contents or your browser’s Find command.</p></noscript></section>')


def catalog_chapter(kind):
    entity = kind == "entity"
    title = "Every entity" if entity else "Every API operation"
    intro = ("36 stable entity identities with a common version contract. Field tables include required presence, nullable shapes, enums and declared bounds; shared values are linked to the appendix."
             if entity else "108 operation contracts: 74 reads and 34 mutations. Each entry includes its purpose, use case, wire target, scope, request and response fields, semantics, examples, errors and predecessor mapping.")
    body = ''
    for module, (label, desc) in MODULES.items():
        names = [n for n in ENTITY_NAMES if MODEL["$defs"][n]["x-module"] == module] if entity else [n for n, op in OPERATIONS.items() if op["module"] == module]
        body += f'<section class="module-group" id="{kind}-module-{module}"><header class="module-heading"><h3>{esc(label)} · {len(names)} {"entities" if entity else "operations"}</h3><p>{esc(desc)}</p></header>'
        body += "".join(entity_card(name) if entity else operation_card(name) for name in names) + '</section>'
    return chapter("entities" if entity else "operations", "05 · Entity catalog" if entity else "06 · Operation catalog", title, body, intro)


def value_types():
    body = '<p>These are owned value types and transport structures, not additional entities or independent version resources. An owned value changes only through its entity owner. The full-schema disclosures preserve conditional clauses and composition exactly.</p>'
    for context, names, definitions, label in [("model", MODEL_VALUES, MODEL["$defs"], "Model values"), ("rpc", RPC_VALUES, RPC["$defs"], "RPC values")]:
        body += '<h3>' + label + ' · ' + str(len(names)) + '</h3><div class="section-links">' + "".join(anchor("value-" + context, name) for name in names) + '</div>'
        for name in names:
            schema = definitions[name]
            body += f'<section class="value-card" id="value-{context}-{esc(name)}" data-value-name="{esc(name)}" data-value-context="{context}"><h3>{esc(name)}</h3>'
            body += prose(schema.get("description", "")) + fields_table(schema, context, name) + schema_details(schema) + '</section>'
    body += '<h3>Projection profiles</h3><p>The Projection.value contract selects the corresponding owned result shape for its registered profile.</p>'
    body += table(["Profile", "Result value type"], [[code(profile), anchor("value-model", value)] for profile, value in MODEL["x-projectionProfiles"].items()])
    return chapter("values", "07 · Type appendix", "Shared values and nested structures", body)


ERROR_RECOVERY = {
    "ValidationException": "Correct the fields, union, precision or reference scope before retrying.",
    "UnauthenticatedException": "Establish a current verified caller identity.",
    "AccessDeniedException": "Restore valid current authority if appropriate; denial is not an empty result.",
    "ResourceNotFoundException": "Verify the exact visible identity/version and required parents. Do not substitute a current head.",
    "VersionConflictException": "Read and review the changed head. A deliberate new intent requires a new token and chosen precondition.",
    "IdempotencyConflictException": "Keep the original payload for replay, or use a new token for a genuinely new intent.",
    "CommandInProgressException": "Inspect the returned command; retry the identical token and payload after the supplied delay.",
    "InvalidStateException": "Reconcile the relevant state, source context, bindings and invariants before a deliberate new intent.",
    "PaginationTokenExpiredException": "Explicitly restart traversal; do not merge a new publication into an expired one.",
    "EvidenceUnavailableException": "Surface the retention/unavailability outcome; do not infer absence, success or a fallback version.",
    "RequestTooLargeException": "Reduce the body or use the declared managed artifact path; obey both byte and collection bounds.",
    "UnsupportedMediaTypeException": "Use application/x-amz-json-1.1.",
    "ThrottlingException": "Honor retryAfterSeconds with bounded backoff and retain the same mutation intent token.",
    "InternalServerException": "Reconcile the durable receipt; a missing response does not establish that no effect occurred.",
    "ServiceUnavailableException": "Retry the exact intent within its replay guarantee; reconcile uncertain effects first.",
}


def error_chapter():
    body = '<p>Clients parse the typed exception, stable code and structured field paths. Human messages are explanatory. A retryable console error does not authorize reissuing an uncertain provider mutation; Command state and adapter reconciliation govern that decision.</p>'
    rows = []
    for name, error in CATALOG["errors"].items():
        rows.append([f'<span id="error-{name}">{code(name)}</span>', code(error["status"]), "Yes" if error["retryable"] else "No", esc(error["description"]), esc(ERROR_RECOVERY[name])])
    body += table(["Exception", "HTTP", "Retryable", "Meaning", "Recovery"], rows)
    body += '<p>Error body fields are specified by ' + anchor("value-rpc", "RpcError") + ' and ' + anchor("value-rpc", "FieldViolation") + '.</p>'
    for example in API_EXAMPLES["errors"]:
        body += disclosure(example["name"] + " · " + example["operation"] + " · HTTP " + str(example["status"]), raw_json(example["response"]))
    return chapter("errors", "08 · Error reference", "Recover without changing the intent accidentally", body)


def profile_chapter():
    body = '<p>The 65 registered profiles preserve native identity, payload fields, read operations and unknown provider output. A profile is a typed adapter contract, not automatically a new CRUD entity. Its listed native operations describe provider coverage; only the operation catalog above defines the console facade.</p>'
    for profile in ADAPTERS["profiles"]:
        ident = profile["profileId"]
        body += f'<section class="profile-card" id="profile-{esc(ident)}" data-profile-id="{esc(ident)}"><h3>{code(ident)}</h3>'
        body += prose(profile["family"])
        body += metadata([
            ("Prior package", esc(profile["sourceService"]) + " · " + source_link(profile["sourcePath"], SOURCE_COMMIT)),
            ("Disposition", code(profile["disposition"])),
            ("Canonical entities", ", ".join(anchor("entity", n) for n in profile.get("canonicalEntities", [])) or "No new first-class entity"),
            ("Source shapes", ", ".join(code(n) for n in profile.get("sourceShapes", []))),
            ("Identity basis", esc(profile.get("identityBasis", ""))),
            ("Native reads", ", ".join(code(n) for n in profile.get("readOperations", [])) or "None declared"),
            ("Deferred mutations", ", ".join(code(n) for n in profile.get("deferredNativeMutations", [])) or "None declared"),
        ])
        if profile.get("mutationDeferralReason"):
            body += prose(profile["mutationDeferralReason"])
        if profile.get("notes"):
            body += prose(profile["notes"])
        if profile.get("observedFields"):
            body += table(["Observed native field", "Recorded source type"], [[code(k), code(v) if not isinstance(v, dict) else raw_json(v)] for k, v in profile["observedFields"].items()])
        body += '<p class="source-note">Unknown native fields: ' + ("retained" if profile.get("preserveUnknownFields") else "see profile") + '. Unknown provider values: ' + ("retained" if profile.get("preserveUnknownProviderValues") else "see profile") + '.</p>'
        if profile.get("sourceBinding") or profile.get("normalizedBinding"):
            body += disclosure("Source and normalized bindings", raw_json({k: profile[k] for k in ["sourceBinding", "normalizedBinding"] if k in profile}))
        body += '</section>'
    return chapter("profiles", "09 · Adapter profiles", "Keep the native source inspectable", body)


def lineage_chapter():
    body = '<p>History is linked to exact repository commits. “Introduced by consolidation” identifies an application abstraction, not a previously existing AWS resource. Names retained as aliases are crosswalk evidence, not additional current entities.</p>'
    packages = [
        ("DevOps Agent", "aws/devops-agent/analysis/README.md", "58 files", "Tasks, executions, journal evidence, observed membership, approvals and investigation UI contracts."),
        ("FIS and general workflow", "aws/fis/analysis/README.md", "55 files", "Native experiments, targets/actions/reports, plus generalized scenario/run/step/attempt and adapter contracts."),
        ("Health", "aws/health/analysis/README.md", "26 files", "Event/context/impact, communication, delivery, lifecycle catalog, exposure and local work."),
        ("Resilience Hub", "aws/resilience-hub/analysis/README.md", "87 files", "System/journey/service structure, dependency topology, assessment context, findings, recommendations and the earlier 44-operation facade."),
    ]
    body += table(["Earlier analysis", "Frozen inventory", "Contribution"], [[source_link(path, SOURCE_COMMIT, name), esc(count), esc(desc)] for name, path, count, desc in packages])
    body += '<p>The frozen inventory contains 226 active files across the four service directories, with generalized workflow and resilience RPC work nested inside them. ' + canonical_source("INVENTORY.md", "Complete previous-work inventory") + ' · ' + canonical_source("inventory.json", "Paths, sizes, hashes and history") + '.</p>'
    body += '<h3>Every source-concept mapping</h3><p>All 174 mapping rows and 340 recorded aliases are retained here, including owned values, projections and deferred native breadth.</p>'
    body += disclosure("Complete concept crosswalk · 174 rows", mapping_table(ADAPTERS["mappings"]))
    body += '<h3>Every predecessor operation</h3><p>The 161 dispositions cover 44 earlier Resilience operations, 16 generalized workflow operations, and all 101 V1 consolidated operations. The source packages include both RPC and earlier HTTP bindings; those bindings are not silently treated as the current transport.</p>'
    body += disclosure("Complete operation predecessor crosswalk · 161 rows", predecessor_table(CATALOG["predecessorMappings"]))
    body += '<h3>All declared entity relationships</h3>' + relationship_rows()
    sources = [
        ("Current model, identity and versioning", "model/schema.json"),
        ("Model explanations and invariants", "MODEL.md"),
        ("Typed RPC input/output contract", "api/rpc.schema.json"),
        ("Operation metadata and predecessor mappings", "api/operations.json"),
        ("Protocol, concurrency, replay and coverage", "api/PROTOCOL.md"),
        ("Historical concept mappings and adapter profiles", "model/adapter-profiles.json"),
        ("Synthetic entity representations", "model/examples.json"),
        ("Synthetic operation examples", "api/examples.json"),
        ("Editable diagrams and reviewed export manifest", "diagrams/model.drawio"),
        ("Review findings and correction decisions", "REVIEW.md"),
        ("Validation evidence and runtime limits", "VALIDATION.md"),
    ]
    body += '<h3>Canonical source register</h3><ol class="source-register">' + "".join('<li>' + canonical_source(path, label) + ' — ' + code(path) + '</li>' for label, path in sources) + '</ol>'
    body += '<p>The HTML is generated from those checked contracts and the editorial notes in ' + code('reference/entity-notes.json') + ' and ' + code('reference/operation-notes.json') + '. It intentionally preserves the source baseline while adding a complete navigable explanation. Generation inputs and coverage checks are recorded in ' + code('reference/build-report.json') + '.</p>'
    return chapter("lineage", "10 · Provenance", "Trace the model back to the earlier work", body)


NAV = [
    ("context", "Context and scope"), ("protocol", "Shared model/API rules"),
    ("use-cases", "Cross-module use cases"), ("diagrams", "Draw.io diagrams"),
    ("catalog-search", "Find an entry"), ("entities", "All 36 entities"),
    ("operations", "All 108 operations"), ("values", "Shared value types"),
    ("errors", "Errors and recovery"), ("profiles", "Adapter profiles"),
    ("lineage", "Earlier work and sources"),
]


def navigation():
    main = "".join(f'<a href="#{ident}">{esc(label)}</a>' for ident, label in NAV)
    modules = ''
    for module, (label, _) in MODULES.items():
        entities = [name for name in ENTITY_NAMES if MODEL["$defs"][name]["x-module"] == module]
        operations = [name for name, op in OPERATIONS.items() if op["module"] == module]
        links = '<p class="nav-label">Entities</p><ul>' + "".join('<li>' + anchor("entity", name) + '</li>' for name in entities) + '</ul>'
        links += '<p class="nav-label">Operations</p><ul>' + "".join('<li>' + anchor("operation", name) + '</li>' for name in operations) + '</ul>'
        modules += '<details><summary>' + esc(label) + '</summary>' + links + '</details>'
    return ('<aside class="sidebar"><a class="brand" href="#top">Consolidated<br>Operations Console</a><span class="edition">MODEL &amp; API REFERENCE<br>Contract revision 2 · 5 November 2026</span>'
            '<nav aria-label="Document contents">' + main + '<div class="nav-group">' + modules + '</div></nav>'
            '<footer>36 entities · 108 operations<br>Native Draw.io atlas<br>Self-contained, offline document</footer></aside>'
            '<details class="mobile-nav"><summary>Contents · Model and API reference</summary><nav aria-label="Mobile contents">' + main + '</nav></details>')


def build_html():
    css = (ROOT / "reference/reference.css").read_text(encoding="utf-8")
    font_faces = []
    for filename, family, weight in [
        ("DejaVuSans", "DejaVu Sans", 400), ("DejaVuSans-Bold", "DejaVu Sans", 700),
        ("DejaVuSansMono", "DejaVu Sans Mono", 400), ("DejaVuSansMono-Bold", "DejaVu Sans Mono", 700),
    ]:
        encoded = base64.b64encode((ROOT / ("reference/fonts/" + filename + ".woff")).read_bytes()).decode("ascii")
        font_faces.append("@font-face{font-family:'" + family + "';font-style:normal;font-weight:" + str(weight)
                          + ";font-display:swap;src:url(data:font/woff;base64," + encoded + ") format('woff');}")
    css = "\n".join(font_faces) + "\n" + css
    js = (ROOT / "reference/reference.js").read_text(encoding="utf-8")
    hero = ('<header class="hero" id="top"><p class="eyebrow">Frontier Agents · Contract revision 2</p><h1>Consolidated model<br>and API reference</h1>'
            '<p class="lead">Every entity. Every operation. The use cases they serve and the earlier work they consolidate.</p>'
            '<div class="facts"><div><strong>36</strong><span>versioned entities</span></div><div><strong>108</strong><span>typed operations</span></div><div><strong>7</strong><span>modules</span></div><div><strong>8</strong><span>Draw.io pages</span></div></div>'
            '<p class="baseline">Prepared 5 November 2026 · Model/API baseline ' + source_link(PACKAGE + "README.md", BASELINE, BASELINE[:7]) + ' · Previous analysis baseline ' + source_link("aws", SOURCE_COMMIT, SOURCE_COMMIT[:7], directory=True) + '</p>'
            '<div class="section-links"><a href="#entities">Explore entities</a><a href="#operations">Explore operations</a><a href="#use-cases">Follow a use case</a><a href="#lineage">Trace earlier definitions</a></div>'
            '<button type="button" class="button screen-only" id="print-reference">Print reference</button>'
            '<p class="small muted">The document needs no network to read or search. Source links open the pinned repository evidence. Print includes narrative, field tables and examples; duplicate full-schema disclosures stay in the HTML.</p></header>')
    body = (overview() + protocol() + use_case_chapter() + diagrams() + filters() + catalog_chapter("entity")
            + catalog_chapter("operation") + value_types() + error_chapter() + profile_chapter() + lineage_chapter())
    font_license = (ROOT / "reference/fonts/LICENSE.txt").read_text(encoding="utf-8")
    footer = ('<footer class="footer"><p>Generated from the reviewed model and API contracts. All examples are synthetic; no service, provider mutation or production runtime is represented as implemented.</p>'
              + disclosure("Embedded diagram fonts · license", "<pre>" + esc(font_license) + "</pre>", css="raw-schema")
              + '<p><a href="#top">Return to the beginning</a></p></footer>')
    document = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="Complete reference for 36 versioned entities and 108 AWS RPC style operations, with use cases, Draw.io diagrams and historical provenance.">'
            '<title>Consolidated Operations Console — Model and API Reference</title><style>\n' + css + '\n</style></head><body>'
            '<a class="skip-link" href="#main">Skip to the reference</a>' + navigation() + '<main id="main">' + hero + body + footer
            + '</main><script>\n' + js + '\n</script></body></html>\n')
    # Keep generated diffs readable without altering SVG text or JSON payloads.
    return re.sub(r'(</(?:p|h[1-6]|li|ul|ol|section|article|table|tr|thead|tbody|div|details|summary|dl|dt|dd|pre)>)(?=<)', r'\1\n', document)


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.entries = Counter()
        self.assets = []
        self.value_names = []
        self.profile_ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in ("script", "img", "iframe", "link", "source", "video", "audio") and (attrs.get("src") or attrs.get("href")):
            self.assets.append(attrs.get("src") or attrs.get("href"))
        if attrs.get("data-kind"):
            self.entries[(attrs["data-kind"], attrs["data-name"])] += 1
        if attrs.get("data-value-name"):
            self.value_names.append((attrs["data-value-context"], attrs["data-value-name"]))
        if attrs.get("data-profile-id"):
            self.profile_ids.append(attrs["data-profile-id"])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_inputs():
    require(len(ENTITY_NAMES) == 36 and len(OPERATIONS) == 108, "Unexpected catalog size; update the editorial counts deliberately")
    require(set(ENTITY_NOTES) == set(ENTITY_NAMES), "Entity note coverage does not match the model")
    require(set(OPERATION_NOTES) == set(OPERATIONS), "Operation note coverage does not match the catalog")
    require(set(EXAMPLES) == set(OPERATIONS), "API example coverage does not match the catalog")
    require(len(ADAPTERS["mappings"]) == 174 and len(ADAPTERS["profiles"]) == 65, "Unexpected source mapping/profile count")
    require(len(CATALOG["predecessorMappings"]) == 161, "Unexpected operation predecessor count")
    historical_sources = set()
    for name, note in ENTITY_NOTES.items():
        for field in ("purpose", "ownership", "lifecycle", "useCases", "historicalOrigins"):
            require(bool(note.get(field)), f"{name}: missing {field}")
        for case in note["useCases"]:
            require(isinstance(case, dict) and all(case.get(k) for k in ("title", "scenario", "howEntityIsUsed", "outcome")), f"{name}: incomplete use case")
        for origin in note["historicalOrigins"]:
            require(origin.get("previousUse") and origin.get("consolidation"), f"{name}: incomplete historical explanation")
            if origin.get("sourcePath"):
                commit = origin.get("sourceCommit") or (BASELINE if origin["sourcePath"].startswith(PACKAGE) else SOURCE_COMMIT)
                historical_sources.add((commit, origin["sourcePath"]))
        for target in note.get("relatedEntities", []):
            require(target in ENTITY_NAMES, f"{name}: unknown related entity {target}")
    for name, note in OPERATION_NOTES.items():
        require(note.get("purpose") and isinstance(note.get("useCase"), dict), f"{name}: missing purpose/use case")
        case = note["useCase"]
        for field in ("title", "actor", "scenario", "whenToUse", "steps", "intendedResult"):
            require(bool(case.get(field)), f"{name}: incomplete use case {field}")
        for target in note.get("nextSteps", []) + note.get("relatedOperations", []):
            require(target in OPERATIONS, f"{name}: unknown next operation {target}")
        for target in note.get("relatedEntities", []):
            require(target in ENTITY_NAMES, f"{name}: unknown related entity {target}")
    for case in CROSS_CASES:
        require(set(case["entities"]) <= set(ENTITY_NAMES), f"Unknown entity in {case['title']}")
        require(set(case["operations"]) <= set(OPERATIONS), f"Unknown operation in {case['title']}")
    for commit, path in sorted(historical_sources):
        result = subprocess.run(["git", "cat-file", "-e", f"{commit}:{path}"], cwd=REPO, capture_output=True)
        require(result.returncode == 0, f"Historical source missing at pinned commit: {commit}:{path}")
    return historical_sources


def audit_document(document, historical_sources):
    audit = AuditParser()
    audit.feed(document)
    duplicates = [ident for ident, count in Counter(audit.ids).items() if count > 1]
    require(not duplicates, f"Duplicate HTML IDs: {duplicates[:10]}")
    ids = set(audit.ids)
    missing_links = [link for link in audit.links if link.startswith("#") and link[1:] not in ids]
    require(not missing_links, f"Broken internal links: {missing_links[:10]}")
    expected_entries = {("entity", name) for name in ENTITY_NAMES} | {("operation", name) for name in OPERATIONS}
    require(set(audit.entries) == expected_entries and all(n == 1 for n in audit.entries.values()), "Entity/operation sections are not exact and unique")
    expected_values = {("model", n) for n in MODEL_VALUES} | {("rpc", n) for n in RPC_VALUES}
    require(set(audit.value_names) == expected_values and len(audit.value_names) == len(expected_values), "Value type coverage mismatch")
    require(set(audit.profile_ids) == {p["profileId"] for p in ADAPTERS["profiles"]}, "Profile coverage mismatch")
    require(not audit.assets, f"Offline document unexpectedly loads resources: {audit.assets}")
    require(not re.search(r'@import|url\(["\']?https?://|\bfetch\s*\(|XMLHttpRequest|WebSocket', document), "Unexpected network-loading behavior")
    require(document.count('<svg ') == 8, "Draw.io SVG count mismatch")
    require(document.count('class="request-example"') == 108 and document.count('class="response-example"') == 108, "Missing operation examples")
    require(len(MODEL["x-relationships"]) == 45, "Unexpected relationship count")
    files = ["model/schema.json", "model/adapter-profiles.json", "model/examples.json", "api/operations.json", "api/rpc.schema.json", "api/examples.json", "inventory.json", "diagrams/manifest.json", "reference/entity-notes.json", "reference/operation-notes.json", "reference/reference.css", "reference/reference.js", "tools/build_reference.py"]
    files += [d["svg"]["path"] for d in DIAGRAMS["diagrams"]]
    files += [str(path.relative_to(ROOT)) for path in sorted((ROOT / "reference/fonts").iterdir())]
    return {
        "format": "consolidated-html-reference/1", "status": "PASS", "contractVersion": 2,
        "modelApiBaselineCommit": BASELINE, "earlierAnalysisCommit": SOURCE_COMMIT,
        "output": "reference.html", "outputSha256": hashlib.sha256(document.encode()).hexdigest(),
        "coverage": {
            "entities": len(ENTITY_NAMES), "entityFields": sum(len(MODEL["$defs"][n]["properties"]) for n in ENTITY_NAMES),
            "operations": len(OPERATIONS), "requestFields": sum(len(RPC["$defs"][n+"Request"]["properties"]) for n in OPERATIONS),
            "responseFields": sum(len(RPC["$defs"][n+"Response"]["properties"]) for n in OPERATIONS),
            "entityUseCases": sum(len(n["useCases"]) for n in ENTITY_NOTES.values()),
            "entityHistoricalOrigins": sum(len(n["historicalOrigins"]) for n in ENTITY_NOTES.values()),
            "operationUseCases": len(OPERATION_NOTES), "crossModuleUseCases": len(CROSS_CASES),
            "modelValueTypes": len(MODEL_VALUES), "rpcValueTypes": len(RPC_VALUES),
            "relationships": 45, "drawioPages": 8, "sourceMappingRows": 174,
            "sourceAliases": sum(len(m["sourceConcepts"]) for m in ADAPTERS["mappings"]),
            "sourceProfiles": 65, "operationPredecessorMappings": 161,
            "rpcPayloadExamples": 216, "rpcErrorExamples": len(API_EXAMPLES["errors"]),
            "uniqueEntityHistoricalSources": len(historical_sources), "internalLinks": len([x for x in audit.links if x.startswith('#')]),
        },
        "checks": {
            "exactCatalogCoverage": True, "useCasesAndHistoricalOriginsPresent": True,
            "pinnedEntitySourcePathsExist": True, "allInternalLinksResolve": True,
            "uniqueHtmlAndEmbeddedSvgIds": True, "noExternalRuntimeAssets": True,
            "canonicalSchemasAndExamplesRendered": True,
        },
        "limits": ["These checks validate document coverage and generation, not production runtime behavior.", "Visual and interaction QA is recorded separately in reference/README.md."],
        "inputs": [{"path": path, "sha256": hashlib.sha256((ROOT/path).read_bytes()).hexdigest()} for path in files],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify committed HTML/report match current inputs; do not write")
    args = parser.parse_args()
    global ENTITY_NOTES, OPERATION_NOTES
    entity_rows = read_json("reference/entity-notes.json")["entities"]
    operation_rows = read_json("reference/operation-notes.json")["operations"]
    ENTITY_NOTES = {note["entity"]: note for note in entity_rows}
    OPERATION_NOTES = {note["operation"]: note for note in operation_rows}
    require(len(ENTITY_NOTES) == len(entity_rows), "Duplicate entity narrative")
    require(len(OPERATION_NOTES) == len(operation_rows), "Duplicate operation narrative")
    sources = validate_inputs()
    document = build_html()
    report = audit_document(document, sources)
    report_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        require(OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") == document, "reference.html is stale; run tools/build_reference.py")
        require(REPORT.exists() and REPORT.read_text(encoding="utf-8") == report_text, "reference/build-report.json is stale")
        print("PASS: HTML and coverage report exactly reproduce from current contracts and notes.")
    else:
        OUTPUT.write_text(document, encoding="utf-8")
        REPORT.write_text(report_text, encoding="utf-8")
        print(f"Wrote {OUTPUT.relative_to(REPO)} ({len(document.encode()):,} bytes)")
    print(json.dumps(report["coverage"], sort_keys=True))


if __name__ == "__main__":
    main()
