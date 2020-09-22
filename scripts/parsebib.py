#!/usr/bin/env python3

"""Parse bib files and output in standard format

Currently this only works on article class bib files. It will add two new
fields: annote and keywords. The filename extension should not be included.
To change the file in place, run

echo "$(parseBib.py [filebase]) > [filebase].bib
"""

# For now assumes bib file is article

import argparse


FIELDS = ['title', 'author', 'journal', 'volume', 'number',
          'pages', 'year', 'issn', 'doi', 'url', 'abstract']


def main():
    args = parse_args()
    filebase = args.filebase

    filename = filebase + '.bib'

    with open(filename) as inp:
        lines = inp.readlines()

    field_dic = {}
    merged_line = ''
    for line in lines[1:]:
        if '@' in line:
            continue
        line = line.lstrip()
        line = line.rstrip('\n')
        if line[0] == '}':
            continue
        if line[-2] != '}':
            merged_line = merged_line + line
            continue
        else:
            if merged_line != '':
                line = merged_line + line
                merged_line = ''
        if line == '\n':
            continue
        else:
            field_dic = find_entry(line, field_dic)

    # modify field contents (capitilization, brackets, etc.)
    output_standard_bib(filebase, field_dic)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filebase', help='Filebase of bib file')

    return parser.parse_args()


def find_entry(line, field_dic):
    field_entry = line.split('=')
    field = field_entry[0].split()[0].lower()
    if field in FIELDS:
        entry = field_entry[1]
        while entry[0] in [' ', '{', '"']:
            entry = entry[1:]

        while entry[-1] in [' ', '}', '"', ',', '\n']:
            entry = entry[:-1]

        field_dic[field] = entry

    return field_dic


def output_standard_bib(filebase, field_dic):
    print('@article{{{},'.format(filebase))
    for field, entry in field_dic.items():
        print('    {} = {{{}}},'.format(field, entry))

    print('    keywords = {},')
    print('    annote = {}')
    print('}')


if __name__ == '__main__':
    main()
