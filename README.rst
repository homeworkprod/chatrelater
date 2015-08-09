Chat Relater
============

**Chat Relater** is a tool consisting of two command-line scripts:

* The analyzer extracts user relations from chat logs. The gained data
  is serialized as JSON.

* The visualizer takes that data, generates a DOT_ file, and calls the
  GraphViz_ application to render the graph in the requested output
  format (e. g. PDF, PNG, SVG).

It is actually a conceptual clone of the PieSpy_ Social Network Bot.
However, Chat Relater does not act as an IRC bot (although this could be
easily accomplished by making use of the irc_ package), but therefore
allows to be run on any logfiles that produce similar output to those
created by XChat_. Of course, this includes logs from Jabber, SILC or
any other communication (but it might require some minor changes to the
log reader).

The GraphViz_ usage is pretty basic and output may be improved somehow,
but so far, the graphs created by PieSpy_ look **much** nicer.

Python_ 2.7+ or 3.3+ is required.

The required Python packages can be installed via pip:

.. code:: sh

    $ pip install -r requirements.txt

To run tests, install the dependencies once, then run tests with tox:

.. code:: sh

    $ pip install -r requirements-test.txt
    $ tox


.. _DOT:        http://www.graphviz.org/doc/info/lang.html
.. _GraphViz:   http://www.graphviz.org/
.. _PieSpy:     http://www.jibble.org/piespy/
.. _irc:        https://bitbucket.org/jaraco/irc
.. _XChat:      http://www.xchat.org/
.. _Python:     http://www.python.org/


:Copyright: 2007-2015 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 27-Jul-2015
:License: MIT, see LICENSE for details.
:Version: 0.2
