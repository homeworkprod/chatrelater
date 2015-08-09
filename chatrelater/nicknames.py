# -*- coding: utf-8 -*-

"""
chatrelater.nicknames
~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""


class NicknameRegistry(object):

    def __init__(self, nicknames):
        self.nicknames = frozenset(nicknames)
        self._case_insensitive_index = \
            {remove_case(nickname): nickname for nickname in nicknames}

    def find(self, nickname):
        """Try to case-insensitively match the nickname and return the
        original spelling (or `None` if not matching).
        """
        return self._case_insensitive_index.get(remove_case(nickname))


def remove_case(nickname):
    return nickname.lower()
