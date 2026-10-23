"""Build the empty guided interface; no account or measurement fixtures."""
from pathlib import Path
import re,hashlib,base64
ROOT=Path(__file__).resolve().parent

def build(destination=None):
    text=(ROOT/'static/setup.html').read_text()
    styles=[(ROOT/'static'/n).read_text() for n in ('style.css','aws.css','setup.css')]
    scripts=[(ROOT/'static/setup.js').read_text().replace("offline:location.protocol==='file:'",'offline:true')]
    text=re.sub(r'<link rel="stylesheet" href="/static/[^\"]+">','',text)
    text=re.sub(r'<script defer src="/static/[^\"]+"></script>','',text)
    hashes=lambda xs:' '.join("'sha256-"+base64.b64encode(hashlib.sha256(x.encode()).digest()).decode()+"'" for x in xs)
    csp="default-src 'none'; script-src "+hashes(scripts)+"; style-src "+hashes(styles)+"; connect-src 'none'; img-src data:; base-uri 'none'; form-action 'none'"
    text=text.replace('<head>','<head><meta http-equiv="Content-Security-Policy" content="'+csp+'">'+''.join('<style>'+x+'</style>' for x in styles))
    text=text.replace('</body>',''.join('<script>'+x.replace('</script','<\\/script')+'</script>' for x in scripts)+'</body>')
    target=Path(destination or ROOT/'setup-preview.html');target.write_text(text);return target
if __name__=='__main__':print(build())
