# -*- coding: utf-8 -*-

"""
:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from chatrelater.nicknames import clean_nickname


@pytest.mark.parametrize('input, expected', [
  ('@oper',   'oper'   ),
  ('%halfop', 'halfop' ),
  ('+voice',  'voice'  ),
  ('nothing', 'nothing'),
])
def test_clean_nickname(input, expected):
    assert clean_nickname(input) == expected
