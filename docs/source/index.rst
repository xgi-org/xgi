
.. image:: ../../logo/logo.svg
  :width: 200

.. toctree::
   :maxdepth: 1
   :hidden:

   installing
   user_guides
   reference
   xgi-data
   gallery
   contribute
   about_us


About
=====

The Comple\ **X** **G**\ roup **I**\ nteractions `(XGI) <https://github.com/xgi-org/xgi>`_
library provides data structures and algorithms for modeling, analyzing, and visualizing complex systems
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
mind. Browse the `list of projects Using XGI <using-xgi.html>`_ to get an idea.
We thank all our great `contributors <contributors.html>`_! 

Sign up for our `mailing list <http://eepurl.com/igE6ez>`_ and follow XGI on `Twitter <https://twitter.com/xginets>`_ or `Mastodon <https://mathstodon.xyz/@xginets>`_!



Corresponding Data
==================

A number of higher-order datasets are available in the `XGI-DATA repository <https://github.com/xgi-org/xgi-data>`_ and can be easily accessed with the ``load_xgi_data()`` function.



How to Cite
===========
We acknowledge the importance of good software to support research, and we note
that research becomes more valuable when it is communicated effectively. To
demonstrate the value of XGI, we ask that you cite the XGI
`paper <https://doi.org/10.21105/joss.05162>`_ in your work.
You can cite XGI either by going to our repository page
`repository page <https://github.com/xgi-org/xgi>`_ and
clicking the "cite this repository" button on the right sidebar (which will generate
a citation in your preferred format) or by copying the following BibTeX entry:

.. code:: text

  @article{Landry_XGI_2023,
  author = {Landry, Nicholas W. and Lucas, Maxime and Iacopini, Iacopo and Petri, Giovanni and Schwarze, Alice and Patania, Alice and Torres, Leo},
  title = {{XGI: A Python package for higher-order interaction networks}},
  doi = {10.21105/joss.05162},
  journal = {Journal of Open Source Software},
  publisher = {The Open Journal},
  year = {2023},
  month = may,
  volume = {8},
  number = {85},
  pages = {5162},
  url = {https://doi.org/10.21105/joss.05162},
  }


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

Copyright (C) 2021-2024 XGI Developers
