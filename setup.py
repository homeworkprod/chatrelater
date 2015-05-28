#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chat Relater's setup script
~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

import chatrelater


author, author_email = chatrelater.__author__[:-1].split(' <')


setup(
    name = 'ChatRelater',
    version = chatrelater.__version__,
    description = 'Analyze and visualize relations between chat users.',
    long_description = chatrelater.__doc__,
    license = chatrelater.__license__,
    author = author,
    author_email = author_email,
    url = chatrelater.__url__,
    packages = find_packages(),
    zip_safe = False,
    include_package_data = True,
    classifiers = [
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: Log Analysis',
    ],
    install_requires = [
        'pydot >= 0.9.10',
        'pyparsing >= 1.4.6',
        'PyYAML >= 3.05',
    ],
    extras_require = {
        'test': ['py >= 0.9.0'],
    },
)
