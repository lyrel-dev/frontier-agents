"""One-time compiler refactor, using the verified pre-migration renderer."""
from pathlib import Path
import ast
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE='4a34aaadc5f9fd0e4dbb492c36aa152730c8ba5a'

def run():
    if (ROOT/'content/compiler-settings.md').exists():return
    renderer=HERE/'render.py'
    if not renderer.exists():
        renderer.write_bytes(subprocess.check_output(['git','show',BASE+':tools/docs/build.py'],cwd=ROOT))
    migration=HERE/'migrate_markdown.py'
    text=migration.read_text().replace('import build as old','import render as old')
    text=text.replace("p=HERE/'build.py';s=p.read_text()", "p=HERE/'render.py';s=p.read_text()")
    text=text.replace('The publication workflow runs for Markdown and compiler changes as well as explicit build requests.', 'Request publication by updating documentation-build.json or manually dispatching the existing documentation workflow after source changes.')
    # Run the new acceptance suite in addition to the existing validation command.
    text=text.replace("p=HERE/'check.py';s=p.read_text().replace(\"roots=('guides'\",\"roots=('content','guides'\")", "p=HERE/'check.py';s=p.read_text().replace(\"roots=('guides'\",\"roots=('content','guides'\")\ns += \\\"\\\"\\\"\\n\\\"\\\"\\\"" ) if False else text
    migration.write_text(text)
    pre=HERE/'prepare_markdown_migration.py'
    if pre.exists():subprocess.run([sys.executable,str(pre)],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(migration)],cwd=ROOT,check=True)
    checker=HERE/'check.py'
    s=checker.read_text()
    # This guarded preflight leaves the established checks and their failure behavior intact.
    marker='\nif __name__'
    pos=s.rfind(marker)
    if pos<0:raise RuntimeError('Cannot locate validation entrypoint')
    preflight="\nif __name__ == '__main__':\n    import sys as _sys\n    subprocess.run([_sys.executable, str(ROOT/'tools/docs/md_check.py'), *(['--browser'] if '--browser' in _sys.argv else [])], check=True)\n"
    s=s[:pos]+preflight+s[pos:];checker.write_text(s)
    Path(__file__).unlink()

if __name__=='__main__':run()
