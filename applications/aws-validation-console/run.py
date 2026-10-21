#!/usr/bin/env python3
"""Start the local console. No credentials are accepted through the browser."""
import os, secrets
from pathlib import Path
import uvicorn
from app.server import create_app
if __name__ == '__main__':
    if not (Path(__file__).parent / 'static' / 'console.html').exists():
        from build_ui import build_ui
        build_ui()
    token = os.environ.get('CONSOLE_TOKEN') or secrets.token_urlsafe(32)
    host = os.environ.get('CONSOLE_BIND', '127.0.0.1')
    port = int(os.environ.get('CONSOLE_PORT', '8787'))
    print('\nValidation console: http://127.0.0.1:' + str(port), flush=True)
    print('Unlock token (keep private): ' + token, flush=True)
    print('Fault execution is not implemented. All workspace records stay in the local data directory.\n', flush=True)
    uvicorn.run(create_app(token=token), host=host, port=port, access_log=False)
