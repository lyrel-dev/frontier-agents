#!/usr/bin/env python3
"""Audit the authored API catalog against an explicitly supplied, pinned AWS model.

No network is used unless --fetch is requested. This checks documentation against
the model; it is not an AWS payload validator, collector, or account-level test.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
PIN_COMMIT = "27fc40eff0e85422e62858ee3d2e9a133bdb1038"
PIN_URL = (
    "https://raw.githubusercontent.com/boto/botocore/" + PIN_COMMIT
    + "/botocore/data/devops-agent/2026-01-01/service-2.json"
)
PIN_SHA256 = "c9650e8c0aa3546f3f45ecb829f96223156bfc07f720b580bed23a7407aaad59"
CATALOG = ROOT / "annexes/Investigation_API_Catalog.md"
INVENTORY = ROOT / "qa/native-api-inventory.json"
EVIDENCE = ROOT / "qa/native-api-audit.json"

REQUEST_OPERATIONS = (
    "CreateBacklogTask", "GetBacklogTask", "ListBacklogTasks", "UpdateBacklogTask",
    "ListExecutions", "ListJournalRecords", "ListPendingMessages", "CreateChat",
    "ListChats", "SendMessage", "UpdateApprovalAction", "ListAssets", "GetAsset",
    "ListAssetVersions", "GetAssetContent", "GetAssetFile", "ListAssetFiles",
    "ListRecommendations", "UpdateRecommendation",
)
SELECTED_TYPES = (
    "Task", "TaskFilter", "ReferenceInput", "ReferenceOutput", "Execution",
    "JournalRecord", "UserReference", "ChatExecution", "PendingMessage", "Message",
    "UserMessageBlock", "AssistantMessageBlock", "SendMessageContext",
    "ApprovalAction", "ApprovalPattern", "SendMessageEvents",
    "SendMessageResponseCreatedEvent", "SendMessageResponseInProgressEvent",
    "SendMessageResponseCompletedEvent", "SendMessageResponseFailedEvent",
    "SendMessageContentBlockStartEvent", "SendMessageContentBlockDeltaEvent",
    "SendMessageContentBlockDelta", "SendMessageTextDelta", "SendMessageJsonDelta",
    "SendMessageContentBlockStopEvent", "SendMessageSummaryEvent",
    "SendMessageHeartbeatEvent", "SendMessageUsageInfo", "Asset",
    "AssetVersionMetadata", "AssetTypeSummary", "AssetContent", "AssetFile",
    "AssetFileBody", "AssetFileContent", "AssetFileSummary", "AssetSourceUrlContent",
    "AssetZipContent", "AgentSpace", "RegisteredService", "Association",
    "ServiceConfiguration", "Recommendation", "RecommendationContent", "Goal",
    "GoalContent", "Trigger", "TriggerCondition", "Webhook",
    "PrivateConnectionSummary", "UsageMetric",
)


def digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def cells(line: str) -> list[str]:
    """Split GFM table cells without splitting an escaped regex alternation."""
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip()[1:-1])]


def section(text: str, number: int) -> str:
    match = re.search(rf"^## {number}\. [^\n]+\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise ValueError(f"Missing catalog section {number}")
    return match.group(1)


def subsections(text: str) -> dict[str, str]:
    parts = re.findall(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", text, re.M | re.S)
    if len(parts) != len({name for name, _ in parts}):
        raise ValueError("Duplicate catalog subsection")
    return dict(parts)


def display_type(shapes: dict, name: str) -> str:
    shape = shapes[name]
    kind = shape["type"]
    if shape.get("document"):
        return "`JSON document`"
    if kind == "list":
        return f"`list<{shape['member']['shape']}>`"
    if kind == "map":
        return f"`map<{shape['key']['shape']}, {shape['value']['shape']}>`"
    suffix = " union" if shape.get("union") else ""
    return f"`{name} ({kind}{suffix})`"


def constraint_text(shapes: dict, name: str, member: dict | None = None) -> str:
    shape = shapes[name]
    result = []
    for key in ("min", "max"):
        if key in shape:
            result.append(f"{key} {shape[key]}")
    if "pattern" in shape:
        result.append("pattern `" + shape["pattern"].replace("|", "\\|") + "`")
    if "enum" in shape:
        result.append(" / ".join(f"`{value}`" for value in shape["enum"]))
    if "timestampFormat" in shape:
        result.append("format " + shape["timestampFormat"])
    if shape.get("document"):
        result.append("any JSON value; nested schema not defined here")
    if shape.get("union"):
        result.append("one member")
    member = member or {}
    if member.get("idempotencyToken"):
        result.append("idempotency token")
    if member.get("deprecated"):
        result.append("deprecated; see API documentation")
    return "; ".join(result) or "—"


def field_rows(model: dict, name: str, request: bool) -> list[list[str]]:
    shapes = model["shapes"]
    shape = shapes[name]
    required = set(shape.get("required", []))
    rows = []
    for field, member in shape.get("members", {}).items():
        ref = member["shape"]
        row = [f"`{field}`", "Yes" if field in required else "No"]
        type_label = display_type(shapes, ref)
        constraints = constraint_text(shapes, ref, member)
        if request:
            row.extend([member.get("location", "body"), type_label + "; " + constraints])
        else:
            row.extend([type_label, constraints])
        rows.append(row)
    return rows


def error_group(operation: dict) -> str:
    names = {error["shape"] for error in operation.get("errors", [])}
    return "E+IDC" if "IdentityCenterServiceException" in names else "E"


def audit_catalog(model: dict, text: str) -> tuple[list[str], dict]:
    errors = []
    operations = model["operations"]
    shapes = model["shapes"]
    operation_rows = {}
    for line in section(text, 1).splitlines():
        if not line.startswith("| ["):
            continue
        row = cells(line)
        match = re.fullmatch(r"\[([A-Za-z0-9]+)\]\(https://docs\.aws\.amazon\.com/devopsagent/latest/APIReference/API_\1\.html\)", row[0])
        if not match:
            errors.append("Unrecognized operation link: " + row[0])
            continue
        name = match.group(1)
        if name in operation_rows:
            errors.append("Duplicate operation: " + name)
        operation_rows[name] = row
    if set(operation_rows) != set(operations):
        errors.append("Operation inventory differs from the pinned model")
    for name, operation in operations.items():
        output = shapes[operation["output"]["shape"]].get("members", {}) if "output" in operation else {}
        expected = [
            f"[{name}](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_{name}.html)",
            f"`{operation['http']['method']} {operation['http']['requestUri']}`",
            ", ".join(f"`{field}`" for field in output) or "Acknowledgement",
        ]
        if operation_rows.get(name) != expected:
            errors.append("Operation route/response mismatch: " + name)

    request_sections = subsections(section(text, 2))
    type_sections = subsections(section(text, 3))
    if list(request_sections) != list(REQUEST_OPERATIONS):
        errors.append("Detailed request selection/order differs from the declared 19-table scope")
    if list(type_sections) != list(SELECTED_TYPES):
        errors.append("Selected type selection/order differs from the declared 52-table scope")
    table_fingerprints = {"requests": {}, "types": {}}
    member_count = 0
    for request, names, sections in ((True, REQUEST_OPERATIONS, request_sections), (False, SELECTED_TYPES, type_sections)):
        for name in names:
            shape_name = operations[name]["input"]["shape"] if request else name
            body = sections.get(name, "")
            actual = [cells(line) for line in body.splitlines() if re.match(r"^\| `[A-Za-z0-9_]+` \|", line)]
            expected = field_rows(model, shape_name, request)
            if actual != expected:
                errors.append("Member/type/constraint mismatch: " + name)
            if not request:
                shape = shapes[name]
                if bool(shape.get("union")) != ("**Union: select one member.**" in body):
                    errors.append("Union declaration mismatch: " + name)
                if bool(shape.get("eventstream")) != ("**Streaming union: one event variant per event.**" in body):
                    errors.append("Streaming declaration mismatch: " + name)
                if not expected and "No modeled members." not in body:
                    errors.append("Missing empty-structure declaration: " + name)
            member_count += len(expected)
            table_fingerprints["requests" if request else "types"][name] = digest(expected)

    transport = {}
    for line in section(text, 6).splitlines():
        if re.match(r"^\| `[A-Za-z0-9]+` \| `(?:cp|dp)\.`,? \|", line):
            row = cells(line)
            name = row[0].strip("`")
            if name in transport:
                errors.append("Duplicate transport operation: " + name)
            transport[name] = row
    if set(transport) != set(operations):
        errors.append("Transport/error-set inventory differs from the pinned model")
    for name, operation in operations.items():
        expected = [f"`{name}`", f"`{operation['endpoint']['hostPrefix']}`", str(operation['http']['responseCode']), error_group(operation)]
        if transport.get(name) != expected:
            errors.append("Endpoint/success/error-group mismatch: " + name)

    common_errors = set.intersection(*({e["shape"] for e in op["errors"]} for op in operations.values()))
    extra_errors = {"IdentityCenterServiceException"}
    for name, operation in operations.items():
        actual = {e["shape"] for e in operation["errors"]}
        expected = common_errors | (extra_errors if error_group(operation) == "E+IDC" else set())
        if actual != expected:
            errors.append("Error-group definition no longer represents operation: " + name)
    error_rows = {}
    for line in section(text, 6).splitlines():
        if re.match(r"^\| `[A-Za-z0-9]+Exception` \|", line):
            row = cells(line)
            name = row[0].strip("`")
            if name in error_rows:
                errors.append("Duplicate error contract: " + name)
            error_rows[name] = row
    error_names = sorted(common_errors | extra_errors)
    if set(error_rows) != set(error_names):
        errors.append("Error contract table has missing or additional error types")
    for name in error_names:
        shape = shapes[name]
        status = shape.get("error", {}).get("httpStatusCode")
        expected_status = str(status) if status is not None else "Not modeled; documented 400"
        member_names = ", ".join(f"`{member}`" for member in shape.get("members", {}))
        expected_prefix = [f"`{name}`", expected_status, member_names]
        if error_rows.get(name, [])[:3] != expected_prefix:
            errors.append("Error status/member mismatch: " + name)
    return errors, {"expandedMemberRows": member_count, "tableFingerprints": table_fingerprints}


def inventory(model: dict, detail: dict) -> dict:
    operations = []
    error_names = set()
    for name, op in sorted(model["operations"].items()):
        input_shape = model["shapes"][op["input"]["shape"]] if "input" in op else {}
        output_shape = model["shapes"][op["output"]["shape"]] if "output" in op else {}
        errors = sorted(error["shape"] for error in op.get("errors", []))
        error_names.update(errors)
        operations.append({
            "name": name, "method": op["http"]["method"], "route": op["http"]["requestUri"],
            "endpointHostPrefix": op["endpoint"]["hostPrefix"], "successStatus": op["http"]["responseCode"],
            "inputShape": op.get("input", {}).get("shape"), "outputShape": op.get("output", {}).get("shape"),
            "outputMembers": list(output_shape.get("members", {})), "errors": errors,
            "idempotentTrait": op.get("idempotent", False),
            "idempotencyTokenMembers": [name for name, m in input_shape.get("members", {}).items() if m.get("idempotencyToken")],
        })
    errors = {}
    for name in sorted(error_names):
        shape = model["shapes"][name]
        errors[name] = {
            "modeledHttpStatus": shape.get("error", {}).get("httpStatusCode"),
            "members": {field: member["shape"] for field, member in shape.get("members", {}).items()},
            "required": shape.get("required", []), "retryableTrait": shape.get("retryable"),
        }
    return {
        "schemaVersion": "native-api-inventory/v1", "sourceUrl": PIN_URL,
        "sourceSha256": PIN_SHA256, "apiVersion": model["metadata"]["apiVersion"],
        "signingName": model["metadata"]["signingName"], "protocol": model["metadata"]["protocol"],
        "operationCount": len(operations), "enumeratedShapeCount": len(model["shapes"]),
        "shapeNames": sorted(model["shapes"]),
        "endpointPrefixCounts": dict(sorted(Counter(op["endpointHostPrefix"] for op in operations).items())),
        "errorGroups": {
            "E": sorted(set.intersection(*(set(op["errors"]) for op in operations))),
            "E+IDC": sorted(error_names),
        },
        "operations": operations, "errorShapes": errors,
        "selectedTableFingerprints": detail["tableFingerprints"],
        "fingerprintEncoding": "SHA-256 of UTF-8 compact sorted-key JSON of expected catalog rows",
        "limits": [
            "All 560 shape names are inventoried; only 19 request and 52 selected type tables are expanded and compared.",
            "ValidationException HTTP 400 is documented by the AWS API reference but is not an error.httpStatusCode trait in this Botocore snapshot.",
            "No live service, authorization, journal profile, transition, event-delivery, retention or application HTTP contract is validated.",
        ],
    }


def negative_controls(model: dict, text: str) -> list[str]:
    changes = [
        ("route", "`POST /journal/agent-space/{agentSpaceId}/journalRecords`", "`GET /journal/agent-space/{agentSpaceId}/journalRecords`"),
        ("required field", "| `taskId` | Yes | `String (string)`", "| `taskId` | No | `String (string)`"),
        ("document type", "`JSON document`", "`String (string)`"),
        ("enum", " / `WAITING`", " / `INVENTED_STATE`"),
        ("page limit", "`ListJournalRecordsRequestLimitInteger (integer)`; min 1; max 100", "`ListJournalRecordsRequestLimitInteger (integer)`; min 1; max 1000"),
        ("endpoint prefix", "| `CreateBacklogTask` | `dp.` | 201 | E |", "| `CreateBacklogTask` | `cp.` | 201 | E |"),
        ("success status", "| `GetBacklogTask` | `dp.` | 200 | E |", "| `GetBacklogTask` | `dp.` | 201 | E |"),
        ("error group", "| `ListExecutions` | `dp.` | 200 | E |", "| `ListExecutions` | `dp.` | 200 | E+IDC |"),
        ("union", "**Union: select one member.**", "Ordinary structure."),
    ]
    passed = []
    for label, before, after in changes:
        if before not in text:
            raise ValueError("Negative-control anchor missing: " + label)
        errors, _ = audit_catalog(model, text.replace(before, after, 1))
        if not errors:
            raise ValueError("Checker failed to detect negative control: " + label)
        passed.append(label)
    return passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--model", type=Path, help="Read a local pinned Botocore service-2.json; no network")
    source.add_argument("--fetch", action="store_true", help="Explicitly download the pinned official model")
    parser.add_argument("--write-evidence", action="store_true", help="Regenerate compact inventory and audit evidence after checks pass")
    parser.add_argument("--self-test", action="store_true", help="Run nine bounded negative controls against the catalog checker")
    args = parser.parse_args()
    raw = urllib.request.urlopen(PIN_URL, timeout=30).read() if args.fetch else args.model.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PIN_SHA256:
        raise ValueError("Model checksum differs from the review pin; review and update the pin deliberately")
    model = json.loads(raw)
    if model["metadata"]["apiVersion"] != "2026-01-01" or len(model["operations"]) != 63 or len(model["shapes"]) != 560:
        raise ValueError("Pinned model metadata/inventory mismatch")
    text = CATALOG.read_text(encoding="utf-8")
    errors, detail = audit_catalog(model, text)
    if errors:
        print("FAIL: " + "\nFAIL: ".join(errors), file=sys.stderr)
        return 1
    controls = negative_controls(model, text) if args.self_test else []
    compact = inventory(model, detail)
    evidence = {
        "schemaVersion": "native-api-audit/v1", "reviewDate": "2026-11-05",
        "modelSha256": PIN_SHA256, "catalogSha256": hashlib.sha256(text.encode()).hexdigest(),
        "operationRoutesAndTopLevelResponseFieldsChecked": 63, "transportAndErrorSetsChecked": 63,
        "requestTablesChecked": len(REQUEST_OPERATIONS), "selectedTypeTablesChecked": len(SELECTED_TYPES),
        "expandedMemberRowsChecked": detail["expandedMemberRows"],
        "checks": ["names/order", "requiredness", "type references", "enum/min/max/pattern/timestamp constraints", "request locations", "idempotency-token/deprecation markers", "union/eventstream declarations", "endpoint host prefixes", "success HTTP codes", "modeled error sets/statuses/member names"],
        "negativeControlsDetected": controls, "errors": [],
        "scope": "Static public-model/catalog verification. No AWS account or application HTTP service was exercised.",
    }
    if args.write_evidence:
        if not args.self_test:
            raise ValueError("Use --self-test with --write-evidence so published evidence includes negative controls")
        INVENTORY.write_text(json.dumps(compact, ensure_ascii=False, indent=2) + "\n")
        EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    else:
        if json.loads(INVENTORY.read_text()) != compact:
            raise ValueError("Committed API inventory differs; review changes before regenerating evidence")
        retained = json.loads(EVIDENCE.read_text())
        if retained["modelSha256"] != PIN_SHA256 or retained["catalogSha256"] != evidence["catalogSha256"]:
            raise ValueError("Committed audit evidence is stale; rerun with --self-test --write-evidence")
    print(f"PASS: 63 operations, 63 transport/error contracts, 19 requests, 52 types, {detail['expandedMemberRows']} member rows; pinned model verified.")
    if controls:
        print(f"PASS: {len(controls)} negative controls detected.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
