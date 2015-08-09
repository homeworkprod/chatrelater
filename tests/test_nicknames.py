# -*- coding: utf-8 -*-

"""
:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from chatrelater.nicknames import NicknameRegistry


@pytest.mark.parametrize('search, expected', [
  ('TheDude1', 'TheDude1'),
  ('thedude1', 'TheDude1'),
  ('THEDUDE1', 'TheDude1'),
  ('monster',  'MONSTER' ),
  ('MIMI',     'mimi'    ),
  ('MiMi',     'mimi'    ),
  ('0z3l0t',   '0Z3l0t'  ),
  ('0Z3L0T',   '0Z3l0t'  ),
])
def test_nickname_registry(search, expected):
    nicknames = {'TheDude1', 'MONSTER', 'mimi', '0Z3l0t'}

    registry = NicknameRegistry(nicknames)

    assert registry.find(search) == expected
