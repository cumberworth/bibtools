#!/usr/bin/env python3

"""Parse bib files and output in standard format; warn if missing information"""

# For now assumes bib file is article

import argparse


FIELDS = ['title', 'author', 'journal', 'volume', 'number', 'pages', 'year', 'issn', 'doi', 'url', 'abstract']


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filebase', help='Filebase of bib file')
    args = parser.parse_args()
    filebase = args.filebase

    filename = filebase + '.bib'


    with open(filename) as inp:
        lines = inp.readlines()

    field_dic = {}
    for line in lines[1:]:
        if line == '\n':
            continue
        else:
            field_dic = find_entry(line, field_dic)

    #modify field contents (capitilization, brackets, etc.)
    output_standard_bib(filebase, field_dic)


if __name__ == '__main__':
    main()
