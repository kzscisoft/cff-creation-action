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

# Some tidy up from the bash
for arg in ['title', 'message', 'language', 'authors', 'affiliation', 'doi', 'repo_url']:
    _arg = getattr(args, arg)
    if not isinstance(_arg, str):
        continue
    if _arg[0] == "'":
        _arg = _arg[1:]
    if _arg[-1] == "'":
        _arg = _arg[:-1]
    setattr(args, arg, _arg)

language = None
script = None

if args.language:
    language = args.language.lower()
else:
    for lang in SEARCH:
        files = SEARCH[lang]['files']
        if any(os.path.exists(i) for i in files):
            language = lang
            break

if not os.path.exists(args.input_directory):
    raise FileNotFoundError(
        f"Could not find directory '{args.input_directory}'"
    )

if not language or language not in SEARCH:
    raise RuntimeError(f"Could not identify source language '{language}'")

script = SEARCH[language]['script']

if language == "r":
    input_loc = f'--input-file="{os.path.join(args.input_directory, "DESCRIPTION")}"'
elif language == "python":
    if os.path.exists(os.path.join(args.input_directory), "setup.py"):
        input_loc = f'--input-file="{os.path.join(args.input_directory, "setup.py")}"'
    else:
        input_loc = f'--input-file="{os.path.join(args.input_directory, "pyproject.toml")}"'
elif language == "julia":
    input_loc = f'--input-file="{os.path.join(args.input_directory, "Project.toml")}"'
else:
    input_loc = args.input_directory

cmd_ = [
    script,
    input_loc
]

for arg in ['title', 'message', 'authors', 'affiliation', 'doi', 'repo_url']:
    if getattr(args, arg):
        cmd_ += [f'--{arg.replace("_", "-")}="{getattr(args, arg)}"']

print("Running the Command: "+' '.join(cmd_))

run_ = subprocess.Popen(cmd_, shell=False)
run_.wait()
