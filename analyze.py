#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chat Relater's Analyzer
~~~~~~~~~~~~~~~~~~~~~~~

Analyze (not necessarily) IRC logfiles and determine relations between
chat users.

So far, only logfiles produced by XChat_ were tested.

For a line to be recognized, it has to start with a nickname in angle
brackets, followed by a space (e. g. `<SomeUser23> hey what's up?`).

Also, users are expected to use the nickname autocompletion feature, so
only exact nicknames with matching case are recognized.

.. _XChat: http://www.xchat.org/

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import print_function
from argparse import ArgumentParser

from chatrelater.analyzer import analyze
from chatrelater.serialization import save_data


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
        print()
        for rel in sorted(relations, key=lambda x: str.lower(x[0])):
            print(connection_template % (rel[2], rel[0], rel[1]))
        print()
        print('Found %d nicknames in %d relations.'
            % (len(nicknames), len(relations)))

    # Store result.
    data = {
        'nicknames': list(nicknames),
        'relations': relations,
        'directed': args.directed,
    }
    save_data(data, args.output_filename)


if __name__ == '__main__':
    main()
