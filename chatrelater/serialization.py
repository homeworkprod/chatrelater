# -*- coding: utf-8 -*-

"""
chatrelater.serialization
~~~~~~~~~~~~~~~~~~~~~~~~~

Serialization of chat log analysis results as JSON.

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import json
import sys


def save_data(data, filename=None):
    """Export data to file.

    Keyword arguments are attached to the shelve dictionary
    with the keyword names as keys.
    """
    def dump(stream):
        json.dump(data, stream)

    if filename:
        with open(filename, 'w') as f:
            dump(f)
    else:
        dump(sys.stdout)


def load_data(filename):
    """Import data from file."""
    with open(filename, 'r') as f:
        d = json.load(f)

    return d['nicknames'], d['relations'], d['directed']
