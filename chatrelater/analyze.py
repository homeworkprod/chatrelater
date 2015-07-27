#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chat Relater's Analyzer
~~~~~~~~~~~~~~~~~~~~~~~

Analyze (not necessarily) IRC logfiles and determine relations between
chat users.

So far, only logfiles produced by XChat_ were tested. Also, users are
expected to use the nickname autocompletion feature, so only exact
nicknames with matching case are recognized.

.. _XChat: http://www.xchat.org/

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser
import json
from sys import stdout


# ---------------------------------------------------------------- #
# parsing and analysis

def iter_files(filenames):
    """Yield lines from multiple files."""
    for fn in filenames:
        with open(fn, 'rb') as f:
            for line in f:
                yield line


def parse_logfile(lineiter):
    """Return a set of nicknames and a list of (nickname, message) tuples
    extracted from the given lines.
    """
    nicknames = set()
    loglines = []
    for line in lineiter:
        # Skip everything that is not a public (or query) message
        # (joins, parts, modes, notices etc.).
        if not line.startswith('<'):
            continue

        try:
            nickname, message = line[1:].strip().split('> ', 1)
            nicknames.add(nickname)
            loglines.append((nickname, message))
        except ValueError:
            pass

    return nicknames, loglines


def relate_nicknames(nicknames, loglines):
    """Try to figure out relations between users.

    Line beginnings are checked to find textual references between users.
    """
    for nickname, message in loglines:
        first = message.split(' ', 1)[0].strip(':,.?!')
        if first in nicknames:
            yield nickname, first


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


# ---------------------------------------------------------------- #
# serialization


def save_data(data, filename=None):
    """Export data to file.

    Keyword arguments are attached to the shelve dictionary
    with the keyword names as keys.
    """
    def dump(stream):
        json.dump(data, stream)

    if filename:
        with open(filename, 'wb') as f:
            dump(f)
    else:
        dump(stdout)


def load_data(filename):
    """Import data from file."""
    with open(filename, 'rb') as f:
        d = json.load(f)

    return d['nicknames'], d['relations'], d['directed']


def parse_args():
    """Setup and apply the command line parser."""
    parser = ArgumentParser()

    parser.add_argument(
        '-d', '--directed',
        action='store_true',
        dest='directed',
        help='preserve directed relations instead of unifying them')

    parser.add_argument(
        '-n', '--no-unrelated-nicknames',
        action='store_true',
        dest='no_unrelated_nicknames',
        help='exclude unrelated nicknames to avoid unconnected nodes to be drawn')

    parser.add_argument(
        '-o', '--output-filename',
        dest='output_filename',
        help='save the output to this file (default: write to STDOUT)')

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        help='display the resulting relations')

    parser.add_argument(
        'filenames',
        metavar='FILENAME',
        nargs='+')

    return parser.parse_args()


def main():
    args = parse_args()

    # Analyze data.
    nicknames, relations = analyze(args.filenames, args.directed,
                                   args.no_unrelated_nicknames)

    # Show details.
    if args.verbose:
        connection_template = '%3dx %s <-> %s'
        if args.directed:
            connection_template = connection_template.replace('<', '')
        print
        for rel in sorted(relations, key=lambda x: str.lower(x[0])):
            print connection_template % (rel[2], rel[0], rel[1])
        print
        print 'Found %d nicknames in %d relations.' \
            % (len(nicknames), len(relations))

    # Store result.
    data = {
        'nicknames': list(nicknames),
        'relations': relations,
        'directed': args.directed,
    }
    save_data(data, args.output_filename)


if __name__ == '__main__':
    main()
