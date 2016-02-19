#!/usr/bin/env python

"""Search reference .bib files for keywords and return requisted info.

"""

import argparse
import os
import pytest


class SearchString:

#_fields
#_terms
#_operators

    def __init__(self, input_list):

        # Parse search term
        fields = []
        terms = []
        operators = []
        for term in input_list:
            if 'field:' in term:
                field = term.split(':')[1]
                fields.append(field)
                terms.append([])
            elif term in ['and', 'or', 'not']:
                operators.append(term)
            else:
                terms[-1].append(term)

        self._fields = fields
        self._terms = terms
        self._operators = operators
        self._count = 0
        self._field_count = len(fields)

    def __next__(self):
        if self._count == self._field_count:
            raise StopIteration()

        field = self._fields[self._count]
        terms = self._terms[self._count]
        self._count += 1
        return field, terms

    def __iter__(self):
        return self

    def fields_match(self, tested_fields):
        pass

    def _parse(self):
        pass


class Bibliography:

#_bibfile_names

    def __init__(self, bib_directory):
        pass

    def match_and_print_fields(self, search_string, fields):
        pass


class BibFile:

    def __init__(self, file_name):
        pass

    def search_string_match(self, search_string):
        pass

    def get_fields(self, fields):
        pass


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('terms', type=str, nargs='+')
    arguments = argument_parser.parse_args()

    terms = args.terms


if __name__ == '__main__':
    main()
#---
#
#for fil in os.listdir('/home/alexc/refs/bibs'):
#    keys = []
#    filname = fil.split('.')[0]
#    with open('/home/alexc/refs/bibs/{}'.format(fil)) as inp:
#        lins = inp.read().splitlines()
#    for lin in lins:
#        try:
#            bibt = lin.split()[0]
#        except IndexError:
#            continue
#        if bibt == 'title':
#            title = lin.split('=')[1].replace(' {', '').replace('}', '')
#        elif bibt == 'keywords':
#            keys = lin.split()[2]
#        elif bibt == 'annote':
#            annote = lin.split('=')[1].replace(' {', '').replace('}', '')
#    if keys == []:
#        continue
#    keys = keys.replace('{', '')
#    keys = keys.replace('}', '')
#    keys = keys.split(',')
#    if set(terms).issubset(set(keys)):
#        print(title)
#        print(annote)
#        print(filname)
#        print('')
