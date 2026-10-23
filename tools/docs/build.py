#!/usr/bin/env python3
"""Compile frontmatter Markdown into the existing HTML documentation routes."""
from pathlib import Path
import argparse
import subprocess
import sys

_ROOT=Path(__file__).resolve().parents[2]
if __name__=='__main__' and not (_ROOT/'content/compiler-settings.md').exists():
    subprocess.run([sys.executable,str(_ROOT/'tools/docs/md_bootstrap.py')],cwd=_ROOT,check=True)

# Existing validators import the renderer's public definitions from this module.
from render import *  # noqa: F401,F403,E402

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit',action='store_true')
    args=parser.parse_args()
    commit() if args.commit else build()
