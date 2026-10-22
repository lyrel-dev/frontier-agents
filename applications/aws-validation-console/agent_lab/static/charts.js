/* Small dependency-free charts. All points originate in collected records.
   Gaps stay gaps; isolated scalar measurements are not interpolated into a trend. */
'use strict';
window.LabCharts = (() => {
  const NS='http://www.w3.org/2000/svg';
  const colors=['#127a78','#a24b35','#6d63a4','#4976a0'];
  const escapeCSV=v=>{let s=String(v??'');if(typeof v!=='number'&&/^[=+\-@\t\r]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};
  function download(name,text,type='text/csv'){
    const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
  }
  function node(tag,attrs={}){const n=document.createElementNS(NS,tag);for(const [k,v]of Object.entries(attrs))n.setAttribute(k,String(v));return n;}
  function format(value){if(value===null||value===undefined)return 'No sample';return typeof value==='number'?Number(value.toFixed(4)).toLocaleString():String(value);}
  function draw(host,spec){
    host.replaceChildren();host.classList.add('chart');
    const header=document.createElement('div');header.className='chart-header';
    const h=document.createElement('strong');h.textContent=spec.title;header.append(h);
    const u=document.createElement('span');u.className='muted';u.textContent=spec.unit||'';header.append(u);host.append(header);
    const traces=(spec.series||[]).map((s,i)=>({...s,color:s.color||colors[i%colors.length],points:(s.points||[]).map(p=>({...p,x:typeof p.t==='number'?p.t:Date.parse(p.t)})).filter(p=>Number.isFinite(p.x))}));
    let low=Infinity,high=-Infinity;
    for(const s of traces)for(const p of s.points){low=Math.min(low,p.x);high=Math.max(high,p.x);}
    if(low===Infinity){const p=document.createElement('div');p.className='chart-empty';p.textContent='No measured samples';host.append(p);return;}
    if(low===high){low-=30000;high+=30000;}
    const extent=[low,high];let range=[...extent],hidden=new Set(),index=0;
    const controls=document.createElement('div');controls.className='chart-controls';
    const plot=document.createElement('div');plot.className='chart-plot';
    const svg=node('svg',{viewBox:'0 0 720 220',tabindex:'0',role:'img','aria-label':spec.title+'. Arrow keys inspect samples; plus/minus zoom.'});
    const tooltip=document.createElement('div');tooltip.className='chart-readout';tooltip.setAttribute('aria-live','polite');
    const table=document.createElement('details');const summary=document.createElement('summary');summary.textContent='Source samples';table.append(summary);
    const tablebox=document.createElement('div');tablebox.className='sample-table';table.append(tablebox);
    const legend=document.createElement('div');legend.className='chart-legend';
    let dragStart=null;
    function all(){return traces.filter((_,i)=>!hidden.has(i)).flatMap(s=>s.points.map(p=>({...p,series:s.name}))).filter(p=>p.x>=range[0]&&p.x<=range[1]).sort((a,b)=>a.x-b.x);}
    function stamp(x){return spec.relative?((x/1000).toFixed(0)+' s'):new Date(x).toISOString().slice(11,19)+' UTC';}
    function inspect(i){const pts=all();if(!pts.length){tooltip.textContent='No samples in selected range';return;}index=Math.max(0,Math.min(i,pts.length-1));const p=pts[index];tooltip.textContent=stamp(p.x)+' · '+p.series+' · '+format(p.value)+' '+(spec.unit||'')+(p.source?' · '+p.source:'');}
    function zoom(factor){const middle=(range[0]+range[1])/2,half=(range[1]-range[0])*factor/2;range=[Math.max(extent[0],middle-half),Math.min(extent[1],middle+half)];render();}
    function button(label,fn){const b=document.createElement('button');b.type='button';b.textContent=label;b.addEventListener('click',fn);controls.append(b);return b;}
    button('Zoom +',()=>zoom(.5));button('Zoom −',()=>zoom(2));button('Reset',()=>{range=[...extent];render();});
    button('CSV',()=>{const rows=[['series','timestamp_utc','value','unit','source']];for(const s of traces)for(const p of s.points)rows.push([s.name,spec.relative?String(p.x/1000):new Date(p.x).toISOString(),p.value,spec.unit,p.source||'']);download((spec.title||'metric').replace(/[^a-z0-9]+/gi,'-')+'.csv',rows.map(r=>r.map(escapeCSV).join(',')).join('\n'));});
    traces.forEach((s,i)=>{const b=document.createElement('button');b.type='button';b.textContent=s.name;b.style.borderColor=s.color;b.setAttribute('aria-pressed','true');b.onclick=()=>{hidden.has(i)?hidden.delete(i):hidden.add(i);b.setAttribute('aria-pressed',String(!hidden.has(i)));render();};legend.append(b);});
    function render(){
      svg.replaceChildren();const pts=all();let ymin=Infinity,ymax=-Infinity;
      for(const p of pts)if(p.value!==null&&Number.isFinite(Number(p.value))){ymin=Math.min(ymin,Number(p.value));ymax=Math.max(ymax,Number(p.value));}
      if(ymin===Infinity){ymin=0;ymax=1;}if(ymin===ymax){const pad=Math.abs(ymin)*.1||1;ymin-=pad;ymax+=pad;}
      const x=v=>52+(v-range[0])/(range[1]-range[0]||1)*650,y=v=>180-(v-ymin)/(ymax-ymin)*155;
      for(let i=0;i<4;i++){const value=ymin+(ymax-ymin)*i/3;svg.append(node('line',{x1:52,x2:702,y1:y(value),y2:y(value),stroke:'#e2e8ea'}));const t=node('text',{x:45,y:y(value)+4,'text-anchor':'end','font-size':10,fill:'#647682'});t.textContent=format(value);svg.append(t);}
      for(const [i,s]of traces.entries()){
        if(hidden.has(i))continue;
        let segment=[],previous=null;const segments=[];
        for(const p of s.points.filter(p=>p.x>=range[0]&&p.x<=range[1])){
          if(p.value===null||(previous&&s.interval_ms&&p.x-previous.x>s.interval_ms*1.5)){if(segment.length)segments.push(segment);segment=[];}
          if(p.value!==null){segment.push(p);previous=p;}
        }if(segment.length)segments.push(segment);
        for(const values of segments){
          // Bound rendered vertices; preserve complete source values in CSV.
          let shown=values;
          if(values.length>1200){shown=[];const width=Math.ceil(values.length/300);for(let k=0;k<values.length;k+=width){const group=values.slice(k,k+width);const extremes=[group[0],group.reduce((a,b)=>a.value<b.value?a:b),group.reduce((a,b)=>a.value>b.value?a:b),group.at(-1)].sort((a,b)=>a.x-b.x);shown.push(...extremes);}}
          if(!s.isolated&&shown.length>1)svg.append(node('polyline',{points:shown.map(p=>x(p.x)+','+y(Number(p.value))).join(' '),fill:'none',stroke:s.color,'stroke-width':2}));
          if(shown.length<25||s.isolated)for(const p of shown)svg.append(node('circle',{cx:x(p.x),cy:y(Number(p.value)),r:3.5,fill:s.color}));
        }
      }
      for(const event of spec.events||[]){const t=typeof event.t==='number'?event.t:Date.parse(event.t);if(t<range[0]||t>range[1])continue;const l=node('line',{x1:x(t),x2:x(t),y1:22,y2:182,stroke:'#b68547','stroke-dasharray':'3,4'});const title=node('title');title.textContent=event.label;l.append(title);svg.append(l);}
      for(const [v,anchor,pos]of [[range[0],'start',52],[range[1],'end',702]]){const t=node('text',{x:pos,y:205,'text-anchor':anchor,'font-size':10,fill:'#647682'});t.textContent=stamp(v);svg.append(t);}
      inspect(index);
    }
    svg.addEventListener('keydown',e=>{if(['ArrowRight','ArrowLeft','Home','End','+','-','='].includes(e.key)){e.preventDefault();if(e.key==='ArrowRight')inspect(index+1);if(e.key==='ArrowLeft')inspect(index-1);if(e.key==='Home')inspect(0);if(e.key==='End')inspect(all().length-1);if(['+','='].includes(e.key))zoom(.5);if(e.key==='-')zoom(2);}});
    const atPointer=e=>{const r=svg.getBoundingClientRect();return range[0]+Math.max(0,Math.min(1,((e.clientX-r.left)/r.width*720-52)/650))*(range[1]-range[0]);};
    svg.addEventListener('pointermove',e=>{const time=atPointer(e);const pts=all();let nearest=0,diff=Infinity;for(let i=0;i<pts.length;i++){const d=Math.abs(pts[i].x-time);if(d<diff){diff=d;nearest=i;}}inspect(nearest);});
    svg.addEventListener('pointerdown',e=>{dragStart=atPointer(e);svg.setPointerCapture(e.pointerId);});
    svg.addEventListener('pointerup',e=>{const stop=atPointer(e);if(dragStart!==null&&Math.abs(stop-dragStart)>(range[1]-range[0])*.02){range=[Math.min(stop,dragStart),Math.max(stop,dragStart)];render();}dragStart=null;});
    table.addEventListener('toggle',()=>{if(!table.open)return;tablebox.replaceChildren();const p=document.createElement('p');p.textContent='First 200 source rows. CSV contains all samples, including explicit gaps.';tablebox.append(p);const t=document.createElement('table');const head=document.createElement('tr');for(const s of ['Time','Series','Value']){const th=document.createElement('th');th.textContent=s;head.append(th);}t.append(head);for(const row of traces.flatMap(s=>s.points.map(p=>({...p,series:s.name}))).slice(0,200)){const tr=document.createElement('tr');for(const value of [stamp(row.x),row.series,format(row.value)]){const td=document.createElement('td');td.textContent=value;tr.append(td);}t.append(tr);}tablebox.append(t);});
    plot.append(svg);host.append(controls,plot,tooltip,legend,table);render();
  }
  return {draw,download};
})();
