#!/usr/bin/env python

"""Search reference .bib files for keywords and return requisted info.

"""

import argparse
import os
import pytest
import pdb


BIB_DIRECTORY = '/home/alexc/refs/bibs/'


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

        self.fields = fields
        self.terms = terms
        self._operators = operators
        self._count = 0
        self._field_count = len(fields)

    def __next__(self):
        if self._count == self._field_count:
            self._count = 0
            raise StopIteration()

        field = self.fields[self._count]
        terms = self.terms[self._count]
        self._count += 1
        return field, terms

    def __iter__(self):
        return self

    def fields_match(self, tested_fields):
        # This is ugly. Indicates a deeper problem with design
        if len(self._operators) == 0:
            pass
        else:
            if self._operators[0] == 'not':
                tested_fields[0] = not tested_fields[0]
            else:
                pass

        operators_without_negations = []
        field_index = 1
        # Loop through operators, apply negations, and remove from operators
        for operator_index, operator in enumerate(self._operators):
            if operator in ('and', 'or'):
                try:
                    if self._operators[operator_index + 1] == 'not':
                        tested_fields[field_index] = not tested_fields[field_index]
                    else:
                        pass
                except IndexError:
                    pass
                field_index += 1
                operators_without_negations.append(operator)
            elif operator == 'not':
                pass

        # Loop through again and apply conjunctions and disjunctions
        previous_fields = tested_fields[0]
        next_field_index = 1
        for operator in operators_without_negations:
            next_field = tested_fields[next_field_index]
            if operator == 'and':
                previous_fields = previous_fields and next_field
                next_field_index += 1
            elif operator == 'or':
                previous_fields = previous_fields or next_field
                next_field_index += 1

        match = previous_fields
        return match


class BibFile:

    def __init__(self, file_name):
        with open(file_name) as file:
            file_lines = file.readlines()
            #file_lines = [file_line.lower() for file_line in file_lines]
        
        # There are a lot of better ways to parse the file
        self._file_lines = file_lines

    def search_string_match(self, search_string):
        # I am using a fragile method to this, probably also slow
        tested_fields = [False] * len(search_string.fields)
        for line in self._file_lines:
            line = line.lower()
            for field_index, (field, terms) in enumerate(search_string):
                if field + ' =' in line:
                    if all(term in line for term in terms):
                        tested_fields[field_index] = True
                    else:
                        pass
                else:
                    pass

        match = search_string.fields_match(tested_fields)

        return match

    def get_field_texts(self, fields):
        field_texts = []
        for field in fields:
            for line in self._file_lines:
                # make this a seperate method
                if field + ' =' in line:
                    field_start = line.find('{') + 1
                    field_end = line.rfind('}')
                    field_text = line[field_start:field_end]
                    field_texts.append(field_text)
                    break

        return field_texts


class Bibliography:

    def __init__(self, bib_directory):
        bibfile_names = []
        for bibfile_name in os.listdir(bib_directory):
            if bibfile_name[0] == '.':
                continue
            bibfile_name_full = bib_directory + bibfile_name
            bibfile_names.append(bibfile_name_full)

        self._bibfile_names = bibfile_names

    def match_and_print_fields(self, search_string, fields):
        print('')
        for bibfile_name in self._bibfile_names:
            bibfile = BibFile(bibfile_name)
            match = bibfile.search_string_match(search_string)
            if match:
                field_texts = bibfile.get_field_texts(fields)
                self._print_field_texts(field_texts)
            else:
                pass

    def _print_field_texts(self, field_texts):
        for field_text in field_texts:
            print(field_text)

        print('')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-s',
            type=str,
            nargs='+',
            dest='search_string',
            help='Search string')
    parser.add_argument(
            '-t',
            type=str,
            nargs='+',
            default = ['title', 'year', 'author', 'annote'],
            dest='terms',
            help='Terms to print')
    args = parser.parse_args()

    bibliography = Bibliography(BIB_DIRECTORY)
    search_string = SearchString(args.search_string)
    bibliography.match_and_print_fields(search_string, args.terms)


if __name__ == '__main__':
    main()
