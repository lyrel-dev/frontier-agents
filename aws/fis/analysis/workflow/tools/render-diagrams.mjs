/** Deterministic SVG rendering of the proposal's canonical Mermaid sources. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { parse, render } from 'pele';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const items = [
  ['01_entities', 'Assessment workflow entities', 'All six identity-bearing core concepts, their ownership and scoped relationships.'],
  ['02_owned_values', 'Owned workflow values', 'Step definitions, operation locks, admission snapshots, check results and external references. These are not independent CRUD resources.'],
  ['03_lifecycle', 'Run lifecycle', 'Local orchestration phases. Remote effect disposition and workload assessment remain separate.']
];
const escape = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
const theme = '--pele-bg:#ffffff;--pele-fg:#182b3a;--pele-muted:#526776;--pele-line:#60808b;--pele-surface:#f0f7f7;--pele-surface-alt:#e4f1f0;--pele-border:#9db8bf;--pele-accent:#087f83;--pele-font:Arial,sans-serif;--pele-font-mono:monospace;--pele-radius:5px';
const palette = {'--_bg':'#ffffff','--_fg':'#182b3a','--_m':'#526776','--_l':'#60808b','--_s':'#f0f7f7','--_a':'#e4f1f0','--_b':'#9db8bf','--_c':'#087f83','--_r':'5px','--_hw':'bold','--_fm':'monospace', ...Object.fromEntries(theme.split(';').map(pair => { const at = pair.indexOf(':'); return [pair.slice(0, at), pair.slice(at + 1)]; }))};
const blocks = [...fs.readFileSync(path.join(root, 'model.md'), 'utf8').matchAll(/```mermaid\n([\s\S]*?)\n```/g)].map(match => match[1] + '\n');
if (blocks.length !== items.length) throw new Error('Unexpected embedded diagram membership');
const results = [];
for (let i = 0; i < items.length; i++) {
  const [id, title, description] = items[i];
  const source = fs.readFileSync(path.join(root, `diagrams/${id}.mmd`), 'utf8');
  if (source !== blocks[i]) throw new Error(`Embedded Mermaid differs: ${id}`);
  parse(source);
  const result = render(source, {idPrefix: `assessment-${id}`, fontFamily: 'Arial, sans-serif', fontFamilyMono: 'monospace', fontSize: 15, padding: 28, responsive: false, autoDirection: false, links: false, images: false});
  const titleId = `assessment-${id}-title`;
  let svg = result.svg.replace(/<svg\b([^>]*)>/, (_, attributes) => {
    let attrs = attributes.replace(/\srole="[^"]*"/g, '').replace(/\saria-labelledby="[^"]*"/g, '');
    attrs = /\sstyle="/.test(attrs) ? attrs.replace(/\sstyle="([^"]*)"/, ` style="${theme};$1"`) : attrs + ` style="${theme}"`;
    return `<svg${attrs} role="img" aria-labelledby="${titleId}"><title id="${titleId}">${escape(title)}</title><desc>${escape(description)}</desc>`;
  }) + '\n';
  // Literal SVG presentation values also render in PDF/image tools without CSS custom properties.
  svg = svg.replace(/var\((--[\w-]+)(?:,([^)]*))?\)/g, (_, key, fallback) => {
    const value = palette[key] ?? fallback;
    if (value === undefined) throw new Error(`Unresolved SVG theme variable ${key}`);
    return value;
  });
  fs.writeFileSync(path.join(root, `diagrams/${id}.svg`), svg);
  results.push({id, title, source: `${id}.mmd`, rendered: `${id}.svg`, width: result.width, height: result.height, sourceSha256: sha256(source), svgSha256: sha256(svg)});
}
fs.writeFileSync(path.join(root, 'diagrams/manifest.json'), JSON.stringify({renderer: 'pele', version: '1.6.0', rendererSha256: sha256(fs.readFileSync(fileURLToPath(import.meta.url))), diagrams: results}, null, 2) + '\n');
for (const item of results) console.log(`${item.id}: ${item.width} × ${item.height}`);
