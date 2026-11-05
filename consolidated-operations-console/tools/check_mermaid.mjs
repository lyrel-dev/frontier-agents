/** Parse every generated class diagram in the pinned Mermaid runtime.
 * This checks syntax, not a particular Obsidian installation or SVG layout.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const toolsDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(toolsDir, '..');
const runtimeDir = process.env.CONSOLE_DIAGRAM_RUNTIME || toolsDir;
const require = createRequire(path.join(runtimeDir, 'package.json'));
const { JSDOM } = await import(pathToFileURL(require.resolve('jsdom')).href);
const dom = new JSDOM('');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import(pathToFileURL(require.resolve('mermaid')).href);
mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'diagrams/manifest.json')));
const result = [];
for (const diagram of manifest.diagrams) {
  const source = fs.readFileSync(path.join(root, diagram.mmd.path), 'utf8');
  const parsed = await mermaid.parse(source);
  if (!parsed || parsed.diagramType !== 'class') throw new Error(`Invalid class diagram ${diagram.mmd.path}`);
  result.push({ source: diagram.mmd.path, sha256: crypto.createHash('sha256').update(source).digest('hex'), syntax: 'passed' });
}
const negative = await mermaid.parse('classDiagram\nclass Example {\n', { suppressErrors: true });
if (negative) throw new Error('Malformed class diagram negative control unexpectedly parsed');
const packageVersion = name => JSON.parse(fs.readFileSync(path.join(runtimeDir, 'node_modules', name, 'package.json'))).version;
const evidence = {
  scope: 'Syntax parsing of editable Mermaid sources. SVG layout is independently rendered from the schema with Graphviz.',
  mermaidVersion: packageVersion('mermaid'), jsdomVersion: packageVersion('jsdom'),
  negativeControl: 'Malformed unclosed class rejected', diagrams: result,
};
const output = path.join(root, 'diagrams/mermaid-syntax.json');
const body = JSON.stringify(evidence, null, 2) + '\n';
if (process.argv.includes('--write')) fs.writeFileSync(output, body);
else if (!fs.existsSync(output) || fs.readFileSync(output, 'utf8') !== body) throw new Error('Mermaid syntax evidence is stale; run --write after reviewing changes.');
console.log(`PASS: ${result.length} class diagrams parsed with Mermaid ${evidence.mermaidVersion}; negative control rejected.`);
dom.window.close();
