/* Progressive enhancement only. Every contract remains readable without JavaScript. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const search = document.getElementById('reference-search');
  const moduleFilter = document.getElementById('module-filter');
  const kindFilter = document.getElementById('kind-filter');
  const reset = document.getElementById('reset-filters');
  const count = document.getElementById('result-count');
  const results = document.getElementById('search-results');
  const cards = [...document.querySelectorAll('.reference-card[data-kind]')];
  const groups = [...document.querySelectorAll('.module-group')];
  const catalogChapters = ['entities', 'operations'].map(id => document.getElementById(id));
  const index = cards.map(card => ({
    card,
    text: (card.dataset.search || card.textContent).normalize('NFKC').toLowerCase(),
    name: card.dataset.name,
    kind: card.dataset.kind,
    module: card.dataset.module
  }));

  function filter() {
    const tokens = search.value.normalize('NFKC').toLowerCase().trim().split(/\s+/).filter(Boolean);
    const active = tokens.length > 0 || moduleFilter.value !== 'all' || kindFilter.value !== 'all';
    const matches = [];
    index.forEach(item => {
      const shown = (moduleFilter.value === 'all' || item.module === moduleFilter.value)
        && (kindFilter.value === 'all' || item.kind === kindFilter.value)
        && tokens.every(token => item.text.includes(token));
      item.card.hidden = !shown;
      if (shown) matches.push(item);
    });
    groups.forEach(group => {
      group.hidden = !group.querySelector('.reference-card:not([hidden])');
    });
    catalogChapters.forEach(chapter => {
      chapter.hidden = !chapter.querySelector('.reference-card:not([hidden])');
    });
    const entities = matches.filter(item => item.kind === 'entity').length;
    const operations = matches.length - entities;
    count.textContent = `${entities} of 36 entities · ${operations} of 108 operations` +
      (matches.length ? (active ? ' match. Select a result below or continue to the catalog.' : '. All entries are shown below.')
        : '. No matches. Clear the filters or try a broader term.');
    results.replaceChildren();
    results.hidden = !active || !matches.length;
    if (active) {
      const fragment = document.createDocumentFragment();
      matches.forEach(item => {
        const link = document.createElement('a');
        link.href = '#' + item.card.id;
        const label = document.createElement('span');
        label.textContent = item.name;
        const type = document.createElement('span');
        type.className = 'result-type';
        type.textContent = `${item.kind === 'entity' ? 'Entity' : 'Operation'} · ${item.module}`;
        link.append(label, type);
        fragment.append(link);
      });
      results.append(fragment);
    }
  }

  function clearFilters() {
    search.value = '';
    moduleFilter.value = 'all';
    kindFilter.value = 'all';
    filter();
  }

  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    const card = target.closest('.reference-card');
    if (card && card.hidden) clearFilters();
    let parent = target;
    while (parent) {
      if (parent.tagName === 'DETAILS') parent.open = true;
      parent = parent.parentElement;
    }
    if (typeof target.scrollIntoView === 'function') target.scrollIntoView({ block: 'start' });
  }

  search.addEventListener('input', filter);
  moduleFilter.addEventListener('change', filter);
  kindFilter.addEventListener('change', filter);
  reset.addEventListener('click', () => { clearFilters(); search.focus(); });
  window.addEventListener('hashchange', revealHash);
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link && link.hash === location.hash) revealHash();
  });
  document.querySelectorAll('[data-diagram-zoom]').forEach(button => {
    button.addEventListener('click', () => {
      const frame = document.getElementById(button.dataset.diagramZoom);
      const zoomed = frame.classList.toggle('zoomed');
      button.textContent = zoomed ? 'Fit to page' : 'View at full size';
      button.setAttribute('aria-pressed', String(zoomed));
    });
  });
  const printButton = document.getElementById('print-reference');
  printButton.addEventListener('click', () => window.print());
  const printOpen = new Map();
  window.addEventListener('beforeprint', () => {
    document.querySelectorAll('main details:not(.raw-schema)').forEach(detail => {
      printOpen.set(detail, detail.open);
      detail.open = true;
    });
  });
  window.addEventListener('afterprint', () => {
    printOpen.forEach((wasOpen, detail) => { detail.open = wasOpen; });
    printOpen.clear();
  });
  filter();
  if (location.hash) revealHash();
})();
