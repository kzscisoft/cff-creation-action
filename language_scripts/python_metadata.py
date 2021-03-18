#!/usr/bin/python3
import os
import toml
import argparse

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
    import sys
    import types
    module_dict = {}
    m = types.ModuleType('distutils.core')
    m.setup = lambda **kwargs: module_dict.update(kwargs)
    sys.modules['distutils.core'] = m

    sys.path.append(os.path.dirname(args.input_file))

    import setup

    output_cff_dat['title'] = module_dict['name']
    output_cff_dat['version'] = module_dict['version']
    
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
    
    if 'url' in metadata:
        output_cff_dat['url'] = metadata['url']

    if 'description' in metadata:
        output_cff_dat['abstract'] = metadata['description']

    if 'keywords' in metadata:
        output_cff_dat['keywords'] = metadata['keywords']

if args.doi:
    output_cff_dat['doi'] = args.doi

if args.repo_url:
    output_cff_dat['repository-code'] = args.repo_url
