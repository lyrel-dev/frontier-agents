#!/usr/bin/env python3
"""Check the authored demo's native raw objects against the pinned AWS model.

Run from analysis:
  python3 tools/check_fixture_schema.py --model /path/to/service-2.json --self-test

Python standard library and Node.js are the only runtime dependencies. The local,
trusted CommonJS fixture is executed by Node; only the five declared collections'
raw payloads are checked. No AWS account or network is accessed unless --fetch is
explicitly used to retrieve the immutable public model.

This is normalized-fixture validation, not an AWS wire/SDK conformance test:
BackLogTimestamp uses timezone-qualified ISO 8601 text; timestamps without an
explicit format use finite epoch seconds. Ordinary model strings are counted as
Unicode code points, not UTF-8 bytes. The selected model patterns are evaluated
with Python re.search (unanchored unless the model supplies anchors). Open JSON
documents retain null, scalars, arrays and arbitrary object keys. Native blobs are
not represented by this JSON fixture; encountering one fails with an explicit
unsupported-representation error. Wrapper metadata, EventBridge envelopes,
cross-object relationships and application projections are outside this check.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

from check_native_api import PIN_SHA256, PIN_URL, ROOT, digest


FIXTURE = ROOT / "app/src/mock-data.js"
EVIDENCE = ROOT / "qa/fixture-schema-audit.json"
COLLECTIONS = {
    "taskObservations": "Task",
    "executionObservations": "Execution",
    "journalRecords": "JournalRecord",
    "assetObservations": "Asset",
    "assetFiles": "AssetFile",
}
NORMALIZATION = [
    "Node executes the trusted local fixture and exports only the five declared collections' raw payloads.",
    "The loader rejects non-JSON values, non-finite numbers, sparse arrays, custom objects and cycles before JSON serialization.",
    "BackLogTimestamp is timezone-qualified ISO 8601 text; other fixture timestamps are finite epoch seconds, not SDK datetime objects.",
    "String lengths use Unicode code points; this does not establish accepted UTF-8/upload byte limits.",
    "Patterns use Python re.search; only the pinned selected patterns are claimed, not general Smithy regex-dialect conformance.",
    "Document values remain arbitrary JSON; a required Document member may contain JSON null.",
    "Numbers originate as JavaScript Number values; this fixture does not test arbitrary-precision document numbers or 64-bit round trips.",
    "Blob payloads are unsupported in this normalized fixture format and fail if encountered; only AssetFile.content.text is exercised.",
]
LIMITS = [
    "No AWS calls, wire serialization, SDK deserialization, authorization or live behavior is tested.",
    "Only modeled members of the five selected raw collections are checked; wrapper fields and EventBridge notifications are excluded.",
    "Requiredness, types, enums and applicable modeled constraints are checked only for values reached in this fixture.",
    "Open Document payloads have no inferred profile: journal contents, asset metadata and nested references are not semantically validated.",
    "No scope/identity relationships, timestamp ordering, graph references, snapshot persistence or application HTTP contract is validated here.",
    "No service-guide content profiles, encoded-request limits, binary assets or unexercised optional branches are validated.",
    "Strict pinned enums, members and constraints are fixture-authoring checks, not a live response rejection policy; unknown enum values must be preserved by production clients.",
]
NODE_LOADER = r"""
const data = require(process.argv[1]);
const collections = JSON.parse(process.argv[2]);
function jsonValue(value, path, ancestors = new Set()) {
  const kind = typeof value;
  if (value === null || kind === 'string' || kind === 'boolean') return;
  if (kind === 'number' && Number.isFinite(value)) return;
  if (kind !== 'object') throw new Error(path + ': non-JSON value');
  if (ancestors.has(value)) throw new Error(path + ': cyclic value');
  if (!Array.isArray(value) && Object.getPrototypeOf(value) !== Object.prototype &&
      Object.getPrototypeOf(value) !== null) throw new Error(path + ': custom object');
  if (Reflect.ownKeys(value).some(key => typeof key !== 'string' ||
      (key !== 'length' && !Object.prototype.propertyIsEnumerable.call(value, key))))
    throw new Error(path + ': non-JSON property');
  ancestors.add(value);
  if (Array.isArray(value)) {
    if (Object.keys(value).length !== value.length)
      throw new Error(path + ': sparse array or extra array properties');
    for (let i = 0; i < value.length; i++) jsonValue(value[i], path + '/' + i, ancestors);
  } else {
    for (const [key, child] of Object.entries(value))
      jsonValue(child, path + '/' + key, ancestors);
  }
  ancestors.delete(value);
}
const result = {};
for (const name of Object.keys(collections)) {
  if (!Array.isArray(data[name]) || !data[name].length)
    throw new Error(name + ': missing or empty fixture collection');
  result[name] = data[name].map((row, index) => {
    if (!row || !Object.prototype.hasOwnProperty.call(row, 'raw'))
      throw new Error(name + '/' + index + ': missing raw payload');
    jsonValue(row.raw, name + '/' + index + '/raw');
    return { fixtureId: String(row.id ?? index), raw: row.raw };
  });
}
process.stdout.write(JSON.stringify(result));
"""


class ValidationError(ValueError):
    """A fixture value fails an explicit model or normalization rule."""


def fail(path: str, reason: str) -> None:
    raise ValidationError(path + ": " + reason)


def json_document(value: object, path: str) -> None:
    """Validate JSON representability only; do not invent a Document schema."""
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float) and math.isfinite(value):
        return
    if isinstance(value, list):
        for i, child in enumerate(value):
            json_document(child, f"{path}/{i}")
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for key, child in value.items():
            json_document(child, f"{path}/{key}")
        return
    fail(path, "unsupported JSON value")


def validate(model: dict, name: str, value: object, path: str, visited: set[str]) -> None:
    shape = model["shapes"][name]
    visited.add(name)
    if shape.get("document"):
        json_document(value, path)
        return
    kind = shape["type"]
    if kind == "structure":
        if not isinstance(value, dict):
            fail(path, "expected structure")
        members = shape.get("members", {})
        missing = set(shape.get("required", [])) - value.keys()
        if missing:
            fail(path, "missing required member(s): " + ", ".join(sorted(missing)))
        unknown = value.keys() - members.keys()
        if unknown:
            fail(path, "unknown modeled member(s): " + ", ".join(sorted(unknown)))
        if shape.get("union") and len(value) != 1:
            fail(path, "union requires exactly one member")
        for key, child in value.items():
            validate(model, members[key]["shape"], child, f"{path}/{key}", visited)
        return
    if kind == "string":
        if not isinstance(value, str):
            fail(path, "expected string")
        if "enum" in shape and value not in shape["enum"]:
            fail(path, "value outside modeled enum")
        if "pattern" in shape and re.search(shape["pattern"], value) is None:
            fail(path, "value fails modeled pattern")
        measure = len(value)
    elif kind in ("integer", "long"):
        if type(value) is not int:
            fail(path, "expected integer")
        bits = 32 if kind == "integer" else 64
        if not -(2 ** (bits - 1)) <= value < 2 ** (bits - 1):
            fail(path, f"value outside signed {bits}-bit range")
        measure = value
    elif kind in ("float", "double"):
        if type(value) not in (int, float) or not math.isfinite(value):
            fail(path, "expected finite number")
        measure = value
    elif kind == "boolean":
        if type(value) is not bool:
            fail(path, "expected boolean")
        return
    elif kind == "timestamp":
        if shape.get("timestampFormat") == "iso8601":
            if not isinstance(value, str) or not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",
                value,
            ):
                fail(path, "expected timezone-qualified ISO 8601 fixture timestamp")
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                fail(path, "invalid ISO 8601 fixture timestamp")
        elif "timestampFormat" not in shape:
            if type(value) not in (int, float) or not math.isfinite(value):
                fail(path, "expected finite epoch-seconds fixture timestamp")
        else:
            fail(path, "unsupported timestamp normalization: " + shape["timestampFormat"])
        return
    elif kind in ("list", "map"):
        if kind == "list":
            if not isinstance(value, list):
                fail(path, "expected list")
            for i, child in enumerate(value):
                validate(model, shape["member"]["shape"], child, f"{path}/{i}", visited)
        else:
            if not isinstance(value, dict):
                fail(path, "expected map")
            for key, child in value.items():
                validate(model, shape["key"]["shape"], key, f"{path}/<key>", visited)
                validate(model, shape["value"]["shape"], child, f"{path}/{key}", visited)
        measure = len(value)
    elif kind == "blob":
        fail(path, "unsupported blob representation in normalized JSON fixture")
    else:
        fail(path, "unsupported modeled type: " + kind)
    for bound, comparator in (("min", lambda a, b: a < b), ("max", lambda a, b: a > b)):
        if bound in shape and comparator(measure, shape[bound]):
            fail(path, f"value violates modeled {bound} {shape[bound]}")


def audit(model: dict, fixture: dict) -> tuple[list[str], set[str]]:
    errors, visited = [], set()
    for collection, shape in COLLECTIONS.items():
        for row in fixture[collection]:
            path = collection + "/" + row["fixtureId"] + "/raw"
            try:
                validate(model, shape, row["raw"], path, visited)
            except ValidationError as exc:
                errors.append(str(exc))
    return errors, visited


def controls(model: dict, fixture: dict) -> tuple[list[str], list[str]]:
    task = fixture["taskObservations"][0]["raw"]
    asset = fixture["assetObservations"][0]["raw"]
    asset_file = fixture["assetFiles"][0]["raw"]
    dropped = {key: value for key, value in task.items() if key != "taskId"}
    altered_model = deepcopy(model)
    altered_model["shapes"]["String"]["type"] = "unsupported_test_type"
    negative = [
        ("missing required field", model, "Task", dropped, "missing required member"),
        ("invalid enum", model, "Task", {**task, "status": "INVENTED"}, "outside modeled enum"),
        ("wrong payload type", model, "Task", {**task, "version": True}, "expected integer"),
        ("integer overflow", model, "Task", {**task, "version": 2 ** 31}, "outside signed 32-bit range"),
        ("invalid pattern", model, "Asset", {**asset, "assetId": "!!!"}, "fails modeled pattern"),
        ("overlong path", model, "AssetFile", {**asset_file, "path": "a" * 513}, "violates modeled max"),
        ("multiple union members", model, "AssetFile", {**asset_file, "content": {"text": "x", "bytes": "eA=="}}, "union requires"),
        ("unsupported model type", altered_model, "Task", task, "unsupported modeled type"),
    ]
    detected = []
    for label, control_model, name, value, expected in negative:
        try:
            validate(control_model, name, value, "negative-control", set())
        except ValidationError as exc:
            if expected not in str(exc):
                raise ValueError("Unexpected negative-control failure: " + label) from exc
            detected.append(label)
        else:
            raise ValueError("Negative control was accepted: " + label)
    record = fixture["journalRecords"][0]["raw"]
    examples = {
        "null": None, "boolean": True, "number": 1.25, "string": "opaque",
        "array": [None, {"future": [False, 3]}], "object": {"unknown": {"arbitrary": []}},
    }
    for label, value in examples.items():
        validate(model, "JournalRecord", {**record, "content": value}, "open-json/" + label, set())
    return detected, list(examples)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--model", type=Path, help="Read a local checksum-pinned service-2.json; no network")
    source.add_argument("--fetch", action="store_true", help="Explicitly download the pinned official model")
    parser.add_argument("--node", default="node", help="Node.js executable (default: node)")
    parser.add_argument("--self-test", action="store_true", help="Run negative controls and open-JSON positive controls")
    parser.add_argument("--write-evidence", action="store_true", help="Regenerate compact evidence after all checks pass")
    args = parser.parse_args()
    if args.write_evidence and not args.self_test:
        raise ValueError("Use --self-test with --write-evidence")
    raw = urllib.request.urlopen(PIN_URL, timeout=30).read() if args.fetch else args.model.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PIN_SHA256:
        raise ValueError("Model checksum differs from the review pin")
    model = json.loads(raw)
    fixture_bytes = FIXTURE.read_bytes()
    loaded = subprocess.run(
        [args.node, "-e", NODE_LOADER, str(FIXTURE), json.dumps(COLLECTIONS)],
        capture_output=True, text=True, timeout=30, check=True,
    )
    if FIXTURE.read_bytes() != fixture_bytes:
        raise ValueError("Fixture changed during validation; rerun against a stable file")
    fixture = json.loads(loaded.stdout)
    errors, visited = audit(model, fixture)
    if errors:
        print("FAIL: " + "\nFAIL: ".join(errors), file=sys.stderr)
        return 1
    negative, positive = controls(model, fixture) if args.self_test else ([], [])
    counts = {shape: len(fixture[collection]) for collection, shape in COLLECTIONS.items()}
    evidence = {
        "schemaVersion": "fixture-schema-audit/v1",
        "modelSource": PIN_URL, "modelSha256": PIN_SHA256,
        "constraintSemanticsSources": ["https://smithy.io/2.0/spec/simple-types.html",
                                       "https://smithy.io/2.0/spec/constraint-traits.html"],
        "fixture": FIXTURE.relative_to(ROOT).as_posix(),
        "fixtureSha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "normalizedRawObjectsSha256": digest(fixture),
        "validatorSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "nativeObjectsChecked": sum(counts.values()), "objectsByShape": counts,
        "modeledShapesReached": sorted(visited),
        "modeledTypesReached": dict(sorted(Counter(model["shapes"][name]["type"] for name in visited).items())),
        "checks": ["required-member presence", "modeled structure members", "recursive types",
                   "enums", "applicable min/max and patterns", "union cardinality",
                   "explicit timestamp normalization", "JSON document representability"],
        "normalization": NORMALIZATION, "limits": LIMITS,
        "negativeControlsDetected": negative, "openJsonPositiveControlsAccepted": positive,
        "errors": [],
    }
    if args.write_evidence:
        EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    else:
        retained = json.loads(EVIDENCE.read_text())
        # Controls are compared when executed, and all source/result fields always are.
        for field, value in evidence.items():
            if not args.self_test and field in ("negativeControlsDetected", "openJsonPositiveControlsAccepted"):
                continue
            if retained.get(field) != value:
                raise ValueError("Committed fixture evidence is stale at " + field + "; review before --self-test --write-evidence")
    print(f"PASS: {sum(counts.values())} native-shaped raw objects across {len(counts)} root shapes; {len(visited)} modeled shapes reached.")
    if args.self_test:
        print(f"PASS: {len(negative)} negative controls detected; {len(positive)} open-JSON kinds accepted.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print("FAIL: Node fixture loading failed: " + exc.stderr.strip(), file=sys.stderr)
        raise SystemExit(1)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
