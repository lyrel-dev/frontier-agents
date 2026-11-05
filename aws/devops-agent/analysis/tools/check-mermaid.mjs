/** Syntax validation in the pinned Mermaid runtime; not an Obsidian UI test. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { JSDOM } from 'jsdom';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const write = process.argv.includes('--write');
const evidencePath = path.join(root, 'qa/mermaid-syntax.json');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'diagrams/manifest.json'), 'utf8'));
const dom = new JSDOM('');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });
const packageJson = name => JSON.parse(fs.readFileSync(path.join(root, 'tools/node_modules', name, 'package.json'), 'utf8'));
const results = [];
for (const diagram of manifest.diagrams) {
  const source = fs.readFileSync(path.join(root, diagram.filename), 'utf8');
  const parsed = await mermaid.parse(source);
  if (!parsed) throw new Error(`Mermaid rejected ${diagram.id}`);
  results.push({
    id: diagram.id,
    source: diagram.filename,
    sha256: crypto.createHash('sha256').update(source).digest('hex'),
    diagramType: parsed.diagramType,
    syntax: 'passed'
  });
}
const malformedAccepted = await mermaid.parse('erDiagram\n    A ||--||', { suppressErrors: true });
if (malformedAccepted) throw new Error('Negative control failed: malformed ER relationship was accepted');
const evidence = {
  schemaVersion: 1,
  mermaidVersion: packageJson('mermaid').version,
  jsdomVersion: packageJson('jsdom').version,
  scope: 'Mermaid syntax parsing with strict sanitization; no browser layout or installed Obsidian test',
  negativeControl: { case: 'incomplete ER relationship', result: 'rejected' },
  diagrams: results
};
const serialized = JSON.stringify(evidence, null, 2) + '\n';
if (write) fs.writeFileSync(evidencePath, serialized);
else if (!fs.existsSync(evidencePath) || fs.readFileSync(evidencePath, 'utf8') !== serialized) {
  throw new Error('Mermaid evidence is stale; review changes and run node tools/check-mermaid.mjs --write');
}
console.log(`PASS: ${results.length} sources parsed by Mermaid ${evidence.mermaidVersion}; negative control rejected.`);
dom.window.close();
