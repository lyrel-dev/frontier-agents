'use strict';

// Cross-surface assertions use the product invariant and explicit fixture
// expectations, not merely the runtime's own schema validator.
const test = require('node:test');
const assert = require('node:assert/strict');
const model = require('../model.js');
const { createRuntime } = require('../api/runtime.cjs');

test('browser and RPC expose the same explainable current versus retained evidence at baseline and after expiry', () => {
  const browser = model.createState();
  let now = Date.parse(browser.now);
  const runtime = createRuntime({ state: browser, now: () => now, secret: 'cross-surface-evidence-review' });

  function compare(expected) {
    const metrics = model.metrics(browser);
    const summary = runtime.execute('GetWorkspaceSummary', {}).summary;
    assert.equal(metrics.totalServices, 8);
    assert.equal(summary.serviceCount, 8);
    assert.equal(metrics.currentAssessed, expected.currentCount);
    assert.equal(summary.currentAssessedCount, expected.currentCount);
    assert.equal(metrics.currentAssessmentCoverage, expected.currentPercent);
    assert.equal(summary.currentAssessmentCoverage, expected.currentPercent);
    assert.equal(metrics.lastKnownAssessed, 7);
    assert.equal(summary.lastKnownAssessedCount, 7);
    assert.equal(metrics.lastKnownAssessmentCoverage, 88);
    assert.equal(summary.lastKnownAssessmentCoverage, 88);
    assert.equal(metrics.attention, 8);
    assert.equal(summary.attentionCount, 8);
    assert.equal(new Set(summary.contributorServiceArns).size, summary.serviceCount);
    assert.equal(new Set(summary.membershipContext.map(item => item.serviceArn)).size, summary.serviceCount);
    assert.equal(summary.evidenceRuleVersion, 'assessment-evidence-24h-v2');
    for (const service of browser.services) {
      const status = runtime.execute('GetServiceStatus', { serviceArn: service.arn }).serviceStatus;
      const coverage = model.assessmentCoverage(browser, service);
      assert.equal(status.assessmentCoverage.status, coverage.status, service.name + ' coverage');
      assert.equal(status.assessmentCoverage.current, coverage.current, service.name + ' currentness');
      assert.deepEqual(status.assessmentCoverage.expectedComponents, coverage.expectedComponents);
      assert.deepEqual(status.attentionReasons.map(reason => reason.code).sort(), model.attentionReasons(browser, service).map(reason => reason.code).sort(), service.name + ' attention explanation');
      assert.equal(status.needsAttention, status.attentionReasons.length > 0);
      assert.ok(status.selectedObservations, 'The read includes evidence, not only a badge.');
    }
  }

  compare({ currentCount: 6, currentPercent: 75 });
  now += 48 * 60 * 60 * 1000;
  browser.now = new Date(now).toISOString();
  compare({ currentCount: 0, currentPercent: 0 });
});

test('an empty visible scope has no percentage denominator on either surface', () => {
  const state = model.createState();
  const runtime = createRuntime({ state, now: () => Date.parse(state.now), secret: 'empty-scope-review' });
  const query = 'no-service-matches-this-review-scope';
  const metrics = model.metrics(state, { query });
  const summary = runtime.execute('GetWorkspaceSummary', { query }).summary;
  assert.equal(metrics.totalServices, 0);
  assert.equal(summary.serviceCount, 0);
  assert.equal(metrics.currentAssessmentCoverage, null);
  assert.equal(metrics.lastKnownAssessmentCoverage, null);
  assert.equal(summary.currentAssessmentCoverage, null);
  assert.equal(summary.lastKnownAssessmentCoverage, null);
  assert.deepEqual(summary.contributorServiceArns, []);
  assert.deepEqual(summary.membershipContext, []);
});

test('a claimed repair creates the same local reassessment obligation on both surfaces without changing observed posture', () => {
  const browser = model.createState();
  let now = Date.parse(browser.now);
  const runtime = createRuntime({ state: browser, now: () => now, secret: 'triage-parity-review' });
  const finding = browser.findings.find(item => item.id === 'edge-cache');
  const service = browser.services.find(item => item.arn === finding.serviceArn);
  const beforePosture = structuredClone(service.posture);
  const command = { serviceArn: finding.serviceArn, findingId: finding.findingId, status: 'RESOLVED', comment: 'Claimed repair awaiting independent evidence.', expectedVersion: 1, clientToken: 'triage-parity-review' };
  assert.equal(model.updateFinding(browser, finding.id, command.status, command.comment).ok, true);
  now = Date.parse(browser.now);
  const result = runtime.execute('UpdateFailureModeFinding', command).finding;
  const status = runtime.execute('GetServiceStatus', { serviceArn: finding.serviceArn }).serviceStatus;
  assert.deepEqual(service.posture, beforePosture);
  assert.equal(finding.verification, 'UNVERIFIED');
  assert.equal(result.verification, 'UNVERIFIED');
  assert.equal(service.reassessmentRequired, true);
  assert.equal(status.reassessmentRequired, true);
  assert.equal(model.assessmentCoverage(browser, service).status, 'PARTIAL');
  assert.equal(status.assessmentCoverage.status, 'PARTIAL');
  assert.equal(status.posture.state, beforePosture.state);
  assert.deepEqual(status.attentionReasons.map(item => item.code).sort(), model.attentionReasons(browser, service).map(item => item.code).sort());
  assert.ok(status.attentionReasons.some(item => item.code === 'LOCAL_REASSESSMENT_REQUIRED'));
  assert.equal(runtime.execute('GetService', { serviceArn: finding.serviceArn }).service.version, 1, 'Triage does not edit service configuration.');
});
