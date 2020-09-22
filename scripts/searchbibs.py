#!/usr/env python

"""Search bibliography database with and output given terms."""


import argparse

import bibtools.bib as btl


BIB_DIRECTORY = '/home/alexc/refs/bibs/'


def main():
    args = parse_args()
    bibliography = btl.Bibliography(BIB_DIRECTORY)
    search_string = btl.SearchString(args.search_string)
    bibliography.match_and_print_fields(search_string, args.terms)


def parse_args():
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
        default=['title', 'year', 'author', 'annote'],
        dest='terms',
        help='Terms to print')

    return parser.parse_args()


if __name__ == '__main__':
    main()
