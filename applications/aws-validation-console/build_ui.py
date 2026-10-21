"""Build offline HTML, Grafana JSON, examples and schema from tracked sources."""
from pathlib import Path
import json
from build_metrics import build
ROOT = Path(__file__).resolve().parent

def build_ui():
    r = ROOT / 'static'
    metrics = build()
    data = (r / 'ui-data.json').read_text().replace('</', '<\\/')
    extra = json.dumps(metrics, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    css = (r / 'style.css').read_text() + '\n' + (r / 'metrics.css').read_text()
    js = (r / 'app.js').read_text() + '\n' + (r / 'metrics-charts.js').read_text() + '\n' + (r / 'metrics.js').read_text()
    page = (r / 'shell.html').read_text().replace('__CSS__', css).replace('__DATA__', 'const APP_DATA = ' + data + ';\nconst APP_METRICS = ' + extra + ';').replace('__JS__', js)
    (r / 'console.html').write_text(page)
    return page

if __name__ == '__main__':
    build_ui()
    print('Built static/console.html and metrics assets')
