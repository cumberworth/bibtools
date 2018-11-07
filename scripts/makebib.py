#!/usr/bin/env python

"""Read cited references from latex file and compile a bib file"""

import argparse
import re

import mybiblib.bib as mbl


BIB_DIRECTORY = '/home/alexc/refs/bibs/'
ABBREVS_FILE = '/home/alexc/share/cassi-abbreviations.csv'


def main()
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

    reg = re.compile('cite{|t|num}{[a-z0-9\*,-]*}')
    cite_commands =  reg.findall(raw)
    empty_citations = 0
    bib_keys = []
    for cite in cite_commands:
        keys = parse_cite_command()
        if empty_citation(keys)
            empty_citations += 1
            continue

        for key in keys:
            if key in bib_keys:
                continue
            else:
                bib_keys.append(key)

    print('There are {} empty citations'.format(empty_citations))

    return bib_keys


def parse_cite_command(cite_command):
    cite = cite.replace('cite{', '')
    cite = cite.replace('citet{', '')
    cite = cite.replace('citenum{', '')
    cite = cite.replace('*', '')
    cite = cite.replace('}', '')
    bib_keys = cite.split(',')

    return cite


def empty_citation(keys):
    return keys == ['']


def create_bib_entries(bib_keys):
    bib_entries = []
    bib = mbl.Bibliography(BIB_DIRECTORY)
    abbs = mbl.Abbreviations(ABBREVS_FILE)
    for bib_key in bib_keys:
        try:
            bib_entry = bib[cite]
        except KeyError:
            print('No reference for {}'.format(cite))
            continue

        bib_entry.abbreviate_journal(abbs)
        bib_entry.standarize_order_and_fields()

        bib_entries.append(bib_entry.as_string)

    return bib_entries


def write_bibfile(bib_entries, filename):
    bibstring = '\n\n'.join(bib_entries)
    with open(filename, 'w') as out:
        out.write(bibstring)


if __name__ == '__main__':
    main()
