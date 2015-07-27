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

from optparse import OptionParser

from graphviz import Digraph, Graph
from graphviz.files import ENGINES, FORMATS

from analyze import load_data


def generate_dot(nicknames, relations, name, format, engine, directed=False):
    """Create dot graph representations."""
    # Create graph.
    dot_attrs = {
        'name': name,
        'format': format,
        'engine': engine,
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


if __name__ == '__main__':
    # Create parser.
    parser = OptionParser(
        usage='usage: %prog [options] <data filename> <output filename prefix>')
    parser.add_option('-f', '--format', dest='format', default='dot',
        choices=sorted(FORMATS),
        help='output format supported by GraphViz (default: dot)')
    parser.add_option('-p', '--prog', dest='prog', default='dot',
        choices=sorted(ENGINES),
        help='GraphViz program to create output with (default: dot)')

    # Parse command-line input.
    opts, args = parser.parse_args()
    try:
        input_filename, output_filename = args
    except ValueError:
        parser.print_help()
        parser.exit()

    # Draw graphs.
    nicknames, relations, directed = load_data(input_filename)
    dot = generate_dot(nicknames, relations, output_filename, opts.format,
                       engine=opts.prog, directed=directed)
    write_file(dot)
