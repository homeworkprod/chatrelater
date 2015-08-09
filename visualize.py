#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chat Relater's Visualizer
~~~~~~~~~~~~~~~~~~~~~~~~~

Visualize relations between chat partners using GraphViz_ (has to be
installed).

.. _GraphViz:   http://www.graphviz.org/

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser

from graphviz.files import ENGINES, FORMATS

from chatrelater.serialization import load_data
from chatrelater.visualization import DEFAULT_FORMAT, DEFAULT_PROGRAM, \
    generate_dot, write_file


def parse_args():
    """Setup and apply the command line parser."""
    parser = ArgumentParser()

    parser.add_argument(
        '-f', '--format',
        dest='format',
        default=DEFAULT_FORMAT,
        choices=sorted(FORMATS),
        help='output format supported by GraphViz (default: {})'.format(DEFAULT_FORMAT))

    parser.add_argument(
        '-p', '--program',
        dest='program',
        default=DEFAULT_PROGRAM,
        choices=sorted(ENGINES),
        help='GraphViz program to create output with (default: {})'.format(DEFAULT_PROGRAM))

    parser.add_argument(
        'input_filename',
        metavar='INPUT_FILENAME')

    parser.add_argument(
        'output_filename_prefix',
        metavar='OUTPUT_FILENAME_PREFIX')

    return parser.parse_args()


def main():
    args = parse_args()

    nicknames, relations, directed = load_data(args.input_filename)

    dot = generate_dot(nicknames, relations, args.output_filename_prefix,
                       args.format, program=args.program, directed=directed)

    write_file(dot)


if __name__ == '__main__':
    main()
