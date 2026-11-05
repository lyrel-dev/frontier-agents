#!/usr/bin/env node
'use strict';

const contract = require('./contract.cjs');

/** Minimal Node 18+ client for this loopback mock, not an AWS SDK client. */
async function call(operation, input = {}, { endpoint = 'http://127.0.0.1:8787/', fetch: transport = globalThis.fetch } = {}) {
  const url = new URL(endpoint);
  if (!['127.0.0.1', 'localhost', '[::1]'].includes(url.hostname)) throw new Error('The demonstration client accepts only loopback endpoints.');
  const response = await transport(url, { method: 'POST', headers: { 'content-type': contract.mediaType, 'x-amz-target': contract.namespace + '.' + operation }, body: JSON.stringify(input) });
  const data = await response.json();
  if (!response.ok) {
    const error = new Error(data.message || 'RPC request failed.');
    Object.assign(error, { type: data.__type, statusCode: response.status, requestId: response.headers.get('x-amzn-requestid') });
    throw error;
  }
  return { data, requestId: response.headers.get('x-amzn-requestid') };
}
if (require.main === module) {
  const [operation = 'GetWorkspaceSummary', body = '{}', endpoint] = process.argv.slice(2);
  Promise.resolve().then(() => call(operation, JSON.parse(body), endpoint ? { endpoint } : {})).then(result => console.log(JSON.stringify(result, null, 2))).catch(error => { console.error(JSON.stringify({ type: error.type || 'ClientError', message: error.message, statusCode: error.statusCode, requestId: error.requestId }, null, 2)); process.exitCode = 1; });
}
module.exports = { call };
