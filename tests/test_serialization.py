# -*- coding: utf-8 -*-

"""
:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import os
from tempfile import mktemp

from pytest import raises

from chatrelater.serialization import save_data, load_data


class LoadSaveContext(object):
    """A context to create a temporary filename and remove the file afterwards."""

    def __init__(self, data):
        self.data = data

    def __enter__(self):
        self.filename = mktemp()
        save_data(self.data, self.filename)
        return self.filename

    def __exit__(self, *exc_info):
        os.unlink(self.filename)


def test_load_save_data():
    """Test saving data and then loading it again.

    Also, KeyErrors are expected if required keys are missing.
    """
    def assert_required_keys(data, should_raise=False):
        with LoadSaveContext(data) as filename:
            if should_raise:
                raises(KeyError, 'load_data(filename)')
            else:
                load_data(filename)

    # Assure that missing keys raise a ``KeyError``.
    required_keys = frozenset(['nicknames', 'relations', 'directed'])
    for key in required_keys:
        keys = set(required_keys)
        keys.remove(key)
        assert_required_keys(dict.fromkeys(keys), True)
    assert_required_keys({'nicknames': None}, True)
    assert_required_keys(dict.fromkeys(required_keys), False)

    # Assure the exact data saved will be loaded afterwards.
    data = {
        'nicknames': 123,
        'relations': 456,
        'directed': True,
    }
    with LoadSaveContext(data) as filename:
        assert load_data(filename) == (123, 456, True)
