#!/usr/bin/env python2

"""Search reference .bib files for keywords and return requisted info.

"""

import argparse, os


class


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('terms', type=str, nargs='+')
    arguments = argument_parser.parse_args()

    terms = args.terms


if __name__ == '__main__':
    main()

for fil in os.listdir('/home/alexc/refs/bibs'):
    keys = []
    filname = fil.split('.')[0]
    with open('/home/alexc/refs/bibs/{}'.format(fil)) as inp:
        lins = inp.read().splitlines()
    for lin in lins:
        try:
            bibt = lin.split()[0]
        except IndexError:
            continue
        if bibt == 'title':
            title = lin.split('=')[1].replace(' {', '').replace('}', '')
        elif bibt == 'keywords':
            keys = lin.split()[2]
        elif bibt == 'annote':
            annote = lin.split('=')[1].replace(' {', '').replace('}', '')
    if keys == []:
        continue
    keys = keys.replace('{', '')
    keys = keys.replace('}', '')
    keys = keys.split(',')
    if set(terms).issubset(set(keys)):
        print(title)
        print(annote)
        print(filname)
        print('')
