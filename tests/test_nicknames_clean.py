# -*- coding: utf-8 -*-

"""
:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from chatrelater.nicknames import clean_nickname


@pytest.mark.parametrize('dirty_nickname, expected', [
  ('@oper',   'oper'   ),
  ('%halfop', 'halfop' ),
  ('+voice',  'voice'  ),
  ('nothing', 'nothing'),
])
def test_clean_nickname(dirty_nickname, expected):
    assert clean_nickname(dirty_nickname) == expected
