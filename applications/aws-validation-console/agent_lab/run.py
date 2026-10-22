#!/usr/bin/env python3
"""Serve the console; optionally run the local worker in the same process."""
import argparse
import json
import os
from pathlib import Path
import secrets
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
    worker=None
    if args.with_worker:
        worker=Worker(config,store)
        threading.Thread(target=worker.run,name='experiment-worker',daemon=True).start()
    print('Console: http://127.0.0.1:8787 — no preloaded trials; writes '+('enabled' if config.enable_aws_writes else 'disabled'),flush=True)
    try:
        uvicorn.run(create_app(config,store,operator,approval),host=os.environ.get('LAB_BIND','127.0.0.1'),
                    port=int(os.environ.get('LAB_PORT','8787')),access_log=False)
    finally:
        if worker: worker.stop()

if __name__=='__main__': main()
