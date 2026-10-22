'use strict';
(() => {
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const isEditing = () => ['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName);
  const format = seconds => `${Math.floor(seconds / 60).toString().padStart(2,'0')}:${Math.floor(seconds % 60).toString().padStart(2,'0')}`;
  $$('[data-print]').forEach(b => b.addEventListener('click', () => window.print()));
  if (document.body.dataset.view === 'report') {
    const sections = $$('.report-section'), chapters = $$('.chapter');
    const search = $('#search'), type = $('#type'), chapter = $('#chapter');
    function filter() {
      const query = search.value.toLowerCase().trim();
      let count = 0;
      sections.forEach(s => {
        const visible = (!query || s.textContent.toLowerCase().includes(query)) && (!type.value || s.dataset.kind === type.value) && (!chapter.value || s.dataset.chapter === chapter.value);
        s.hidden = !visible;
        if (visible) count++;
      });
      chapters.forEach(c => c.hidden = ![...c.querySelectorAll('.report-section')].some(s => !s.hidden));
      $('#search-status').textContent = `${count} of ${sections.length} sections shown`;
      $('#empty-results').hidden = count !== 0;
    }
    function reset() { search.value = ''; type.value = ''; chapter.value = ''; filter(); }
    [search,type,chapter].forEach(x => x.addEventListener('input',filter));
    $('#reset').addEventListener('click',reset);
    $('#nav-expand').addEventListener('click',() => $$('.toc details').forEach(d => d.open = true));
    $('#nav-collapse').addEventListener('click',() => $$('.toc details').forEach(d => d.open = false));
    function reveal() {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
      const el = document.getElementById(id);
      if (!el) return;
      if (el.matches('.report-section,.chapter') || el.closest('.report-section')) {
        reset();
        const section = el.closest('.report-section') || el.querySelector('.report-section');
        if (section) {
          const link = $$('.toc a[data-section]').find(a => a.dataset.section === section.id);
          if (link) link.closest('details').open = true;
        }
        requestAnimationFrame(() => el.scrollIntoView({block:'start'}));
      }
    }
    window.addEventListener('hashchange',reveal);
    $$('.toc a,.map-link').forEach(a => a.addEventListener('click',() => { reset(); setTimeout(reveal,0); }));
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(e => e.isIntersecting && !e.target.hidden).sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (!visible.length) return;
      const section = visible[0].target;
      $$('.toc a[data-section]').forEach(a => {
        const active = a.dataset.section === section.id;
        a.classList.toggle('active',active);
        if (active) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current');
      });
      $('#reading-location').textContent = section.dataset.path;
    }, {rootMargin:'-80px 0px -60% 0px', threshold:0});
    sections.forEach(s => observer.observe(s));
    document.addEventListener('keydown',e => { if (e.key === '/' && !isEditing()) { e.preventDefault(); search.focus(); } });
    filter(); reveal();
  }
  if (document.body.dataset.view === 'presentation') {
    const slides = $$('.slide'), select = $('#slide-select'), noteBlocks = $$('.note-block');
    const groups = $$('.chapter-strip button'), totalBudget = Number(document.body.dataset.total);
    let index = 0, running = false, totalSpent = 0, last = 0;
    const spent = slides.map(() => 0);
    function collect() {
      if (!running) return;
      const now = performance.now(), delta = Math.max(0,now-last);
      totalSpent += delta; spent[index] += delta; last = now;
    }
    function timers() {
      collect();
      $('#session-time').textContent = `${format(totalSpent/1000)} / ${format(totalBudget)}`;
      $('#slide-time').textContent = `${format(spent[index]/1000)} / ${format(Number(slides[index].dataset.seconds))}`;
      $('#session-clock').classList.toggle('over',totalSpent/1000 > totalBudget);
      $('#slide-clock').classList.toggle('over',spent[index]/1000 > Number(slides[index].dataset.seconds));
    }
    function show(n, updateHash = true) {
      collect(); index = Math.max(0,Math.min(slides.length-1,n));
      slides.forEach((s,i) => s.hidden = i !== index);
      noteBlocks.forEach((s,i) => s.hidden = i !== index);
      select.value = String(index);
      $('#previous').disabled = index === 0; $('#next').disabled = index === slides.length-1;
      const active = slides[index];
      groups.forEach(b => b.setAttribute('aria-current',String(b.dataset.group === active.dataset.group)));
      $('#slide-progress').value = index+1;
      $('#slide-position').textContent = `Slide ${index+1} of ${slides.length} · ${active.dataset.chapter}`;
      $('#slide-announcement').textContent = `Slide ${index+1}: ${active.querySelector('h1').textContent}`;
      if (updateHash) history.replaceState(null,'',`#slide-${String(index+1).padStart(2,'0')}`);
      timers();
    }
    function fromHash() { const m = location.hash.match(/^#slide-(\d+)$/); show(m ? Number(m[1])-1 : 0,false); }
    $('#previous').onclick = () => show(index-1);
    $('#next').onclick = () => show(index+1);
    select.onchange = () => show(Number(select.value));
    groups.forEach(b => b.onclick = () => show(Number(b.dataset.start)));
    $('#agenda-open').onclick = () => $('#agenda').showModal();
    $('#agenda-close').onclick = () => $('#agenda').close();
    $$('#agenda [data-slide]').forEach(b => b.onclick = () => { show(Number(b.dataset.slide)); $('#agenda').close(); });
    $('#timer-toggle').onclick = () => {
      collect(); running = !running; last = performance.now();
      $('#timer-toggle').textContent = running ? 'Pause timer' : 'Start timer';
      $('#timer-toggle').setAttribute('aria-pressed',String(running)); timers();
    };
    $('#timer-reset').onclick = () => { running=false; totalSpent=0; spent.fill(0); $('#timer-toggle').textContent='Start timer'; $('#timer-toggle').setAttribute('aria-pressed','false'); timers(); };
    $('#notes-button').onclick = () => { $('#speaker-notes').open = !$('#speaker-notes').open; if ($('#speaker-notes').open) $('#speaker-notes').scrollIntoView({block:'start'}); };
    $('#fullscreen').onclick = async () => {
      try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); }
      catch { $('#slide-announcement').textContent='Fullscreen is unavailable; browser presentation controls remain active.'; }
    };
    document.addEventListener('keydown',e => {
      if (isEditing() || $('#agenda').open) return;
      const actions = {ArrowRight:()=>show(index+1),PageDown:()=>show(index+1),ArrowLeft:()=>show(index-1),PageUp:()=>show(index-1),Home:()=>show(0),End:()=>show(slides.length-1),n:()=>$('#notes-button').click(),t:()=>$('#timer-toggle').click(),f:()=>$('#fullscreen').click()};
      if (actions[e.key]) { e.preventDefault(); actions[e.key](); }
    });
    window.addEventListener('hashchange',fromHash);
    setInterval(timers,200); fromHash();
  }
})();
