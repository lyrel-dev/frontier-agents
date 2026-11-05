#!/usr/bin/env node
/** Render the editable atlas with the pinned official Draw.io SVG engine.
 * The DOM adapter only supplies browser primitives and plain-text font metrics.
 * Draw.io decodes the mxfile, routes connectors and paints all SVG geometry.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(here);
const args=process.argv.slice(2);
function option(name, fallback){const i=args.indexOf(name);return i<0?fallback:args[i+1];}
const runtime=option('--runtime',process.env.DRAWIO_RUNTIME);
if(!runtime)throw new Error('Set DRAWIO_RUNTIME to the pinned jgraph/drawio checkout; see diagrams/README.md.');
const runtimeWeb=path.join(runtime,'src/main/webapp');
const output=path.resolve(option('--output',path.join(root,'diagrams')));
const source=path.resolve(option('--input',path.join(root,'diagrams/model.drawio')));
const pin=JSON.parse(fs.readFileSync(path.join(here,'drawio-runtime.json'),'utf8'));
const hash=data=>crypto.createHash('sha256').update(data).digest('hex');
for(const [relative,expected] of Object.entries(pin.engineFiles)){
 const p=path.join(runtimeWeb,relative);
 if(!fs.existsSync(p)||hash(fs.readFileSync(p))!==expected)throw new Error('Draw.io runtime differs from pinned source: '+relative);
}
const require=createRequire(import.meta.url);
function dependency(name){
 const paths=[here,...(process.env.CONSOLE_DIAGRAM_NODE_MODULES||'').split(path.delimiter).filter(Boolean)];
 if(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES)paths.push(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES);
 return require(require.resolve(name,{paths}));
}
const {JSDOM,VirtualConsole}=dependency('jsdom');
const {createCanvas}=dependency('@napi-rs/canvas');
const jsdomVersion=dependency('jsdom/package.json').version;
const canvasVersion=dependency('@napi-rs/canvas/package.json').version;
if(jsdomVersion!=='26.1.0'||canvasVersion!=='0.1.100')throw new Error('Use the pinned dependencies in tools/package.json.');
const consoleErrors=[];
const vc=new VirtualConsole();
vc.on('jsdomError',error=>consoleErrors.push(error.message));
const dom=new JSDOM('<!doctype html><html><head></head><body></body></html>',{
 pretendToBeVisual:true,runScripts:'outside-only',url:'http://drawio.local/export3.html',virtualConsole:vc,
});
const w=dom.window;
w.matchMedia=()=>({matches:false,addListener(){},removeListener(){},addEventListener(){},removeEventListener(){}});
w.ResizeObserver=class{observe(){} unobserve(){} disconnect(){}};
const canvasByElement=new WeakMap();
function nativeCanvas(element){
 let canvas=canvasByElement.get(element);
 if(!canvas){canvas=createCanvas(element.width||300,element.height||150);canvasByElement.set(element,canvas);}
 return canvas;
}
w.HTMLCanvasElement.prototype.getContext=function(kind){return nativeCanvas(this).getContext(kind);};
w.HTMLCanvasElement.prototype.toDataURL=function(mime){return nativeCanvas(this).toDataURL(mime||'image/png');};
w.document.fonts={ready:Promise.resolve(),addEventListener(){},check(){return true}};
const metricCanvas=createCanvas(8,8).getContext('2d');
function inherited(element,attribute,fallback){
 for(let n=element;n&&n.getAttribute;n=n.parentNode){const value=n.getAttribute(attribute);if(value!==null&&value!=='')return value;}
 return fallback;
}
function union(boxes){
 if(!boxes.length)return{x:0,y:0,width:0,height:0};
 const x=Math.min(...boxes.map(b=>b.x)),y=Math.min(...boxes.map(b=>b.y));
 return{x,y,width:Math.max(...boxes.map(b=>b.x+b.width))-x,height:Math.max(...boxes.map(b=>b.y+b.height))-y};
}
function transformed(box,transform){
 if(!transform)return box;
 let b={...box};
 for(const m of transform.matchAll(/(translate|scale)\(([^)]+)\)/g)){
  const p=m[2].trim().split(/[ ,]+/).map(Number);
  if(m[1]==='translate'){b.x+=p[0]||0;b.y+=p[1]||0;}
  else{const sx=p[0]||1,sy=p[1]??sx;b={x:b.x*sx,y:b.y*sy,width:b.width*sx,height:b.height*sy};}
 }
 return b;
}
function svgBounds(element){
 const tag=element.localName;
 if(tag==='text'||tag==='tspan'){
  const fontSize=Number.parseFloat(inherited(element,'font-size','13'));
  const family=inherited(element,'font-family','DejaVu Sans');
  const weight=inherited(element,'font-weight','normal');
  const style=inherited(element,'font-style','normal');
  metricCanvas.font=`${style} ${weight} ${fontSize}px ${family}`;
  const text=element.textContent||'';
  const metrics=metricCanvas.measureText(text);
  let x=Number.parseFloat(element.getAttribute('x')||'0');
  const y=Number.parseFloat(element.getAttribute('y')||'0');
  const anchor=inherited(element,'text-anchor','start');
  if(anchor==='middle')x-=metrics.width/2;
  else if(anchor==='end')x-=metrics.width;
  const asc=metrics.actualBoundingBoxAscent||fontSize*.8;
  const desc=metrics.actualBoundingBoxDescent||fontSize*.2;
  return{x,y:y-asc,width:metrics.width,height:asc+desc};
 }
 if(tag==='rect'||tag==='image')return{x:Number(element.getAttribute('x')||0),y:Number(element.getAttribute('y')||0),width:Number(element.getAttribute('width')||0),height:Number(element.getAttribute('height')||0)};
 const boxes=[...element.children].map(child=>transformed(svgBounds(child),child.getAttribute('transform'))).filter(b=>b.width||b.height);
 return union(boxes);
}
w.SVGElement.prototype.getBBox=function(){return svgBounds(this);};
// Fixed positions and explicit line breaks mean no HTML layout or auto-layout shim is needed.
for(const relative of Object.keys(pin.engineFiles))w.eval(fs.readFileSync(path.join(runtimeWeb,relative),'utf8'));
if(w.EditorUi.VERSION!==pin.version)throw new Error('Loaded Draw.io version does not match the pin.');
const xml=fs.readFileSync(source,'utf8');
const xmlDoc=w.mxUtils.parseXml(xml);
if(xmlDoc.querySelector('parsererror'))throw new Error('Draw.io XML is malformed.');
const pages=[...xmlDoc.getElementsByTagName('diagram')];
if(pages.length===0)throw new Error('Draw.io atlas has no pages.');
fs.mkdirSync(output,{recursive:true});
const report={renderer:{name:'Draw.io SVG engine',version:pin.version,sourceRepository:pin.sourceRepository,sourceCommit:pin.sourceCommit,runtime:`JSDOM ${jsdomVersion}; @napi-rs/canvas ${canvasVersion}`,entryPoint:'export.js render + Graph.getSvg',network:'No network used during rendering'},pages:[]};

function insideSegment(a,b,rect){
 const epsilon=2;
 const x1=rect.x+epsilon,y1=rect.y+epsilon,x2=rect.x+rect.width-epsilon,y2=rect.y+rect.height-epsilon;
 if(Math.abs(a.x-b.x)<.01)return a.x>x1&&a.x<x2&&Math.max(a.y,b.y)>y1&&Math.min(a.y,b.y)<y2;
 if(Math.abs(a.y-b.y)<.01)return a.y>y1&&a.y<y2&&Math.max(a.x,b.x)>x1&&Math.min(a.x,b.x)<x2;
 return false;
}
function overlap(a,b){return Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>1&&Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>1;}
function rounded(number){return Math.round(number*1000)/1000;}
function box(state){return Object.fromEntries(['x','y','width','height'].map(k=>[k,rounded(state[k])]));}
if(!overlap({x:0,y:0,width:10,height:10},{x:5,y:5,width:10,height:10})||
 overlap({x:0,y:0,width:10,height:10},{x:12,y:0,width:10,height:10})||
 !insideSegment({x:5,y:-2},{x:5,y:12},{x:0,y:0,width:10,height:10})||
 insideSegment({x:15,y:-2},{x:15,y:12},{x:0,y:0,width:10,height:10}))throw new Error('Geometry negative control failed.');
report.geometryControls={overlappingClassesRejected:true,connectorThroughClassRejected:true,separatedGeometryAccepted:true};

try{
 for(let index=0;index<pages.length;index++){
  const page=pages[index];
  const id=page.getAttribute('id');
  if(!/^[a-z][a-z0-9-]+$/.test(id))throw new Error('Unsafe page id: '+id);
  const graph=w.render({xml,format:'svg',scale:1,border:0,from:index,theme:'light',exportType:'page'});
  const started=Date.now();
  while(!w.document.getElementById('LoadingComplete')){
   if(Date.now()-started>10000)throw new Error('Draw.io did not finish rendering '+id);
   await new Promise(resolve=>setTimeout(resolve,10));
  }
  const svg=graph.getSvg('#F8FAFC',1,0,false,null,true,null,null,null,false,false,'light','page');
  svg.setAttribute('role','img');svg.setAttribute('aria-labelledby',id+'-title '+id+'-description');
  const title=svg.ownerDocument.createElementNS(w.mxConstants.NS_SVG,'title');title.setAttribute('id',id+'-title');title.textContent=page.getAttribute('name');
  const description=svg.ownerDocument.createElementNS(w.mxConstants.NS_SVG,'desc');description.setAttribute('id',id+'-description');description.textContent=page.getAttribute('alt');
  svg.insertBefore(description,svg.firstChild);svg.insertBefore(title,svg.firstChild);
  for(const group of svg.querySelectorAll('[data-cell-id]'))group.setAttribute('id','cell-'+group.getAttribute('data-cell-id'));
  for(const link of svg.querySelectorAll('a')){
   for(const attribute of ['href','xlink:href']){
    const value=link.getAttribute(attribute);
    if(value?.startsWith('data:page/id,'))link.setAttribute(attribute,value.slice('data:page/id,'.length)+'.svg');
   }
  }
  if(svg.querySelector('foreignObject'))throw new Error('Use plain SVG text, not HTML labels: '+id);
  const body=w.mxUtils.getXml(svg)+'\n';
  fs.writeFileSync(path.join(output,id+'.svg'),body);
  const nodes=[],edges=[];
  for(const cell of Object.values(graph.getModel().cells)){
   const state=graph.view.getState(cell);
   if(!state)continue;
   if(cell.vertex&&cell.value?.getAttribute?.('entity'))nodes.push({id:cell.id,entity:cell.value.getAttribute('entity'),boundary:cell.value.getAttribute('boundary')==='1',...box(state)});
   if(cell.edge&&cell.value?.getAttribute?.('relationshipIndex')!==null&&cell.value?.getAttribute){
    edges.push({id:cell.id,relationshipIndex:Number(cell.value.getAttribute('relationshipIndex')),from:cell.source.id,to:cell.target.id,points:state.absolutePoints.filter(Boolean).map(p=>({x:rounded(p.x),y:rounded(p.y)})),label:state.text?.boundingBox?box(state.text.boundingBox):null});
   }
  }
  const overlaps=[];for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++)if(overlap(nodes[i],nodes[j]))overlaps.push([nodes[i].entity,nodes[j].entity]);
  const intrusions=[];
  for(const edge of edges)for(const n of nodes){if(n.id===edge.from||n.id===edge.to)continue;for(let i=1;i<edge.points.length;i++)if(insideSegment(edge.points[i-1],edge.points[i],n)){intrusions.push({edge:edge.relationshipIndex,entity:n.entity});break;}}
  const labelIntrusions=[];
  for(const edge of edges)if(edge.label)for(const n of nodes)if(overlap(edge.label,n))labelIntrusions.push({edge:edge.relationshipIndex,entity:n.entity});
  const textOverflows=[];
  for(const n of nodes){
   for(const id of [n.id,n.id+'-fields']){
    const state=graph.view.getState(graph.getModel().getCell(id));
    const b=state?.text?.boundingBox;
    if(b&&(b.x<n.x+4||b.y<n.y+3||b.x+b.width>n.x+n.width-4||b.y+b.height>n.y+n.height-3))textOverflows.push({entity:n.entity,cell:id,bounds:box(b)});
   }
  }
  const encoded=new w.mxCodec().encode(graph.getModel());
  const decoded=new w.mxGraphModel();
  new w.mxCodec(encoded.ownerDocument).decode(encoded,decoded);
  const decodedEntities=Object.values(decoded.cells).filter(c=>c.value?.getAttribute?.('entity')).map(c=>c.value.getAttribute('entity')).sort();
  const decodedRelationships=Object.values(decoded.cells).filter(c=>c.edge&&c.value?.getAttribute?.('relationshipIndex')!=null).map(c=>Number(c.value.getAttribute('relationshipIndex'))).sort((a,b)=>a-b);
  if(JSON.stringify(decodedEntities)!==JSON.stringify(nodes.map(n=>n.entity).sort())||JSON.stringify(decodedRelationships)!==JSON.stringify(edges.map(e=>e.relationshipIndex).sort((a,b)=>a-b)))throw new Error('Native Draw.io codec round trip lost model metadata: '+id);
  const model=page.getElementsByTagName('mxGraphModel')[0];
  report.pages.push({id,title:page.getAttribute('name'),kind:page.getAttribute('kind'),pageSize:{width:Number(model.getAttribute('pageWidth')),height:Number(model.getAttribute('pageHeight'))},nodes,edges,classOverlaps:overlaps,connectorIntrusions:intrusions,labelIntrusions,textOverflows,nativeCodecRoundTrip:{entities:decodedEntities.length,relationships:decodedRelationships.length,metadataPreserved:true},svgSha256:hash(body),svgBytes:Buffer.byteLength(body)});
  console.log(`${id}: ${nodes.length} classes; ${edges.length} associations; ${overlaps.length} class overlaps; ${intrusions.length} connector intrusions; ${labelIntrusions.length} label intrusions; ${textOverflows.length} text overflows`);
  graph.destroy();
 }
 if(consoleErrors.length)throw new Error('Draw.io DOM errors: '+consoleErrors.join('; '));
 fs.writeFileSync(path.join(output,'render-report.json'),JSON.stringify(report,null,2)+'\n');
 if(report.pages.some(p=>p.classOverlaps.length||p.connectorIntrusions.length||p.labelIntrusions.length||p.textOverflows.length))process.exitCode=2;
} finally {
 // Let Draw.io's already-resolved font promises drain before disposing the DOM.
 await new Promise(resolve=>setImmediate(resolve));
 dom.window.close();
}
