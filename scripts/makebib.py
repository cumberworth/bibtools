#!/usr/bin/env python

"""Read cited references from latex file and compile a bib file"""

import argparse
import pkg_resources
import re

import bibtools.bib as btl


ABBREVS_FILE = pkg_resources.resource_filename(
    'bibtools', 'data/cassi-abbreviations.csv')


def main():
    args = parse_args()
    bib_keys = parse_latex_file(args.latex_file)
    bib_entries = create_bib_entries(bib_keys)
    write_bibfile(bib_entries, args.bib_file)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'latex_file',
        type=str,
        help='Input tex file')
    parser.add_argument(
        'bib_file',
        type=str,
        help='Output bib file')
    return parser.parse_args()


def parse_latex_file(filename):
    with open(filename) as f:
        latex_file = f.read()

    cite_commands = re.finditer(r'(cite)(t|num)?(\{)(?P<keys>[\w*,-]*)(\})',
                                latex_file)
    empty_citations = 0
    bib_keys = []
    for cite in cite_commands:
        keys = parse_cite_command(cite)
        if empty_citation(keys):
            empty_citations += 1
            continue

        for key in keys:
            if key in bib_keys:
                continue
            else:
                bib_keys.append(key)

    print('There are {} empty citations'.format(empty_citations))

    return bib_keys


def parse_cite_command(cite):
    cite = cite.group('keys')
    cite = cite.replace('*', '')
    bib_keys = cite.split(',')

    return bib_keys


def empty_citation(keys):
    return keys == ['']


def create_bib_entries(bib_keys):
    bib_entries = []
    bib = btl.Bibliography(btl.BIB_DIRECTORY)
    abbs = btl.Abbreviations(ABBREVS_FILE)
    for bib_key in bib_keys:
        try:
            bib_entry = bib[bib_key]
        except KeyError:
            print('No reference for {}'.format(bib_key))
            continue

        bib_entry.abbreviate_journal(abbs)
        bib_entry.standarize_order_and_fields()

        bib_entries.append(bib_entry.as_string())

    return bib_entries


def write_bibfile(bib_entries, filename):
    bibstring = '\n\n'.join(bib_entries)
    with open(filename, 'w') as out:
        out.write(bibstring)


if __name__ == '__main__':
    main()
