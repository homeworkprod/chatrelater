# -*- coding: utf-8 -*-

"""
Chat Relater
~~~~~~~~~~~~

Chat Relater is a tool consisting of two command-line scripts:

* The analyzer extracts user relations from chat logs. The gained data is
  serialized as YAML.
* The visualizer takes that data and utilizes GraphViz_ to create a graph.

It is actually a conceptual clone of the PieSpy_ Social Network Bot. However,
Chat Relater does not act as an IRC bot (although this could be easily
accomplished by making use of the irclib_ package), but therefore allows to
be run on any logfiles that produce similar output to those created by
XChat_. Of course, this includes logs from Jabber, SILC or any other
communication (but it might require some minor changes to the log reader).

The GraphViz usage is pretty basic and output may be improved somehow, but
so far, the graphs created by PieSpy look **much** nicer.

Python_ 2.5 or higher is required. Required Python packages are declared in
the setup script.

.. _GraphViz:   http://www.graphviz.org/
.. _YAML:       http://yaml.org/spec/current.html
.. _PieSpy:     http://www.jibble.org/piespy/
.. _irclib:     http://python-irclib.sourceforge.net/
.. _XChat:      http://www.xchat.org/
.. _Python:     http://www.python.org/

:date: 2007-07-05
:copyright: 2007 Jochen Kupperschmidt
:license: MIT, see LICENSE for details.
"""
