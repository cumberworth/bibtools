#!/usr/bin/env python3

"""Parse bib files and output in standard format

Currently this only works on article and misc class bib files. It will add two new
fields: annote and keywords. The filename extension should not be included.
To change the file in place, run

echo "$(parseBib.py [filename])" > [filename].bib
"""

# For now assumes bib file is article

import argparse


FIELDS = {
    "article": [
        "title",
        "author",
        "journal",
        "volume",
        "number",
        "pages",
        "year",
        "issn",
        "doi",
        "url",
        "abstract",
    ]
}


def main():
    args = parse_args()
    filename = args.filename

    with open(filename) as inp:
        lines = inp.readlines()

    entry_type, field_dic = parse_lines(lines)
    output_standard_bib(filename, entry_type, field_dic)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("filename", help="Filename of bib file")

    return parser.parse_args()


def parse_lines(lines):
    field_dic = {}
    merged_line = ""
    entry_type = None
    for line in lines:

        # Will create this from scratch
        if "@" in line:
            if "article" in line:
                entry_type = "article"
            elif "misc" in line:
                entry_type = "misc"
            else:
                print("Entry type not implemented")
                raise
            continue

        # Remove white space and line break
        line = line.strip()

        # Check if start of an entry
        if "=" in line and len(line.split("=")[0].split()) == 1:
            find_entry(merged_line, entry_type, field_dic)
            merged_line = line
        else:
            merged_line = merged_line + " " + line
    else:
        find_entry(merged_line, entry_type, field_dic)

    return entry_type, field_dic


def find_entry(line, entry_type, field_dic):
    if "=" not in line:
        return field_dic

    split_line = line.split("=")
    field = split_line[0].rstrip().lower()
    entry = "".join(split_line[1:])
    if entry_type == "misc" or field in FIELDS[entry_type]:

        # Remove enclosing characters, the comma on the right, and any space
        entry = entry.lstrip()[1:].lstrip()

        while entry[-1] in [" ", "\n", ",", '"', "}"]:
            entry = entry.rstrip()[:-1]

        field_dic[field] = entry

    return field_dic


def output_standard_bib(filename, entry_type, field_dic):
    filebase = filename.split(".")[0]
    print(f"@{entry_type}{{{filebase},")
    for field, entry in field_dic.items():
        print(f"    {field} = {{{entry}}},")

    print("    keywords = {},")
    print("    annote = {}")
    print("}")


if __name__ == "__main__":
    main()
