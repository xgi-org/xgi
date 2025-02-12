
.. image:: ../../logo/logo.png
  :class: only-light
  :width: 200

.. image:: ../../logo/logo_white.png
  :class: only-dark
  :width: 200

.. toctree::
   :maxdepth: 1
   :hidden:

   installing
   user_guides
   api_reference
   xgi-data
   auto_examples/index
   contribute
   using-xgi

|release_announcement|

Software for higher-order networks
==================================

The Comple\ **X** **G**\ roup **I**\ nteractions `(XGI) <https://github.com/xgi-org/xgi>`_
library provides data structures and algorithms for modeling, analyzing, and visualizing complex systems
with group (higher-order) interactions. It provides tools to:

* load and store higher-order networks in standard formats
* generate many random and non-random higher-order networks from models
* analyze the structure of higher-order networks with metrics and algorithms
* compute nodes and edge statistics in a unified interface
* draw higher-order networks
* manipulate hypergraphs (undirected and directed) and simplicial complexes


Higher-order networks generalize standard (pairwise) networks by allowing to encode higher-order interactions, 
that is, interactions between any number of entities. Collaborations and contagion processes are typical
examples where these higher-order interactions are crucial.
For more information about what higher-order
interactions are, see a `brief overview <higher-order.html>`_.

XGI is implemented in pure Python and is designed to seamlessly interoperate with the
rest of the Python scientific stack (numpy, scipy, pandas, matplotlib, etc).  XGI is
designed and developed by network scientists with the needs of network scientists in
mind. Browse the `list of projects using XGI <using-xgi.html>`_ to get an idea of what XGI can do and how it is being used by other people.

Get started immediately by `installing XGI <installing.html>`_ and checking the `XGI in 1 minute <api/tutorials/getting_started_1.html>`_ tutorial.


Corresponding Data
==================

A number of higher-order datasets are available in the `XGI-DATA repository <https://github.com/xgi-org/xgi-data>`_ and can be easily accessed with the ``load_xgi_data()`` function.
More information about the datasets and how to load them is in the `XGI-DATA menu <xgi-data.html>`_.


Get involved
============

To simply getting news and updates, you can sign up for our `mailing list <http://eepurl.com/igE6ez>`_ and follow XGI on `Twitter <https://twitter.com/xginets>`_!

If you want to contribute, even better! The XGI community always welcomes contributions, no matter how small.
For more information, see our `contribution guide <contribute.html>`_.



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
  <https://doi.org/10.1137/20M1355896>`_, Torres, L., Blevins, A.S., Bassett, D. and Eliassi-Rad, T., 2021. SIAM Review, 63(3), pp.435-485.

* `Networks beyond pairwise interactions: Structure and dynamics
  <https://doi.org/10.1016/j.physrep.2020.05.004>`_, Battiston, F., Cencetti, G., Iacopini, I., Latora, V., Lucas, M., Patania, A., Young, J.G. and Petri, G., 2020. Physics reports, 874, pp.1-92.

* `What are higher-order networks? <https://arxiv.org/abs/2104.11329>`_, Bick, C., Gross, E., Harrington, H.A. and Schaub, M.T., 2023. SIAM Review, 65(3), pp.686-731.

* `From networks to optimal higher-order models of complex systems
  <https://www.nature.com/articles/s41567-019-0459-y>`_, Lambiotte, R., Rosvall, M. and Scholtes, I., 2019. Nature physics, 15(4), pp.313-320.


Support
=======

.. image:: _static/nsf-logo.svg
  :height: 50
  :alt: NSF
  :target: https://www.nsf.gov

.. image:: _static/zulip-org-logo.svg
  :height: 50
  :alt: Zulip
  :target: https://zulip.com


See details `here <https://github.com/xgi-org/xgi/blob/main/SUPPORT.md>`_.

License
=======

This project is licensed under the `BSD 3-Clause License
<https://github.com/xgi-org/xgi/blob/main/LICENSE.md>`_.

