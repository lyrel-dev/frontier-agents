#!/usr/bin/env python3
"""One-time clean replacement. Earlier material remains in Git history only."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'reference/devops.json'
d = json.loads(p.read_text())
for f in d['functions']:
    if f['id'] == 'D06':
        f.update(name='Steer, resume and fork an investigation',
                 input='A running or completed investigation, an additional fact or correction, or a selected timeline message from which to fork.',
                 operation='Messages can redirect an investigation. A completed investigation can resume with its prior context; a fork explores another line without changing the original. These controls change the analysis lifecycle, not the underlying production resources.',
                 output='An updated or branched investigation record with its own sequence of evidence and conclusions.',
                 entry='Use Chat with investigation to supply facts or resume completed work. Use Fork on the relevant timeline message to test an alternative line of analysis.',
                 limits='Resuming can incur additional analysis. Forking inherits prior context, which may include a wrong premise. A new branch of reasoning is not independent verification of its inputs.',
                 check='Fork a prepared investigation to test a competing hypothesis. Compare the observations each branch actually collected and identify premises inherited without a fresh check.',
                 refs=['incident','history'])
d['functions'].append({
 'id':'D14','group':'incident','name':'Assess the quality of a completed investigation','status':'Documented',
 'input':'A completed investigation record, with any reference root cause on its linked incident or ticket.',
 'operation':'Review reads the reported problem, collected evidence and conclusion. It produces a separate helpful/not-helpful verdict and criterion-level assessments of scope alignment, evidence grounding, completeness, environment impact and accuracy. It does not rerun the investigation or alter its record.',
 'output':'A Review result with pass, fail or not applicable per criterion and supporting reasoning. Accuracy is not applicable when no reference diagnosis is available.',
 'entry':'Incident Response → completed investigation → Review; inspect the separate Review tab. The Grader agent instructions can tailor the criteria for future reviews.',
 'limits':'Review assesses the record it is given. A passing grade cannot establish facts absent from that record or substitute for an independent telemetry check.',
 'check':'Inspect whether a real reference root cause exists before interpreting Accuracy. Compare one evidence-grounding judgment with the cited source observation rather than accepting only the overall verdict.',
 'refs':['review','instructions','history']})
d['functions'].append({
 'id':'D15','group':'context','name':'Execute analysis code in an investigation sandbox','status':'Preview','activation':'Explicit Agent Space opt-in',
 'input':'An investigation requiring computation, a configured Sandbox, allowed destinations and preinstalled packages.',
 'operation':'The agent can run shell commands, write files and execute code in an ephemeral Linux environment scoped to one investigation. It can parse evidence or compute results and read them back into the analysis. AWS CLI/SDK access uses the documented read-only proxy; allowed HTTP destinations remain a separate effect boundary.',
 'output':'Computed results and investigation evidence from that environment, not a persistent deployment or a shared execution host.',
 'entry':'Agent Space → Capabilities → Sandbox → Configure. Set narrowly scoped hosts, methods and paths and the required pip/npm packages before saving.',
 'limits':'Preview, limited regions, and investigation use only in the cited guidance. It is not enabled by default and is not documented as a general execution feature for Chat or custom agents. Removing configuration stops provisioning for new investigations.',
 'check':'Use a known small dataset and independently recompute the result. Test a disallowed destination and inspect the configured egress rules; an AWS read-only proxy does not make arbitrary external application endpoints harmless.',
 'refs':['sandbox','history','regions']})
d['sources']['sandbox'] = {'title':'Set up a Sandbox: execution, egress and package configuration','url':'https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html'}
d['procedures'][0]['functions'].append('D14')
save(p,d)
p = ROOT / 'reference/security.json'
d = json.loads(p.read_text())
d['functions'].append({
 'id':'S10','group':'design','name':'Generate structured requirements from policy documents','status':'Documented',
 'input':'Security policies or standards in supported DOC, DOCX, Markdown, PDF or text files, submitted to a custom requirement pack.',
 'operation':'The service extracts security-relevant content and generates workload-level requirements with applicability, compliance criteria and remediation guidance. The operator reviews, edits or deletes the generated criteria before enabling the pack for new assessments.',
 'output':'A custom pack of reviewable requirements. Generation does not show that an application meets the source policy.',
 'entry':'Security requirements → Custom security requirements packs → create or select a pack → Choose files → Generate requirements. Review and enable only after checking the generated criteria.',
 'limits':'A new upload replaces all requirements in that pack, including hand-written entries. Concurrent uploads to the same pack are not allowed while generation is in progress.',
 'check':'Map generated criteria back to selected source-policy clauses. Check applicability and observable compliance conditions; reject ambiguous or unsupported interpretations before enabling the pack.',
 'refs':['import-requirements','requirements']})
save(p,d)
for key in ('devops','security','finops'):
    p=ROOT/'reference'/f'{key}.json'
    d=json.loads(p.read_text())
    for f in d['functions']:
        original=f.pop('status')
        f['availability']='Documented' if original in ('Opt-in','Integration') else original
        f.setdefault('activation', 'Explicit opt-in' if original=='Opt-in' else 'Configured integration' if original=='Integration' else 'See invocation and prerequisites')
    d['functions']=sorted(d['functions'],key=lambda f:([g['id'] for g in d['groups']].index(f['group']),int(f['id'][1:])))
    save(p,d)

keep={
 '.github/workflows/document-suite.yml','.gitignore','documentation-build.json',
 'reference/devops.json','reference/security.json','reference/finops.json','reference/teaching.json',
 'tools/build_reference.py','tools/check_reference.py','tools/prepare_rebuild.py'}
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
for name in tracked:
    if name and name not in keep:
        path=ROOT/name
        if path.is_file() or path.is_symlink(): path.unlink()
(ROOT/'.gitignore').write_text('__pycache__/\n*.pyc\nqa/screens/\nqa/rendered/\n',encoding='utf-8')
# This transition is not part of the ongoing build. No archive is created.
Path(__file__).unlink()
print('Prepared canonical references and removed superseded tracked documents; history unchanged.')
