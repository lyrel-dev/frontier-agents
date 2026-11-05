#!/usr/bin/env node
'use strict';

const http = require('node:http');
const crypto = require('node:crypto');
const contract = require('./contract.cjs');
const { createRuntime, RpcError } = require('./runtime.cjs');

function principalFor(role = 'demo') {
  const accepted = ['reader', 'operator', 'admin', 'ingestor', 'demo'];
  if (!accepted.includes(role)) throw new Error('--role must be reader, operator, admin, ingestor, or demo.');
  return { id: 'mock-' + role, tenantId: 'northstar', roles: role === 'demo' ? ['reader', 'operator', 'admin', 'ingestor'] : [role] };
}

function readBody(request, limit) {
  return new Promise((resolve, reject) => {
    let size = 0, done = false;
    const chunks = [];
    request.on('data', chunk => {
      size += chunk.length;
      if (size > limit) {
        if (!done) { done = true; chunks.length = 0; reject(new RpcError('RequestEntityTooLargeException', 'The request body exceeds the 1 MiB limit.')); }
      } else if (!done) chunks.push(chunk);
    });
    request.on('end', () => { if (!done) { done = true; resolve(Buffer.concat(chunks).toString('utf8')); } });
    request.on('error', error => { if (!done) { done = true; reject(error); } });
    request.on('aborted', () => { if (!done) { done = true; reject(new RpcError('ValidationException', 'The request body was interrupted.')); } });
  });
}

/** Server-side options are trusted configuration, never derived from request headers. */
function createServer(options = {}) {
  const runtime = options.runtime || createRuntime({ ...(options.runtimeOptions || {}), principal: options.principal || principalFor(options.role) });
  const server = http.createServer(async (request, response) => {
    const requestId = crypto.randomUUID();
    response.setHeader('Content-Type', contract.mediaType);
    response.setHeader('x-amzn-RequestId', requestId);
    response.setHeader('Cache-Control', 'no-store');
    response.setHeader('X-Content-Type-Options', 'nosniff');
    const sendError = (error, overrideStatus) => {
      if (response.destroyed || response.writableEnded) return;
      const exposed = error instanceof RpcError ? error : new RpcError('InternalServerException', 'The local mock could not complete the request.');
      response.statusCode = overrideStatus || exposed.statusCode;
      response.setHeader('x-amzn-ErrorType', exposed.type);
      response.end(JSON.stringify(exposed.toJSON()));
      if (!(error instanceof RpcError) && options.onError) options.onError(error, requestId);
    };
    try {
      if (request.method !== 'POST') { response.setHeader('Allow', 'POST'); request.resume(); return sendError(new RpcError('ValidationException', 'Use POST / for this RPC endpoint.'), 405); }
      if (request.url !== '/') { request.resume(); return sendError(new RpcError('ValidationException', 'The RPC endpoint path is /.')); }
      const mediaType = request.headers['content-type'];
      if (typeof mediaType !== 'string' || !/^application\/x-amz-json-1\.1(?:\s*;\s*charset\s*=\s*"?utf-8"?)?$/i.test(mediaType)) { request.resume(); return sendError(new RpcError('UnsupportedMediaTypeException', 'Content-Type must be application/x-amz-json-1.1 with optional UTF-8 charset.')); }
      const target = request.headers['x-amz-target'];
      if (typeof target !== 'string' || !target.startsWith(contract.namespace + '.') || !/^[A-Za-z]+$/.test(target.slice(contract.namespace.length + 1))) { request.resume(); return sendError(new RpcError('ValidationException', 'X-Amz-Target must be ' + contract.namespace + '.OperationName.')); }
      const declaredLength = Number(request.headers['content-length']);
      if (Number.isFinite(declaredLength) && declaredLength > contract.limits.bodyBytes) { request.resume(); return sendError(new RpcError('RequestEntityTooLargeException', 'The request body exceeds the 1 MiB limit.')); }
      const raw = await readBody(request, contract.limits.bodyBytes);
      let input;
      try { input = JSON.parse(raw); } catch { return sendError(new RpcError('ValidationException', 'The request body must contain one valid JSON object.')); }
      const result = runtime.execute(target.slice(contract.namespace.length + 1), input);
      response.statusCode = 200;
      response.end(JSON.stringify(result));
    } catch (error) { sendError(error); }
  });
  server.requestTimeout = 15000;
  server.headersTimeout = 10000;
  server.runtime = runtime;
  return server;
}

if (require.main === module) {
  try {
    const args = process.argv.slice(2);
    let port = 8787, role = 'demo';
    for (let i = 0; i < args.length; i++) {
      if (args[i] === '--port') port = Number(args[++i]);
      else if (args[i] === '--role') role = args[++i];
      else throw new Error('Usage: node api/server.cjs [--port 8787] [--role demo|reader|operator|admin|ingestor]');
    }
    if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('--port must be an integer between 1 and 65535.');
    const server = createServer({ role, onError: (error, requestId) => console.error('Mock request ' + requestId + ' failed:', error.message) });
    server.listen(port, '127.0.0.1', () => {
      console.log(`Resilience workspace mock RPC listening at http://127.0.0.1:${port}/`);
      console.log(`Target: ${contract.namespace}.OperationName; role: ${role}; ${contract.operations.length} operations; in-memory fixture state; no AWS calls.`);
    });
    server.on('error', error => { console.error(error.message); process.exitCode = 1; });
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}

module.exports = { createServer, principalFor };
