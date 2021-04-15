#!/usr/bin/python3
import toml
import argparse
import os
import re
import yaml
import time

julia_info_parser = argparse.ArgumentParser('JuliaInfoParser')
julia_info_parser.add_argument('project_toml')
julia_info_parser.add_argument('--cff-version', default='1.1.0')
julia_info_parser.add_argument('--title', default=None)
julia_info_parser.add_argument('--message', default=None)
julia_info_parser.add_argument('--authors', default=None)
julia_info_parser.add_argument('--affiliation', default=None)
julia_info_parser.add_argument('--doi', default=None)
julia_info_parser.add_argument('--repo-url', default=None)

args = julia_info_parser.parse_args()

output_cff_dat = {}

current_time = time.localtime()

author_strs = None

if not args.title or not args.version:
    if not os.path.exists(args.project_toml):
        raise FileNotFoundError(
            "Could not load title and version metadata for Julia project, file "
            f"'{args.project_toml}' does not exist."
        )

    metadata = toml.load(args.project_toml)
    output_cff_dat['version'] = metadata['version']
    output_cff_dat['title'] = metadata['name']

    if 'authors' in metadata:
        author_strs = metadata['authors']
        authors = []

    if 'uuid' in metadata:
        output_cff_dat['identifiers'] = [
            {
                'type': 'other',
                'value': metadata['uuid']
            }
        ]
else:
    output_cff_dat['title'] = args.title

if args.authors:
    author_strs = args.authors.split(',')

    authors = []

if author_strs:
    for author_str in author_strs:
        if re.findall(r'<(.+)>', author_str):
            email = re.findall(r'<(.+)>', author_str)[0].strip()
            author = author = author_str.split('<')[0].strip()
            if ' ' in author:
                author = author.split(' ', -1)
        else:
            author = author_str.strip()
            if ' ' in author:
                author = author.split(' ', -1)

        if isinstance(author, list):
            authors.append(
                {
                    'family-names': author[1],
                    'given-names': author[0].split(' ')
                }
            )
        else:
            authors.append({'given-names': author.strip()})
        if args.affiliation:
            authors[-1]['affiliation'] = args.affiliation
        output_cff_dat['authors'] = authors

if args.doi:
    output_cff_dat['doi'] = args.doi

if args.repo_url:
    output_cff_dat['repository-code'] = args.repo_url

output_cff_dat['date-released'] = time.strftime('%Y-%m-%d', current_time)
output_cff_dat['message'] = args.message
output_cff_dat['cff-version'] = args.cff_version


# Get rid of extra quotes
for key in output_cff_dat:
    _val = output_cff_dat[key]

    while _val[0] in ["'", '"']:
        _val = _val[1:]

    while _val[-1] in ["'", '"']:
        _val = _val[:-1]

with open('CITATION.cff', 'w') as f:
    yaml.dump(output_cff_dat, f)
