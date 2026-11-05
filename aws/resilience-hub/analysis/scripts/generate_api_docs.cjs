'use strict';

// The operation notes are executable documentation: examples are obtained from
// the same runtime used by HTTP, and schemas are read directly from its contract.
const fs = require('node:fs');
const path = require('node:path');
const contract = require('../api/contract.cjs');
const root = path.resolve(__dirname, '..');
const check = process.argv.includes('--check');
const catalogueOnly = process.argv.includes('--catalogue-only');
const outputs = new Map();
const quote = value => JSON.stringify(value);
const json = value => JSON.stringify(value, null, 2);
const code = value => '`' + value + '`';
const slug = value => value.replace(/([a-z0-9])([A-Z])/g, '$1-$2').replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-|-$/g, '').toLowerCase();
const anchor = value => value.toLowerCase().replace(/[^a-z0-9-]/g, '');
const cell = value => String(value).replace(/\|/g, '\\|').replace(/\n/g, ' ');
const mdTable = (headers, rows) => [headers, headers.map(() => '---'), ...rows].map(row => '| ' + row.map(cell).join(' | ') + ' |').join('\n');
const fence = (language, content) => '```' + language + '\n' + content + '\n```';
const sourceUrl = operation => 'https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_' + operation + '.html';
const nativeLinks = operation => operation.nativeOperations.length ? operation.nativeOperations.map(name => '[' + name + '](' + sourceUrl(name) + ')').join(', ') : 'Application-owned; no native mutation or read is asserted.';
const provenanceText = {
  NATIVE_ADAPTER: 'Native-backed facade with local validation, versions, idempotency and response normalization.',
  COMPOSED_READ: 'Application projection or capture composed from observed provider data and local storage.',
  LOCAL: 'Application-owned command or data; no corresponding native mutation is asserted.',
  INGEST: 'Trusted integration ingestion into the product observation/event store.',
  LOCAL_PROJECTION: 'Application projection or capture composed from observed provider data and local storage.',
  LOCAL_COMMAND: 'Application-owned command or integration ingestion; no corresponding native mutation is asserted.'
};

function frontMatter(id, title, type, related, extra = {}) {
  const properties = { id, title, type, service: 'aws-resilience-hub', status: 'implemented-mock', created: contract.version, updated: contract.version,
    tags: ['aws', 'resilience-hub', 'api', ...(type === 'api-operation' ? ['rpc-operation'] : ['rpc'])], aliases: [title], related, ...extra };
  return '---\n' + Object.entries(properties).map(([key, value]) => Array.isArray(value)
    ? key + ':' + (value.length ? '\n' + value.map(item => '  - ' + quote(item)).join('\n') : ' []')
    : key + ': ' + quote(value)).join('\n') + '\n---\n\n';
}

function typeText(schema, relative = '') {
  if (!schema || typeof schema !== 'object') throw new Error('Invalid schema node: ' + String(schema));
  if (schema.$ref) {
    const name = schema.$ref.split('/').pop();
    if (!contract.shapes[name]) throw new Error('Unresolved schema: ' + schema.$ref);
    return '[' + name + '](' + relative + 'shapes.md#' + anchor(name) + ')';
  }
  if (schema.anyOf) return schema.anyOf.map(item => typeText(item, relative)).join(' or ');
  if (schema.oneOf) return schema.oneOf.map(item => typeText(item, relative)).join(' or ');
  if (schema.type === 'array') return 'Array of ' + typeText(schema.items, relative);
  if (schema.type === 'object' && schema.additionalProperties && typeof schema.additionalProperties === 'object') return 'Map of ' + typeText(schema.additionalProperties, relative);
  return code(schema.type || (schema.const === null ? 'null' : 'value'));
}

function constraints(schema) {
  const rows = [];
  if (schema.enum) rows.push(schema.enum.map(code).join(', '));
  if (Object.hasOwn(schema, 'const')) rows.push('Exactly ' + code(json(schema.const)));
  if (schema.minLength !== undefined || schema.maxLength !== undefined) rows.push('Length ' + (schema.minLength ?? 0) + '–' + (schema.maxLength ?? 'unbounded'));
  if (schema.minimum !== undefined) rows.push('Minimum ' + schema.minimum);
  if (schema.maximum !== undefined) rows.push('Maximum ' + schema.maximum);
  if (schema.minItems !== undefined || schema.maxItems !== undefined) rows.push('Items ' + (schema.minItems ?? 0) + '–' + (schema.maxItems ?? 'unbounded'));
  if (schema.minProperties !== undefined || schema.maxProperties !== undefined) rows.push('Properties ' + (schema.minProperties ?? 0) + '–' + (schema.maxProperties ?? 'unbounded'));
  if (schema.pattern) rows.push('Pattern ' + code(schema.pattern));
  if (schema.additionalProperties === false) rows.push('Unknown members rejected');
  if (schema.anyOf || schema.oneOf) rows.push('See full schema');
  return rows.join('; ') || 'See shared shape or field semantics.';
}

function fieldTable(schema, relative = '') {
  return mdTable(['Member', 'Required', 'Type', 'Constraints'], Object.entries(schema.properties || {}).map(([name, field]) => [code(name), (schema.required || []).includes(name) ? 'Yes' : 'No', typeText(field, relative), constraints(field)]));
}

const families = [...new Set(contract.operations.map(operation => operation.family))];
const index = [frontMatter('resilience-workspace-api-index', 'Resilience Workspace API reference', 'api-reference', ['protocol.md', 'aws-mapping.md', 'entities.md', 'shapes.md', 'errors.md', 'workflows.md', '../report.md', '../validation.md']),
  '# Resilience Workspace API reference',
  'An executable mock API for the reviewed AWS Resilience Hub operator model. **' + contract.operations.length + ' operations** cover the ten requested entities, input sources, status projections and event ingestion. Every operation has an Obsidian Markdown note with YAML properties, request and response schemas, generated examples, access roles, errors and lifecycle effects.',
  '> This is a product-owned RPC facade. The mock makes no AWS calls. Its AWS-shaped transport is a design choice; native Resilience Hub v2 has its own HTTP routes and SDK contract. The existing browser UI and this HTTP server currently maintain separate local mock states.',
  '## Start here',
  mdTable(['Note', 'Contents'], [
    ['[Protocol](protocol.md)', 'Transport, identities, authorization, idempotency, versions, pagination and freshness.'],
    ['[AWS mapping](aws-mapping.md)', 'Operation-by-operation native evidence, adapter boundaries and reviewed field corrections.'],
    ['[Entity mapping](entities.md)', 'How the ten requested concepts and ER relationships map to RPC operations.'],
    ['[Shared schemas](shapes.md)', 'Canonical reusable DTO definitions generated from the executable contract.'],
    ['[Errors](errors.md)', 'Typed errors, status codes and client recovery behavior.'],
    ['[Workflows](workflows.md)', 'UI tasks, command lifecycle, event reconciliation and sequence diagrams.'],
    ['[Reviewed model](../report.md)', 'Source-backed analysis and the five ER diagram notes.'],
    ['[Validation](../validation.md)', 'Checks completed and explicit integration boundaries.']
  ]),
  '## Run locally',
  'From ' + code('aws/resilience-hub/analysis') + ' with Node.js 18 or later:',
  fence('bash', 'node api/server.cjs\n# Optional: node api/server.cjs --port 8788 --role reader'),
  'The default endpoint is ' + code('http://127.0.0.1:8787/') + '. The server binds to loopback, stores mutations only in memory, and uses a trusted demo principal configured at startup. Restarting resets its state. The default ' + code('demo') + ' context includes all four application roles; read-only mode uses ' + code('--role reader') + '. No AWS credentials are required.',
  fence('bash', "curl --silent --show-error http://127.0.0.1:8787/ \\\n  -H 'Content-Type: application/x-amz-json-1.1' \\\n  -H 'X-Amz-Target: " + contract.namespace + ".ListSystems' \\\n  --data '{\"maxResults\":20}'"),
  'Successful responses use HTTP 200 and operation-specific JSON. See [protocol](protocol.md) for the full envelope and [errors](errors.md) for non-2xx responses. Timestamps on the wire are numeric epoch seconds. The fixture clock starts at 2026-11-05T10:24:00Z and advances with elapsed process time; generated examples and tests inject a fixed clock.',
  'The included [Node client](client.cjs) handles the RPC headers and exposes the server request ID. With the server running:',
  fence('bash', "node api/client.cjs ListSystems '{\"maxResults\":20}'\nnode api/client.cjs GetWorkspaceSummary '{}'"),
  '## Operation catalogue',
  'The provenance column refers to the facade implementation. Native-backed operations still add local guarantees; composed operations do not invent new AWS endpoints. Integration operations require an ingestor or administrator context. The [mapping note](aws-mapping.md) explains each classification.'
];
for (const family of families) {
  index.push('### ' + family, mdTable(['Operation', 'Mode', 'Provenance', 'Purpose'], contract.operations.filter(operation => operation.family === family).map(operation => ['[' + operation.name + '](operations/' + operation.name + '.md)', operation.mutating ? 'Mutation' : 'Read', code(operation.provenance), operation.description])));
}
index.push('## Maintain the contract and notes',
  'Edit [contract.cjs](contract.cjs) and the runtime together, then regenerate the operation notes and shared schemas. Generated notes carry stable IDs and relative links suitable for an Obsidian vault. The hand-authored protocol, mapping, entity and workflow notes explain intent and native boundaries.',
  fence('bash', 'node scripts/generate_api_docs.cjs\nnode scripts/generate_api_docs.cjs --check\nnode --test tests/*.test.cjs\npython scripts/check_notes.py'),
  'The generator executes every documented example against a fresh runtime. Setup commands in delete examples create disposable entities. Request and response JSON schemas resolve ' + code('#/$defs/<Shape>') + ' through the definitions in [shapes.md](shapes.md) or ' + code('contract.shapes') + '. [contract.cjs](contract.cjs), [runtime.cjs](runtime.cjs) and [server.cjs](server.cjs) are source code; all human-readable documents and diagrams are Markdown notes with YAML headers.'
);
outputs.set('api/index.md', index.join('\n\n') + '\n');

const shapeSections = [frontMatter('resilience-workspace-api-shapes', 'Shared API schemas', 'api-reference', ['index.md', 'entities.md', 'protocol.md']),
  '# Shared API schemas',
  'Generated from [contract.cjs](contract.cjs). These JSON Schema definitions describe the implemented mock facade, including local enrichments and projections. They are not a transcription of AWS service models. See [AWS mapping](aws-mapping.md) for provider field ownership and [entity mapping](entities.md) for relationship constraints.',
  'The schema dialect is JSON Schema 2020-12. A schema containing ' + code('#/$defs/Name') + ' is resolved by attaching ' + code('contract.shapes') + ' as ' + code('$defs') + '. Fields listed in ' + code('required') + ' must be present even when their value may be null. Unknown object properties are rejected unless explicitly permitted. Timestamp fields contain numeric epoch seconds. The runtime validator covers the keywords used by this contract; it is not a general-purpose JSON Schema implementation.',
  '## Definitions',
  Object.keys(contract.shapes).map(name => '- [' + name + '](#' + anchor(name) + ')').join('\n')
];
for (const [name, schema] of Object.entries(contract.shapes)) shapeSections.push('## ' + name, fieldTable(schema), fence('json', json(schema)));
outputs.set('api/shapes.md', shapeSections.join('\n\n') + '\n');

const recovery = {
  ValidationException: 'Correct the request or restart pagination with no token. Do not blindly retry the same invalid body.',
  AccessDeniedException: 'Use a trusted context with the required role and resource scope. Request headers do not grant access.',
  ResourceNotFoundException: 'Refresh the scoped collection and confirm the entity still exists. A child ID in another parent scope is not a match.',
  ConflictException: 'Re-read local versions or remove the blocking reference. If an idempotency token was reused with changed input, choose a new token only for a new intended command.',
  RequestEntityTooLargeException: 'Reduce the request body to the documented limit.',
  UnsupportedMediaTypeException: 'Send Content-Type: application/x-amz-json-1.1.',
  InternalServerException: 'Retry only after considering an uncertain outcome; retain the same clientToken for an identical mutation.'
};
outputs.set('api/errors.md', [frontMatter('resilience-workspace-api-errors', 'RPC errors and recovery', 'api-reference', ['index.md', 'protocol.md']),
  '# RPC errors and recovery',
  'The mock uses typed errors with a non-2xx HTTP status, a JSON ' + code('__type') + ' discriminator and a ' + code('message') + '. HTTP responses also carry ' + code('x-amzn-ErrorType') + ' and a per-attempt ' + code('x-amzn-RequestId') + '. This table is generated from [contract.cjs](contract.cjs).',
  mdTable(['Error', 'HTTP', 'Meaning', 'Client response'], Object.entries(contract.errors).map(([name, definition]) => [code(name), definition.statusCode, definition.description, recovery[name] || 'Inspect the operation contract before retrying.'])),
  'A non-POST request is the transport exception to the table: it returns HTTP 405 with ' + code('ValidationException') + ' and ' + code('Allow: POST') + '. An invalid path or unknown target returns HTTP 400. These transport checks occur before operation execution.',
  '## Conflict handling',
  'A stale ' + code('expectedVersion') + ', a changed payload using an existing idempotency token, a duplicate identity/name, an active assessment or a reference guard can produce a conflict. An identical successful replay with the same principal, operation, body and token returns the cached result before checking the now-stale version. Compare error details and current state before deciding whether to retry a changed command.',
  '## Native adapter errors',
  'This mock does not issue AWS calls, exhaust AWS quotas or inject AWS throttling. A production adapter must preserve or deliberately map native failures, including retryability and any provider request ID. AWS documents ' + code('ServiceQuotaExceededException') + ' as HTTP 402 in the native Create contracts; throttling is a separate error condition. Do not normalize all quota failures to a transient 429. See [AWS mapping](aws-mapping.md) for sources and differences.',
  '## Uncertain outcomes',
  'A client losing its HTTP response cannot assume the command failed. Retrying the exact body with the same token avoids repeated local side effects while the in-memory idempotency result exists. A process restart loses that result. Durable command state and a remote-outcome reconciliation strategy are production requirements; the mock does not claim exactly-once execution across AWS.'
].join('\n\n') + '\n');

if (!catalogueOnly) {
  const { createRuntime } = require('../api/runtime.cjs');
  for (const operation of contract.operations) {
    const runtime = createRuntime({ now: () => 1793874240000, secret: 'resilience-workspace-documentation-secret-v1' });
    const sample = runtime.runSample(operation.name);
    if (!sample || !sample.request || !sample.response) throw new Error('Invalid sample for ' + operation.name);
    const setup = sample.setup || [];
    const sections = [frontMatter('resilience-workspace-operation-' + slug(operation.name), operation.name, 'api-operation', ['../index.md', '../protocol.md', '../aws-mapping.md', '../shapes.md', '../errors.md'], {
      operation: operation.name, api_version: contract.version, provenance: operation.provenance, mutating: operation.mutating, native_operations: operation.nativeOperations
    }),
    '# ' + operation.name,
    operation.description,
    mdTable(['Property', 'Value'], [
      ['Target', code(contract.namespace + '.' + operation.name)],
      ['Transport', code('POST /') + '; ' + code(contract.mediaType)],
      ['Operation kind', operation.mutating ? 'Mutation against the local mock store' : 'Read from the local mock store'],
      ['Provenance', code(operation.provenance) + ' — ' + (provenanceText[operation.provenance] || 'See the native mapping.')],
      ['Allowed application roles', operation.roles.map(code).join(', ')],
      ['Native adapter basis', nativeLinks(operation)]
    ]),
    'Native names above identify the intended adapter basis, not HTTP calls made by this mock. Any local versions, tokens, display metadata, hydration and projections follow the [facade protocol](../protocol.md). See [AWS mapping](../aws-mapping.md) for supported native fields and limitations.'
    ];
    if (setup.length) {
      sections.push('## Example prerequisites', 'Run these calls first against a fresh server. Their returned identifiers are used in the request example. These setup entities isolate deletion examples from shared demo data.');
      setup.forEach((entry, ordinal) => {
        const original = (operation.sampleSetup || [])[ordinal] || {};
        sections.push('### ' + (ordinal + 1) + '. ' + (entry.operation || original.operation), fence('json', json(entry.request || entry.input || original.input)));
      });
    }
    sections.push('## Request', fieldTable(operation.inputSchema, '../'),
      '### HTTP example', fence('http', 'POST / HTTP/1.1\nHost: 127.0.0.1:8787\nContent-Type: ' + contract.mediaType + '\nX-Amz-Target: ' + contract.namespace + '.' + operation.name + '\n\n' + json(sample.request)),
      '### Request schema', 'Schema references resolve through the [shared definitions](../shapes.md).', fence('json', json(operation.inputSchema)),
      '## Response', fieldTable(operation.outputSchema, '../'),
      '### Successful response example', 'HTTP 200. This body is generated by executing the request above against a fresh deterministic mock runtime' + (setup.length ? ' after its setup calls' : '') + '.', fence('json', json(sample.response)),
      '### Response schema', fence('json', json(operation.outputSchema)),
      '## Consistency and lifecycle');
    if (operation.mutating) {
      sections.push('Supply one stable ' + code('clientToken') + ' for the logical command. Identical retries return the prior result within the local idempotency window; a changed body with the same token conflicts. Authorization uses trusted server-side context. No request makes a real AWS mutation.');
      if (operation.inputSchema.properties.expectedVersion) sections.push('Use the latest local ' + code('version') + ' as ' + code('expectedVersion') + '. A conflict requires a fresh read and a decision about the intervening change. The revision belongs to the product store; it is not an AWS conditional-write token.');
      sections.push((operation.sideEffects || []).map(effect => '- ' + effect).join('\n'));
    } else {
      sections.push('This operation reads the local observation store. Its response can contain provider-like fields and application-owned metadata. Observation age, representation and provenance must remain visible to callers.');
      if (operation.inputSchema.properties.nextToken) sections.push('Pagination defaults to ' + contract.limits.defaultMaxResults + ' results and permits at most ' + contract.limits.maxResults + '. Continue with the returned opaque ' + code('nextToken') + ' and unchanged filters. A local snapshot expires after ' + contract.limits.cursorTtlSeconds + ' seconds; it is not a provider-wide atomic snapshot.');
    }
    sections.push('## Errors', mdTable(['Error', 'HTTP', 'Meaning'], operation.errors.map(name => [code(name), contract.errors[name].statusCode, contract.errors[name].description])),
      'Transport errors and client recovery guidance are in [RPC errors](../errors.md). Error availability is a common facade envelope; it does not imply that every listed condition occurs on every execution.',
      '## Documentation source', 'Generated from [contract.cjs](../contract.cjs) and [runtime.cjs](../runtime.cjs) by [generate_api_docs.cjs](../../scripts/generate_api_docs.cjs). Regenerate after editing the executable contract; use ' + code('--check') + ' to detect drift. The mock server and browser prototype use separate local state.');
    outputs.set('api/operations/' + operation.name + '.md', sections.join('\n\n') + '\n');
  }
}

let mismatches = 0;
for (const [relative, contents] of outputs) {
  const file = path.join(root, relative);
  if (check) {
    if (!fs.existsSync(file) || fs.readFileSync(file, 'utf8') !== contents) {
      console.error('Documentation differs: ' + relative);
      mismatches += 1;
    }
  } else {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, contents);
  }
}
const operationDirectory = path.join(root, 'api', 'operations');
if (!catalogueOnly && fs.existsSync(operationDirectory)) {
  const expected = new Set(contract.operations.map(operation => operation.name + '.md'));
  for (const file of fs.readdirSync(operationDirectory)) if (file.endsWith('.md') && !expected.has(file)) {
    console.error('Unexpected stale operation note: ' + file);
    mismatches += 1;
  }
}
if (mismatches) process.exitCode = 1;
else console.log((check ? 'Verified ' : 'Generated ') + outputs.size + ' API Markdown notes' + (catalogueOnly ? ' (catalogue only)' : ' including ' + contract.operations.length + ' executed operation examples') + '.');
