'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const { once } = require('node:events');
const contract = require('../api/contract.cjs');
const { createRuntime } = require('../api/runtime.cjs');
const { createServer } = require('../api/server.cjs');
const { call } = require('../api/client.cjs');
const fixed = () => createRuntime({ now: () => 1793874240000, secret: 'test-secret' });

async function listen(server) { server.listen(0, '127.0.0.1'); await once(server, 'listening'); return 'http://127.0.0.1:' + server.address().port + '/'; }
async function close(server) { server.closeAllConnections(); await new Promise(resolve => server.close(resolve)); }
function raw(endpoint, { method = 'POST', target = contract.namespace + '.GetWorkspaceSummary', type = contract.mediaType, body = '{}', headers = {}, path = '/', chunked = false } = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint);
    const request = http.request({ hostname: url.hostname, port: url.port, path, method, headers: { ...(type ? { 'Content-Type': type } : {}), ...(target ? { 'X-Amz-Target': target } : {}), ...(chunked ? {} : { 'Content-Length': Buffer.byteLength(body) }), ...headers } }, response => { const chunks = []; response.on('data', chunk => chunks.push(chunk)); response.on('end', () => resolve({ status: response.statusCode, headers: response.headers, body: JSON.parse(Buffer.concat(chunks).toString()) })); });
    request.on('error', reject); if (chunked) { request.write(body.slice(0, 100)); request.write(body.slice(100)); request.end(); } else request.end(body);
  });
}

test('all 44 catalog operations are reachable using AWS-style JSON RPC transport', async () => {
  let runtime = fixed(); const server = createServer({ runtime: { execute: (...args) => runtime.execute(...args) } });
  const endpoint = await listen(server);
  try {
    for (const operation of contract.operations) {
      const sample = fixed().runSample(operation.name);
      runtime = fixed();
      for (const step of operation.sampleSetup || []) runtime.execute(step.operation, step.input);
      const result = await raw(endpoint, { target: contract.namespace + '.' + operation.name, body: JSON.stringify(sample.request) });
      assert.equal(result.status, 200, operation.name + ': ' + JSON.stringify(result.body));
      assert.equal(result.headers['content-type'], contract.mediaType);
      assert.match(result.headers['x-amzn-requestid'], /^[a-f0-9-]{36}$/);
      assert.deepEqual(result.body, sample.response, operation.name);
      assert.equal(result.headers['x-amzn-errortype'], undefined);
    }
  } finally { await close(server); }
});

test('transport validates path, method, media type, target, body shape, body size and error headers', async () => {
  const server = createServer({ runtime: fixed() }), endpoint = await listen(server);
  try {
    const cases = [
      [{ method: 'GET', body: '' }, 405, 'ValidationException'],
      [{ path: '/GetService' }, 400, 'ValidationException'],
      [{ type: 'application/json' }, 415, 'UnsupportedMediaTypeException'],
      [{ type: null }, 415, 'UnsupportedMediaTypeException'],
      [{ target: null }, 400, 'ValidationException'],
      [{ target: 'ResilienceHub.ListServices' }, 400, 'ValidationException'],
      [{ target: contract.namespace + '.MissingOperation' }, 400, 'ValidationException'],
      [{ body: '{' }, 400, 'ValidationException'],
      [{ body: 'null' }, 400, 'ValidationException'],
      [{ body: '[]' }, 400, 'ValidationException'],
      [{ body: '{"tenantId":"evil","role":"admin"}' }, 400, 'ValidationException'],
      [{ body: 'x'.repeat(contract.limits.bodyBytes + 1) }, 413, 'RequestEntityTooLargeException'],
      [{ body: 'x'.repeat(contract.limits.bodyBytes + 1), chunked: true }, 413, 'RequestEntityTooLargeException']
    ];
    for (const [request, status, type] of cases) {
      const result = await raw(endpoint, request);
      assert.equal(result.status, status); assert.equal(result.headers['x-amzn-errortype'], type);
      assert.equal(result.body.__type, contract.namespace + '#' + type);
      assert.equal(typeof result.body.message, 'string'); assert.ok(result.headers['x-amzn-requestid']);
      assert.equal(result.headers['content-type'], contract.mediaType);
    }
    const utf8 = await raw(endpoint, { type: 'application/x-amz-json-1.1; charset=utf-8' }); assert.equal(utf8.status, 200);
  } finally { await close(server); }
});

test('server-configured read role cannot be escalated by client headers; client returns request IDs', async () => {
  const server = createServer({ role: 'reader', runtimeOptions: { now: () => 1793874240000 } }), endpoint = await listen(server);
  try {
    const read = await call('GetWorkspaceSummary', {}, { endpoint }); assert.equal(read.data.summary.serviceCount, 8); assert.ok(read.requestId);
    const denied = await raw(endpoint, { target: contract.namespace + '.CreateSystem', body: JSON.stringify({ name: 'should-not-exist', clientToken: 'auth-test' }), headers: { 'x-role': 'admin', 'x-principal-role': 'admin', 'x-tenant-id': 'northstar' } });
    assert.equal(denied.status, 403); assert.equal(denied.headers['x-amzn-errortype'], 'AccessDeniedException');
    await assert.rejects(() => call('CreateSystem', { name: 'denied-client', clientToken: 'client-auth-test' }, { endpoint }), { statusCode: 403 });
    assert.equal(server.runtime.state.systems.length, 3);
  } finally { await close(server); }
});

test('unexpected server errors expose typed safe errors with request identifiers', async () => {
  let logged;
  const server = createServer({ runtime: { execute() { throw new Error('private internal detail'); } }, onError: error => { logged = error; } });
  const endpoint = await listen(server);
  try { const result = await raw(endpoint); assert.equal(result.status, 500); assert.equal(result.headers['x-amzn-errortype'], 'InternalServerException'); assert.ok(result.headers['x-amzn-requestid']); assert.ok(!JSON.stringify(result.body).includes('private internal detail')); assert.equal(logged.message, 'private internal detail'); } finally { await close(server); }
});
