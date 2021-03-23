import multiprocessing
from setuptools import setup, find_packages
from setuptools.command.test import test as setup_test
import os
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "discrete_differentiator",
    version = "0.1",
    test_suite='nose2.collector.collector',
    # Dependencies on other packages:
    # Couldn't get numpy install to work without
    # an out-of-band: sudo apt-get install python-dev
    setup_requires   = ['pytest-runner'],
    install_requires = [
                        'nose2>=0.9.2',     # For testing
                        ],

    tests_require    =[
                       'testfixtures>=6.14.1',
                       ],

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "differentiate pointwise",
    long_description_content_type = "text/markdown",
    long_description = long_description,
    license = "BSD",
    url = "https://github.com/paepcke/discrete_differentiator.git"
)

print("To run tests, type 'nose2'")
