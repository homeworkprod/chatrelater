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

:date: 2007-07-05
:copyright: 2007 Jochen Kupperschmidt
:license: MIT, see LICENSE for details.
"""

from __future__ import with_statement
from optparse import OptionParser
from sys import stdout

import yaml


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
        yaml.safe_dump(data, stream)

    if filename:
        with open(filename, 'wb') as f:
            dump(f)
    else:
        dump(stdout)

def load_data(filename):
    """Import data from file."""
    with open(filename, 'rb') as f:
        d = yaml.safe_load(f)
        return d['nicknames'], d['relations'], d['directed']

def main():
    # Create parser.
    parser = OptionParser(
        usage='usage: %prog [options] <filename1> [filename2] ...')
    parser.add_option('-d', '--directed', action='store_true', dest='directed',
        help='preserve directed relations instead of unifying them')
    parser.add_option('-n', '--no-unrelated-nicknames', action='store_true',
        dest='no_unrelated_nicknames',
        help='exclude unrelated nicknames to avoid unconnected nodes to be drawn')
    parser.add_option('-o', '--output-filename', dest='output_filename',
        help='save the output to FILE (default: print to stdout)', metavar='FILE')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
        help='display the resulting relations')

    # Parse input.
    opts, args = parser.parse_args()
    if not args:
        parser.print_help()
        parser.exit()

    # Analyze data.
    nicknames, relations = analyze(args, opts.directed,
        opts.no_unrelated_nicknames)

    # Show details.
    if opts.verbose:
        format = '%3dx %s <-> %s'
        if opts.directed:
            format = format.replace('<', '')
        print
        for rel in sorted(relations, key=lambda x: str.lower(x[0])):
            print format % (rel[2], rel[0], rel[1])
        print
        print 'Found %d nicknames in %d relations.' \
            % (len(nicknames), len(relations))

    # Store result.
    data = dict(nicknames=nicknames, relations=relations,
        directed=bool(opts.directed))
    save_data(data, opts.output_filename)


if __name__ == '__main__':
    main()
