#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chat Relater's Visualizer
~~~~~~~~~~~~~~~~~~~~~~~~~

Visualize relations between chat partners.

For graphical output, GraphViz_ will be utilized (has to be installed) and
various formats can be written. Also, the pydot_ Python bindings for it are
needed, which itself require the pyparsing_ library.

.. _GraphViz:   http://www.graphviz.org/
.. _pydot:      http://dkbza.org/pydot.html
.. _Pyparsing:  http://pyparsing.wikispaces.com/

:Copyright: 2007 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from optparse import OptionParser

from pydot import Dot, Node, Edge

from analyze import load_data


def generate_dot(nicknames, relations, directed=False):
    """Create dot graph representations."""
    # Create graph.
    dot = Dot('Relations')
    if directed:
        dot.set_type('digraph')
    else:
        dot.set_type('graph')

    # Create nodes.
    for nick in nicknames:
        dot.add_node(Node(nick, label=nick))

    # Create edges.
    max_count = float(max(rel[2] for rel in relations))
    max_width = 4
    for nick1, nick2, count in sorted(relations, key=lambda x: x[0]):
        width = (count / max_count * max_width) + 1
        dot.add_edge(Edge(nick1, nick2, style='setlinewidth(%d)' % width))

    return dot


def write_file(dot, name, prog, format):
    """Create a graphics file from the DOT data."""
    filename = '%s_%s.%s' % (name, prog, format)
    dot.write(filename, prog, format)
    print "Wrote %s output to '%s' using %s." % (format, filename, prog)


if __name__ == '__main__':
    # Create parser.
    parser = OptionParser(
        usage='usage: %prog [options] <data filename> <output filename prefix>')
    parser.add_option('-f', '--format', dest='format', default='dot',
        choices=(Dot.formats + ['raw']),
        help='output format supported by GraphViz (default: dot)')
    parser.add_option('-p', '--prog', dest='prog', default='dot',
        choices=('dot', 'twopi', 'neato', 'circo', 'fdp'),
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
    dot = generate_dot(nicknames, relations, directed)
    write_file(dot, output_filename, opts.prog, opts.format)
