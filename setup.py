import glob
from setuptools import setup

setup(
    name='mybiblib',
    packages=['mybiblib'],
    scripts=glob.glob('scripts/*.py'),
    install_requires=['biblib']
)
