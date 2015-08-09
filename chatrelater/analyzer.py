# -*- coding: utf-8 -*-

"""
chatrelater.analyzer
~~~~~~~~~~~~~~~~~~~~

Analyze (not necessarily only) IRC logfiles and determine relations
between chat users.

So far, only logfiles produced by XChat_ were tested.

For a line to be recognized, it has to start with a nickname in angle
brackets, followed by a space (e. g. `<SomeUser23> hey what's up?`).

Also, users are expected to use the nickname autocompletion feature, so
only exact nicknames with matching case are recognized.

.. _XChat: http://www.xchat.org/

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from .nicknames import clean_nickname, NicknameRegistry


def iter_files(filenames):
    """Yield lines from multiple files."""
    for fn in filenames:
        with open(fn, 'rb') as f:
            for line in f:
                yield line


def parse_logfile(lines):
    """Return a set of nicknames and a list of (nickname, message) tuples
    extracted from the given lines.
    """
    nicknames = set()
    loglines = []

    for nickname, message in parse_log(lines):
        nicknames.add(nickname)
        loglines.append((nickname, message))

    return nicknames, loglines


def parse_log(lines):
    """Select relevant lines and split each of those into a
    (nickname, message) pair.
    """
    for line in lines:
        line = line.decode('utf-8')

        # Skip everything that is not a public (or query) message
        # (joins, parts, modes, notices etc.).
        if not line.startswith('<'):
            continue

        try:
            nickname, message = line[1:].strip().split('> ', 1)
            nickname = clean_nickname(nickname)
            yield nickname, message
        except ValueError:
            pass


def relate_nicknames(nicknames, loglines):
    """Try to figure out relations between users.

    Line beginnings are checked to find textual references between users.
    """
    nickname_registry = NicknameRegistry(nicknames)

    for author_nickname, message in loglines:
        addressed_nickname = message.split(' ', 1)[0].strip(':,.?!@')
        matching_addressed_nickname = nickname_registry.find(addressed_nickname)
        if matching_addressed_nickname:
            yield author_nickname, matching_addressed_nickname


def compress_relations(relations, unify=False):
    """Combine one or more equal (nick1, nick2) tuples into a single
    (nick1, nick2, count) tuple.

    If ``unify`` is true, relations with identic items in different order
    will be put in the same order so they are equal.
    """
    if unify:
        relations = (tuple(sorted(rel)) for rel in relations)

    relations = list(relations)
    for rel in set(relations):
        yield rel[0], rel[1], relations.count(rel)


def analyze(filenames, directed=False, no_unrelated_nicknames=False):
    """Parse logfiles and return nicknames and their determined relations."""
    nicknames, loglines = parse_logfile(iter_files(filenames))
    relations = relate_nicknames(nicknames, loglines)
    relations = list(compress_relations(relations, unify=not directed))

    if no_unrelated_nicknames:
        nicknames = set()
        for rel in relations:
            nicknames.update(rel[:2])

    return nicknames, relations
