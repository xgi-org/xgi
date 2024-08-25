.. image:: https://github.com/xgi-org/xgi/raw/main/logo/logo.svg
   :alt: XGI
   :width: 200

.. image:: https://www.repostatus.org/badges/latest/active.svg
   :target: https://www.repostatus.org/#active
   :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.

.. image:: https://img.shields.io/badge/Python%20versions%20supported-3.8%2B-forest
   :target: https://www.repostatus.org/#active
   :alt: Supports Python versions 3.8 and above.

.. image:: https://github.com/xgi-org/xgi/workflows/test/badge.svg?branch=main
   :target: https://github.com/xgi-org/xgi/actions?query=workflow%3A%22test%22
   :alt: Test Status

.. image:: https://codecov.io/gh/xgi-org/xgi/branch/main/graph/badge.svg?token=BI6TX2WDSG
   :target: https://codecov.io/gh/xgi-org/xgi
   :alt: codecov

.. image:: https://img.shields.io/badge/contribute-Good%20First%20Issue-forest
   :target: https://github.com/xgi-org/xgi/issues?q=is%3Aopen+is%3Aissue+label%3A%22Good+First+Issue%22
   :alt: Good First Issue

.. image:: https://joss.theoj.org/papers/10.21105/joss.05162/status.svg
   :target: https://doi.org/10.21105/joss.05162
   :alt: DOI

.. image:: https://tinyurl.com/y22nb8up
   :target: https://github.com/pyOpenSci/software-review/issues/115
   :alt: pyOpenSci

* `**Source** <https://github.com/xgi-org/xgi>`_
* `**Bug reports** <https://github.com/xgi-org/xgi/issues>`_
* `**GitHub Discussions** <https://github.com/xgi-org/xgi/discussions>`_
* `**Documentation** <https://xgi.readthedocs.io>`_
* `**Contributors** <https://xgi.readthedocs.io/en/stable/contributors.html>`_
* `**Projects using XGI** <https://xgi.readthedocs.io/en/stable/using-xgi.html>`_

Sign up for our `mailing list <http://eepurl.com/igE6ez>`_ and follow XGI
on `Twitter <https://twitter.com/xginets>`_ or `Mastodon <https://mathstodon.xyz/@xginets>`_!

### Table of Contents: ###
- `What is XGI? <#what-is-xgi>`_
- `Installation <#installation>`_
- `Getting Started <#getting-started>`_
- `Corresponding Data <#corresponding-data>`_
- `How to Contribute <#how-to-contribute>`_
- `How to Cite <#how-to-cite>`_
- `License <#license>`_
- `Funding <#funding>`_
- `Other Resources <#other-resources>`_

## What is XGI?

Comple\ **X** **G**\ roup **I**\ nteractions (XGI) is a Python package for
higher-order networks (If you want more information on what
higher-order networks are, see our
`brief introduction <https://xgi.readthedocs.io/en/stable/higher-order.html>`_).

**XGI is a software designed to streamline working with higher-order networks from start to finish**.
XGI can

* Create synthetic datasets from many **generative models**
* **Read and write** higher-order datasets in a user-friendly way
* Represent **hypergraphs, directed hypergraphs, and simplicial complexes** with efficient and flexible data structures
* Analyze higher-order networks with **measures and algorithms**
* **Manipulate node and edge statistics** in a flexible and customizable way
* Draw higher-order networks in a variety of **visually striking ways**
(See our `gallery <https://xgi.readthedocs.io/en/stable/gallery.html>`_ for several examples.)

## Installation

XGI runs on Python 3.8 or higher.

To install the latest version of XGI, run the following command::

   pip install xgi

To install this package locally:

* Clone this repository
* Navigate to the folder on your local machine
* Run the following command::

   pip install -e .["all"]

* If that command does not work, you may try the following instead::

   pip install -e .\[all\]

## Getting Started
To get started, take a look at the
`tutorials <https://xgi.readthedocs.io/en/stable/api/tutorials.html>`_
illustrating the library's basic functionality.


## Corresponding Data
A number of higher-order datasets are available in the
`XGI-DATA repository <https://github.com/xgi-org/xgi-data>`_
and can be easily accessed with the ``load_xgi_data()`` function.

## How to Contribute
If you want to contribute to this project, please make sure to read the
`contributing guidelines <https://github.com/xgi-org/xgi/blob/main/HOW_TO_CONTRIBUTE.md>`_.
We expect respectful and kind interactions by all contributors and users as laid out in our
`code of conduct<https://github.com/xgi-org/xgi/blob/main/CODE_OF_CONDUCT.md>`_.

The XGI community always welcomes contributions, no matter how small. We're happy to help troubleshoot XGI issues you run into, assist you if you would like to add functionality or fixes to the codebase, or answer any questions you may have.

Some concrete ways that you can get involved:

* **Get XGI updates** by following the XGI `Twitter <https://twitter.com/xginets>`_ account,
signing up for our `mailing list <http://eepurl.com/igE6ez>`_, or starring this repository.
* **Spread the word** when you use XGI by sharing with your colleagues and friends.
* **Request a new feature or report a bug** by raising a
`new issue <https://github.com/xgi-org/xgi/issues/new>`_.
* **Create a Pull Request (PR)** to address an
`open issue <https://github.com/xgi-org/xgi/discussions>`_ or add a feature.
* **Join our `Zulip channel <https://xgi.zulipchat.com/join/7agfwo7dh7jo56ppnk5kc23r/>`_**
to be a part of the daily goings-on of XGI.


## How to Cite
We acknowledge the importance of good software to support research,
and we note that research becomes more valuable when it is communicated effectively.
To demonstrate the value of XGI, we ask that you cite the XGI
`paper <https://doi.org/10.21105/joss.05162>`_` in your work.
You can cite XGI either by going to our repository page `repository page <https://github.com/xgi-org/xgi>`_
(if you haven't already) and clicking the "cite this repository" button on the right sidebar
(which will generate a citation in your preferred format) or by copying the following BibTeX entry:

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

## License
Released under the 3-Clause BSD license
(see ```LICENSE.md`` <https://github.com/xgi-org/xgi/blob/main/LICENSE.md>`_).

Copyright (C) 2021-2024 XGI Developers

## Funding
The XGI package has been supported by NSF Grant 2121905,
`"HNDS-I: Using Hypergraphs to Study Spreading Processes in Complex Social Networks" <https://www.nsf.gov/awardsearch/showAward?AWD_ID=2121905>`_.

.. ## Other Resources
.. This library may not meet your needs and if this is this case, consider checking out these other resources:

.. **Julia**
.. * [HyperGraphs.jl](https://github.com/lpmdiaz/HyperGraphs.jl): A Julia package for representing, analyzing, and generating hypergraphs which may be oriented and weighted.
.. * [SimpleHypergraphs.jl](https://pszufe.github.io/SimpleHypergraphs.jl/v0.1): A Julia package for representing, analyzing, and generating hypergraphs.

.. **Python**
.. * [EasyGraph](https://easy-graph.github.io/): A Python package for analyzing undirected and directed networks as well as hypergraphs.
.. * [halp](http://murali-group.github.io/halp): A Python package with directed and undirected hypergraph implementations and several algorithms.
.. * [Hypergraph Analysis Toolbox (HAT)](https://hypergraph-analysis-toolbox.readthedocs.io): A Python/Matlab package for hypergraph construction, visualization, and analysis (Especially for Pore-C data).
.. * [Hypergraphx](https://hypergraphx.readthedocs.io): A Python for representing, analyzing, and visualizing hypergraphs.
.. * [HyperNetX](https://hypernetx.readthedocs.io): A Python package for representing, analyzing, and visualizing hypergraphs.
.. * [NetworkX](https://networkx.org): A Python package for representing, analyzing, and visualizing networks.
.. * [Reticula](https://docs.reticula.network): A Python package wrapping C++ functions for representing, analyzing, and visualizing temporal and static graphs and hypergraphs.

.. **R**
.. * [hyperG](https://cran.r-project.org/package=HyperG): An R package for storing and analyzing hypergraphs
