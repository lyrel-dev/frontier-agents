"""Rebuild the single-file UI from local sources; no network or bundler needed."""
from pathlib import Path
r = Path(__file__).resolve().parent / 'static'
data = (r / 'ui-data.json').read_text().replace('</', '<\\/')
page = (r / 'shell.html').read_text().replace('__CSS__', (r / 'style.css').read_text()).replace('__DATA__', 'const APP_DATA = ' + data + ';').replace('__JS__', (r / 'app.js').read_text())
(r / 'console.html').write_text(page)
print('Built static/console.html')
