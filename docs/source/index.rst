###
XGI
###

.. image:: ../../logo/logo.svg
  :width: 200

About
=====

The `XGI <https://github.com/ComplexGroupInteractions/xgi>`_ library provides data structures and algorithms for modeling and analyzing
complex systems with group (higher-order) interactions.

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


``XGI`` was developed and tested for Python 3.7-3.10 on Mac OS, Windows, and Ubuntu.


License
=======

This project is licensed under the `BSD 3-Clause License
<https://github.com/ComplexGroupInteractions/xgi/blob/main/LICENSE.md>`_.


Contributing
============

If you want to contribute to this project, please make sure to read the
`code of conduct
<https://github.com/ComplexGroupInteractions/xgi/blob/main/CODE_OF_CONDUCT.md>`_
and the `contributing guidelines
<https://github.com/ComplexGroupInteractions/xgi/blob/main/CONTRIBUTING.md>`_.


Relevant References
===================

`The Why, How, and When of Representations for Complex Systems
<https://doi.org/10.1137/20M1355896>`_, Leo Torres, Ann S. Blevins, Danielle Bassett,
and Tina Eliassi-Rad

`Networks beyond pairwise interactions: Structure and dynamics
<https://doi.org/10.1016/j.physrep.2020.05.004>`_, Federico Battiston, Giulia Cencetti,
Iacopo Iacopini, Vito Latora, Maxime Lucas, Alice Patania, Jean-Gabriel Young, and
Giovanni Petri

`What are higher-order networks? <https://arxiv.org/abs/2104.11329>`_, Christian Bick,
Elizabeth Gross, Heather A. Harrington, Michael T. Schaub


API Reference
=============

.. toctree::
   :maxdepth: 2

   Classes <api/classes/classes.rst>
   Algorithms <api/algorithms/algorithms.rst>
   Generative Models <api/generators/generators.rst>
   Linear Algebra <api/linalg/linalg.rst>
   Read/Write <api/readwrite/readwrite.rst>
   Converting to and from other data formats <api/convert.rst>
   Utilities <api/utils/utils.rst>
