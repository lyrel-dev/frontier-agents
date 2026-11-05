#!/usr/bin/env python3
"""Independently validate the published RPC schema graph and executed examples.

Optional review tool: requires the Python jsonschema package. The browser,
server, Node tests and documentation generator have no dependency on it.
"""
import json
from pathlib import Path
import subprocess
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("Independent schema review requires Python package 'jsonschema'.")

ROOT = Path(__file__).resolve().parents[1]
EXPORT = r"""
const contract = require('./api/contract.cjs');
const { createRuntime } = require('./api/runtime.cjs');
const examples = contract.operations.map(operation => {
  const runtime = createRuntime({ now: () => 1793874240000, secret: 'independent-schema-review' });
  const example = runtime.runSample(operation.name);
  return { name: operation.name, input: operation.inputSchema, output: operation.outputSchema,
    request: example.request, response: example.response };
});
process.stdout.write(JSON.stringify({ shapes: contract.shapes, examples }));
"""


def main():
    result = subprocess.run(
        ["node", "-e", EXPORT], cwd=ROOT, check=True,
        text=True, capture_output=True,
    )
    package = json.loads(result.stdout)
    definitions = package["shapes"]

    def schema_with_definitions(schema):
        return {"$schema": "https://json-schema.org/draft/2020-12/schema",
                **schema, "$defs": definitions}

    for name, shape in definitions.items():
        Draft202012Validator.check_schema(schema_with_definitions(shape))

    for operation in package["examples"]:
        for schema_key, example_key in (("input", "request"), ("output", "response")):
            schema = schema_with_definitions(operation[schema_key])
            Draft202012Validator.check_schema(schema)
            errors = sorted(Draft202012Validator(schema).iter_errors(operation[example_key]),
                            key=lambda error: str(list(error.path)))
            if errors:
                detail = "\n".join(f"  {list(error.path)}: {error.message}" for error in errors)
                raise AssertionError(f"{operation['name']} {example_key} failed:\n{detail}")

    count = len(package["examples"])
    print(f"Independent JSON Schema 2020-12 validation passed: {len(definitions)} shared shapes, "
          f"{count * 2} operation schemas, {count * 2} executed request/response examples.")
    print("The custom x-precision assertion is exercised by the runtime regressions, "
          "not by generic JSON Schema validation.")


if __name__ == "__main__":
    main()
