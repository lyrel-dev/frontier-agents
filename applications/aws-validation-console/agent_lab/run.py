#!/usr/bin/env python3
"""Serve the console; optionally run the local worker in the same process."""
import argparse
import json
import os
from pathlib import Path
import secrets
import signal
import threading
import uvicorn
from lab.models import Configuration
from configure import read_configuration
from lab.store import Store
from lab.api import create_app
from lab.worker import Worker


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',default=os.environ.get('LAB_CONFIG','config.json'))
    parser.add_argument('--data',default=os.environ.get('LAB_DATA','data'))
    parser.add_argument('--with-worker',action='store_true')
    args=parser.parse_args()
    config=read_configuration(args.config)
    store=Store(args.data)
    operator=os.environ.get('LAB_OPERATOR_TOKEN') or secrets.token_urlsafe(32)
    approval=os.environ.get('LAB_APPROVAL_TOKEN') or secrets.token_urlsafe(32)
    if 'LAB_OPERATOR_TOKEN' not in os.environ: print('Local operator token (keep private): '+operator,flush=True)
    if 'LAB_APPROVAL_TOKEN' not in os.environ: print('Separate approval token (keep private): '+approval,flush=True)
    app=create_app(config,store,operator,approval)
    server=uvicorn.Server(uvicorn.Config(app,host=os.environ.get('LAB_BIND','127.0.0.1'),
                         port=int(os.environ.get('LAB_PORT','8787')),access_log=False))
    worker=None; worker_thread=None
    supervisor_stop=threading.Event()
    if args.with_worker:
        worker=Worker(config,store)
        # Lock acquisition and startup complete before binding the HTTP port.
        worker_thread=worker.start_background()
        def supervise():
            while not supervisor_stop.wait(.1):
                if worker.finished.is_set() or not worker_thread.is_alive():
                    server.should_exit=True
                    return
        threading.Thread(target=supervise,name='worker-supervisor',daemon=True).start()
    print('Console: http://127.0.0.1:'+os.environ.get('LAB_PORT','8787')+' — no preloaded trials; writes '+('enabled' if config.enable_aws_writes else 'disabled'),flush=True)
    # Uvicorn re-raises captured signals after stopping HTTP. Retain an outer
    # handler so a foreground SIGTERM cannot terminate before the worker drains.
    original_handlers={sig:signal.getsignal(sig) for sig in (signal.SIGINT,signal.SIGTERM)}
    def request_shutdown(signum,frame):
        server.should_exit=True
    for sig in original_handlers:
        signal.signal(sig,request_shutdown)
    try:
        server.run()
    finally:
        try:
            supervisor_stop.set()
            if worker:
                worker.stop()
                worker_thread.join(timeout=30)
                if worker_thread.is_alive():
                    # In-flight intents remain durable and require reconciliation.
                    print('Worker shutdown deadline exceeded; inspect operation intents before restarting.',flush=True)
                    raise SystemExit(1)
                if worker.failure:
                    print('Experiment worker failed: '+worker.failure,flush=True)
                    raise SystemExit(1)
        finally:
            for sig,handler in original_handlers.items():
                signal.signal(sig,handler)

if __name__=='__main__': main()
