#/usr/env python

import cProfile
import pstats
import searchRefs
import pyximport
pyximport.install()
import searchRefs_cython
import sys

# Command line arguments
input_string = ['field:keywords', 'review']
terms = ['title']

# Setup objects
bibliography = searchRefs.Bibliography(searchRefs.BIB_DIRECTORY)
bibliography_cython = searchRefs_cython.Bibliography(searchRefs_cython.BIB_DIRECTORY)
search_string = searchRefs.SearchString(input_string)
search_string_cython = searchRefs_cython.SearchString(input_string)
command_string = 'bibliography.match_and_print_fields(search_string, terms)'
command_string_cython = 'bibliography_cython.match_and_print_fields(search_string_cython, terms)'

# Profile
profile_file = 'python_profile.stats'
profile_file_cython = 'cython_profile.stats'
output_dump = '/tmp/searcRefs.txt'
sys.stdout = open(output_dump, 'w')
cProfile.run(command_string, profile_file)
cProfile.run(command_string_cython, profile_file_cython)

# Customize and write statistics
stats_output = 'python_profile.txt'
sys.stdout = open(stats_output, 'w')
python_profile_stats = pstats.Stats(profile_file)
python_profile_stats.strip_dirs()
python_profile_stats.sort_stats('cumtime')
python_profile_stats.print_stats()
