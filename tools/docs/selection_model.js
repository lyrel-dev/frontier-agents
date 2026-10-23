/* Semantic selections and source snapshots; independent of the AWS entity model. */
(() => {
  'use strict';
  const SCHEMA = 'frontier-selection/v1';
  const fields = ['id','anchor','kind','label','target_ids','context_ids','membership_sha256'];
  const copy = value => JSON.parse(JSON.stringify(value));
  const unique = values => [...new Set(values)];
  function create(source) {
    const nodes = source.selections || {};
    const key = element => element?.dataset?.reviewScope;
    const element = id => nodes[id] ? document.getElementById(nodes[id].anchor) : null;
    function ancestors(id) {
      const result=[]; const seen=new Set();
      while (id && nodes[id] && !seen.has(id)) {result.push(id);seen.add(id);id=nodes[id].parent;}
      return result;
    }
    function normalize(ids) {
      const existing=unique(ids).filter(id=>nodes[id]);
      return existing.filter(id=>!ancestors(id).slice(1).some(p=>existing.includes(p)))
        .sort((a,b)=>nodes[a].order-nodes[b].order);
    }
    const targets = roots => unique(normalize(roots).flatMap(id=>nodes[id].target_ids));
    function snapshot(roots) {
      const ids=normalize(roots);
      return {schema:SCHEMA,content_revision:source.content_revision,
        roots:ids.map(id=>Object.fromEntries(fields.map(field=>[field,copy(nodes[id][field])]))),
        target_ids:targets(ids), context_ids:unique(ids.flatMap(id=>nodes[id].context_ids))};
    }
    function validate(note) {
      if (!note.selection) {
        if(note.scope==='structure')throw new Error('Structural selection snapshot is missing');
        return;
      }
      const s=note.selection;
      if(s.schema!==SCHEMA||typeof s.content_revision!=='string'||!Array.isArray(s.roots)||!s.roots.length||s.roots.length>10000||!Array.isArray(s.target_ids)||!Array.isArray(s.context_ids))throw new Error('Invalid structural selection');
      const ids=new Set(), members=[], contexts=[];
      for(const root of s.roots){
        if(!root||typeof root.id!=='string'||ids.has(root.id)||typeof root.anchor!=='string'||typeof root.kind!=='string'||typeof root.label!=='string'||!Array.isArray(root.target_ids)||!Array.isArray(root.context_ids)||!/^[a-f0-9]{64}$/.test(root.membership_sha256)||Object.keys(root).sort().join('|')!==[...fields].sort().join('|'))throw new Error('Invalid structural root');
        if([...root.target_ids,...root.context_ids].some(id=>typeof id!=='string'))throw new Error('Invalid structural member');
        ids.add(root.id);members.push(...root.target_ids);contexts.push(...root.context_ids);
      }
      if(JSON.stringify(unique(members))!==JSON.stringify(s.target_ids)||JSON.stringify(unique(contexts))!==JSON.stringify(s.context_ids)||JSON.stringify(note.targets.map(t=>t.block_id))!==JSON.stringify(s.target_ids))throw new Error('Structural source membership does not match its snapshot');
    }
    function stale(note) {
      if(!note.selection)return false;
      if(note.selection.content_revision!==source.content_revision)return true;
      if(note.document!==source.document)return false;
      return note.selection.roots.some(root=>!nodes[root.id]||root.membership_sha256!==nodes[root.id].membership_sha256);
    }
    function locate(note) {
      if(note.selection){
        if(note.document!==source.document)return null;
        return note.selection.roots.map(root=>element(root.id)).find(Boolean)||null;
      }
      return [...document.querySelectorAll('[data-review-block]')].find(el=>note.targets.some(t=>t.block_id===el.dataset.reviewBlock&&t.path===source.targets[t.block_id]?.path))||null;
    }
    function associated(note, id) {
      if(note.selection)return note.document===source.document&&note.selection.roots.some(root=>root.id===id);
      const bid=element(id)?.dataset.reviewBlock;
      return note.scope!=='document'&&!!bid&&note.targets.some(t=>t.block_id===bid&&t.path===source.targets[bid]?.path);
    }
    function range(from,to,visible) {
      if(!nodes[from]||!nodes[to])return [to];
      const a=nodes[from],b=nodes[to];
      let ordered;
      if(a.kind===b.kind&&a.parent===b.parent&&['section','subsection','chapter','slide','group'].includes(a.kind)){
        ordered=Object.keys(nodes).filter(id=>nodes[id].parent===a.parent&&nodes[id].kind===a.kind).sort((x,y)=>nodes[x].order-nodes[y].order);
      }else{
        ordered=visible.filter(id=>nodes[id]&&element(id)?.hasAttribute('data-review-block'));
      }
      const i=ordered.indexOf(from),j=ordered.indexOf(to);
      return i<0||j<0?[to]:ordered.slice(Math.min(i,j),Math.max(i,j)+1);
    }
    return {nodes,key,element,ancestors,normalize,targets,snapshot,validate,stale,locate,associated,range};
  }
  window.FrontierSelection={create,schema:SCHEMA};
})();
