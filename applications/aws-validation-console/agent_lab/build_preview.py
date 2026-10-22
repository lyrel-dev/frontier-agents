#!/usr/bin/env python3
"""Build an empty, self-contained UI preview. No accounts or observations are embedded."""
from pathlib import Path
import re,hashlib,base64
ROOT=Path(__file__).resolve().parent

def build(destination=None):
    text=(ROOT/'static/index.html').read_text()
    css=(ROOT/'static/style.css').read_text()
    scripts=[(ROOT/'static'/name).read_text() for name in ('charts.js','app.js')]
    text=text.replace('<link rel="stylesheet" href="/static/style.css">','<style>'+css+'</style>')
    text=re.sub(r'<script defer src="/static/(?:charts|app)\.js"></script>','',text)
    # Preview is always offline, including when opened from another HTTP host.
    scripts[1]=scripts[1].replace("offline:location.protocol==='file:'","offline:true")
    hashes=lambda items:' '.join("'sha256-"+base64.b64encode(hashlib.sha256(item.encode()).digest()).decode()+"'" for item in items)
    csp="default-src 'none'; script-src "+hashes(scripts)+"; style-src "+hashes([css])+"; connect-src 'none'; img-src data:; base-uri 'none'; form-action 'none'"
    text=text.replace('<head>','<head>\n<meta http-equiv="Content-Security-Policy" content="'+csp+'">')
    text=text.replace('</body>',''.join('<script>'+s.replace('</script','<\\/script')+'</script>' for s in scripts)+'</body>')
    target=Path(destination or ROOT/'preview.html');target.write_text(text);return target

if __name__=='__main__':print(build())
