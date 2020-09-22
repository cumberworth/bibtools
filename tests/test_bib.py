#!/usr/env python

import pytest

import bibtools as btl


@pytest.fixture
def search_string_simple():
    input_list = ['field:keywords', 'stuff', 'thing']
    search_string = btl.SearchString(input_list)
    return search_string


@pytest.fixture
def search_string_negation():
    input_list = ['not', 'field:keywords', 'stuff', 'thing']
    search_string = btl.SearchString(input_list)
    return search_string


@pytest.fixture
def search_string_conjunction():
    input_list = ['field:keywords', 'stuff',
                  'thing', 'and', 'field:author', 'pande']
    search_string = btl.SearchString(input_list)
    return search_string


@pytest.fixture
def search_string_disjunction():
    input_list = ['field:keywords', 'stuff',
                  'thing', 'or', 'field:author', 'pande']
    search_string = btl.SearchString(input_list)
    return search_string


class TestSearchString:

    @pytest.mark.parametrize('search_string, field_list, terms_list', [
        (search_string_simple(), ['keywords'], [['stuff', 'thing']]),
        (search_string_negation(), ['keywords'], [['stuff', 'thing']]),
        (search_string_conjunction(), ['keywords', 'author'], [['stuff',
                                                                'thing'],
                                                               ['pande']]),
        (search_string_disjunction(), ['keywords', 'author'], [['stuff',
                                                                'thing'],
                                                               ['pande']])])
    def test__iter__(self, search_string, field_list, terms_list):
        test_field_list = []
        test_terms_list = []
        for field, terms in search_string:
            test_field_list.append(field)
            test_terms_list.append(terms)
        assert test_field_list == field_list
        assert test_terms_list == terms_list

    @pytest.mark.parametrize('search_string, tested_fields, match', [
        (search_string_simple(), [True], True),
        (search_string_simple(), [False], False),
        (search_string_negation(), [True], False),
        (search_string_negation(), [False], True),
        (search_string_conjunction(), [True, True], True),
        (search_string_conjunction(), [True, False], False),
        (search_string_conjunction(), [False, True], False),
        (search_string_conjunction(), [False, False], False),
        (search_string_disjunction(), [True, True], True),
        (search_string_disjunction(), [True, False], True),
        (search_string_disjunction(), [False, True], True),
        (search_string_disjunction(), [False, False], False)
    ])
    def test_fields_match(self, search_string, tested_fields, match):
        test_match = search_string.fields_match(tested_fields)
        assert test_match == match


@pytest.fixture()
def bibfile_pande():
    bibfile_pande = btl.BibFile('pande2010.bib')
    return bibfile_pande


@pytest.fixture
def search_string_pande_1():
    input_list = ['field:keywords', 'review', 'msm']
    search_string = btl.SearchString(input_list)
    return search_string


@pytest.fixture
def search_string_pande_2():
    input_list = ['field:keywords', 'review', 'msm', 'thing']
    search_string = btl.SearchString(input_list)
    return search_string


@pytest.fixture
def search_string_pande_3():
    input_list = ['field:keywords', 'review',
                  'msm', 'and', 'field:author', 'pande']
    search_string = btl.SearchString(input_list)
    return search_string


@pytest.fixture
def search_string_pande_4():
    input_list = ['field:keywords', 'review', 'msm',
                  'and', 'not', 'field:author', 'pande']
    search_string = btl.SearchString(input_list)
    return search_string


@pytest.fixture
def search_string_pande_5():
    input_list = ['field:keywords', 'review',
                  'msm', 'or', 'not', 'field:author', 'pande']
    search_string = btl.SearchString(input_list)
    return search_string


class TestBibFile:

    @pytest.mark.parametrize('search_string, match', [
        (search_string_pande_1(), True),
        (search_string_pande_2(), False),
        (search_string_pande_3(), True),
        (search_string_pande_4(), False),
        (search_string_pande_5(), True)])
    def test_search_string_match(self, bibfile_pande, search_string, match):
        test_match = bibfile_pande.search_string_match(search_string)
        assert test_match == match

    @pytest.mark.parametrize('fields, first_words', [
        (['annote'], ['Review']),
        (['annote', 'title'], ['Everything', 'Review'])])
    def test_get_field(self, bibfile_pande, fields, first_words):
        field_texts = bibfile_pande.get_field_texts(fields)
        test_first_words = [field_text.split()[0]
                            for field_text in field_texts]
        assert test_first_words == first_words


class TestBibliography:

    def test_match_and_print_fields(self):
        pass
