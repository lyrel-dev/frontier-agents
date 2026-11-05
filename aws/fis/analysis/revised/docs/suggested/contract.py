"""Static proposal checks and small reference decision functions; not a runner.

The decision functions consume already authenticated/normalized facts. They do not
discover evidence coverage, implement atomic storage, compile CEL, or contact AWS.
"""
from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
DIAGRAM_ROOT = ROOT.parents[1] / "diagrams" / "suggested"
SCHEMA = json.loads((ROOT / "scenario.schema.json").read_text())
CATALOGUE = json.loads((ROOT / "operation-catalog.json").read_text())
DIAGRAM_FILES = ("01_entities.mmd", "02_owned_values.mmd", "03_lifecycle.mmd")
BINDING = re.compile(r"^\$\{\{\s*(.*?)\s*\}\}$", re.S)
REFERENCE = re.compile(r"\b(inputs|bindings|steps)\.([A-Za-z][A-Za-z0-9_]*)(?:\.([A-Za-z][A-Za-z0-9_]*))?(?:\.([A-Za-z][A-Za-z0-9_]*))?")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class ContractError(ValueError):
    """Invalid proposal document or normalized reference facts."""


class UniqueLoader(yaml.SafeLoader):
    """Reject YAML duplicate keys before a parser can discard a step."""


# Use YAML 1.2 boolean spellings; a retry key named `on` must stay a string.
UniqueLoader.yaml_implicit_resolvers = {
    key: [(tag, regex) for tag, regex in values if tag != "tag:yaml.org,2002:bool"]
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
UniqueLoader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|false|True|False|TRUE|FALSE)$"), list("tTfF"))


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ContractError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_document(path):
    return yaml.load(Path(path).read_text(), Loader=UniqueLoader)


def digest(value):
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def check_json(value, schema, location):
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value), key=lambda e: str(list(e.path)))
    if errors:
        error = errors[0]
        path = ".".join(map(str, error.path))
        raise ContractError(f"{location}{'.' + path if path else ''}: {error.message}")


def check_literal(value, schema, location):
    """Check known literals; typed expressions require a future CEL compiler."""
    if isinstance(value, str) and BINDING.fullmatch(value):
        return
    if "oneOf" in schema:
        valid = []
        for branch in schema["oneOf"]:
            try:
                check_literal(value, branch, location)
                valid.append(branch)
            except ContractError:
                pass
        if len(valid) != 1:
            raise ContractError(f"{location}: must match exactly one operation input form")
        return
    if schema.get("type") == "object" and isinstance(value, dict):
        required = set(schema.get("required", []))
        if not required.issubset(value):
            raise ContractError(f"{location}: missing {sorted(required - set(value))}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and set(value) - set(properties):
            raise ContractError(f"{location}: unknown fields {sorted(set(value) - set(properties))}")
        for key, item in value.items():
            if key in properties:
                check_literal(item, properties[key], f"{location}.{key}")
        return
    if schema.get("type") == "array" and isinstance(value, list):
        for index, item in enumerate(value):
            check_literal(item, schema.get("items", {}), f"{location}[{index}]")
        check_json(value, {k: v for k, v in schema.items() if k != "items"}, location)
        return
    check_json(value, schema, location)


def expression_strings(value):
    if isinstance(value, str):
        match = BINDING.fullmatch(value)
        if match:
            yield match.group(1)
    elif isinstance(value, dict):
        for item in value.values():
            yield from expression_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from expression_strings(item)


def alias_operations(catalogue):
    """Current authoring aliases; published admission uses retained digests."""
    return {alias: catalogue["revisions"][ref] for alias, ref in catalogue["aliases"].items()}


def validate_document(document, catalogue=CATALOGUE):
    Draft202012Validator.check_schema(SCHEMA)
    check_json(document, SCHEMA, "scenario")
    Draft202012Validator.check_schema(document["inputs"])
    inputs = document["inputs"]["properties"]
    if set(document["inputs"]["required"]) - set(inputs):
        raise ContractError("inputs.required names an undeclared input")
    bindings = document["bindings"]
    main, finalizers = document["steps"], document.get("finally", {})
    if set(main) & set(finalizers):
        raise ContractError("step keys must be unique across main and finalization graphs")
    all_steps = {**main, **finalizers}
    operations = alias_operations(catalogue)
    ancestors = {}

    for phase, graph in (("main", main), ("finalizer", finalizers)):
        visiting = set()

        def visit(key):
            if key in visiting:
                raise ContractError(f"cycle in {phase} graph at {key}")
            if key in ancestors:
                return ancestors[key]
            visiting.add(key)
            result = set()
            for predecessor in graph[key].get("needs", []):
                if predecessor not in graph:
                    raise ContractError(f"{key}: dependency {predecessor} is not in its {phase} graph")
                if predecessor == key:
                    raise ContractError(f"{key}: self dependency")
                result.add(predecessor)
                result.update(visit(predecessor))
            visiting.remove(key)
            ancestors[key] = result
            return result

        for key in graph:
            visit(key)

    for key, step in all_steps.items():
        phase = "main" if key in main else "finalizer"
        alias = step["uses"]
        if alias not in operations:
            raise ContractError(f"{key}: unknown operation {alias}")
        operation = operations[alias]
        if step.get("assessmentRole") and not operation["isCheck"]:
            raise ContractError(f"{key}: assessment role requires a check operation")
        if operation["isCheck"] and "assessmentRole" not in step:
            raise ContractError(f"{key}: check operation requires an explicit assessment role")
        if phase == "finalizer" and any(field in step for field in ("if", "enabledWhen", "assessmentRole")):
            raise ContractError(f"{key}: finalizers are unconditional cleanup, with adapter-proven no-ops")
        if phase == "main" and operation["effect"] == "compensate":
            raise ContractError(f"{key}: compensation operation belongs in the finalization graph")
        if phase == "finalizer" and operation["effect"] != "compensate":
            raise ContractError(f"{key}: v0.2 finalizers are cleanup operations")
        if phase == "main" and operation["effect"] == "mutate" and step.get("after", "success") == "settled":
            raise ContractError(f"{key}: settled main mutation forbidden")
        if phase == "finalizer" and step.get("after", "settled") != "settled":
            raise ContractError(f"{key}: finalization dependencies require settled semantics")
        if operation["isCheck"] and step.get("retry", {}).get("maxAttempts", 1) > 1:
            raise ContractError(f"{key}: assertion retries cannot turn false into passed")
        if step.get("retry", {}).get("maxAttempts", 1) > 1 and not operation["safeNewAttemptRetry"]:
            raise ContractError(f"{key}: operation does not authorize a new-attempt retry")
        budget = document["policies"]["timeoutSeconds" if phase == "main" else "finalizationTimeoutSeconds"]
        if step["timeoutSeconds"] > budget:
            raise ContractError(f"{key}: step timeout exceeds its graph budget")
        check_literal(step["with"], operation["inputSchema"], f"steps.{key}.with")

        expressions = list(expression_strings(step["with"]))
        expressions.extend(step[field] for field in ("if", "enabledWhen") if field in step)
        if operation["isCheck"] and "expect" in step["with"]:
            expressions.append(step["with"]["expect"])
        if "enabledWhen" in step and re.search(r"\b(steps|bindings|value)\b", step["enabledWhen"]):
            raise ContractError(f"{key}: enabledWhen may use only inputs and deployment")
        allowed = ancestors[key] | (set(main) if phase == "finalizer" else set())
        for expression in expressions:
            for namespace, name, member, output in REFERENCE.findall(expression):
                if namespace == "inputs" and name not in inputs:
                    raise ContractError(f"{key}: undeclared input {name}")
                if namespace == "bindings" and name not in bindings:
                    raise ContractError(f"{key}: undeclared binding {name}")
                if namespace == "steps":
                    if name not in all_steps:
                        raise ContractError(f"{key}: reference to unknown step {name}")
                    if name not in allowed:
                        raise ContractError(f"{key}: reference to non-ancestor step {name}")
                    if member not in ("ref", "execution", "outputs", "check"):
                        raise ContractError(f"{key}: unsupported step projection member {member}")
                    if member == "outputs" and output:
                        output_fields = operations[all_steps[name]["uses"]]["outputSchema"].get("properties", {})
                        if output not in output_fields:
                            raise ContractError(f"{key}: undeclared output {name}.{output}")
    return {"steps": len(main), "finalizers": len(finalizers), "criteria": [k for k, s in main.items() if s.get("assessmentRole") == "criterion"]}


def make_lock(document, catalogue=CATALOGUE):
    """Produce a synthetic review lock, not a production publication compiler."""
    validate_document(document, catalogue)
    aliases = sorted({step["uses"] for graph in (document["steps"], document.get("finally", {})) for step in graph.values()})
    entries = {}
    for alias in aliases:
        operation = alias_operations(catalogue)[alias]
        entries[alias] = {
            "implementationDigest": operation["implementationDigest"],
            "inputSchemaDigest": digest(operation["inputSchema"]),
            "outputSchemaDigest": digest(operation["outputSchema"]),
            "capabilityDigest": digest({field: operation[field] for field in ("effect", "isCheck", "safeNewAttemptRetry", "sideEffects")}),
        }
    lock = {"schemaVersion": "assessment-lock/0.2", "synthetic": True, "programDigest": digest(document), "expressionContract": "cel/assessment-v0.2", "reducerVersion": "assessment-reducer/0.2", "operations": entries}
    return {**lock, "digest": digest(lock)}


def validate_lock(document, lock, catalogue=CATALOGUE):
    if set(lock) != {"schemaVersion", "synthetic", "programDigest", "expressionContract", "reducerVersion", "operations", "digest"}:
        raise ContractError("invalid published lock shape")
    body = {key: value for key, value in lock.items() if key != "digest"}
    if lock["digest"] != digest(body) or lock["programDigest"] != digest(document):
        raise ContractError("published lock does not match the fixed program or integrity digest")
    if lock["schemaVersion"] != "assessment-lock/0.2" or lock["expressionContract"] != "cel/assessment-v0.2" or lock["reducerVersion"] != "assessment-reducer/0.2":
        raise ContractError("unsupported pinned contract version")
    aliases = {step["uses"] for graph in (document["steps"], document.get("finally", {})) for step in graph.values()}
    if aliases != set(lock["operations"]):
        raise ContractError("published lock has missing or extraneous operation contracts")
    pinned_aliases = {}
    for alias, entry in lock["operations"].items():
        if set(entry) != {"implementationDigest", "inputSchemaDigest", "outputSchemaDigest", "capabilityDigest"} or any(not isinstance(value, str) or not DIGEST.fullmatch(value) for value in entry.values()):
            raise ContractError("lock contains a non-digest dependency")
        ref = entry["implementationDigest"]
        if ref not in catalogue["revisions"] or ref in catalogue.get("revokedDigests", []):
            raise ContractError(f"pinned operation unavailable or revoked: {alias}")
        operation = catalogue["revisions"][ref]
        expected = {
            "implementationDigest": operation["implementationDigest"],
            "inputSchemaDigest": digest(operation["inputSchema"]),
            "outputSchemaDigest": digest(operation["outputSchema"]),
            "capabilityDigest": digest({field: operation[field] for field in ("effect", "isCheck", "safeNewAttemptRetry", "sideEffects")}),
        }
        if entry != expected or operation["operationAlias"] != alias:
            raise ContractError(f"pinned operation contract mismatch: {alias}")
        pinned_aliases[alias] = ref
    validate_document(document, {**catalogue, "aliases": pinned_aliases})


def assessment(case):
    required = case["requiredCriteria"]
    if len(required) != len(set(required)):
        raise ContractError("duplicate required criterion")
    final = case["final"]
    counts = dict(passedCount=0, failedCount=0, inconclusiveCount=0, pendingCount=0)
    results = case["results"]
    for key in required:
        value = results.get(key)
        field = {"passed": "passedCount", "failed": "failedCount", "inconclusive": "inconclusiveCount"}.get(value)
        if field is None:
            field = "inconclusiveCount" if final or key in results else "pendingCount"
        counts[field] += 1
    verdict = "not_evaluated" if not required else "failed" if counts["failedCount"] else "passed" if counts["passedCount"] == len(required) else "inconclusive"
    return {"verdict": verdict, "final": final, "requiredCount": len(required), **counts}


def eligibility(case):
    main = case["phase"] == "main"
    if main and case["effect"] == "mutate" and case["after"] == "settled":
        return {"decision": "reject", "reasonCode": "SETTLED_MUTATION_FORBIDDEN"}
    if main and case["cancellationAccepted"]:
        return {"decision": "skip", "reasonCode": "RUN_CANCELLED"}
    if any(value is None for value in case["dependencyOutcomes"].values()):
        return {"decision": "wait", "reasonCode": "DEPENDENCY_PENDING"}
    if main and case["effect"] == "mutate" and any(v != "passed" for v in case["preconditionVerdicts"].values()):
        return {"decision": "skip", "reasonCode": "PRECONDITION_NOT_PASSED"}
    if case["after"] == "success" and any(v != "succeeded" for v in case["dependencyOutcomes"].values()):
        return {"decision": "skip", "reasonCode": "DEPENDENCY_UNSUCCESSFUL"}
    return {"decision": "run", "reasonCode": "ELIGIBLE"}


def proof(case):
    def result(verdict, reason):
        return {"verdict": verdict, "reasonCode": reason}
    if case["sourceTrusted"] is not True:
        return result("inconclusive", "UNTRUSTED_SOURCE")
    if case["collection"] not in ("complete", "partial"):
        return result("inconclusive", "INSUFFICIENT_EVIDENCE")
    if case["proof"] == "witness" and (type(case.get("matchingRecords")) is not int or case["matchingRecords"] < 0):
        raise ContractError("matchingRecords must be a nonnegative integer")
    if case["proof"] == "witness" and case["matchingRecords"] > 0:
        return result("passed", "QUALIFYING_WITNESS")
    if case["collection"] != "complete" or case["coverage"] != "sufficient":
        return result("inconclusive", "INSUFFICIENT_EVIDENCE")
    if not case["windowClosed"]:
        return result("inconclusive", "WINDOW_OPEN")
    if case["proof"] == "witness":
        return result("failed", "NO_WITNESS_IN_COVERED_WINDOW")
    if case["proof"] != "complete" or type(case.get("predicateValue")) is not bool:
        raise ContractError("expected a typed boolean predicate or exists witness mode")
    value = case["predicateValue"]
    return result("passed" if value else "failed", "PREDICATE_TRUE" if value else "PREDICATE_FALSE")


def cancellation(case):
    if case["tokenReplay"]:
        if not case["payloadMatches"]:
            return {"decision": "conflict", "httpStatus": 409, "newIntent": False, "reasonCode": "IdempotencyConflict"}
        return {"decision": "replay", **case["recordedReceipt"], "newIntent": False}
    if case["runSealed"]:
        return {"decision": "no_op", "httpStatus": 200, "accepted": False, "newIntent": False, "reasonCode": "RUN_ALREADY_FINISHED"}
    if case["existingIntent"]:
        return {"decision": "join_existing", "httpStatus": 202, "accepted": True, "newIntent": False, "replaceOriginalIntent": False}
    return {"decision": "accept", "httpStatus": 202, "accepted": True, "newIntent": True, "fenceMainDispatch": True}


def termination(case):
    unresolved = case["unresolvedEffects"] > 0
    if not unresolved and not case["requiredFinalizersSucceeded"] and not (case["substantiveFailure"] or case["deadlineTermination"]):
        raise ContractError("incomplete required finalization needs a failure or deadline cause")
    outcome = (
        "indeterminate" if unresolved else
        "failed" if case["substantiveFailure"] else
        "timed_out" if case["deadlineTermination"] else
        "cancelled" if case["cancellationAccepted"] else
        "blocked" if case["preconditionBlocked"] else "succeeded"
    )
    return {"outcome": outcome, "finalizationStatus": "complete" if not unresolved and case["requiredFinalizersSucceeded"] else "incomplete", "retainScopeHold": unresolved}


DECISIONS = {name: globals()[name] for name in ("assessment", "eligibility", "proof", "cancellation", "termination")}


def check_package():
    summaries = []
    for path in sorted((ROOT / "examples").glob("*.yaml")):
        document = read_document(path)
        summaries.append((path.name, validate_document(document)))
        validate_lock(document, json.loads(path.with_suffix(".lock.json").read_text()))
    for alias, operation in alias_operations(CATALOGUE).items():
        for field in ("inputSchema", "outputSchema"):
            Draft202012Validator.check_schema(operation[field])
        if not DIGEST.fullmatch(operation["implementationDigest"]):
            raise ContractError(f"{alias}: invalid synthetic implementation digest")
    blocks = re.findall(r"```mermaid\n(.*?)\n```", (ROOT / "model.md").read_text(), re.S)
    if len(blocks) != len(DIAGRAM_FILES):
        raise ContractError("unexpected diagram membership")
    for filename, block in zip(DIAGRAM_FILES, blocks):
        if (DIAGRAM_ROOT / filename).read_text() != block + "\n":
            raise ContractError(f"stale embedded diagram: {filename}")
    manifest = json.loads((DIAGRAM_ROOT / "manifest.json").read_text())
    raw_hash = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    if manifest["rendererSha256"] != raw_hash(ROOT / "tools/render-diagrams.mjs"):
        raise ContractError("workflow diagram renderer changed since recorded render")
    if {item["source"] for item in manifest["diagrams"]} != set(DIAGRAM_FILES):
        raise ContractError("workflow diagram manifest membership differs")
    for item in manifest["diagrams"]:
        for field, hash_field in (("source", "sourceSha256"), ("rendered", "svgSha256")):
            if raw_hash(DIAGRAM_ROOT / item[field]) != item[hash_field]:
                raise ContractError(f"workflow diagram bytes differ: {item[field]}")
        svg = ET.parse(DIAGRAM_ROOT / item["rendered"]).getroot()
        if svg.tag != "{http://www.w3.org/2000/svg}svg" or svg.find("{http://www.w3.org/2000/svg}title") is None:
            raise ContractError(f"workflow diagram is not a titled SVG: {item['rendered']}")
    cases = json.loads((ROOT / "review-cases.json").read_text())["cases"]
    if len({case["id"] for case in cases}) != len(cases):
        raise ContractError("duplicate review case ID")
    for case in cases:
        actual = DECISIONS[case["category"]](case["input"])
        if actual != case["expected"]:
            raise ContractError(f"review case {case['id']}: {actual} != {case['expected']}")
    for name, summary in summaries:
        print(f"{name}: {summary['steps']} main steps, {summary['finalizers']} finalizers, {len(summary['criteria'])} declared criteria; synthetic lock verified")
    print(f"Verified {len(cases)} independent decision cases and {len(blocks)} canonical diagrams. No workflows or CEL executed.")


if __name__ == "__main__":
    check_package()
