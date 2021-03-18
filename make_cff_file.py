#!/usr/bin/python3
import subprocess
import argparse
import os

SEARCH = {
    'python': {
        'files': ['setup.py', 'pyproject.toml'],
        'script': 'python_metadata'
    },
    'r': {
        'files': ['DESCRIPTION'],
        'script': 'R_metadata'
    },
    'julia': {
        'files': ['Project.toml'],
        'script': 'julia_metadata'
    }
}

SCRIPT_PATH = os.path.basename(__file__)

repo_parser = argparse.ArgumentParser('RepositoryParser')
repo_parser.add_argument('input_directory')
repo_parser.add_argument('--title', default=None)
repo_parser.add_argument('--message', default=None)
repo_parser.add_argument('--authors', default=None)
repo_parser.add_argument('--affiliation', default=None)
repo_parser.add_argument('--doi', default=None)
repo_parser.add_argument('--repo-url', default=None)
repo_parser.add_argument('--language', default=None)

args = repo_parser.parse_args()
language = None
script = None

if args.language:
    language = args.language
else:
    for lang in SEARCH:
        files = SEARCH[lang]['files']
        if any(os.path.exists(i) for i in files):
            language = lang
            script = SEARCH[lang]['script']
            break

if not language:
    raise RuntimeError("Could not identify source language")

cmd_ = [
    script,
    args.input_directory,
    f'--title "{args.title}"',
    f'--message "{args.message}"',
    f'--authors "{args.authors}"',
    f'--affiliation "{args.affiliation}"',
    f'--doi "{args.doi}"',
    f'--repo-url "{args.repo_url}"'
]

run_ = subprocess.Popen(cmd_, shell=False)
run_.wait()