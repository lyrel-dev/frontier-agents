#!/usr/bin/env python3
"""Run the durable worker separately from the web process."""
import argparse
import os
from pathlib import Path
import signal
from lab.models import Configuration
from configure import read_configuration
from lab.store import Store
from lab.worker import Worker


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',default=os.environ.get('LAB_CONFIG','config.json'))
    parser.add_argument('--data',default=os.environ.get('LAB_DATA','data'))
    args=parser.parse_args()
    worker=Worker(read_configuration(args.config),Store(args.data))
    for sig in (signal.SIGTERM,signal.SIGINT): signal.signal(sig,lambda *_:worker.stop())
    worker.run()

if __name__=='__main__': main()
