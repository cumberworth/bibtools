#!/usr/env python

from searchRefs import *
import pytest

For each try various combinations of matching term lists. how?


@pytest.fixture(params=[{
    'input_list': ['field:keywords', 'stuff', 'thing'],
    'field_list': ['keywords'],
    'terms_list':[['stuff', 'thing']],
    }, {
    'input_list': ['not', 'field:keywords', 'stuff', 'thing'],
    'field_list': ['keywords'],
    'terms_list':[['stuff', 'thing']]
    }, {
    'input_list': ['field:keywords', 'stuff', 'thing', 'and', 'field:author', 'pande'],
    'field_list': ['keywords', 'author'],
    'terms_list': [['stuff', 'thing'], ['pande']]
    }, {
    'input_list': ['field:keywords', 'stuff', 'thing', 'or', 'field:author', 'pande'],
    'field_list': ['keywords', 'author'],
    'terms_list': [['stuff', 'thing'], ['pande']]
    }])
def input_expected(request):
    return request.param


@pytest.fixture()
def search_string(input_expected):
    input_list = input_expected['input_list']
    search_string = SearchString(input_list)
    return search_string


@pytest.fixture()
def search_string_expect_fields_and_terms(input_expected):
    input_list = input_expected['input_list']
    search_string = SearchString(input_list)
    field_list = input_expected['field_list']
    terms_list = input_expected['terms_list']
    return search_string, field_list, terms_list

    
class TestSearchString:

    def test__init__(self, search_string):
        pass

    def test__iter__(self, search_string_expect_fields_and_terms):
        search_string = search_string_expect_fields_and_terms[0]
        field_list = search_string_expect_fields_and_terms[1]
        terms_list = search_string_expect_fields_and_terms[2]
        test_field_list = []
        test_terms_list = []
        for field, terms in search_string:
            test_field_list.append(field)
            test_terms_list.append(terms)
        assert test_field_list == field_list
        assert test_terms_list == terms_list

    def test_fields_match(self):
        pass


class TestBibliography:

    def test__init__(self):
        pass

    def test_match_and_print_fields(self):
        pass


class TestBibFile:

    def test__init__(self):
        pass

    def test_search_string_match(self):
        pass

    def test_get_field(self):
        pass
