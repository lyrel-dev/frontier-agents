/* Dependency-free charts. No network access, inferred history or interpolated gaps. */
(function installMetricCharts() {
  'use strict';
  const registry = new Map();
  let sequence = 0;
  const escape = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const numeric = v => typeof v === 'boolean' ? Number(v) : (typeof v === 'number' && Number.isFinite(v) ? v : null);
  const date = t => new Date(t).toISOString();
  const stamp = t => date(t).replace('T', ' ').replace('.000Z', ' UTC');
  const format = (v, unit) => {
    if (v === null || v === undefined) return 'No sample';
    if (typeof v === 'boolean') return v ? 'True (1)' : 'False (0)';
    const x = unit === 'ratio' ? v * 100 : v;
    return new Intl.NumberFormat('en-GB', {maximumFractionDigits: Math.abs(x) < 1 ? 4 : 2}).format(x) + (unit === 'ratio' ? '%' : '');
  };
  function allPoints(spec) { return spec.traces.flatMap(t => t.points.map(p => ({...p, trace:t.label, source:t.source, ref:p.ref || t.ref, unit:spec.unit}))).sort((a,b) => a.t-b.t); }
  function extent(spec) {
    let lo=Infinity,hi=-Infinity;
    for(const trace of spec.traces)for(const p of trace.points)if(Number.isFinite(p.t)){if(p.t<lo)lo=p.t;if(p.t>hi)hi=p.t;}
    if(lo===Infinity)return null;
    return hi === lo ? [lo-30000, hi+30000] : [lo,hi];
  }
  function visible(entry) { return entry.spec.traces.filter((_,i) => !entry.hidden.has(i)); }
  function geometry(entry) {
    const mini=entry.mini, width=mini?260:640, height=mini?86:240;
    const pad=mini?{l:10,r:10,t:10,b:15}:{l:65,r:18,t:20,b:38};
    const range=entry.range || extent(entry.spec) || [0,1];
    let low=Infinity,high=-Infinity;
    const include=v=>{const n=numeric(v);if(n!==null){if(n<low)low=n;if(n>high)high=n;}};
    for(const trace of visible(entry))for(const p of trace.points)if(p.t>=range[0]&&p.t<=range[1])include(p.value);
    if(!mini)for(const limit of entry.spec.limits||[])include(limit.value);
    if(low===Infinity){low=0;high=1;}
    if (low === high) { const gap=Math.abs(low)*.1 || 1; low-=gap; high+=gap; }
    else { const gap=(high-low)*.12; low-=gap; high+=gap; }
    const x=t=>pad.l+(t-range[0])/(range[1]-range[0])*(width-pad.l-pad.r);
    const y=v=>height-pad.b-(v-low)/(high-low)*(height-pad.t-pad.b);
    return {width,height,pad,range,low,high,x,y};
  }
  function segments(trace, range) {
    const result=[];let current=[],previous=null;
    for(const p of trace.points){
      if(p.t<range[0]||p.t>range[1])continue;
      const gap=previous!==null&&trace.cadence&&p.t-previous>trace.cadence*1500;
      if(numeric(p.value)===null||gap){if(current.length)result.push(current);current=[];}
      if(numeric(p.value)!==null)current.push(p);
      previous=p.t;
    }
    if(current.length)result.push(current);
    return result;
  }
  // Preserve each segment's endpoints and bucket extrema; never bridge a gap.
  function reduced(points, max=600) {
    if(points.length<=max)return points;
    const step=Math.ceil(points.length/(max/2)),out=[points[0]];
    for(let i=1;i<points.length-1;i+=step){
      const bucket=points.slice(i,Math.min(i+step,points.length-1));
      let a=bucket[0],b=bucket[0];for(const p of bucket){if(numeric(p.value)<numeric(a.value))a=p;if(numeric(p.value)>numeric(b.value))b=p;}
      out.push(...(a===b?[a]:[a,b].sort((p,q)=>p.t-q.t)));
    }
    out.push(points.at(-1));return out;
  }
  function svg(entry) {
    const {spec,mini,id}=entry,g=geometry(entry),{width,height,pad,x,y,range}=g;
    const data=visible(entry).flatMap(t=>t.points).filter(p=>p.t>=range[0]&&p.t<=range[1]&&numeric(p.value)!==null);
    let body=`<defs><clipPath id="${id}-clip"><rect x="${pad.l-2}" y="${pad.t-3}" width="${width-pad.l-pad.r+4}" height="${height-pad.t-pad.b+6}"/></clipPath></defs>`;
    if(!mini)for(let i=0;i<4;i++){
      const v=g.low+(g.high-g.low)*i/3,yy=y(v);
      body+=`<line class="mc-grid" x1="${pad.l}" x2="${width-pad.r}" y1="${yy}" y2="${yy}"/><text class="mc-axis" x="${pad.l-8}" y="${yy+4}" text-anchor="end">${escape(format(v,spec.unit))}</text>`;
    }
    if(!mini)for(let i=0;i<3;i++){
      const t=range[0]+(range[1]-range[0])*i/2;
      body+=`<text class="mc-axis" x="${x(t)}" y="${height-14}" text-anchor="${i===0?'start':i===2?'end':'middle'}">${escape((range[1]-range[0]>86400000?date(t).slice(5,16).replace('T',' '):date(t).slice(11,19)))}</text>`;
    }
    body+=`<g clip-path="url(#${id}-clip)">`;
    if(!mini)for(const limit of spec.limits||[]){const v=numeric(limit.value);if(v!==null)body+=`<line class="mc-limit" x1="${pad.l}" x2="${width-pad.r}" y1="${y(v)}" y2="${y(v)}"><title>${escape(limit.label)}: ${escape(format(limit.value,spec.unit))}</title></line>`;}
    const events=new Map();
    for(const trace of visible(entry))for(const e of trace.events||[])if(e.t>=range[0]&&e.t<=range[1])events.set(e.t+'|'+e.label,e);
    if(!mini)for(const e of events.values())body+=`<line class="mc-event" x1="${x(e.t)}" x2="${x(e.t)}" y1="${pad.t}" y2="${height-pad.b}"><title>${escape(e.label)} · ${escape(stamp(e.t))}</title></line><path class="mc-event-marker" d="M ${x(e.t)-4} ${pad.t} l 8 0 l -4 6 z"/>`;
    spec.traces.forEach((trace,i)=>{
      if(entry.hidden.has(i))return;
      for(const segment of segments(trace,range)){
        const ps=reduced(segment,mini?80:600),cls=`mc-series mc-s${i%6}`;
        if(trace.connected&&ps.length>1)body+=`<path class="${cls}" fill="none" d="${ps.map((p,j)=>`${j?'L':'M'}${x(p.t).toFixed(2)},${y(numeric(p.value)).toFixed(2)}`).join(' ')}"/>`;
        if(!trace.connected||ps.length<100)for(const p of ps)body+=`<circle class="mc-point mc-s${i%6}" cx="${x(p.t)}" cy="${y(numeric(p.value))}" r="${mini?2.5:3.2}"/>`;
      }
    });
    body+='</g>';
    if(!data.length)body+=`<text class="mc-empty" x="${width/2}" y="${height/2}" text-anchor="middle">${extent(spec)?'No samples in this view':'No recorded samples'}</text>`;
    body+=`<line class="mc-cursor" x1="0" x2="0" y1="${pad.t}" y2="${height-pad.b}" visibility="hidden"/><rect class="mc-selection" y="${pad.t}" height="${height-pad.t-pad.b}" width="0"/>`;
    return `<svg class="mc-svg" viewBox="0 0 ${width} ${height}" role="img" tabindex="0" aria-label="${escape(spec.title)}. ${escape(spec.unit)}. Arrow keys inspect samples; plus and minus zoom; Home and End select endpoints. Drag horizontally to zoom.">${body}</svg>`;
  }
  function table(entry){
    const rows=allPoints(entry.spec);
    return `<details class="mc-data"><summary>Samples and provenance (${rows.length})</summary><div class="table-wrap"><table><thead><tr><th>UTC</th><th>Raw value</th><th>Unit</th><th>Series</th><th>Source / reference</th></tr></thead><tbody>${rows.slice(0,200).map(p=>`<tr><td class="mono">${escape(stamp(p.t))}</td><td>${escape(p.value===null?'Missing':p.value)}</td><td>${escape(p.unit)}</td><td>${escape(p.trace)}</td><td>${escape(p.source)}<br>${escape(p.ref)}</td></tr>`).join('')}</tbody></table></div>${rows.length>200?'<p class="small-note">First 200 rows shown. CSV contains every sample.</p>':''}</details>`;
  }
  function eventList(entry){
    const events=new Map();for(const t of entry.spec.traces)for(const e of t.events||[])events.set(e.t+'|'+e.label,e);
    return events.size?`<details class="mc-data"><summary>Incident markers (${events.size})</summary><ul>${[...events.values()].sort((a,b)=>a.t-b.t).map(e=>`<li>${escape(stamp(e.t))} · ${escape(e.label)}</li>`).join('')}</ul></details>`:'';
  }
  function card(spec,options={}){
    const id='mc-'+(++sequence),entry={id,spec,mini:!!options.mini,hidden:new Set(),range:null,cursor:0};registry.set(id,entry);
    const latest=allPoints(spec).at(-1);
    const latestText=spec.traces.length>1?spec.traces.length+' series':latest?format(latest.value,spec.unit):'Not measured';
    return `<section class="mc-card ${entry.mini?'mc-mini':''}" data-chart="${id}">${options.heading===false?'':`<header class="mc-header"><div><h3>${escape(spec.title)}</h3><span class="mc-unit">${escape(spec.unit)}${spec.synthetic?' · SYNTHETIC':''}</span></div><div class="mc-value-block"><strong class="mc-value">${escape(latestText)}</strong><small>${spec.traces.length>1?'No cross-series aggregation':latest?'Last recorded sample':'No source evidence'}</small></div></header>`}<div class="mc-plot">${svg(entry)}</div><div class="mc-tooltip" aria-live="polite" hidden></div>${entry.mini?`<button class="mc-expand text-link" data-mc="expand">Inspect graph</button>`:`<div class="mc-controls"><button data-mc="in" title="Zoom in">+</button><button data-mc="out" title="Zoom out">−</button><button data-mc="reset">Reset range</button><button data-mc="csv">Export CSV</button><span>UTC · drag to zoom</span></div><div class="mc-legend">${spec.traces.map((t,i)=>`<button data-mc="toggle" data-trace="${i}" aria-pressed="true"><i class="mc-key mc-s${i%6}"></i>${escape(t.label)}</button>`).join('')}</div><p class="mc-note">${escape(spec.note||'Individual observations; not a continuous telemetry feed.')}</p>${(spec.limits||[]).map(l=>`<p class="mc-limit-note">${escape(l.label)}: ${escape(format(l.value,spec.unit))} ${escape(spec.unit)}. This line is not a pointwise pass/fail decision.</p>`).join('')}${eventList(entry)}${table(entry)}`}</section>`;
  }
  function redraw(root,entry){const focused=document.activeElement===root.querySelector('.mc-svg');root.querySelector('.mc-plot').innerHTML=svg(entry);root.querySelector('.mc-tooltip').hidden=true;if(focused)root.querySelector('.mc-svg').focus();}
  function inspect(root,entry,t){
    const ps=allPoints({...entry.spec,traces:visible(entry)}).filter(p=>p.t>=(entry.range||[-Infinity,Infinity])[0]&&p.t<=(entry.range||[-Infinity,Infinity])[1]);
    if(!ps.length)return;
    let index=0;ps.forEach((p,i)=>{if(Math.abs(p.t-t)<Math.abs(ps[index].t-t))index=i;});entry.cursor=index;
    const p=ps[index],tip=root.querySelector('.mc-tooltip');
    const events=visible(entry).flatMap(s=>s.events||[]).filter(e=>Math.abs(e.t-p.t)<1000).map(e=>e.label);
    tip.textContent=`${stamp(p.t)} · ${format(p.value,entry.spec.unit)} ${entry.spec.unit} · ${p.trace} · ${p.source}${events.length?' · '+events.join(', '):''}`;tip.hidden=false;
    const g=geometry(entry),line=root.querySelector('.mc-cursor');line.setAttribute('x1',g.x(p.t));line.setAttribute('x2',g.x(p.t));line.setAttribute('visibility','visible');
  }
  function zoom(root,entry,factor){const r=entry.range||extent(entry.spec);if(!r)return;const mid=(r[0]+r[1])/2,span=Math.max(1000,(r[1]-r[0])*factor/2);entry.range=[mid-span,mid+span];redraw(root,entry);}
  function csv(spec){
    // Prevent spreadsheet formula interpretation in text cells; retain numeric values.
    const cell=(v,numericCell=false)=>{let s=String(v??'');if(!numericCell&&/^[\s]*[=+@-]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};
    return ['timestamp_utc,value,unit,series,source,evidence_ref',...allPoints(spec).map(p=>[cell(date(p.t)),cell(p.value,true),cell(p.unit),cell(p.trace),cell(p.source),cell(p.ref)].join(','))].join('\r\n');
  }
  function save(name,text,type){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([text],{type}));a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);}
  document.addEventListener('click',event=>{
    const button=event.target.closest('[data-mc]');if(!button)return;event.preventDefault();
    const root=button.closest('[data-chart]'),entry=registry.get(root?.dataset.chart);if(!entry)return;
    const action=button.dataset.mc;
    if(action==='in'||action==='out')zoom(root,entry,action==='in'?.5:2);
    if(action==='reset'){entry.range=null;redraw(root,entry);}
    if(action==='toggle'){const i=Number(button.dataset.trace);entry.hidden.has(i)?entry.hidden.delete(i):entry.hidden.add(i);button.setAttribute('aria-pressed',String(!entry.hidden.has(i)));redraw(root,entry);}
    if(action==='csv')save(entry.spec.metric+'.csv',csv(entry.spec),'text/csv;charset=utf-8');
    if(action==='expand')document.dispatchEvent(new CustomEvent('metric-expand',{detail:entry.spec}));
  });
  function context(event){const element=event.target.closest('.mc-svg'),root=element?.closest('[data-chart]'),entry=registry.get(root?.dataset.chart);return {element,root,entry};}
  function atPointer(event,element,entry){const box=element.getBoundingClientRect(),g=geometry(entry);const x=(event.clientX-box.left)/box.width*g.width;return g.range[0]+Math.min(1,Math.max(0,(x-g.pad.l)/(g.width-g.pad.l-g.pad.r)))*(g.range[1]-g.range[0]);}
  document.addEventListener('pointermove',event=>{const {element,root,entry}=context(event);if(!entry)return;const t=atPointer(event,element,entry);inspect(root,entry,t);if(entry.drag!==undefined){const g=geometry(entry),rect=element.querySelector('.mc-selection');rect.setAttribute('x',Math.min(g.x(entry.drag),g.x(t)));rect.setAttribute('width',Math.abs(g.x(entry.drag)-g.x(t)));}});
  document.addEventListener('pointerdown',event=>{const {element,entry}=context(event);if(!entry||entry.mini||event.button!==0)return;entry.drag=atPointer(event,element,entry);element.setPointerCapture(event.pointerId);});
  document.addEventListener('pointerup',event=>{const {element,root,entry}=context(event);if(!entry||entry.drag===undefined)return;const start=entry.drag,end=atPointer(event,element,entry);delete entry.drag;if(Math.abs(end-start)>500){entry.range=[Math.min(start,end),Math.max(start,end)];redraw(root,entry);}});
  document.addEventListener('pointercancel',event=>{const {root,entry}=context(event);if(entry){delete entry.drag;redraw(root,entry);}});
  document.addEventListener('keydown',event=>{
    const {root,entry}=context(event);if(!entry)return;
    const key=event.key;if(['ArrowLeft','ArrowRight','Home','End','+','=','-','0'].includes(key))event.preventDefault();
    if(key==='+'||key==='=')zoom(root,entry,.5);if(key==='-')zoom(root,entry,2);if(key==='0'){entry.range=null;redraw(root,entry);}
    const points=allPoints({...entry.spec,traces:visible(entry)}).filter(p=>p.t>=(entry.range||[-Infinity,Infinity])[0]&&p.t<=(entry.range||[-Infinity,Infinity])[1]);if(!points.length)return;
    if(key==='ArrowRight')entry.cursor=Math.min(points.length-1,entry.cursor+1);if(key==='ArrowLeft')entry.cursor=Math.max(0,entry.cursor-1);if(key==='Home')entry.cursor=0;if(key==='End')entry.cursor=points.length-1;
    if(['ArrowLeft','ArrowRight','Home','End'].includes(key))inspect(root,entry,points[entry.cursor].t);
  });
  window.MetricCharts={card,csv,extent,format,numeric,escape,source:'('+installMetricCharts.toString()+')();',registry,
    prune(){for(const id of registry.keys())if(!document.querySelector(`[data-chart="${id}"]`))registry.delete(id);}};
})();
