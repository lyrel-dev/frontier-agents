/* Offline behavior. Content and diagrams remain in the HTML document. */
(()=>{
  'use strict';
  const $=(selector,root=document)=>root.querySelector(selector);
  const $$=(selector,root=document)=>Array.from(root.querySelectorAll(selector));
  const time=seconds=>Math.floor(seconds/60).toString().padStart(2,'0')+':'+Math.floor(seconds%60).toString().padStart(2,'0');
  $$('[data-print]').forEach(button=>button.addEventListener('click',()=>window.print()));
  let printDetails=[];
  addEventListener('beforeprint',()=>{printDetails=$$('details.case-reference').map(el=>[el,el.open]);printDetails.forEach(([el])=>el.open=true);});
  addEventListener('afterprint',()=>printDetails.forEach(([el,open])=>el.open=open));

  function setupGuide(){
    const sections=$$('.report-section'),chapters=$$('.chapter');
    const search=$('#search'),chapter=$('#chapter'),type=$('#type');
    function filter(){
      const terms=search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);let visible=0;
      sections.forEach(section=>{
        const text=section.textContent.toLowerCase();
        const show=terms.every(term=>text.includes(term))&&(!chapter.value||chapter.value===section.dataset.chapter)&&(!type.value||type.value===section.dataset.kind);
        section.hidden=!show;if(show)visible++;
      });
      chapters.forEach(c=>c.hidden=!$('.report-section:not([hidden])',c));
      $('#search-status').textContent=visible+' of '+sections.length+' technical sections shown';
      $('#empty-results').hidden=visible!==0;
    }
    function reset(){search.value='';chapter.value='';type.value='';filter();}
    [search,chapter,type].forEach(el=>el.addEventListener('input',filter));
    $('#reset').addEventListener('click',reset);
    $('#nav-expand').addEventListener('click',()=>$$('.toc details').forEach(el=>el.open=true));
    $('#nav-collapse').addEventListener('click',()=>$$('.toc details').forEach(el=>el.open=false));
    function reveal(){
      const id=decodeURIComponent(location.hash.slice(1));if(!id)return;
      const target=document.getElementById(id);if(!target)return;
      const section=target.closest('.report-section');
      if(target.matches('.report-section,.chapter')||section)reset();
      const navId=section?section.id:id;
      const nav=$$('.toc a').find(a=>a.getAttribute('href')==='#'+id)||$$('.toc a').find(a=>a.getAttribute('href')==='#'+navId);
      if(nav){nav.closest('details').open=true;$$('.toc a').forEach(a=>a.classList.toggle('active',a===nav));}
      requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
    }
    addEventListener('hashchange',reveal);filter();if(location.hash)reveal();
    addEventListener('keydown',event=>{
      if(event.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){event.preventDefault();search.focus();}
    });
  }

  function setupCatalog(root){
    const entries=$$('.usecase-entry',root),search=$('[data-uc-search]',root);
    const selectors=['platform','group','delivery','cadence'].map(name=>[name,$('[data-uc-'+name+']',root)]).filter(([,el])=>el);
    function filter(){
      const terms=search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);let shown=0;
      entries.forEach(entry=>{
        const text=entry.textContent.toLowerCase();
        const show=terms.every(term=>text.includes(term))&&selectors.every(([name,el])=>!el.value||(name==='platform'?entry.dataset.platform.split(' ').includes(el.value):el.value===entry.dataset[name]));
        entry.hidden=!show;if(show)shown++;
      });
      $$('[data-uc-group-block]',root).forEach(group=>group.hidden=!$('.usecase-entry:not([hidden])',group));
      $('[data-uc-count]',root).textContent=shown+' of '+entries.length+' use cases shown';
      $('[data-uc-empty]',root).hidden=shown!==0;
    }
    function reset(){search.value='';selectors.forEach(([,el])=>el.value='');filter();}
    search.addEventListener('input',filter);selectors.forEach(([,el])=>el.addEventListener('input',filter));
    $('[data-uc-reset]',root).addEventListener('click',reset);
    const params=new URLSearchParams(location.search);
    selectors.forEach(([name,el])=>{const value=params.get(name);if(value&&Array.from(el.options).some(option=>option.value===value))el.value=value;});
    function reveal(){
      const id=decodeURIComponent(location.hash.slice(1));const target=document.getElementById(id);
      if(!target||!root.contains(target)||!target.matches('.usecase-entry,.catalog-group'))return;
      reset();requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
    }
    filter();addEventListener('hashchange',reveal);if(location.hash)reveal();
  }

  function setupDeck(){
    const slides=$$('.slide'),notes=$$('.note-block'),select=$('#slide-select'),noteBox=$('#speaker-notes');
    let current=0,running=false,session=0,slideElapsed=0,last=performance.now();
    const total=Number(document.body.dataset.total);
    function updateClock(){
      const now=performance.now();if(running){session+=(now-last)/1000;slideElapsed+=(now-last)/1000;}last=now;
      $('#session-time').textContent=time(session);$('#slide-time').textContent=time(slideElapsed)+' / '+time(Number(slides[current].dataset.seconds));
      $('#session-time').classList.toggle('over',session>total);$('#slide-time').classList.toggle('over',slideElapsed>Number(slides[current].dataset.seconds));
    }
    function show(index,writeHash=true){
      updateClock();index=Math.max(0,Math.min(slides.length-1,index));if(index!==current)slideElapsed=0;current=index;
      slides.forEach((slide,i)=>{slide.hidden=i!==current;slide.classList.toggle('active',i===current);});
      notes.forEach((note,i)=>note.hidden=i!==current);select.value=String(current);
      $('#previous').disabled=current===0;$('#next').disabled=current===slides.length-1;
      $$('.chapter-strip button').forEach(button=>button.setAttribute('aria-current',String(button.dataset.chapterButton===slides[current].dataset.group)));
      if(writeHash)history.replaceState(null,'','#'+slides[current].id);
      updateClock();
    }
    function fromHash(){const match=location.hash.match(/^#slide-(\d+)$/);show(match?Number(match[1])-1:0,false);}
    select.addEventListener('change',()=>show(Number(select.value)));
    $('#previous').addEventListener('click',()=>show(current-1));$('#next').addEventListener('click',()=>show(current+1));
    $$('[data-slide]').forEach(button=>button.addEventListener('click',()=>{show(Number(button.dataset.slide));if($('#agenda').open)$('#agenda').close();}));
    $('#agenda-open').addEventListener('click',()=>$('#agenda').showModal());$('#agenda-close').addEventListener('click',()=>$('#agenda').close());
    $('#notes-button').addEventListener('click',()=>{noteBox.open=!noteBox.open;$('#notes-button').setAttribute('aria-expanded',String(noteBox.open));});
    noteBox.addEventListener('toggle',()=>$('#notes-button').setAttribute('aria-expanded',String(noteBox.open)));
    $('#timer-toggle').addEventListener('click',()=>{updateClock();running=!running;$('#timer-toggle').textContent=running?'Pause timer':'Start timer';});
    $('#timer-reset').addEventListener('click',()=>{running=false;session=0;slideElapsed=0;last=performance.now();$('#timer-toggle').textContent='Start timer';updateClock();});
    $('#fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch(error){$('#fullscreen').textContent='Fullscreen unavailable';}});
    addEventListener('keydown',event=>{
      if(/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)||event.ctrlKey||event.metaKey||event.altKey||$('#agenda').open)return;
      if(['ArrowRight','PageDown','ArrowLeft','PageUp','Home','End'].includes(event.key))event.preventDefault();
      if(['ArrowRight','PageDown'].includes(event.key))show(current+1);
      if(['ArrowLeft','PageUp'].includes(event.key))show(current-1);
      if(event.key==='Home')show(0);if(event.key==='End')show(slides.length-1);
      if(event.key.toLowerCase()==='n')$('#notes-button').click();
    });
    addEventListener('hashchange',fromHash);fromHash();setInterval(updateClock,200);
  }
  if(document.body.dataset.view==='report')setupGuide();
  $$('[data-usecase-catalog]').forEach(setupCatalog);
  if(document.body.dataset.view==='presentation')setupDeck();
})();
