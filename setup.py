import glob
from setuptools import setup

setup(
    name='bibtools',
    packages=['bibtools'],
    scripts=glob.glob('scripts/*.py'),
    package_data={'bibtools': ['data/cassi-abbreviations.csv']},
    install_requires=['biblib']
)
