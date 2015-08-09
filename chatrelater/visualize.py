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

from __future__ import print_function

from graphviz import Digraph, Graph


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
    print("Wrote %s output to '%s' using %s."
        % (dot.format, rendered_filename, dot.engine))
