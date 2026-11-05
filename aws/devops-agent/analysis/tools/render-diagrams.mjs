/** Render the reviewed Mermaid sources without a browser or network at runtime. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { parse, render } from 'pele';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'diagrams/manifest.json'), 'utf8'));
const esc = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const theme = '--pele-bg:#ffffff;--pele-fg:#172b3a;--pele-muted:#516675;--pele-line:#607a8b;--pele-surface:#eff6f7;--pele-surface-alt:#e1f0f0;--pele-border:#9fb7bd;--pele-accent:#087f83;--pele-font:Arial,sans-serif;--pele-font-mono:monospace;--pele-radius:5px';
const results = [];
for (const diagram of manifest.diagrams) {
  const source = fs.readFileSync(path.join(root, diagram.filename), 'utf8');
  parse(source);
  const result = render(source, {
    idPrefix: `devops-${diagram.id.toLowerCase()}`,
    fontFamily: 'Arial, sans-serif',
    fontFamilyMono: 'monospace',
    fontSize: 15,
    responsive: false,
    autoDirection: false,
    padding: 26,
    links: false,
    images: false
  });
  const titleId = `devops-${diagram.id.toLowerCase()}-title`;
  let svg = result.svg.replace(/<svg\b([^>]*)>/, (_, attributes) => {
    let attrs = attributes.replace(/\srole="[^"]*"/g, '').replace(/\saria-labelledby="[^"]*"/g, '');
    attrs = /\sstyle="/.test(attrs)
      ? attrs.replace(/\sstyle="([^"]*)"/, ` style="${theme};$1"`)
      : attrs + ` style="${theme}"`;
    return `<svg${attrs} role="img" aria-labelledby="${titleId}">`;
  });
  svg = svg.replace(/(<svg[^>]*>)/, `$1<title id="${titleId}">${esc(diagram.id + ' — ' + diagram.title)}</title><desc>${esc('Reviewed AWS DevOps Agent logical model. Editable source: ' + diagram.filename + '. Native and application-derived entities are explained in report.md.')}</desc>`);
  fs.writeFileSync(path.join(root, diagram.rendered), svg + '\n');
  results.push({
    id: diagram.id, source: diagram.filename, rendered: diagram.rendered,
    type: result.type, width: result.width, height: result.height,
    sourceSha256: crypto.createHash('sha256').update(source).digest('hex'),
    svgSha256: crypto.createHash('sha256').update(svg + '\n').digest('hex')
  });
}
fs.mkdirSync(path.join(root, 'qa'), { recursive: true });
fs.writeFileSync(path.join(root, 'qa/diagram-render.json'), JSON.stringify({
  renderer: 'pele', version: '1.6.0', diagrams: results
}, null, 2) + '\n');
console.log(`Parsed and rendered ${results.length} diagrams with Pele 1.6.0.`);
for (const item of results) console.log(`${item.id}: ${item.width} × ${item.height}`);
