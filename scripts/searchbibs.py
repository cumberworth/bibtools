#!/usr/env python

"""Search bibliography database.

The search string takes the format of field:[field name] followed by a list of
terms to search for in that field. The implied boolean operator between these
terms is "and". To use other boolean operators with the same field, the
field:[field name] must be repeated after the operator. More generally, the
boolean operators "and", "or", and "not" can be placed before the field
specifier. The "and" operator is again the default between field specifiers.
The same field names are used to specify the desired output.

Example:

searchbibs.py -s field:keywords anillin and not field:keywords review -t title year author keywords

"""


import argparse

import bibtools.bib as btl


def main():
    args = parse_args()
    bibliography = btl.Bibliography(btl.BIB_DIRECTORY)
    search_string = btl.SearchString(args.search_string)
    bibliography.match_and_print_fields(search_string, args.terms)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-s", type=str, nargs="+", dest="search_string", help="Search string"
    )
    parser.add_argument(
        "-t",
        type=str,
        nargs="+",
        default=["title", "year", "author", "annote"],
        dest="terms",
        help="Terms to print",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
