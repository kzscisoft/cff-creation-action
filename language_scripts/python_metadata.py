#!/usr/bin/python3
import os
import toml
import argparse
import yaml
import setuptools
import unittest.mock
import sys
import re

python_info_parser = argparse.ArgumentParser('PythonInfoParser')
python_info_parser.add_argument('input_file')
python_info_parser.add_argument('--cff-version', default='1.1.0')
python_info_parser.add_argument('--title', default=None)
python_info_parser.add_argument('--message', default=None)
python_info_parser.add_argument('--authors', default=None)
python_info_parser.add_argument('--affiliation', default=None)
python_info_parser.add_argument('--doi', default=None)
python_info_parser.add_argument('--repo-url', default=None)

args = python_info_parser.parse_args()

output_cff_dat = {}

if os.path.splitext(args.input_file)[1] == '.toml':
    toml_data = toml.load(args.input_file)

    if 'flit' in toml_data['tool']:
        # Project metadata stored via Flit
        metadata = toml_data['tool']['flit']['metadata']

        output_cff_dat['title'] = metadata['module']

        if 'author' in metadata:
            author = metadata['author'].strip()
            if ' ' in author:
                author = author.split(' ', -1)
            if isinstance(author, list):
                authors = [
                    {
                        'family-names': author[1],
                        'given-names': author[0].split(' ')
                    }
                ]
            else:
                authors = [{'given-names': author.strip()}]
            if args.affiliation:
                authors[-1]['affiliation'] = args.affiliation
            output_cff_dat['authors'] = authors

        if 'home-page' in metadata:
            output_cff_dat['url'] = metadata['home-page']

        if 'classifiers' in metadata:
            for classifier in metadata['classifiers']:
                if classifier.split('::')[0].strip().lower() == 'license':
                    #FIXME: This won't return https://spdx.org/licenses/ valid identifier
                    output_cff_dat['license'] = classifier.split('::')[-1].strip()

    elif 'poetry' in toml_data['tool']:
        # Project metadata stored via Poetry
        metadata = toml_data['tool']['poetry']

        output_cff_dat['title'] = metadata['name']
        output_cff_dat['version'] = metadata['version']
        output_cff_dat['abstract'] = metadata['description']

        if 'authors' in metadata and metadata['authors']:
            authors = []
            for author_str in metadata['authors']:
                if re.findall(r'<(.+)>', author_str):
                    email = re.findall(r'<(.+)>', author_str)[0].strip()
                    author = author_str.split('<')[0].strip()
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

        if 'license' in metadata:
            output_cff_dat['license'] = metadata['license']
  
        if 'keywords' in metadata and metadata['keywords']:
            output_cff_dat['keywords'] = metadata['keywords']
else:
    sys.path.append(os.path.dirname(args.input_file))
    with unittest.mock.patch.object(setuptools, 'setup') as mock_setup:
        import setup

    # called arguments are in `mock_setup.call_args`
    _, module_dict = mock_setup.call_args

    output_cff_dat['title'] = module_dict['name']
    output_cff_dat['version'] = module_dict['version']

    if 'author' in module_dict:
        author = module_dict['author'].strip()
        if ' ' in author:
            author = author.split(' ', -1)
        if isinstance(author, list):
            authors = [
                {
                    'family-names': author[1],
                    'given-names': author[0].split(' ')
                }
            ]
        else:
            authors = [{'given-names': author.strip()}]
        if args.affiliation:
            authors[-1]['affiliation'] = args.affiliation
        output_cff_dat['authors'] = authors

    if 'url' in module_dict:
        output_cff_dat['url'] = module_dict['url']

    if 'description' in module_dict:
        output_cff_dat['abstract'] = module_dict['description']

    if 'keywords' in module_dict:
        output_cff_dat['keywords'] = module_dict['keywords']

if args.doi:
    output_cff_dat['doi'] = args.doi

if args.repo_url:
    output_cff_dat['repository-code'] = args.repo_url

with open('CITATION.cff', 'w') as f:
    yaml.dump(output_cff_dat, f)
