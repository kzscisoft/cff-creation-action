#!/usr/bin/python3

import argparse
import re

license_parser = argparse.ArgumentParser('LicenseIdentifier')
license_parser.add_argument('license')

LICENSES = {
    'AGPL': 'GNU AFFERO GENERAL PUBLIC LICENSE',
    'GPL': 'GNU GENERAL PUBLIC LICENSE',
    'LGPL': 'GNU LESSER GENERAL PUBLIC LICENSE',
    'MPL': 'Mozilla Public License',
    'Apache': 'Apache License',
    'MIT': 'MIT License',
    'BSL': 'Boost Software License',
    'Unlicense': 'This is free and unencumbered software released',
    'BSD': 'BSD'
}

license_lines = open(license_parser.parse_args().license).readlines()
license_lines = [i for i in license_lines if i.strip()]

version = ''

for i, _ in enumerate(license_lines):
    for license, first_line in LICENSES.items():
        if first_line in license_lines[i]:
            version = re.findall(r'Version\s([\d+\.]+)', license_lines[i])
            if not version:
                version = re.findall(license+r'\s*([\d\.]+)', license_lines[i])
            if not version:
                version = re.findall(r'Version\s([\d+\.]+)', license_lines[i+1])
            if not version:
                print(license)
                exit()
            if license == 'BSD':
                version = f'{license} {version[0]} Clause'
                break
            elif '.' not in version[0]:
                version[0] += '.0'
            version = f'{license}-{version[0]}'
            break

print(version)
