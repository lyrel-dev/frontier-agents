'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const Model = require('../src/model.js');
const fixture = require('../src/mock-data.js');
const copy = () => structuredClone(fixture);

// These assertions exercise semantic boundaries from the reviewed model rather
// than DOM structure or cosmetic implementation details.
test('the normalized scenario validates and retains its distinct counting units', () => {
  assert.deepEqual(Model.validateData(fixture), []);
  assert.deepEqual(Model.metrics(fixture), {
    events: 10,
    openIssues: 3,
    affectedAccounts: 5,
    impairedEntities: 4,
    pendingEntities: 5,
    reportedEntities: 21,
    mappedResources: 19,
    unknownEntities: 5,
    unsuppliedEntities: 1,
    actionRequiredEvents: 4
  });
  const network = Model.eventRows(fixture).find(row => row.id === 'evt-ec2-network');
  assert.equal(network.summaryContexts.length, 1);
  assert.equal(network.contexts.length, 2, 'organization summary cannot add another affected account');
  assert.equal(network.accounts.length, 2);
});

test('public notification visibility never becomes affected-account attribution', () => {
  for (const account of fixture.accounts) {
    const rows = Model.eventRows(fixture, { account: account.id, scope: 'PUBLIC' });
    assert.equal(rows.length, 1);
    assert.equal(rows[0].id, 'evt-s3-public');
    assert.deepEqual(rows[0].accounts, []);
    assert.equal(rows[0].entityCount, 0);
    assert.equal(Model.metrics(fixture, { account: account.id, scope: 'PUBLIC' }).affectedAccounts, 0);
  }
  const repeated = copy();
  repeated.deliveries.push(...structuredClone(repeated.deliveries));
  assert.equal(Model.metrics(repeated).events, 10, 'additional delivery attempts are not additional Health events');
});

test('account-scoped totals count the visible contexts and retain the public advisory', () => {
  const filters = { account: '111100001002' };
  assert.deepEqual(Model.eventRows(fixture, filters).map(row => row.id), ['evt-s3-public', 'evt-lambda-runtime', 'evt-ec2-retirement']);
  assert.deepEqual(Model.metrics(fixture, filters), {
    events: 3, openIssues: 1, affectedAccounts: 1,
    impairedEntities: 0, pendingEntities: 3, reportedEntities: 3,
    mappedResources: 3, unknownEntities: 0, unsuppliedEntities: 0,
    actionRequiredEvents: 2
  });
  const narrowed = Model.metrics(fixture, { account: '111100001002', region: 'eu-west-1', category: 'scheduledChange' });
  assert.equal(narrowed.events, 2);
  assert.equal(narrowed.reportedEntities, 3);
  assert.equal(Model.metrics(fixture, { q: 'nothing-matches-this-demo' }).events, 0);
  assert.equal(Model.metrics(fixture, { actionability: 'ACTION_REQUIRED' }).events, 4);
  assert.equal(Model.metrics(fixture, { actionability: 'required' }).events, 4);
});

test('status filtering matches individual contexts while mixed is an explicit local rollup', () => {
  const data = copy();
  data.contexts.find(context => context.id === 'ctx-lambda-development').statusCode = 'closed';
  const row = Model.eventRows(data, { status: 'closed' }).find(event => event.id === 'evt-lambda-runtime');
  assert.ok(row, 'a closed account context qualifies the event even when other accounts remain open');
  assert.equal(row.status, 'mixed');
  assert.equal(row.statusIsDerived, true);
  assert.equal(row.statusCounts.open, 2);
  assert.equal(row.statusCounts.closed, 1);
  const accountRow = Model.eventRows(data, { account: '111100001005', status: 'closed' }).find(event => event.id === 'evt-lambda-runtime');
  assert.equal(accountRow.status, 'closed');
  assert.equal(accountRow.statusIsDerived, false);
  assert.equal(accountRow.accounts.length, 1);
});

test('explicit UNKNOWN, unsupplied status, and impaired state remain distinct', () => {
  const values = Model.metrics(fixture);
  assert.equal(values.unknownEntities, 5);
  assert.equal(values.unsuppliedEntities, 1);
  assert.equal(values.impairedEntities, 4);
  const billing = Model.eventRows(fixture).find(row => row.id === 'evt-rds-billing');
  assert.equal(billing.unknownCount, 0);
  assert.equal(billing.unsuppliedCount, 1);
  assert.equal(billing.entities[0].statusCode, null);
  const forwardCompatible = copy();
  forwardCompatible.entities.find(entity => entity.statusCode === 'UNKNOWN').statusCode = 'NEW_PROVIDER_STATE';
  assert.deepEqual(Model.validateData(forwardCompatible), [], 'an unfamiliar provider enum should be preserved, not guessed');
  assert.equal(Model.metrics(forwardCompatible).unknownEntities, 4);
  assert.equal(Model.metrics(forwardCompatible).reportedEntities, 21);
});

test('operator completion and verification cannot resolve provider impact or stale inventory exposure', () => {
  const before = JSON.stringify(fixture);
  const initial = Model.workRows(fixture, fixture.workItems).find(item => item.id === 'wi-lambda-webhook');
  assert.equal(initial.state, 'completed');
  assert.equal(initial.pendingProviderCount, 1);
  const localItems = structuredClone(fixture.workItems);
  localItems.find(item => item.id === 'wi-lambda-webhook').state = 'verified';
  const changed = Model.workRows(fixture, localItems).find(item => item.id === 'wi-lambda-webhook');
  assert.equal(changed.state, 'verified');
  assert.equal(changed.pendingProviderCount, 1);
  assert.equal(Model.metrics(fixture).pendingEntities, 5);
  assert.equal(Model.lifecycleRows(fixture).find(row => row.id === 'exposure-lambda-webhook').riskStatus, 'due_soon');
  assert.equal(JSON.stringify(fixture), before, 'selectors must not mutate source or local fixture state');
});

test('one verified resource in two events is two impact records but one resource', () => {
  const rows = Model.eventRows(fixture);
  const impacts = rows.flatMap(row => row.entities).filter(entity => entity.resourceId === 'res-warehouse-writer');
  assert.equal(impacts.length, 2);
  assert.notEqual(impacts[0].id, impacts[1].id);
  assert.notEqual(impacts[0].contextId, impacts[1].contextId);
  assert.equal(rows.flatMap(row => row.entities).filter(entity => entity.resource).length, 20);
  assert.equal(Model.metrics(fixture).mappedResources, 19);
  assert.equal(Model.metrics(fixture, { q: 'warehouse', region: 'us-east-1' }).mappedResources, 2);
});

test('incomplete coverage cannot be presented as healthy when no event is returned', () => {
  const coverage = Model.coverageSummary(fixture);
  assert.equal(coverage.state, 'partial');
  assert.equal(coverage.complete, 3);
  assert.equal(coverage.total, 5);
  assert.deepEqual(new Set(coverage.issues.map(record => record.status)), new Set(['stale', 'partial']));
  assert.equal(coverage.lastCollectedAt, '2026-11-05T13:29:00Z');
  const matrix = Model.serviceMatrix(fixture);
  const oregonS3 = matrix.find(row => row.service === 'S3').cells.find(cell => cell.region === 'us-west-2');
  assert.equal(oregonS3.count, 0);
  assert.equal(oregonS3.state, 'unknown');
  const oregonEC2 = matrix.find(row => row.service === 'EC2').cells.find(cell => cell.region === 'us-west-2');
  assert.equal(oregonEC2.state, 'issue', 'an observed issue remains visible even with incomplete coverage');
  assert.equal(oregonEC2.coverage.state, 'partial');
  const frankfurtLambda = matrix.find(row => row.service === 'LAMBDA').cells.find(cell => cell.region === 'eu-central-1');
  assert.equal(frankfurtLambda.state, 'clear');
  assert.equal(frankfurtLambda.label, 'No open events observed');
  const absent = copy();
  absent.coverage = [];
  assert.equal(Model.coverageSummary(absent).state, 'unknown');
  assert.ok(Model.serviceMatrix(absent, { q: 'nothing-matches-this-demo' }).flatMap(row => row.cells).every(cell => cell.state === 'unknown'));
});

test('lifecycle risk uses the snapshot clock and preserves the unmatched deployment as unknown', () => {
  const rows = Model.lifecycleRows(fixture);
  assert.equal(rows.filter(row => !row.unmatched).length, 7);
  assert.equal(rows.filter(row => row.unmatched).length, 1);
  const unmatched = rows.find(row => row.unmatched);
  assert.equal(unmatched.deploymentId, 'deployment-development-eks');
  assert.equal(unmatched.riskStatus, 'unknown');
  assert.equal(unmatched.daysUntil, null);
  const eks = rows.find(row => row.id === 'exposure-eks-analytics');
  assert.equal(eks.daysUntil, 7);
  assert.equal(eks.riskStatus, 'due_soon');
  assert.equal(rows.find(row => row.id === 'exposure-rds-writer').riskStatus, 'overdue');
  const future = copy();
  future.meta.asOf = '2026-11-13T13:30:00Z';
  const later = Model.lifecycleRows(future).find(row => row.id === 'exposure-eks-analytics');
  assert.equal(later.daysUntil, -1);
  assert.equal(later.riskStatus, 'overdue');
  assert.equal(Model.lifecycleRows(fixture, { account: '111100001002' }).length, 2);
});

test('reference review catches context, identity, account, and exactly-one target violations', () => {
  const invalid = copy();
  invalid.entities[0].contextId = invalid.contexts.find(context => context.kind === 'ORG_SUMMARY').id;
  invalid.entities[1].awsAccountId = '111100001005';
  invalid.workItemTargets[0].exposureId = invalid.exposures[0].id;
  invalid.events.push(Object.assign({}, invalid.events[0], { id: 'duplicate-event-identity' }));
  invalid.exposures[0].deploymentId = 'missing-deployment';
  const errors = Model.validateData(invalid);
  assert.ok(errors.some(error => error.includes('ORG_SUMMARY must not own entity')));
  assert.ok(errors.some(error => error.includes('awsAccountId contradicts')));
  assert.ok(errors.some(error => error.includes('exactly one')));
  assert.ok(errors.some(error => error.includes('Duplicate eventArn')));
  assert.ok(errors.some(error => error.includes('missing-deployment')));
});
