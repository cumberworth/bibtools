# bibtools

A set of tools for processing a reference database composed of bib files.

The package is built around the [bib file parser](https://github.com/aclements/biblib) of aclements.
Scripts are included for three common tasks: parsing downloaded bib files, searching the database, and creating project specific bibliographies.
A csv file with journal name abbreviations has been [included](bibtools/data/cassi-abbreviations.csv).
This was manually created for journals I have referred to using the [CAS Source Index (CASSI) Search Tool](https://cassi.cas.org/search.jsp).
To add an entry, enter the full journal name, a semicolon as a delimiter, and the abbreviated name.

## Installation

The location of the directory that the bib file data base is located must first be specified.
This is done by changing the `BIB_DIRECTORY` variable in [bibtools/bib.py](bibtools/byb.py).
Then run
```
python setup.py install --user
```
