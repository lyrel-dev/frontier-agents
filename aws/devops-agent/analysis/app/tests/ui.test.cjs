'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const Model = require('../src/model.js');
const Data = require('../src/mock-data.js');

// Exercise the actual UI functions against a small DOM boundary. These checks
// validate content and identity choices; browser review covers layout and focus.
function loadUI({model = Model, saved = null, writeError = false} = {}) {
  const elements = new Map();
  const listeners = new Map();
  const writes = [];
  function element(selector) {
    if (!elements.has(selector)) elements.set(selector, {
      innerHTML: '', hidden: false, open: false, inert: false, dataset: {},
      classList: {toggle() {}}, setAttribute() {}, removeAttribute() {},
      addEventListener() {}, focus() {}, showModal() { this.open = true; },
      close() { this.open = false; }, querySelector() { return element('close-control'); },
      querySelectorAll() { return []; }, getClientRects() { return [{}]; }, closest() { return null; }
    });
    return elements.get(selector);
  }
  const context = {
    DemoData: Data, DemoModel: model, LensDiagrams: [],
    document: {
      activeElement: null, querySelector: element, getElementById: id => element('#' + id),
      addEventListener: (name, handler) => listeners.set(name, handler)
    },
    window: {addEventListener() {}, matchMedia: () => ({matches:false, addEventListener() {}})},
    localStorage: {getItem: () => saved, setItem: (key, value) => { if (writeError) throw new Error('Storage quota exceeded'); writes.push({key,value}); }},
    getComputedStyle: () => ({visibility:'visible'}), setTimeout() {}, clearTimeout() {},
    setInterval() {}, clearInterval() {}
  };
  const filename = path.join(__dirname, '../src/app.js');
  const source = fs.readFileSync(filename, 'utf8');
  const end = /\n  render\(\);\n\}\)\(\);\s*$/;
  assert.match(source, end, 'UI test hook must replace only the final bootstrap call');
  const instrumented = source.replace(end, `
    globalThis.UI = {
      render, renderStats, renderQueue, renderHistory, summaryPanel, inspectTask, persist, ui,
      state: () => state, recovery: () => stateRecovery
    };
  })();`);
  vm.runInNewContext(instrumented, context, {filename});
  return {api:context.UI, element, writes, listeners};
}

function atStage(stage) {
  const state = Model.createState();
  for (let i = 0; i < stage; i += 1) Model.advance(state);
  return Model.view(state);
}

test('Task source inspection uses the exact selected revision, including historical views', () => {
  const {api, element} = loadUI();
  const completed = atStage(3);
  const early = Object.values(completed.sources).find(source => source.payload?.taskType === 'INVESTIGATION');
  assert.notEqual(early.payload.version, completed.task.version, 'Fixture retains an older task revision');
  api.inspectTask(completed);
  const selected = Model.lookupSource(completed, completed.currentTaskSourceRefId);
  assert.ok(element('#inspector').innerHTML.includes(selected.revisionId));
  assert.ok(element('#inspector').innerHTML.includes('&quot;version&quot;: 9'));
  assert.ok(!element('#inspector').innerHTML.includes('&quot;version&quot;: 4'));

  const state = Model.createState();
  for (let i = 0; i < 5; i += 1) Model.advance(state);
  const retained = Model.view(state, Data.scenario.primaryInvestigationKey, state.snapshots[0].snapshotId);
  api.inspectTask(retained);
  assert.ok(element('#inspector').innerHTML.includes('&quot;version&quot;: 9'));
});

test('Rendered lifecycle card exposes an accessible Task source action wired to the selected revision', () => {
  const {api, element, listeners} = loadUI();
  api.state().step = 3;
  api.render();
  assert.match(element('#workspace').innerHTML, /<button[^>]*data-action="task-source"[^>]*aria-label="Inspect task source: Completed, version 9"/);
  const control = {dataset:{action:'task-source'},disabled:false,closest:selector => selector === '[data-action]' ? control : null};
  listeners.get('click')({target:control});
  assert.ok(element('#inspector').innerHTML.includes('&quot;version&quot;: 9'));
  assert.ok(!element('#inspector').innerHTML.includes('&quot;version&quot;: 4'));
});

test('Candidate panel renders the actual unselected record and its exact source', () => {
  const {api} = loadUI();
  const view = atStage(1);
  const html = api.summaryPanel(view);
  assert.match(html, /Unselected summary candidate/);
  assert.match(html, /Preliminary investigation summary/);
  assert.match(html, /Connection pool contention is the leading explanation/);
  assert.ok(html.includes(`data-id="${view.summary.sourceRefId}"`));
  assert.ok(!html.includes('The causal explanation is still being investigated.'));
});

test('Unsupported summary payload stays escaped JSON instead of becoming formatted prose', () => {
  const {api} = loadUI();
  const view = atStage(3);
  view.summary.bodyFormat = 'json';
  view.summary.body = JSON.stringify({text:'**Untrusted finding**',html:'<img src=x onerror=alert(1)>'}, null, 2);
  const html = api.summaryPanel(view);
  assert.match(html, /shape is not supported by the rich summary renderer/);
  assert.match(html, /<pre class="raw-json section-gap"/);
  assert.ok(html.includes('**Untrusted finding**'));
  assert.ok(html.includes('&lt;img src=x onerror=alert(1)&gt;'));
  assert.ok(!html.includes('<strong>Untrusted finding</strong>'));
  assert.ok(!html.includes('<img src=x'));
});

test('Result readiness and bounded coverage wording do not infer active work or complete evidence', () => {
  const {api} = loadUI();
  const view = atStage(3);
  view.summary = {...view.summary,status:'none',referenceStatus:'not_reported',body:'',recordId:null};
  const stats = api.renderStats(view);
  assert.match(stats, /No selected summary/);
  assert.match(stats, /Completion reported no summary/);
  assert.match(stats, /No known gaps/);
  assert.ok(!stats.includes('Evidence complete'));
  assert.ok(!stats.includes('Collecting evidence'));

  view.task.status = 'IN_PROGRESS';
  view.summary = {...view.summary,status:'pending',recordId:'later-summary'};
  assert.ok(!api.summaryPanel(view).includes('Task completed.'));
  view.summary.status = 'unresolved';
  assert.match(api.summaryPanel(view), /Reference unresolved/);

  const capturedState=Model.createState();
  for(let i=0;i<3;i+=1) Model.advance(capturedState);
  const captured=Model.view(capturedState,Data.scenario.primaryInvestigationKey,capturedState.snapshots[0].snapshotId);
  const live=Model.view(capturedState);
  const coverageRow=html=>html.match(/<tr><td>Collection coverage<\/td>(.*?)<\/tr>/s)[1];
  assert.ok(coverageRow(api.renderHistory(captured,live)).includes(live.coverage.label));
  assert.ok(!coverageRow(api.renderHistory(captured,live)).includes('<td>complete</td>'));
  captured.coverage.label='4 of 4 evidence scopes complete';
  assert.match(coverageRow(api.renderHistory(captured,live)),/4 of 4 observed execution scopes without known gaps/);
  delete captured.coverage.label;
  const missingLiveRow=coverageRow(api.renderHistory(captured,null));
  assert.match(missingLiveRow,/No known gaps in observed execution scopes/);
  assert.match(missingLiveRow,/<td>Unavailable<\/td>/);
});

test('Queue identity and selection use scoped investigation keys', () => {
  const rows = Model.portfolio(Model.createState());
  const second = {...rows[0],key:rows[0].key.replace('111122223333','444455556666'),code:'INC-OTHER'};
  const {api, element} = loadUI({model:{...Model,portfolio:() => [rows[0],second]}});
  api.ui.investigationKey = second.key;
  api.renderQueue();
  const html = element('#queue').innerHTML;
  assert.ok(html.includes(`data-id="${rows[0].key}"`));
  assert.ok(html.includes(`data-id="${second.key}" aria-current="true"`));
  assert.equal((html.match(/aria-current="true"/g) || []).length, 1);
});

test('Corrupt stored state is retained for recovery and never overwritten by normal persistence', () => {
  const saved = '{"version":1,"state":{"schemaVersion":1,"step":0,"snapshots":[{"snapshotId":"broken"}],"nextSnapshotNumber":2}}';
  const {api, element, writes} = loadUI({saved});
  assert.ok(api.recovery());
  assert.equal(api.recovery().raw, saved);
  assert.equal(api.state().step, 0);
  api.persist();
  assert.equal(writes.length, 0);
  api.render();
  assert.match(element('#workspace').innerHTML, /Saved demonstration could not be restored/);
  assert.match(element('#workspace').innerHTML, /Download saved data/);
});

test('Failed browser persistence has a visible session-only notice, including narrow layouts', () => {
  const {api, element} = loadUI({writeError:true});
  api.persist();
  api.render();
  assert.match(element('#workspace').innerHTML, /Session-only changes/);
  assert.match(element('#workspace').innerHTML, /before reloading or closing the page/);
});

test('Retained history still renders when current view and portfolio are unavailable', () => {
  const state = Model.createState();
  for (let i = 0; i < 3; i += 1) Model.advance(state);
  const snapshotId = state.snapshots[0].snapshotId;
  const model = {
    ...Model,
    portfolio:() => { throw new Error('Current portfolio unavailable'); },
    view:(state,key,id) => { if (!id) throw new Error('Current observations unavailable'); return Model.view(state,key,id); }
  };
  const {api, element, listeners} = loadUI({model,saved:JSON.stringify({version:1,state})});
  api.ui.snapshotId = snapshotId;
  api.ui.tab = 'history';
  assert.doesNotThrow(() => api.render());
  const html = element('#workspace').innerHTML;
  assert.match(html, /Current view unavailable/);
  assert.match(html, /Captured view; current comparison unavailable/);
  assert.match(html, /<td>Unavailable<\/td>/);
  assert.match(html, /data-action="capture" disabled/);
  assert.match(html, /data-action="export"/);
  assert.match(element('#queue').innerHTML, /Retained investigation/);
  assert.match(element('#queue').innerHTML, /This entry shows captured state/);
  const control = {dataset:{action:'return-live'},disabled:false,closest:selector => selector === '[data-action]' ? control : null};
  listeners.get('click')({target:control});
  assert.equal(api.ui.snapshotId,snapshotId);
  assert.match(element('#toast').innerHTML, /retained snapshot remains open/);
});
