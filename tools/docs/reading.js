/* Offline reading controls. Canonical records and guide text are never modified. */
(()=>{
 'use strict';
 const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
 const hash=()=>{try{return decodeURIComponent(location.hash.slice(1));}catch{return '';}};
 const contents=$('#reader-contents');
 if(contents && matchMedia('(max-width:760px)').matches)contents.open=false;
 $$('[data-print]').forEach(b=>b.addEventListener('click',()=>window.print()));
 let priorDetails=[];
 addEventListener('beforeprint',()=>{priorDetails=$$('main details').map(d=>[d,d.open]);priorDetails.forEach(([d])=>d.open=true);});
 addEventListener('afterprint',()=>priorDetails.forEach(([d,open])=>d.open=open));
 function openParents(node){for(let p=node;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;}
 if(document.body.dataset.reader==='guide'){
  const chapters=$$('[data-reader-chapter]'), sections=$$('.report-section');
  const search=$('#guide-search'), all=$('#read-all'), status=$('#guide-search-status');
  let current=0;
  function apply(){
   const terms=search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);let count=0;
   chapters.forEach((c,i)=>{
    let matches=0;
    $$('.report-section',c).forEach(s=>{const match=terms.every(t=>s.textContent.toLowerCase().includes(t));s.hidden=terms.length>0&&!match;if(match)matches++;});
    c.hidden=terms.length>0?matches===0:(!all.checked&&i!==current);
    if(!c.hidden)count+=matches;
   });
   status.textContent=terms.length?count+' matching sections across '+chapters.length+' chapters':(all.checked?'Reading all '+chapters.length+' chapters':'Reading chapter '+(current+1)+' of '+chapters.length);
   $('#guide-empty').hidden=!terms.length||count>0;
   const pager=$('.chapter-pager');pager.hidden=!!terms.length||all.checked;
   const previous=$('#previous-chapter'),next=$('#next-chapter');
   previous.hidden=current===0;next.hidden=current===chapters.length-1;
   if(current>0){previous.href='#'+chapters[current-1].id;previous.textContent='← '+$('h2',chapters[current-1]).textContent;}
   if(current<chapters.length-1){next.href='#'+chapters[current+1].id;next.textContent=$('h2',chapters[current+1]).textContent+' →';}
   $('#chapter-position').textContent=(current+1)+' / '+chapters.length;
   $$('.toc a').forEach(a=>{a.removeAttribute('aria-current');if(a.getAttribute('href')==='#'+chapters[current].id)a.setAttribute('aria-current','location');});
  }
  function reveal(scroll=true){
   const id=hash();if(!id){current=0;apply();return;}
   const target=document.getElementById(id);if(!target)return;
   const chapter=target.closest('[data-reader-chapter]');
   if(chapter){current=chapters.indexOf(chapter);search.value='';all.checked=false;apply();openParents(target);
    const section=target.closest('.report-section');
    $$('.toc a').forEach(a=>{if(a.getAttribute('href')==='#'+id || (section&&a.getAttribute('href')==='#'+section.id)){openParents(a);a.setAttribute('aria-current','location');}});
   }
   if(scroll)requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
  }
  search.addEventListener('input',apply);all.addEventListener('change',apply);
  $('.reader-search').addEventListener('submit',e=>e.preventDefault());
  $('.reader-search').addEventListener('reset',()=>{search.value='';apply();});
  addEventListener('hashchange',()=>reveal());apply();if(hash())reveal();
  addEventListener('keydown',e=>{if(e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();search.focus();}});
 }
 if(document.body.dataset.reader==='directory'){
  const input=$('#case-search'),product=$('#case-product'),group=$('#case-group');
  const entries=$$('.case-index-entry'),groups=$$('.case-group'),routes=JSON.parse($('#case-routes').textContent);
  const params=new URLSearchParams(location.search);
  input.value=params.get('q')||'';product.value=params.get('platform')||'';group.value=params.get('group')||'';
  function filter(save=true){
   const terms=input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);let count=0;
   entries.forEach(e=>{const yes=(!product.value||e.dataset.products.split(' ').includes(product.value))&&(!group.value||e.dataset.group===group.value)&&terms.every(t=>e.textContent.toLowerCase().includes(t));e.hidden=!yes;if(yes)count++;});
   groups.forEach(g=>{g.hidden=!$('.case-index-entry:not([hidden])',g);const a=$('.group-navigation a[href="#'+g.id+'"]');if(a)a.closest('li').hidden=g.hidden;});
   $('#case-count').textContent=count+' of '+entries.length+' use cases';$('#case-empty').hidden=count!==0;
   if(save){const q=new URLSearchParams();if(input.value)q.set('q',input.value);if(product.value)q.set('platform',product.value);if(group.value)q.set('group',group.value);history.replaceState(null,'',location.pathname+(q.size?'?'+q.toString():'')+location.hash);}
  }
  function route(){
   const id=hash();if(routes.cases[id]){location.replace(routes.cases[id]);return;}
   const old=routes.aliases.find(a=>a.id===id);
   if(old){if(old.targets.length===1){location.replace(old.targets[0]);return;}const choice=document.getElementById(id);choice.hidden=false;choice.scrollIntoView();return;}
   const target=document.getElementById(id);
   if(target&&target.classList.contains('case-group')){input.value='';product.value='';group.value='';filter(false);target.scrollIntoView();}
  }
  [input,product,group].forEach(e=>e.addEventListener('input',()=>filter()));
  $('.catalog-search').addEventListener('submit',e=>e.preventDefault());
  $('.catalog-search').addEventListener('reset',()=>{input.value='';product.value='';group.value='';filter();});
  addEventListener('hashchange',route);filter(false);route();
 }
 if(document.body.dataset.reader==='case'){
  function reveal(){const target=document.getElementById(hash());if(target){openParents(target);requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}}
  addEventListener('hashchange',reveal);if(hash())reveal();
 }
})();
