#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chat Relater's Visualizer
~~~~~~~~~~~~~~~~~~~~~~~~~

Visualize relations between chat partners.

For graphical output, GraphViz_ will be utilized (has to be installed) and
various formats can be written.

.. _GraphViz:   http://www.graphviz.org/

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser

from graphviz import Digraph, Graph
from graphviz.files import ENGINES, FORMATS

from analyze import load_data


DEFAULT_FORMAT = 'dot'
DEFAULT_PROGRAM = 'dot'


def generate_dot(nicknames, relations, name, format, program, directed=False):
    """Create dot graph representations."""
    # Create graph.
    dot_attrs = {
        'name': name,
        'format': format,
        'engine': program,
    }
    if directed:
        dot = Digraph(**dot_attrs)
    else:
        dot = Graph(**dot_attrs)

    # Create nodes.
    for nickname in nicknames:
        dot.node(nickname, label=nickname)

    # Create edges.
    max_count = float(max(rel[2] for rel in relations))
    max_width = 4
    for nickname1, nickname2, count in sorted(relations, key=lambda x: x[0]):
        width = (count / max_count * max_width) + 1
        dot.edge(nickname1, nickname2, style='setlinewidth(%d)' % width)

    return dot


def write_file(dot):
    """Create a graphics file from the DOT data."""
    rendered_filename = dot.render(filename=dot.name)
    print "Wrote %s output to '%s' using %s." \
        % (dot.format, rendered_filename, dot.engine)



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
