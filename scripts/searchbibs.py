#!/usr/env python

#import pyximport
#pyximport.install()

from searchRefs_cython import *

def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-s', type=str, nargs='+', dest='search_string', help='Search string')
    argument_parser.add_argument('-t', type=str, nargs='+', dest='terms', help='Terms to print')
    arguments = argument_parser.parse_args()

    bibliography = Bibliography(BIB_DIRECTORY)
    search_string = SearchString(arguments.search_string)
    bibliography.match_and_print_fields(search_string, arguments.terms)


if __name__ == '__main__':
    main()
