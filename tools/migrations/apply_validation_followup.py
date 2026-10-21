"""Idempotent follow-up: corrective feedback, default state, and portable download link."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
REVISION = '2026-10-21-mechanisms-v2'


def apply() -> None:
    path = ROOT / 'content/mechanisms.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    data['revision'] = REVISION
    data['sources']['DF'] = {
        'title': 'Provide feedback on investigations',
        'url': 'https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html#provide-feedback-on-investigations',
        'reviewed': '2026-10-21',
        'note': 'Corrective verdict plus actual root cause creates a reflections memory. Sharing feedback with AWS is a separate, explicit confirmation.'
    }
    data['sources']['DN'] = {
        'title': 'DevOps Agent dated product changes',
        'url': 'https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html',
        'reviewed': '2026-10-21',
        'note': 'Dated entries document monitor memory enabled by default (19 June), learned knowledge moved to memory (27 August), and reflections (4 September 2026).'
    }
    a = data['agents']['devops']
    a['learning'] = 'Historical investigations produce managed context; corrective feedback can produce reflections. Later investigations selectively retrieve relevant memories. Maintained instructions, reusable skills and tool permissions are separate controls.'
    a['learning_refs'] = list(dict.fromkeys(a['learning_refs'] + ['DF', 'DN']))
    first = a['records'][0]
    first['activation'] = 'Monitor memory enabled by default; verify store and entry state'
    first['refs'] = list(dict.fromkeys(first['refs'] + ['DN']))
    record = {
        'id': 'D-M10', 'title': 'Record a corrected cause through investigation feedback',
        'family': 'Memory', 'surface': 'Completed investigation / Knowledge → Memories',
        'availability': 'Documented corrective-feedback memory',
        'activation': 'Submit an incorrect verdict and the actual root cause',
        'mechanism': 'Corrective feedback can create a memory in the reflections store for later investigations of the alarm. This is distinct from recurring-cause summaries and does not establish model-weight training.',
        'prerequisites': 'A completed investigation and an independently established cause.',
        'steps': [
            'Open the completed investigation and choose Add feedback, or provide the correction in Chat.',
            'Select an incorrect verdict and supply the actual root cause. Sharing with AWS requires separate confirmation.',
            'Inspect Knowledge → Memories → reflections and retain the relevant entry and version.'
        ],
        'scope': 'Reflection context relates to the alarm. Latest submitted feedback replaces previous feedback for that investigation.',
        'control': 'Update incorrect feedback. Inspect, correct or deactivate affected memories separately; do not assume feedback replacement removes every historical memory version.',
        'limits': 'A reflection is retained context, not proof of a future diagnosis or broader execution authority.',
        'refs': ['DF', 'DM', 'DN'],
        'checks': [
            'Proposed: use a reviewed, non-production incident whose established cause differs from the original result.',
            'Record feedback and any resulting reflection; check a separate investigation against new evidence.',
            'Report recall as unverified unless the run exposes evidence that the memory was read.'
        ],
        'artifact': 'Investigation ID, reviewed cause, feedback, memory version, subsequent read evidence and reviewer decision.',
        'fallback': 'Keep the reviewed correction as explicit context when reflection creation or recall cannot be observed.',
        'example': 'Illustrative: "The cause was incorrect. The reviewed cause is the staging connection-pool limit; retain the supporting evidence and do not change resources."',
        'slide': ['Correct the investigation result', 'Inspect the reflections store', 'Verify reuse in a separate run', 'Treat retained causes as context'],
        'slide_setup': ['Open a completed investigation.', 'Submit incorrect verdict and actual cause.', 'Inspect the reflections entry and version.'],
        'slide_mechanism': 'Corrective feedback creates alarm-related reflection context for later investigations.',
        'slide_boundary': 'No diagnosis guarantee. Sharing feedback with AWS requires separate confirmation.'
    }
    a['records'] = [r for r in a['records'] if r['id'] != 'D-M10'] + [record]
    a['use_case']['steps'][-1] = [
        'Record a corrected outcome',
        'Submit the reviewed cause using Add feedback; inspect the reflection or a prepared record.',
        'Incident reviewer',
        'Feedback and memory version retained; later recall checked separately.',
        'D-M10', 90
    ]
    a['use_case']['refs'] = list(dict.fromkeys(a['use_case']['refs'] + ['DF', 'DN']))
    data['comparison'][0][1] = 'Managed recurring-cause context, corrective-feedback reflections and explicitly attached custom stores'
    data['evidence_notes'][1] = 'DevOps dated changes identify migration of learned knowledge to memory and monitor memory enabled by default. Older cached pages differ; verify the current UI and do not treat refresh cadence as a completion guarantee.'
    note = 'Follow-up validation rechecked selected memory, feedback, lifecycle and setup sources, not all historical claims. A missing guide in a cached retrieval is not evidence that a feature is absent. See mechanisms/CONTINUATION_VALIDATION.md.'
    data['evidence_notes'] = [n for n in data['evidence_notes'] if not n.startswith('Follow-up validation rechecked')] + [note]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    builder = ROOT / 'tools/build_mechanisms.py'
    text = builder.read_text(encoding='utf-8')
    text = text.replace('31 mechanism records', '32 mechanism records').replace('31 documented mechanism records', '32 documented mechanism records')
    text = text.replace('Reviewed 21 October 2026 against 44 official AWS/Kiro pages.', 'Source register: 46 official AWS/Kiro pages. Original 44-source mechanism review dated 21 October 2026; this follow-up adds two references and rechecks selected critical mechanisms, not every historical claim.')
    text = text.replace('body{margin:0;', 'body{overflow-wrap:anywhere;margin:0;')
    builder.write_text(text, encoding='utf-8')
    builder = ROOT / 'tools/build_suite.py'
    text = builder.read_text(encoding='utf-8').replace(
        'href="dist/frontier-agents-document-suite.zip" download>Download document package',
        'href="https://github.com/lyrel-dev/frontier-agents/blob/main/dist/frontier-agents-document-suite.zip">Document package in GitHub (sign-in may be required)'
    )
    builder.write_text(text, encoding='utf-8')
    qa = ROOT / 'tools/qa_mechanisms_browser.py'
    text = qa.read_text(encoding='utf-8')
    text = text.replace("results={'revision':'2026-10-21-mechanisms-v1'", "results={'revision':json.loads((ROOT/'content/mechanisms.json').read_text())['revision']")
    text = text.replace("['devops','kiro','security','finops','index']", "['devops','kiro','security','finops','index','overview']")
    text = text.replace(".read_text());page.wait_for_timeout(100)", ".read_text(),wait_until='domcontentloaded');page.wait_for_timeout(100)")
    qa.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    apply()
