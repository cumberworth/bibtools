import glob
from setuptools import setup

setup(
    name='bibtools',
    packages=['bibtools'],
    scripts=glob.glob('scripts/*.py'),
    install_requires=['biblib']
)
