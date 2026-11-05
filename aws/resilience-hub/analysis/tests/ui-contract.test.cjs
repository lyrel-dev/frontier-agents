/*
 * Render/command contract tests, using the real application scripts and a small
 * in-memory DOM surface. These do not replace browser layout/accessibility QA.
 * No browser, external library, network request, or timer is used here.
 */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');

function app(initialState, sharedStorage) {
  const listeners = new Map();
  const elements = new Map();
  const storage = sharedStorage || new Map();
  if (initialState) storage.set('northstar-resilience-workspace-v3', JSON.stringify(initialState));
  const document = {
    activeElement: null,
    addEventListener(type, handler) { listeners.set(type, handler); },
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, element(id));
      return elements.get(id);
    },
    querySelector() { return element('focus-target'); },
    createElement() { return element('created'); }
  };
  function element(id) {
    return {
      id, innerHTML: '', textContent: '', open: false, dataset: {},
      classList: {add() {}, remove() {}},
      addEventListener() {},
      showModal() { this.open = true; },
      close() { this.open = false; },
      focus() { document.activeElement = this; },
      querySelector() { return element('focus-target'); },
      click() {}
    };
  }
  const sandbox = {
    document, Intl, Date, JSON, Set, Map, console,
    location: {hash: ''}, history: {replaceState() {}},
    localStorage: {
      getItem(key) { return storage.get(key) || null; },
      setItem(key, value) { storage.set(key, value); }
    },
    setTimeout() { return 0; }, clearTimeout() {},
    addEventListener() {},
    FormData: class {
      constructor(form) { this.fields = form.fields; }
      get(key) { return this.fields[key]; }
    }
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  const context = vm.createContext(sandbox);
  for (const file of ['data.js', 'model.js', 'app.js']) {
    vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), context, {filename: file});
  }
  function click(action, options = {}) {
    listeners.get('click')({
      preventDefault() {},
      target: {closest() { return {dataset: {action, ...options}}; }}
    });
  }
  return {
    click,
    html(id = 'app') { return document.getElementById(id).innerHTML; },
    change(id, value) { listeners.get('change')({target: {id, value}}); },
    submit(id, recordId, fields) {
      listeners.get('submit')({preventDefault() {}, target: {id, dataset: {id: recordId}, fields}});
    },
    state() {
      const value = storage.get('northstar-resilience-workspace-v3');
      return value ? JSON.parse(value) : JSON.parse(JSON.stringify(context.RH_MODEL.createState()));
    }
  };
}

test('every workspace view, service tab and record inspector renders with the fixtures', () => {
  const ui = app();
  const state = ui.state();
  for (const view of ['overview', 'systems', 'services', 'findings', 'dependencies', 'events', 'model']) {
    ui.click('navigate', {view});
    assert.match(ui.html(), /<main id="main"/);
    assert.doesNotMatch(ui.html(), /\[object Object\]/);
  }
  for (const service of state.services) {
    ui.click('service', {id: service.id});
    for (const tab of ['overview', 'findings', 'policy', 'dependencies', 'topology', 'assessments']) {
      ui.click('service-tab', {tab});
      assert.ok(ui.html('service-dialog').includes(service.name));
    }
    ui.click('close-service');
  }
  for (const [action, list] of [['finding', state.findings], ['dependency', state.dependencies], ['event', state.events]]) {
    for (const record of list) {
      ui.click(action, {id: record.id});
      assert.ok(ui.html('inspector-dialog').length > 200);
      ui.click('close-inspector');
    }
  }
});

test('system and journey filters render their distinct service membership', () => {
  const ui = app();
  ui.click('navigate', {view: 'services'});
  ui.change('system-filter', 'customer');
  const serviceIds = html => [...html.matchAll(/class="service-name" data-action="service" data-id="([^"]+)"/g)].map(match => match[1]);
  assert.deepEqual(serviceIds(ui.html()).sort(), ['edge', 'identity', 'notifications', 'orders', 'payments']);
  ui.change('journey-filter', 'recovery');
  assert.deepEqual(serviceIds(ui.html()).sort(), ['edge', 'identity', 'notifications']);
});

test('unestimated recommendation costs remain unknown in the finding inspector', () => {
  const ui = app();
  ui.click('finding', {id: 'payments-db'});
  const html = ui.html('inspector-dialog');
  assert.match(html, /Not estimated/);
  assert.doesNotMatch(html, /USD 0[^<]*cost not yet estimated/);
});

test('the overview and service details distinguish current coverage, retained history and attention reasons', () => {
  const model = require('../model.js');
  const fresh = app();
  assert.match(fresh.html(), /Current assessment coverage/);
  assert.match(fresh.html(), /6 current · 7 last known/);
  fresh.click('service', {id: 'fulfillment'});
  assert.match(fresh.html('service-dialog'), /Partial evidence/);
  assert.match(fresh.html('service-dialog'), /older than the local 24-hour review cadence/);
  assert.match(fresh.html('service-dialog'), /Resource coverage gap/);
  fresh.click('close-service');
  fresh.change('system-filter', 'commerce');
  fresh.click('service', {id: 'edge'});
  assert.match(fresh.html('service-dialog'), /Observed open findings/);
  const old = model.createState();
  old.now = new Date(Date.parse(old.now) + 48 * 60 * 60 * 1000).toISOString();
  const aged = app(old);
  assert.match(aged.html(), /0 current · 7 last known/);
  assert.doesNotMatch(aged.html(), /88<small>%/);
});

test('recommendation detail presence and DNS query coverage never turn unavailable evidence into zero', () => {
  const model = require('../model.js');
  for (const presence of ['omitted', 'null', 'empty']) {
    const state = model.createState();
    const finding = state.findings.find(item => item.id === 'payments-db');
    if (presence === 'omitted') delete finding.recommendations;
    else finding.recommendations = presence === 'null' ? null : [];
    const ui = app(state);
    ui.click('service', {id: 'payments', tab: 'findings'});
    if (presence === 'omitted') assert.match(ui.html('service-dialog'), /Recommendation detail not fetched/);
    if (presence === 'null') assert.match(ui.html('service-dialog'), /Recommendation detail unavailable/);
    ui.click('finding', {id: finding.id});
    if (presence === 'null') assert.match(ui.html('inspector-dialog'), /explicitly unavailable \(null\)/);
    if (presence === 'omitted') assert.match(ui.html('inspector-dialog'), /Missing is not the same as empty/);
    if (presence === 'empty') assert.match(ui.html('inspector-dialog'), /contains no recommendation groups/);
  }
  for (const samples of [undefined, [], [{ queryCount: 0 }]]) {
    const state = model.createState();
    const dependency = state.dependencies[0];
    if (samples === undefined) delete dependency.queryRange;
    else dependency.queryRange.dataPoints = samples;
    const ui = app(state);
    ui.click('dependency', {id: dependency.id});
    if (samples === undefined) assert.match(ui.html('inspector-dialog'), /Query counts unavailable/);
    else if (!samples.length) assert.match(ui.html('inspector-dialog'), /No query samples returned/);
    else assert.match(ui.html('inspector-dialog'), /0 across 1 returned samples/);
  }
  const ui = app();
  ui.click('navigate', {view: 'services'});
  assert.match(ui.html(), /Not collected/, 'A service without a finding capture does not show a measured zero');
  ui.click('service', {id: 'notifications', tab: 'findings'});
  assert.match(ui.html('service-dialog'), /Finding coverage gap/);
  assert.match(ui.html('service-dialog'), /an empty local store is not evidence of zero findings/);
});

test('reviewed fixture starts fresh while preserving invalid legacy conclusions outside the active workspace', () => {
  const model = require('../model.js');
  const legacy = model.createState();
  legacy.schemaVersion = 1;
  const checkout = legacy.services.find(service => service.id === 'checkout');
  checkout.posture.state = 'ACHIEVABLE';
  Object.keys(checkout.posture.components).forEach(key => { checkout.posture.components[key] = 'ACHIEVABLE'; });
  legacy.findings.filter(finding => finding.serviceId === 'checkout').forEach(finding => {
    finding.status = 'RESOLVED';
    finding.verification = 'CONFIRMED_AFTER_REASSESSMENT';
  });
  const previous = JSON.stringify(legacy);
  const storage = new Map([['northstar-resilience-workspace-v2', previous]]);
  const ui = app(undefined, storage);
  assert.match(ui.html(), /fresh fixture because earlier assessment conclusions were invalid/);
  assert.equal(ui.state().schemaVersion, 2);
  assert.equal(ui.state().services.find(service => service.id === 'checkout').posture.state, 'NOT_ACHIEVABLE');
  assert.equal(storage.get('northstar-resilience-workspace-v2'), previous);
  assert.equal(storage.has('northstar-resilience-workspace-v3'), false, 'A notice does not overwrite either saved workspace');
  ui.click('dismiss-cache-notice');
  assert.doesNotMatch(ui.html(), /fresh fixture because earlier assessment conclusions were invalid/);
  assert.doesNotMatch(app(undefined, storage).html(), /fresh fixture because earlier assessment conclusions were invalid/, 'The notice is shown only once');
  ui.click('finding', {id: 'payments-db'});
  ui.submit('finding-form', 'payments-db', {status: 'RESOLVED', comment: 'Reviewed fixture triage.'});
  assert.equal(app(undefined, storage).state().findings.find(finding => finding.id === 'payments-db').status, 'RESOLVED', 'Reviewed state is restored from the new key');
  ui.click('reset-confirm');
  assert.match(ui.html('inspector-dialog'), /Earlier saved versions remain untouched/);
  ui.click('reset');
  assert.equal(ui.state().findings.find(finding => finding.id === 'payments-db').status, 'OPEN');
  assert.equal(storage.get('northstar-resilience-workspace-v2'), previous, 'Normal writes and reset retain the legacy session untouched');
});

test('a run started in a service modal can be completed for that same service', () => {
  const ui = app();
  ui.click('service', {id: 'checkout', tab: 'assessments'});
  assert.match(ui.html('service-dialog'), /data-action="scenarios"/);
  ui.click('start-assessment', {id: 'checkout'});
  assert.equal(ui.state().services.find(service => service.id === 'checkout').assessmentStatus, 'PENDING');
  ui.click('scenarios');
  assert.match(ui.html('inspector-dialog'), /successful assessment for Checkout orchestration/);
  ui.click('scenario', {id: 'assessment-completed'});
  const state = ui.state();
  assert.equal(state.services.find(service => service.id === 'checkout').assessmentStatus, 'SUCCESS');
  assert.equal(state.services.find(service => service.id === 'orders').assessmentStatus, 'IN_PROGRESS');
});

test('finding triage persists an escaped comment while retaining health and posture', () => {
  const ui = app();
  const before = ui.state().services.find(service => service.id === 'payments');
  ui.click('finding', {id: 'payments-db'});
  const comment = '<img src=x onerror="alert(1)"> Operator review & follow-up';
  ui.submit('finding-form', 'payments-db', {status: 'RESOLVED', comment});
  const state = ui.state();
  const finding = state.findings.find(item => item.id === 'payments-db');
  const service = state.services.find(item => item.id === 'payments');
  assert.equal(finding.comment, comment);
  assert.equal(finding.verification, 'UNVERIFIED');
  assert.deepEqual(service.health, before.health);
  assert.deepEqual(service.posture, before.posture);
  assert.match(ui.html('inspector-dialog'), /&lt;img src=x/);
  assert.doesNotMatch(ui.html('inspector-dialog'), /<img src=x/);
});

test('local entrypoint links and Obsidian diagram notes resolve with YAML properties', () => {
  function assertLocalReferences(html) {
    for (const [, value] of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
      if (!value.startsWith('#') && !value.includes('://')) assert.ok(fs.existsSync(path.join(root, value)), value);
    }
  }
  function assertNote(relativePath) {
    const note = fs.readFileSync(path.join(root, relativePath), 'utf8');
    const frontMatter = note.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
    assert.ok(frontMatter, relativePath + ': YAML header');
    for (const property of ['id', 'title', 'type', 'service', 'status', 'created', 'updated', 'tags', 'aliases', 'related']) {
      assert.match(frontMatter[1], new RegExp('^' + property + ':', 'm'), relativePath + ': ' + property);
    }
    assert.match(note.slice(frontMatter[0].length), /^# /m, relativePath + ': note title');
    return note;
  }
  assertLocalReferences(fs.readFileSync(path.join(root, 'index.html'), 'utf8'));
  const ui = app();
  ui.click('navigate', {view: 'model'});
  for (let index = 0; index < 5; index++) {
    ui.click('diagram', {index: String(index)});
    assertLocalReferences(ui.html());
  }
  for (const note of ['README.md', 'report.md', 'review.md', 'validation.md', 'api/index.md']) assertNote(note);
  for (const name of ['01-business-structure', '02-policy-context', '03-assessments-findings', '04-dependencies-topology', '05-events-observations']) {
    assert.ok(fs.existsSync(path.join(root, 'diagrams', name + '.svg')));
    const note = assertNote('diagrams/' + name + '.md');
    assert.equal([...note.matchAll(/^```mermaid[ \t]*$/gm)].length, 1, name + ': exactly one Mermaid block');
    assert.match(note, /```mermaid\n[\s\S]*?\n```/, name + ': closed Mermaid block');
  }
});
