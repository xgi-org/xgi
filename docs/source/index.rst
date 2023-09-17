
.. image:: ../../logo/logo.svg
  :width: 200

.. toctree::
   :maxdepth: 2
   :caption: Home
   :hidden:

   about
   contributors
   higher-order
   gallery
   using-xgi

.. toctree::
   :maxdepth: 2
   :caption: Tutorials
   :hidden:

   See on GitHub <https://github.com/xgi-org/xgi/tree/main/tutorials>

.. toctree::
   :maxdepth: 2
   :caption: Quick reference links
   :hidden:

   Hypergraph class <api/core/xgi.core.hypergraph.Hypergraph.rst>
   Simplicial Complex class <api/core/xgi.core.simplicialcomplex.SimplicialComplex.rst>
   Directed Hypergraph class <api/core/xgi.core.dihypergraph.DiHypergraph>

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   :hidden:

   Core functionality <api/core.rst>
   Node and edge statistics <api/stats.rst>
   Algorithms <api/algorithms.rst>
   Generative Models <api/generators.rst>
   Linear Algebra <api/linalg.rst>
   Read/Write <api/readwrite.rst>
   Dynamics <api/dynamics.rst>
   Drawing <api/drawing.rst>
   Converting to and from other data formats <api/convert.rst>
   Utilities <api/utils.rst>


About
=====

The Comple\ **X** **G**\ roup **I**\ nteractions `(XGI) <https://github.com/xgi-org/xgi>`_
library provides data structures and algorithms for modeling and analyzing complex systems
with group (higher-order) interactions. For more information about what higher-order
interactions are, see a `brief overview <higher-order.html>`_.

Many datasets can be represented as graphs, where pairs of entities (or nodes) are
related via links (or edges).  Examples are road networks, energy grids, social
networks, neural networks, etc.  However, in many other datasets, more than two entities
can be related at a time.  For example, many scientists (entities) can collaborate on a
scientific article together (links), and multiple email accounts (entities) can all
participate on the same email thread (links).  In this latter case, graphs no longer
present a viable alternative to represent such datasets.  It is for this kind of
datasets, where the interactions are given among groups of more than two entities (also
called higher-order interactions), that XGI was designed for.

XGI is implemented in pure Python and is designed to seamlessly interoperate with the
rest of the Python scientific stack (numpy, scipy, pandas, matplotlib, etc).  XGI is
designed and developed by network scientists with the needs of network scientists in
mind.

- Repository: https://github.com/xgi-org/xgi
- PyPI: `latest release <https://pypi.org/project/xgi/>`_
- Twitter: `@xginets <https://twitter.com/xginets>`_
- Contributors: `list <contributors.html>`_
- Projects using XGI: `list <using-xgi.html>`_

Sign up for our `mailing list <http://eepurl.com/igE6ez>`_ and follow XGI on `Twitter <https://twitter.com/xginets>`_ or `Mastodon <https://mathstodon.xyz/@xginets>`_!


Installation
============

To install and use XGI as an end user, execute

.. code:: bash

   pip install xgi

To install for development purposes, first clone the repository and then execute

.. code:: bash

   pip install -e .['all']

If that command does not work, you may try the following instead

.. code:: zsh

   pip install -e .\[all\]

XGI was developed and tested for Python 3.8-3.11 on Mac OS, Windows, and Ubuntu.


Corresponding Data
==================

A number of higher-order datasets are available in the `XGI-DATA repository <https://gitlab.com/complexgroupinteractions/xgi-data>`_ and can be easily accessed with the ``load_xgi_data()`` function.


Contributing
============

If you want to contribute to this project, please make sure to read the
`contributing guidelines <HOW_TO_CONTRIBUTE.md>`_.
We expect respectful and kind interactions by all contributors and users
as laid out in our `code of conduct <CODE_OF_CONDUCT.md>`_.

The XGI community always welcomes contributions, no matter how small.
We're happy to help troubleshoot XGI issues you run into,
assist you if you would like to add functionality or fixes to the codebase,
or answer any questions you may have.

Some concrete ways that you can get involved:

* **Get XGI updates** by following the XGI `Twitter <https://twitter.com/xginets>`_ account, signing up for our `mailing list <http://eepurl.com/igE6ez>`_, or starring this repository.
* **Spread the word** when you use XGI by sharing with your colleagues and friends.
* **Request a new feature or report a bug** by raising a `new issue <https://github.com/xgi-org/xgi/issues/new>`_.
* **Create a Pull Request (PR)** to address an `open issue <../../issues>`_ or add a feature.
* **Join our Zulip channel** to be a part of the `daily goings-on of XGI <https://xgi.zulipchat.com/join/7agfwo7dh7jo56ppnk5kc23r/>`_.

How to Cite
===========
We acknowledge the importance of good software to support research, and we note
that research becomes more valuable when it is communicated effectively. To
demonstrate the value of XGI, we ask that you cite XGI in your work.
Currently, the best way to cite XGI is to go to our
`repository page <https://github.com/xgi-org/xgi>`_ and
click the "cite this repository" button on the right sidebar. This will generate
a citation in your preferred format, and will also integrate well with citation managers.

Academic References
===================

* `The Why, How, and When of Representations for Complex Systems
  <https://doi.org/10.1137/20M1355896>`_, Leo Torres, Ann S. Blevins, Danielle Bassett,
  and Tina Eliassi-Rad.

* `Networks beyond pairwise interactions: Structure and dynamics
  <https://doi.org/10.1016/j.physrep.2020.05.004>`_, Federico Battiston, Giulia
  Cencetti, Iacopo Iacopini, Vito Latora, Maxime Lucas, Alice Patania, Jean-Gabriel
  Young, and Giovanni Petri.

* `What are higher-order networks? <https://arxiv.org/abs/2104.11329>`_, Christian Bick,
  Elizabeth Gross, Heather A. Harrington, Michael T. Schaub.

* `From networks to optimal higher-order models of complex systems
  <https://www.nature.com/articles/s41567-019-0459-y>`_, Renaud Lambiotte, Martin
  Rosvall, and Ingo Scholtes.


Funding
=======

The XGI package has been supported by NSF Grant 2121905,
`HNDS-I: Using Hypergraphs to Study Spreading Processes in Complex Social Networks <https://www.nsf.gov/awardsearch/showAward?AWD_ID=2121905>`_.


License
=======

This project is licensed under the `BSD 3-Clause License
<https://github.com/xgi-org/xgi/blob/main/LICENSE.md>`_.

Copyright (C) 2021-2023 XGI Developers
