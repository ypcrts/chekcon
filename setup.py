#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' setup for checkcon '''

import os
from setuptools import setup, find_packages

from checkcon import PACKAGE_NAME, VERSION

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()
    fh.close()

with open(os.path.join(HERE, 'requirements.txt'), encoding="utf-8") as fh:
    REQUIREMENTS = fh.read().splitlines()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(exclude=['tests', 'tests.*']),
    description='microservice port checker store results in redis',
    long_description=LONG_DESCRIPTION,
    author='Daniel Goeke',
    author_email='dgo+checkcon@stderror.net',
    url='https://github.com/dgo-/chekcon',
    license='GPLv3',
    install_requires=REQUIREMENTS,
    python_requires='>=3.7.*',
    entry_points={'console_scripts': [
        'checkcon=checkcon.cmd:checkcon'
        ]},
)
