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

function app() {
  const listeners = new Map();
  const elements = new Map();
  const storage = new Map();
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
      const value = [...storage.values()][0];
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

test('all local entrypoint and diagram assets exist', () => {
  const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
  for (const [, value] of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
    if (!value.startsWith('#') && !value.includes('://')) assert.ok(fs.existsSync(path.join(root, value)), value);
  }
  for (const name of ['01-business-structure', '02-policy-context', '03-assessments-findings', '04-dependencies-topology', '05-events-observations']) {
    assert.ok(fs.existsSync(path.join(root, 'diagrams', name + '.svg')));
    assert.ok(fs.existsSync(path.join(root, 'diagrams', name + '.mmd')));
  }
  assert.ok(fs.statSync(path.join(root, 'reviewed-report.pdf')).size > 10000);
});
