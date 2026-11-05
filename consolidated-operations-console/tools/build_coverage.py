#!/usr/bin/env python3
"""Build an independent, source-scoped construct coverage audit and mapping rulebook.

Only the standard library and the local pinned Git history are used. The source
diagram denominator is extracted before consulting the reviewed semantic catalog.
The classifications are review judgments backed by explicit evidence; this tool
checks their structure, arithmetic, references and reproducibility.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PREFIX = "consolidated-operations-console/"
SOURCE = "d926a81c584b6b69f41bfb9641532c4f8f2d7cb3"
TARGET = "20650d3cf051ad457378704c15f48f77565a611c"
URL = "https://github.com/lyrel-dev/frontier-agents"
INPUTS = ["coverage/health-resilience.json", "coverage/devops-agent.json", "coverage/fis-workflow.json"]
SERVICE_NAMES = {"health": "AWS Health", "resilience-hub": "AWS Resilience Hub", "devops-agent": "AWS DevOps Agent", "fis": "AWS FIS", "workflow": "Shared assessment workflow"}
LEVELS = ["NORMALIZED", "PARTIAL", "RETAINED_ONLY", "UNMAPPED"]
KINDS = ["NATIVE_RESOURCE", "APPLICATION_ENTITY", "OWNED_VALUE", "RELATIONSHIP", "EXTERNAL_IDENTITY", "HISTORY_REPRESENTATION", "DERIVED_VIEW", "TRANSPORT_DTO", "CONTROL_VALUE"]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(test, message):
    if not test:
        raise ValueError(message)


@lru_cache(maxsize=None)
def git_text(commit, path):
    process = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=REPO, capture_output=True)
    require(process.returncode == 0, f"Missing pinned source: {commit}:{path}")
    return process.stdout.decode("utf-8")


def source_url(path, commit=None, heading=None):
    commit = commit or (TARGET if path.startswith(PREFIX) else SOURCE)
    link = f"{URL}/blob/{commit}/{quote(path, safe='/')}"
    if heading:
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        link += "#" + quote(slug, safe="-_")
    return link


def md(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def link(path, label=None, heading=None):
    return f"[{md(label or path)}]({source_url(path, heading=heading)})"


def evidence_markdown(item):
    if isinstance(item, dict) and item.get("path"):
        result = link(item["path"], heading=item.get("heading"))
        if item.get("symbol"):
            result += " — `" + item["symbol"] + "`"
        return result
    if isinstance(item, str):
        if item.startswith("#/$defs/"):
            return link(PREFIX + "model/schema.json", "model/schema.json") + " — `" + item + "`"
        if item.startswith(("aws/", PREFIX)):
            path, _, fragment = item.partition("#")
            return "[" + item + "](" + source_url(path) + ("#" + fragment if fragment else "") + ")"
        return item
    return "`" + json.dumps(item, ensure_ascii=False) + "`"


def pointer_value(document, pointer):
    if pointer.startswith("schema.json"):
        pointer = pointer.split("#", 1)[-1]
    pointer = pointer.lstrip("#")
    if not pointer:
        return document
    require(pointer.startswith("/"), f"Not a JSON pointer: {pointer}")
    current = document
    for key in pointer[1:].split("/"):
        key = key.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(key)]
        else:
            current = current[key]
    return current


def schema_references(value):
    if isinstance(value, dict):
        reference = value.get("$ref", "")
        if reference.startswith("#/$defs/"):
            yield reference.rsplit("/", 1)[-1]
        for child in value.values():
            yield from schema_references(child)
    elif isinstance(value, list):
        for child in value:
            yield from schema_references(child)


def extract_diagram_declarations(inventory):
    declarations = defaultdict(list)
    files = []
    for item in inventory["files"]:
        path = item["path"]
        if "/diagrams/" not in path or not path.endswith((".mmd", ".md")):
            continue
        content = git_text(SOURCE, path)
        if "erDiagram" not in content and "classDiagram" not in content:
            continue
        service = "workflow" if "/fis/analysis/workflow/" in path else item["service"]
        symbols = set(re.findall(r"^\s*class\s+([A-Za-z][A-Za-z0-9_]*)\b", content, re.M))
        symbols |= set(re.findall(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*\{\s*$", content, re.M))
        for left, right in re.findall(r"^\s*(\w+)\s+[|}o{]+--[|}o{]+\s+(\w+)\s*:", content, re.M):
            symbols.update((left, right))
        files.append({"path": path, "service": service, "symbols": sorted(symbols), "sourceSha256": hashlib.sha256(content.encode()).hexdigest()})
        for symbol in sorted(symbols):
            declarations[(service, symbol)].append(path)
    return declarations, files


def coverage_count(rows):
    counts = Counter(row["coverageLevel"] for row in rows)
    total = len(rows)
    return {"total": total, **{key: counts[key] for key in LEVELS},
            "normalizedPercent": round(100 * counts["NORMALIZED"] / total, 1) if total else None,
            "representedIncludingPartialAndRetained": total - counts["UNMAPPED"]}


def rule_ids(row):
    rules = {"MAP-01", "MAP-03", "MAP-05", "MAP-19"}
    rules.update({
        "NATIVE_RESOURCE": ["MAP-02", "MAP-12", "MAP-17"],
        "APPLICATION_ENTITY": ["MAP-02", "MAP-07", "MAP-13"],
        "OWNED_VALUE": ["MAP-04", "MAP-17"],
        "RELATIONSHIP": ["MAP-06"],
        "EXTERNAL_IDENTITY": ["MAP-18"],
        "HISTORY_REPRESENTATION": ["MAP-03", "MAP-07", "MAP-10"],
        "DERIVED_VIEW": ["MAP-09", "MAP-12"],
        "TRANSPORT_DTO": ["MAP-08", "MAP-14"],
        "CONTROL_VALUE": ["MAP-04", "MAP-15"],
    }[row["sourceSemanticKind"]])
    text = " ".join([row["sourceName"], row.get("previousUse", ""), row.get("coverageReason", "")]).lower()
    if any(word in text for word in ["coverage", "collection", "readattempt", "failedset"]):
        rules.add("MAP-11")
    if any(word in text for word in ["metric", "criterion", "checkresult", "evaluation"]):
        rules.add("MAP-16")
    if row["coverageLevel"] in ["RETAINED_ONLY", "PARTIAL"]:
        rules.add("MAP-08")
    if row["coverageLevel"] != "NORMALIZED":
        rules.add("MAP-20")
    return sorted(rules)


def normalize_pointer(pointer):
    if isinstance(pointer, dict):
        pointer = pointer.get("pointer") or pointer.get("path")
    require(isinstance(pointer, str), f"Invalid schema pointer {pointer}")
    if "#" in pointer:
        pointer = "#" + pointer.split("#", 1)[1]
    elif pointer.startswith("/"):
        pointer = "#" + pointer
    return pointer


def validate_row(row, schema, profiles, entities, identifiers):
    require(row.get("id") and row["id"] not in identifiers, f"Duplicate/missing construct ID: {row.get('id')}")
    identifiers.add(row["id"])
    for key in ["sourceName", "previousUse", "identity", "coverageReason", "evidence"]:
        require(bool(row.get(key)), f"{row['id']}: missing {key}")
    require(row["sourceService"] in SERVICE_NAMES, f"Unknown service for {row['id']}")
    require(row["sourceSemanticKind"] in KINDS, f"Unknown semantic kind for {row['id']}: {row['sourceSemanticKind']}")
    require(row["coverageLevel"] in LEVELS, f"Unknown level for {row['id']}")
    require(isinstance(row.get("originalEntityDeclaration"), bool), f"Missing original declaration decision: {row['id']}")
    require(bool(row.get("declarationReason")), f"Missing declaration rationale: {row['id']}")
    require(set(row.get("canonicalEntities", [])) <= entities, f"Unknown target entity in {row['id']}")
    require(set(row.get("profileIds", [])) <= profiles, f"Unknown source profile in {row['id']}")
    row["schemaPointers"] = list(dict.fromkeys(normalize_pointer(pointer) for pointer in row.get("schemaPointers", [])))
    for pointer in row["schemaPointers"]:
        try:
            pointer_value(schema, pointer)
        except (KeyError, IndexError, ValueError) as exc:
            raise ValueError(f"{row['id']}: unresolved schema pointer {pointer}") from exc
    if row["coverageLevel"] == "NORMALIZED":
        require(bool(row["schemaPointers"]), f"{row['id']}: normalized without a schema binding")
    if row["coverageLevel"] in ["PARTIAL", "UNMAPPED"]:
        require(bool(row.get("gaps")), f"{row['id']}: gap status without a gap description")
    for evidence in row["evidence"]:
        path = evidence["path"]
        content = git_text(SOURCE, path)
        if evidence.get("symbol"):
            require(evidence["symbol"] in content, f"Source symbol missing: {row['id']} {evidence['symbol']}")
        if evidence.get("heading"):
            headings = [match.strip() for match in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", content, re.M)]
            require(evidence["heading"] in headings, f"Source heading missing: {row['id']} {evidence['heading']}")
    row["ruleIds"] = rule_ids(row)


def assemble():
    for path in ["model/schema.json", "model/adapter-profiles.json", "api/rpc.schema.json", "api/operations.json"]:
        require((ROOT/path).read_text(encoding="utf-8") == git_text(TARGET, PREFIX + path),
                f"Target contract changed since the reviewed baseline: {path}. Review the catalog and update TARGET deliberately.")
    inventory = load("inventory.json")
    schema = load("model/schema.json")
    registry = load("model/adapter-profiles.json")
    rules = load("coverage/mapping-rules.json")
    entities = set(schema["x-entities"])
    profiles = {profile["profileId"] for profile in registry["profiles"]}
    declarations, diagram_files = extract_diagram_declarations(inventory)
    require(len(declarations) == 130, "Original diagram population changed; review the denominator")
    rows, findings, native_shapes = [], [], []
    identifiers = set()
    for path in INPUTS:
        document = load(path)
        require(document["sourceCommit"] == SOURCE, f"Source baseline changed: {path}")
        for row in document["constructs"]:
            validate_row(row, schema, profiles, entities, identifiers)
            row["reviewInput"] = path
            rows.append(row)
        findings.extend(document.get("findings", []))
        native_shapes.extend(document.get("nativeShapeCoverage", []))
    rows.sort(key=lambda row: (list(SERVICE_NAMES).index(row["sourceService"]), row["sourceName"].casefold()))
    by_alias = defaultdict(list)
    for row in rows:
        for alias in set(row.get("aliases", []) + [row["sourceName"]]):
            by_alias[(row["sourceService"], alias)].append(row)
    benchmark = []
    for (service, symbol), paths in sorted(declarations.items()):
        matches = by_alias[(service, symbol)]
        require(len(matches) == 1, f"Diagram symbol must resolve exactly once: {(service, symbol)} -> {[x['id'] for x in matches]}")
        row = matches[0]
        benchmark.append({"sourceService": service, "symbol": symbol, "constructId": row["id"],
                          "sourceSemanticKind": row["sourceSemanticKind"], "coverageLevel": row["coverageLevel"],
                          "sourcePaths": paths, "canonicalEntities": row["canonicalEntities"]})
    symbols_by_id = defaultdict(list)
    for item in benchmark:
        symbols_by_id[item["constructId"]].append(item["symbol"])
    for row in rows:
        row["diagramSymbols"] = sorted(symbols_by_id[row["id"]])
        row["population"] = "DIAGRAM_BENCHMARK" if row["diagramSymbols"] else "DICTIONARY_SUPPLEMENT"
    aliases = {(m["sourceService"], name) for m in registry["mappings"] for name in m["sourceConcepts"]}
    require(set(declarations) <= aliases, "A source diagram declaration has no original registry alias")
    native_path = "aws/devops-agent/analysis/annexes/Investigation_API_Catalog.md"
    native_section = git_text(SOURCE, native_path).split("## 3. Returned entities and nested value objects", 1)[1].split("## 4.", 1)[0]
    expected_native = set(re.findall(r"^### ([A-Za-z][A-Za-z0-9_]*)\s*$", native_section, re.M))
    require(len(expected_native) == 52, "Selected native shape population changed")
    require({shape["name"] for shape in native_shapes} == expected_native and len(native_shapes) == 52, "Native SDK shape coverage is incomplete or duplicated")
    for shape in native_shapes:
        require(shape["coverageLevel"] in LEVELS, f"Bad native-shape level: {shape['name']}")
        require(set(shape.get("profileIds", [])) <= profiles, f"Unknown native-shape profile: {shape['name']}")
        for pointer in shape.get("schemaPointers", []):
            pointer_value(schema, normalize_pointer(pointer))
    rule_names = {rule["id"] for rule in rules["rules"]}
    require(len(rule_names) == len(rules["rules"]) == 20, "Mapping rule count/IDs mismatch")
    for rule in rules["rules"]:
        for pointer in rule["schemaPointers"]:
            pointer_value(schema, pointer)
        for path in rule["sourcePaths"]:
            git_text(TARGET if path.startswith(PREFIX) else SOURCE, path)
    for entity in entities:
        entity_schema = schema["$defs"][entity]
        required = entity_schema["required"]
        require(all(key in required for key in ["version", "createdAt", "updatedAt"]), f"Unversioned entity: {entity}")
        require(entity_schema["properties"]["version"] == {"$ref": "#/$defs/Version"}, f"Different version type: {entity}")
        require(all(entity_schema["properties"][key] == {"$ref": "#/$defs/Timestamp"} for key in ["createdAt", "updatedAt"]), f"Different metadata time types: {entity}")
        require(entity_schema.get("x-versioning") == "APPEND_ONLY", f"Different version publication rule: {entity}")
    require(not ({"SourceRevision", "ProjectionRevision", "ScenarioRevision", "AssetVersion"} & entities), "Former version-only entity reintroduced")
    reachable = set(entities)
    queue = list(entities)
    while queue:
        current = queue.pop()
        for target in schema_references(schema["$defs"][current]):
            if target not in reachable:
                reachable.add(target)
                queue.append(target)
    registry_counts = []
    for service in SERVICE_NAMES:
        mappings = [m for m in registry["mappings"] if m["sourceService"] == service]
        entity_targets = {target for m in mappings if m["disposition"] == "canonicalEntity" for target in m["canonicalEntities"]}
        registry_counts.append({"sourceService": service, "mappingRows": len(mappings),
                                "aliases": sum(len(m["sourceConcepts"]) for m in mappings),
                                "dispositions": dict(Counter(m["disposition"] for m in mappings)),
                                "declaredEntityTargets": sorted(entity_targets),
                                "declaredEntityTargetCount": len(entity_targets)})
    entity_targets = {target for m in registry["mappings"] if m["disposition"] == "canonicalEntity" for target in m["canonicalEntities"]}
    aws_entity_targets = {target for m in registry["mappings"] if m["sourceService"] != "workflow" and m["disposition"] == "canonicalEntity" for target in m["canonicalEntities"]}
    counts_by_service = []
    for service in SERVICE_NAMES:
        declarations_for_service = [row for row in benchmark if row["sourceService"] == service]
        catalog_for_service = [row for row in rows if row["sourceService"] == service]
        entity_concepts = [row for row in catalog_for_service if row["sourceSemanticKind"] in ["NATIVE_RESOURCE", "APPLICATION_ENTITY"]]
        counts_by_service.append({"sourceService": service, "label": SERVICE_NAMES[service],
                                  "diagramCoverage": coverage_count(declarations_for_service),
                                  "diagramSemanticKinds": dict(Counter(row["sourceSemanticKind"] for row in declarations_for_service)),
                                  "catalogCoverage": coverage_count(catalog_for_service),
                                  "sourceEntityCoverage": coverage_count(entity_concepts),
                                  "nativeEntityConcepts": len([row for row in entity_concepts if row["sourceSemanticKind"] == "NATIVE_RESOURCE"]),
                                  "applicationEntityConcepts": len([row for row in entity_concepts if row["sourceSemanticKind"] == "APPLICATION_ENTITY"]),
                                  "supplementaryConstructs": len([row for row in catalog_for_service if row["population"] == "DICTIONARY_SUPPLEMENT"]),
                                  "declaredTargetEntities": sorted({target for row in declarations_for_service for target in row["canonicalEntities"]})})
    report = {
        "format": "consolidated-model-coverage/1", "status": "AUDIT_COMPLETE_WITH_QUALIFIED_COVERAGE",
        "sourceCommit": SOURCE, "targetCommit": TARGET, "sourceFileInventoryCount": inventory["fileCount"],
        "countingPolicy": {
            "diagramUnit": "One distinct (sourceService, class/ER symbol) declared in the pinned original model diagrams; occurrences across pages deduplicate.",
            "semanticCatalogUnit": "One reviewed source concept; genuine spelling aliases collapse, semantically different constructs do not.",
            "nativeShapeUnit": "One of the 52 selected DevOps returned/nested SDK types, reported separately and never added to entity counts.",
            "canonicalEntityUnit": "One x-entity definition in the consolidated model.",
            "sourceEntityUnit": "One reviewed substantive source concept classified NATIVE_RESOURCE or APPLICATION_ENTITY. Source-owned children count when they have identity/lifecycle; pure history representations, values, relationships, external references and DTO wrappers are separate.",
            "normalizationDenominator": "Declared diagram symbols for the fixed benchmark; broader dictionary catalog and native DTO shapes have separate denominators.",
            "normalizedMeaning": "The source construct's essential application meaning has a bound typed representation; optional provider breadth can remain retained evidence.",
            "partialMeaning": "A typed core exists but a source-required distinction, binding, ownership detail or invariant is missing/ambiguous.",
            "retainedMeaning": "Inspectable source/native content or a declared source profile preserves the construct, but its application meaning has no complete normalized typed binding.",
            "unmappedMeaning": "The audit found no concrete representation sufficient to preserve the named construct's essential meaning.",
        },
        "awsDiagramCoverage": coverage_count([row for row in benchmark if row["sourceService"] != "workflow"]),
        "workflowDiagramCoverage": coverage_count([row for row in benchmark if row["sourceService"] == "workflow"]),
        "allDiagramCoverage": coverage_count(benchmark), "catalogCoverage": coverage_count(rows),
        "sourceEntityCoverage": {
            "aws": coverage_count([row for row in rows if row["sourceService"] != "workflow" and row["sourceSemanticKind"] in ["NATIVE_RESOURCE", "APPLICATION_ENTITY"]]),
            "workflow": coverage_count([row for row in rows if row["sourceService"] == "workflow" and row["sourceSemanticKind"] in ["NATIVE_RESOURCE", "APPLICATION_ENTITY"]]),
            "includingWorkflow": coverage_count([row for row in rows if row["sourceSemanticKind"] in ["NATIVE_RESOURCE", "APPLICATION_ENTITY"]]),
            "nativeAws": coverage_count([row for row in rows if row["sourceService"] != "workflow" and row["sourceSemanticKind"] == "NATIVE_RESOURCE"]),
            "applicationAws": coverage_count([row for row in rows if row["sourceService"] != "workflow" and row["sourceSemanticKind"] == "APPLICATION_ENTITY"]),
        },
        "nativeShapeCoverageCounts": coverage_count(native_shapes), "byService": counts_by_service,
        "diagramSemanticKinds": dict(Counter(row["sourceSemanticKind"] for row in benchmark)),
        "catalogSemanticKinds": dict(Counter(row["sourceSemanticKind"] for row in rows)),
        "registry": {"mappingRows": len(registry["mappings"]), "aliases": len(aliases), "profiles": len(profiles),
                     "byService": registry_counts, "diagramSymbolsWithAlias": len(set(declarations) & aliases)},
        "targetModel": {"entities": len(entities), "uniformlyVersionedEntities": len(entities),
                        "entityNames": sorted(entities), "projectionProfiles": len(schema["x-projectionProfiles"]),
                        "typedValueDefinitions": len(schema["$defs"]) - len(entities),
                        "unboundValueDefinitions": sorted(set(schema["$defs"]) - reachable),
                        "declaredEntityTargetsFromAwsSolutions": sorted(aws_entity_targets),
                        "declaredEntityTargetsIncludingWorkflow": sorted(entity_targets),
                        "entitiesWithoutCanonicalEntityPredecessorRow": sorted(entities - entity_targets),
                        "targetCountCaveat": "Registry target counts describe declared lineage, not verified semantic completeness; per-service sets overlap."},
        "rules": len(rules["rules"]), "diagramSources": diagram_files,
        "findings": findings,
        "checks": {"independentDiagramPopulation": True, "allDiagramSymbolsResolveExactlyOnce": True,
                   "targetContractsMatchPinnedReviewBaseline": True,
                   "allSchemaPointersResolve": True, "allProfileIdsExist": True, "pinnedSourceEvidenceExists": True,
                   "nativeShapePopulationExact": True, "uniformEntityVersionContract": True,
                   "sameVersionAndTimestampTypesOnAllEntities": True, "noFormerRevisionEntities": True,
                   "semanticReviewIsNotAliasExistenceCheck": True},
        "limitations": ["This is model/contract coverage of the pinned repository solutions, not complete current AWS product/SDK coverage.",
                        "Source profile hints and retained payloads are not executable native SDK validation or implemented adapters.",
                        "The audit preserves the existing 36-entity model. Proposed gap remedies are recommendations, not implemented schema/API changes.",
                        "Schema-pointer checks prove structure; source-to-target classifications and essential-semantics judgments are documented review conclusions."],
    }
    source_inputs = INPUTS + ["coverage/mapping-rules.json", "model/schema.json", "model/adapter-profiles.json", "api/rpc.schema.json", "api/operations.json", "inventory.json", "tools/build_coverage.py"]
    report["inputs"] = [{"path": path, "sha256": hashlib.sha256((ROOT/path).read_bytes()).hexdigest()} for path in source_inputs]
    catalog = {"format": "aws-source-construct-catalog/1", "sourceCommit": SOURCE, "targetCommit": TARGET,
               "countingPolicy": report["countingPolicy"], "constructs": rows, "diagramBenchmark": benchmark,
               "nativeShapeCoverage": sorted(native_shapes, key=lambda row: row["name"])}
    return catalog, report, rules


def table(headers, rows):
    return "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n" + "".join("| " + " | ".join(md(cell) for cell in row) + " |\n" for row in rows)


def status_table(report):
    rows = []
    for item in report["byService"]:
        c = item["diagramCoverage"]
        rows.append([item["label"], c["total"], c["NORMALIZED"], c["PARTIAL"], c["RETAINED_ONLY"], c["UNMAPPED"], f"{c['normalizedPercent']:.1f}%"])
    for label, key in [("Four AWS solutions", "awsDiagramCoverage"), ("Including shared workflow", "allDiagramCoverage")]:
        c = report[key]
        rows.append(["**" + label + "**", c["total"], c["NORMALIZED"], c["PARTIAL"], c["RETAINED_ONLY"], c["UNMAPPED"], f"{c['normalizedPercent']:.1f}%"])
    return table(["Source model", "Declared constructs", "Normalized", "Partial", "Retained only", "Unmapped", "Normalized / total"], rows)


def construct_catalog(catalog):
    out = ["# Source construct catalog\n", "Generated by `tools/build_coverage.py`. The fixed diagram population and supplementary named dictionary constructs are tagged separately. Native SDK shapes have their own appendix and are not added to entity counts.\n"]
    for service, label in SERVICE_NAMES.items():
        out.append(f"## {label}\n")
        for row in [row for row in catalog["constructs"] if row["sourceService"] == service]:
            out.append(f"### {row['id']} — {row['sourceName']}\n")
            out.append(f"**{row['coverageLevel']}** · `{row['sourceSemanticKind']}` · `{row['population']}`\n")
            out.append("**Previous use.** " + row["previousUse"] + "\n")
            out.append("**Identity.** " + row["identity"] + "\n")
            out.append("**Original declaration.** " + row["declarationReason"] + "\n")
            out.append("**Diagram symbols.** " + (", ".join(f"`{symbol}`" for symbol in row["diagramSymbols"]) or "Supplementary dictionary/control concept") + ".\n")
            out.append("**Aliases.** " + (", ".join(f"`{alias}`" for alias in row.get("aliases", [])) or "None") + ".\n")
            out.append("**Target entities.** " + (", ".join(f"`{name}`" for name in row["canonicalEntities"]) or "No claimed target entity") + ".\n")
            out.append("**Typed paths.** " + ("; ".join(f"`{pointer}`" for pointer in row["schemaPointers"]) or "No bound typed representation claimed") + ".\n")
            out.append("**Retained profiles.** " + ("; ".join(f"`{profile}`" for profile in row.get("profileIds", [])) or "None claimed") + ".\n")
            out.append("**Coverage judgment.** " + row["coverageReason"] + "\n")
            if row.get("gaps"):
                out.append("**Gaps / qualifications.**\n\n" + "\n".join("- " + (gap if isinstance(gap, str) else json.dumps(gap, ensure_ascii=False)) for gap in row["gaps"]) + "\n")
            out.append("**Rules.** " + ", ".join(f"[{rule}](../MAPPING_RULES.md#{rule.lower()})" for rule in row["ruleIds"]) + ".\n")
            out.append("**Source evidence.**\n\n" + "\n".join("- " + link(item["path"], heading=item.get("heading")) + (" — `" + item["symbol"] + "`" if item.get("symbol") else "") for item in row["evidence"]) + "\n")
    out.append("## Selected DevOps SDK shapes — separate population\n")
    out.append("The 52 returned/nested type declarations below overlap the native concepts already discussed; they are transport/schema coverage, not 52 additional domain entities.\n")
    out.append(table(["Native type", "Kind", "Coverage", "Interpretation"], [["`" + row["name"] + "`", row["sourceSemanticKind"], row["coverageLevel"], row["coverageReason"]] for row in catalog["nativeShapeCoverage"]]))
    return "\n".join(out).rstrip() + "\n"


def rulebook(rules):
    out = ["# Rules for mapping AWS constructs to the consolidated model\n", rules["scope"] + "\n",
           "Use the rules in this order: establish the source concept and scope; decide entity/value/reference/view/retained-DTO ownership; preserve identity, versions and evidence; then prove the claimed coverage. The same rules apply to all modules.\n",
           "## Decision catalog\n", table(["Rule", "Decision"], [[f"[{rule['id']}](#{rule['id'].lower()})", rule["title"]] for rule in rules["rules"]])]
    for rule in rules["rules"]:
        out.append(f'<a id="{rule["id"].lower()}"></a>\n\n## {rule["id"]} — {rule["title"]}\n')
        out.append(rule["decision"] + "\n")
        out.append("**Required evidence.**\n\n" + "\n".join("- " + item for item in rule["requiredEvidence"]) + "\n")
        out.append("**Example.** " + rule["example"] + "\n")
        out.append("**Failure to avoid.** " + rule["failureMode"] + "\n")
        out.append("**Acceptance.** " + rule["acceptance"] + "\n")
        if rule["schemaPointers"]:
            out.append("**Current contract evidence.** " + "; ".join(f"`{pointer}`" for pointer in rule["schemaPointers"]) + " in [model/schema.json](model/schema.json).\n")
        out.append("**Sources.** " + " · ".join(link(path) for path in rule["sourcePaths"]) + "\n")
    out.append("## Applying the catalog\n\nEach row in the [source construct catalog](coverage/CATALOG.md) records its source evidence, semantic kind, exact target paths, profiles, coverage judgment and applicable rules. The [coverage audit](COVERAGE.md) reports the resulting populations and gaps. The current findings do not authorize treating raw retention as normalization or adding version-only entities.\n")
    return "\n".join(out).rstrip() + "\n"


def overview(catalog, report):
    aws = report["awsDiagramCoverage"]
    all_rows = report["allDiagramCoverage"]
    model = report["targetModel"]
    catalog_counts = report["catalogCoverage"]
    source_entities = report["sourceEntityCoverage"]["aws"]
    out = ["# Model coverage audit\n",
           f"**Target:** main at [`{TARGET[:7]}`]({URL}/commit/{TARGET}). **Original analysis baseline:** [`{SOURCE[:7]}`]({URL}/commit/{SOURCE}). **Audit date:** 5 November 2026.\n",
           f"The consolidated model contains **{model['entities']} uniformly versioned entities**. The broader source catalog identifies **{source_entities['total']} substantive entity concepts** in the four original AWS solutions: **{report['sourceEntityCoverage']['nativeAws']['total']} provider-owned** and **{report['sourceEntityCoverage']['applicationAws']['total']} application-defined**. Of these, **{source_entities['NORMALIZED']} are normalized**, **{source_entities['PARTIAL']} partial**, and **{source_entities['RETAINED_ONLY']} retained-only**; none is wholly unmapped. These are source concepts with identity/lifecycle, not a claim that the products expose that many standalone AWS resources or that the target needs that many entities.\n",
           f"The independently extractable source diagram population is broader than entities: the four AWS solutions declare **{aws['total']} distinct model constructs**, and the shared workflow adds **11**, for **{all_rows['total']}**. All have registry aliases, but only **{aws['NORMALIZED']}/{aws['total']} ({aws['normalizedPercent']:.1f}%)** of the four AWS solutions' constructs meet the normalized-core criterion. One source relationship, **ExperimentMetricBinding**, has no concrete representation despite its named registry row.\n",
           "A source class/ER box is not necessarily an independent domain entity. These source populations include entities, owned values, relationships, external identities, derived views and former revision constructs. The audit does not turn every original box into a target entity.\n",
           "## 1. Entity concepts represented from the original solutions\n",
           table(["Original solution", "Substantive source entities", "Provider-owned", "Application-defined", "Normalized", "Partial", "Retained only", "Unmapped"], [[item["label"], item["sourceEntityCoverage"]["total"], item["nativeEntityConcepts"], item["applicationEntityConcepts"], *[item["sourceEntityCoverage"][level] for level in LEVELS]] for item in report["byService"]]),
           f"**Four AWS solutions:** {source_entities['total']} source entity concepts; {source_entities['NORMALIZED']} normalized, {source_entities['PARTIAL']} partial, {source_entities['RETAINED_ONLY']} retained-only, {source_entities['UNMAPPED']} unmapped. **Including shared workflow:** {report['sourceEntityCoverage']['includingWorkflow']['total']} substantive entity concepts. The original workflow's explicit six-entity table includes ScenarioRevision; this audit counts its five substantive identities separately from that pure history representation, which maps to Scenario.version.\n",
           "The source-entity count is a documented semantic classification over the broader source catalog. It includes identity-bearing owned children and excludes pure historical representations (six across the four AWS solutions; seven including workflow ScenarioRevision), value objects, relationship records, external identity references and transport wrappers. It must not be substituted for the mechanically extracted diagram count below.\n",
           "## 2. Fixed source-model coverage, including values and relationships\n", status_table(report),
           "**Normalized** means the source construct's essential application meaning has a bound typed representation. **Partial** means a typed core exists but a required distinction or binding is missing or ambiguous. **Retained only** means the source content is inspectable through a concrete retained representation/profile but is not fully normalized. **Unmapped** means no sufficient concrete representation was established. Percentages count only NORMALIZED in the numerator; there is no partial-credit weighting.\n",
           "The denominator is extracted independently from class/ER declarations and relationship endpoints in the pinned source diagram files. Repeated symbols across pages count once per source service. The current registry is consulted only after that extraction. [Complete declaration-to-construct mapping](coverage/catalog.json) · [source-file/hash register and counts](coverage/report.json).\n",
           "## 3. What the different counts mean\n",
           table(["Count", "Population", "What it does not establish"], [
               [36, "Current first-class entity definitions; all require version/createdAt/updatedAt", "36 native AWS resources or one-to-one source entity preservation"],
               [source_entities["total"], "Substantive native/application entity concepts reviewed in the four original solution catalogs", "A target entity count or a complete live AWS resource inventory"],
               [119, "Distinct named class/ER constructs in four AWS solution models", "119 independent native entities"],
               [11, "Additional class/ER constructs in the application workflow model", "Another AWS product or eleven extra target entities"],
               [catalog_counts["total"], "Broader reviewed source-concept catalog, including named dictionary/control supplements", "An SDK-wide or instance population"],
               [52, "Selected DevOps returned/nested SDK types, audited separately", "52 additional business entities; this set overlaps model concepts"],
               [182, "The earlier validator's 130 diagram names plus 52 native SDK shape names", "182 distinct source entities or semantic normalization proofs"],
               [174, "Existing mapping rows", "174 distinct original entities; some rows group multiple concepts"],
               [340, "Existing service/concept spelling aliases", "340 represented entities"],
               [65, "Registered retained/native/normalized profiles", "65 implemented adapters or enforced native payload schemas"],
           ]),
           "### Source semantic kinds\n",
           table(["Source semantic kind", "Fixed diagram population", "Broader catalog"], [[kind, report["diagramSemanticKinds"].get(kind, 0), report["catalogSemanticKinds"].get(kind, 0)] for kind in KINDS]),
           "The kinds describe the source role as reviewed in the original solution. NATIVE_RESOURCE denotes an identity-bearing provider object in that solution; APPLICATION_ENTITY denotes an application-owned substantive object. HISTORY_REPRESENTATION is intentionally separate and maps to an owner's ordinary version/evidence mechanism. These labels are review classifications, not claims that all AWS SDK shapes are domain entities.\n",
           "### Broader dictionary and native-shape audit\n",
           table(["Population", "Total", "Normalized", "Partial", "Retained only", "Unmapped"], [[label, counts["total"], *[counts[level] for level in LEVELS]] for label, counts in [("Diagram + named dictionary/control concepts", report["catalogCoverage"]), ("52 selected DevOps SDK types (separate)", report["nativeShapeCoverageCounts"])]]),
           "The broader catalog can expose missing semantics that were not drawn in a diagram. It is not added to the diagram or native-shape populations. [Every audited concept and its proof](coverage/CATALOG.md).\n",
           "## 4. How source entities contribute to the 36-entity model\n",
           f"The registry's `canonicalEntity` rows name **{len(model['declaredEntityTargetsFromAwsSolutions'])} distinct target entities** across the four AWS solutions. Including the application workflow names **{len(model['declaredEntityTargetsIncludingWorkflow'])} of 36**. The remaining target is **Workspace**, introduced as a shared application boundary from earlier scope/context requirements. These are declared lineage counts; a partial source mapping remains partial even if its target entity exists.\n",
           table(["Source package", "Registry mapping rows", "Aliases", "Distinct targets of canonicalEntity rows"], [[SERVICE_NAMES[item["sourceService"]], item["mappingRows"], item["aliases"], item["declaredEntityTargetCount"]] for item in report["registry"]["byService"]]),
           "Per-package target sets overlap through Source, Observation, Collection, Command and other shared entities, so these target counts must not be summed. The [machine report](coverage/report.json) lists the exact sets.\n",
           "All 36 target entities pass the uniform version-field check. The model has 64 owned value definitions and five typed Projection result profiles. A schema reachability check finds **EventDescription** declared but unreachable from any entity: defining a type alone does not bind it into the model.\n",
           "## 5. Findings and decisions\n"]
    for index, finding in enumerate(report["findings"], 1):
        if isinstance(finding, str):
            out.append(f"### Finding {index}\n\n{finding}\n")
            continue
        title = finding.get("title") or finding.get("id") or f"Finding {index}"
        out.append(f"### {finding.get('id', f'F-{index:02d}')} — {title}\n")
        for key, label in [("severity", "Priority"), ("summary", "Finding"), ("finding", "Finding"), ("description", "Finding"), ("evidence", "Evidence"), ("impact", "Impact"), ("recommendation", "Recommended decision"), ("remediation", "Recommended correction")]:
            if finding.get(key):
                value = finding[key]
                if key == "evidence":
                    value = " · ".join(evidence_markdown(item) for item in value) if isinstance(value, list) else evidence_markdown(value)
                elif isinstance(value, list):
                    value = "; ".join(item if isinstance(item, str) else json.dumps(item, ensure_ascii=False) for item in value)
                elif isinstance(value, dict):
                    value = json.dumps(value, ensure_ascii=False)
                out.append(f"**{label}.** {value}\n")
        affected = finding.get("affectedConstructIds", finding.get("affectedConstructs", finding.get("constructIds", [])))
        if affected:
            out.append("**Affected constructs.** " + ", ".join(f"`{item}`" for item in affected) + ".\n")
    out += ["## 6. Mapping rules and consolidation path\n",
            "The [20-rule mapping catalog](MAPPING_RULES.md) makes the representation decision explicit. Its central boundary is: a substantive identity/lifecycle can justify an entity; details with one owner become typed values; versions remain on the substantive entity; interpretations need typed profiles; broad native DTOs may remain retained evidence with that limitation stated. Each audited construct links to the applicable rules.\n",
            "Close gaps in this order:\n\n1. Correct crosswalk/coverage claims so ownedValue or canonicalEntity labels cannot be mistaken for complete normalized support. Preserve the existing raw-source retention paths.\n2. Bind already defined but unbound values and add only the missing owner-local structures required by existing use cases. Preserve one version and one write authority per owner.\n3. Resolve identity/join, contextual-error, graph/evaluation and historical-capture distinctions before claiming source-model parity. Add semantic fixtures for each promised distinction.\n4. Make an explicit scope decision for native administrative breadth and presentation-oriented views: keep them retained-only or add a narrow typed profile when needed.\n5. Implement and test adapters, current authorization, persistence, replay and provider reconciliation at the later gates. Model coverage alone is not runtime coverage.\n",
            "No gap in this audit justifies a version-only entity. The audit leaves the 36-entity schema and 108-operation contract unchanged; it identifies evidence-backed decisions for the next model correction.\n",
            "## 7. Verification and reproducibility\n",
            "```bash\npython consolidated-operations-console/tools/build_coverage.py\npython consolidated-operations-console/tools/build_coverage.py --check\n```\n",
            "The builder independently extracts the 130 source declarations, requires each to resolve exactly once, verifies the selected 52 SDK types, resolves every claimed schema pointer/profile and source heading/symbol, checks all 36 entity version contracts, and regenerates the catalog, counts and rulebook deterministically. It also requires the current model, registry and API contracts to match the pinned target review commit. If a contract changes, review the affected catalog judgments and deliberately update that baseline before claiming current coverage. Semantic judgments are documented review conclusions; pointer existence and a green alias check alone do not prove them.\n",
            "The source evidence is frozen to the original repository analyses and their 226-file inventory. This audit does not claim all current AWS resources/SDK fields, live-account behavior, migration execution or implemented provider adapters.\n",
            "## Files\n\n- [coverage/CATALOG.md](coverage/CATALOG.md): every construct, source evidence, mapping proof, status and applicable rules.\n- [coverage/catalog.json](coverage/catalog.json): machine-readable merged catalog and fixed diagram benchmark.\n- [coverage/report.json](coverage/report.json): counts, source hashes, findings and exact input hashes.\n- [MAPPING_RULES.md](MAPPING_RULES.md): human-readable mapping decisions.\n- [coverage/mapping-rules.json](coverage/mapping-rules.json): rule catalog source.\n"]
    return "\n".join(out).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog, report, rules = assemble()
    outputs = {
        "coverage/catalog.json": json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        "coverage/report.json": json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        "coverage/CATALOG.md": construct_catalog(catalog),
        "MAPPING_RULES.md": rulebook(rules),
        "COVERAGE.md": overview(catalog, report),
    }
    for path, content in outputs.items():
        if args.check:
            require((ROOT/path).exists() and (ROOT/path).read_text(encoding="utf-8") == content, f"Stale coverage output: {path}")
        else:
            (ROOT/path).write_text(content, encoding="utf-8")
    print("PASS: independent coverage population, catalog references and generated outputs" + (" are current." if args.check else " generated."))
    print(json.dumps({"aws": report["awsDiagramCoverage"], "workflow": report["workflowDiagramCoverage"], "all": report["allDiagramCoverage"], "catalog": report["catalogCoverage"], "nativeShapes": report["nativeShapeCoverageCounts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
