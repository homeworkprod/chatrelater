#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for Chat Relater's Analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run with pytest_.

.. _pytest: http://pytest.org/

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import os
from tempfile import mktemp

import pytest
from pytest import raises

from chatrelater.analyze import parse_logfile, clean_nickname, \
    relate_nicknames, compress_relations, save_data, load_data


def test_parse_logfile():
    lines = [
        b'<John> one two',
        b'* some action',
        b'<Jane> threefourfive',
        b'Someone- A message from someone!',
        b'<Mary> foobar',
    ]

    expected_nicknames = {'John', 'Jane', 'Mary'}

    expected_loglines = [
        ('John', 'one two'),
        ('Jane', 'threefourfive'),
        ('Mary', 'foobar'),
    ]

    assert parse_logfile(lines) == (expected_nicknames, expected_loglines)


@pytest.mark.parametrize('input, expected', [
  ('@oper',   'oper'   ),
  ('%halfop', 'halfop' ),
  ('+voice',  'voice'  ),
  ('nothing', 'nothing'),
])
def test_clean_nickname(input, expected):
    assert clean_nickname(input) == expected


def test_relate_nicknames():
    nicknames = {'John', 'Jane', 'Mary'}

    loglines = [
        ('John', 'heyho'),
        ('John', 'Jane, sup?'),
        ('Jane', 'John: I am fine, thanks'),
        ('Mary', 'John?'),
        ('Mary', 'John!'),
        ('Jane', 'John seems to have disappeared...'),
    ]

    expected_relations = [
        ('John', 'Jane'),
        ('Jane', 'John'),
        ('Mary', 'John'),
        ('Mary', 'John'),
        ('Jane', 'John'),
    ]

    result = list(relate_nicknames(nicknames, loglines))
    assert result == expected_relations


def test_compress_relations():
    relations = [
        ('one',  'two'  ),
        ('one',  'three'),
        ('two',  'one'  ),
        ('one',  'three'),
        ('three', 'one' ),
    ]

    expected_compressed = {
        ('one',   'two',   1),
        ('one',   'three', 2),
        ('two',   'one',   1),
        ('three', 'one',   1),
    }

    expected_compressed_unified = {
        ('one',   'two',   2),
        ('one',   'three', 3),
    }

    assert set(compress_relations(relations, False)) == expected_compressed
    assert set(compress_relations(relations, True)) == expected_compressed_unified


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
