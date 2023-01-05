
.. image:: ../../logo/logo.svg
  :width: 200

.. toctree::
   :maxdepth: 2
   :caption: Home
   :hidden:

   about

.. toctree::
   :maxdepth: 2
   :caption: Tutorials
   :hidden:

   See on GitHub <https://github.com/ComplexGroupInteractions/xgi/tree/main/tutorials>

.. toctree::
   :maxdepth: 2
   :caption: Quick reference links
   :hidden:

   Hypergraph class <api/classes/xgi.classes.hypergraph.Hypergraph.rst>
   Simplicial Complex class <api/classes/xgi.classes.simplicialcomplex.SimplicialComplex.rst>

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   :hidden:

   Core classes <api/classes.rst>
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

The Comple\ **X** **G**\ roup **I**\ nteractions `(XGI) <https://github.com/ComplexGroupInteractions/xgi>`_
library provides data structures and algorithms for modeling and analyzing complex systems
with group (higher-order) interactions.

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

- Repository: https://github.com/ComplexGroupInteractions/xgi
- PyPI: https://pypi.org/project/xgi/
- Documentation: https://xgi.readthedocs.io/

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

XGI was developed and tested for Python 3.7-3.11 on Mac OS, Windows, and Ubuntu.

Corresponding Data
==================

A number of higher-order datasets are available in the `XGI-DATA repository <https://gitlab.com/complexgroupinteractions/xgi-data>`_ and can be easily accessed with the ``load_xgi_data()`` function.


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


Contributing
============

If you want to contribute to this project, please make sure to read the
`code of conduct
<https://github.com/ComplexGroupInteractions/xgi/blob/main/CODE_OF_CONDUCT.md>`_
and the `contributing guidelines
<https://github.com/ComplexGroupInteractions/xgi/blob/main/CONTRIBUTING.md>`_.

The best way to contribute to XGI is by submitting a bug or request a new feature by
opening a `new issue <https://github.com/ComplexGroupInteractions/xgi/issues/new>`_.

To get more actively involved, you are invited to browse the `issues page
<https://github.com/ComplexGroupInteractions/xgi/issues>`_ and choose one that you can
work on.  The core developers will be happy to help you understand the codebase and any
other doubts you may have while working on your contribution.

If you are interested in the daily goings-on of XGI, you are invited to join our `Zulip
channel <https://xgi.zulipchat.com/join/7agfwo7dh7jo56ppnk5kc23r/>`_.


Contributors
============

The core XGI team members:

* Nicholas Landry
* Leo Torres
* Maxime Lucas
* Iacopo Iacopini
* Giovanni Petri
* Alice Patania
* Alice Schwarze

Other contributors:

* Martina Contisciani
* Tim LaRock
* Sabina Adhikari
* Marco Nurisso

Funding
=======

The XGI package has been supported by NSF Grant 2121905,
`HNDS-I: Using Hypergraphs to Study Spreading Processes in Complex Social Networks <https://www.nsf.gov/awardsearch/showAward?AWD_ID=2121905>`_.


License
=======

This project is licensed under the `BSD 3-Clause License
<https://github.com/ComplexGroupInteractions/xgi/blob/main/LICENSE.md>`_.

Copyright (C) 2021 XGI Developers
