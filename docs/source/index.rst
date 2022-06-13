
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
   Converting to and from other data formats <api/convert.rst>
   Utilities <api/utils.rst>


About
=====

The Comple\ **X** **G**\ roup **I**\ nteractions `(XGI) <https://github.com/ComplexGroupInteractions/xgi>`_
library provides data structures and algorithms for modeling and analyzing complex systems
with group (higher-order) interactions.

- Repository: https://github.com/ComplexGroupInteractions/xgi
- PyPI: https://pypi.org/project/xgi/
- Documentation: https://xgi.readthedocs.io/


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

XGI was developed and tested for Python 3.7-3.10 on Mac OS, Windows, and Ubuntu.


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

Other contributors:

* Tim LaRock


License
=======

This project is licensed under the `BSD 3-Clause License
<https://github.com/ComplexGroupInteractions/xgi/blob/main/LICENSE.md>`_.

Copyright (C) 2021 XGI Developers
