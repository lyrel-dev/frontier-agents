"""Build the empty AWS/FIS workspace without credentials or any AWS access."""
from pathlib import Path
import re, hashlib, base64
ROOT=Path(__file__).resolve().parent

def build(destination=None):
    text=(ROOT/'static/aws.html').read_text()
    styles=[(ROOT/'static'/s).read_text() for s in ('style.css','aws.css','setup.css')]
    scripts=[(ROOT/'static'/s).read_text() for s in ('charts.js','setup.js','aws.js')]
    scripts=[s.replace("offline:location.protocol==='file:'",'offline:true') for s in scripts]
    text=re.sub(r'<link rel="stylesheet" href="/static/[^\"]+">','',text)
    text=re.sub(r'<script defer src="/static/[^\"]+"></script>','',text)
    hashes=lambda xs:' '.join("'sha256-"+base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()+"'" for s in xs)
    csp="default-src 'none'; script-src "+hashes(scripts)+"; style-src "+hashes(styles)+"; connect-src 'none'; img-src data:; base-uri 'none'; form-action 'none'"
    text=text.replace('<head>','<head><meta http-equiv="Content-Security-Policy" content="'+csp+'">'+''.join('<style>'+s+'</style>' for s in styles))
    text=text.replace('</body>',''.join('<script>'+s.replace('</script','<\\/script')+'</script>' for s in scripts)+'</body>')
    target=Path(destination or ROOT/'aws-preview.html');target.write_text(text);return target

if __name__=='__main__': print(build())
