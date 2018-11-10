"""Custom classes for bib files"""


import csv
from collections import OrderedDict
import os


import biblib.bib


class Abbreviations:
    def __init__(self, abb_filename):
        raw = csv.reader(open(abb_filename))

        self._full_to_abb = {}
        self._abb_to_full = {}
        for row in raw:
            self._full_to_abb[row[0]] = row[1]
            self._abb_to_full[row[1]] = row[0]

    def abbreviate(self, full):
        try:
            abb = self._full_to_abb[full]
        except KeyError:
            print('Abbreviation not in database for journal {}'.format(full))
            raise

        return abb

    def unabbreviate(self, abb):
        try:
            abb = self._abb_to_full[abb]
        except KeyError:
            print('Abbreviation not in database for journal {}'.format(full))
            raise

        return abb


class SearchString:
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
    def __init__(self, entry):
        self._entry = entry

    def search_string_match(self, search_string):
        tested_fields = [False] * len(search_string.fields)
        for field_index, (field, terms) in enumerate(search_string):
            if field in self._entry.keys():
                field_entry = self._entry[field].lower()
                if all(term in field_entry for term in terms):
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
            if field in self._entry.keys():
                field_texts.append(self._entry[field])

        return field_texts

    def standarize_order_and_fields(self):
        key = self._entry.key
        typ = self._entry.typ
        standard = OrderedDict()
        if typ == 'article':
            fields = ['author', 'title', 'journal', 'volume', 'pages', 'year',
                    'doi']
        elif typ == 'book':
            fields = ['author', 'title', 'year', 'publisher', 'isbn']
        elif typ == 'phdthesis':
            fields = ['author', 'title', 'year', 'school']
        else:
            print('Standard not defined for entry type {}'.format(typ))
            print(key)
            raise Exception

        for field in fields:
            try:
                standard[field] = self._entry[field]
            except KeyError:
                print('Entry {} missing field {}'.format(key, field))

        self._entry = biblib.bib.Entry(standard, typ=typ, key=key)

    def abbreviate_journal(self, abbreviations):
        if self._entry.typ == 'article':
            journal = self._entry['journal']
            abb = abbreviations.abbreviate(journal)
            self._entry['journal'] = abb

    def unabbreviate_journal(self, abbreviations):
        if self._typ == 'article':
            journal = self._entry['journal']
            if '.' in journal:
                full = abbreviations.unabbreviate(journal)
                self._entry['journal'] = full

    def write_to_file(self, filename=None):
        if filename == None:
            filename = '{}.tex'.format(self._entry.key)

        with open(filename, 'w') as f:
            f.write(self._entry.to_bib())

    def as_string(self):
        return self._entry.to_bib()


class Bibliography:
    """Bibliography composed of individual bib files in a directory"""
    def __init__(self, bib_directory):
        bibfile_names = []
        for bibfile_name in os.listdir(bib_directory):

            # Ignore hidden files
            if bibfile_name[0] == '.':
                continue
            bibfile_name_full = bib_directory + bibfile_name
            bibfile_names.append(bibfile_name_full)

        self._bibfile_names = bibfile_names

        # Create biblib database
        bibparser = biblib.bib.Parser()
        for filename in bibfile_names:
            bibfile = open(filename)
            bibparser.parse(bibfile)

        self._entries = bibparser.get_entries()

    def __getitem__(self, key):
        return BibFile(self._entries[key])

    def match_and_print_fields(self, search_string, fields):
        print('')
        for entry in self._entries.values():
            bibfile = BibFile(entry)
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
