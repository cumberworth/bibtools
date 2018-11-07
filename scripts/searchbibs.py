#!/usr/env python

"""Search bibliography database with and output given terms."""


def main():
    args = parse_args()
    bibliography = Bibliography(BIB_DIRECTORY)
    search_string = SearchString(args.search_string)
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
            dest='terms',
            help='Terms to print')
    return parser.parse_args()


if __name__ == '__main__':
    main()
