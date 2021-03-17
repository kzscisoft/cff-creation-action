import toml
import argparse
import os
import re
import yaml
import time

DEFAULT_MSG = 'If you use this software, please cite it using these metadata.'

julia_info_parser = argparse.ArgumentParser('JuliaInfoParser')
julia_info_parser.add_argument('project_toml')
julia_info_parser.add_argument('--cff-version', default='1.1.0')
julia_info_parser.add_argument('--title', default=None)
julia_info_parser.add_argument('--message', default=None)
julia_info_parser.add_argument('--authors', default=None)

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

    if 'authors' in output_cff_dat:
        author_strs = metadata['authors']

    if 'uuid' in metadata:
        output_cff_dat['identifiers'] = [
            {
                'type': 'other',
                'value': metadata['uuid']
            }
        ]

if args.authors:
    author_strs = args.authors.split(',')

    authors = []

if author_strs:
    for author_str in author_strs:
        if re.findall(r'<(.+)>', author_str):
            email = re.findall(r'<(.+)>', author_str)[0].strip()
            author = author_str.split('<')[0].strip().split(' ', -1)
        else:
            author = author_str.strip().split(' ', -1)
        authors.append(
            {
                'family-names': author[1],
                'given-names': author[0].split(' ')
            }
        )
        output_cff_dat['authors'] = authors

output_cff_dat['date-released'] = time.strftime('%Y-%m-%d', current_time)
output_cff_dat['message'] = args.message if args.message else DEFAULT_MSG
output_cff_dat['cff-version'] = args.cff_version
output_cff_dat['title']

with open('CITATION.cff', 'w') as f:
    yaml.dump(output_cff_dat, f)
