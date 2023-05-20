# XGI
<img src='logo/logo.svg' width='150px' align="right" style="float:right;margin-left:10pt"></img>
Comple**X** **G**roup **I**nteractions (**XGI**) is a Python package for the representation, manipulation, and study of the structure, dynamics, and functions of complex systems with group (higher-order) interactions.

[![Test Status](https://github.com/xgi-org/xgi/workflows/test/badge.svg?branch=main)](https://github.com/xgi-org/xgi/actions?query=workflow%3A%22test%22)
[![codecov](https://codecov.io/gh/xgi-org/xgi/branch/main/graph/badge.svg?token=BI6TX2WDSG)](https://codecov.io/gh/xgi-org/xgi)
[![Good First Issue](https://img.shields.io/badge/contribute-Good%20First%20Issue-%232EBC4F)](https://github.com/xgi-org/xgi/issues?q=is%3Aopen+is%3Aissue+label%3A%22Good+First+Issue%22)

* [**Source**](../../)
* [**Bug reports**](../../issues)
* [**GitHub Discussions**](../../discussions)
* [**Documentation**](https://xgi.readthedocs.io/en/latest/)

Sign up for our [mailing list](http://eepurl.com/igE6ez) and follow XGI on [Twitter](https://twitter.com/xginets) or [Mastodon](https://mathstodon.xyz/@xginets)!

## Table of Contents:
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [How to Contribute](#contributing)
  - [Corresponding Data](#corresponding-data)
  - [How to Cite](#how-to-cite)
  - [License](#license)
  - [Funding](#funding)
  - [Other Resources](#other-resources)


## Installation
XGI runs on Python 3.8 or higher.

To install the latest version of XGI, run the following command:
```sh
pip install xgi
```

To install this package locally:
* Clone this repository
* Navigate to the folder on your local machine
* Run the following command:
```sh
pip install -e .["all"]
```
* If that command does not work, you may try the following instead
````zsh
pip install -e .\[all\]
````


## Getting Started
To get started, take a look at the [tutorials](/tutorials/) illustrating the library's basic functionality.


## Corresponding Data
A number of higher-order datasets are available in the [XGI-DATA repository](https://gitlab.com/complexgroupinteractions/xgi-data) and can be easily accessed with the `load_xgi_data()` function.


## How to Contribute
If you want to contribute to this project, please make sure to read the
[contributing guidelines](CONTRIBUTING.md). We expect respectful and kind interactions by all contributors and users as laid out in our [code of conduct](CODE_OF_CONDUCT.md).

The XGI community always welcomes contributions, no matter how small. We're happy to help troubleshoot XGI issues you run into, assist you if you would like to add functionality or fixes to the codebase, or answer any questions you may have.

Some concrete ways that you can get involved:

* **Get XGI updates** by following the XGI [Twitter](https://twitter.com/xginets) account, signing up for our [mailing list](http://eepurl.com/igE6ez), or starring this repository.
* **Spread the word** when you use XGI by sharing with your colleagues and friends.
* **Request a new feature or report a bug** by raising a [new issue](https://github.com/xgi-org/xgi/issues/new).
* **Create a Pull Request (PR)** to address an [open issue](../../issues) or add a feature.
* **Join our [Zulip channel](https://xgi.zulipchat.com/join/7agfwo7dh7jo56ppnk5kc23r/)** to be a part of the daily goings-on of XGI.


## How to Cite
We acknowledge the importance of good software to support research, and we note
that research becomes more valuable when it is communicated effectively. To
demonstrate the value of XGI, we ask that you cite XGI in your work.
Currently, the best way to cite XGI is to go to our
[repository page](../../) (if you haven't already) and
click the "cite this repository" button on the right sidebar. This will generate
a citation in your preferred format, and will also integrate well with citation managers.


## License
Released under the 3-Clause BSD license (see [`LICENSE.md`](LICENSE.md))

Copyright (C) 2021-2023 XGI Developers

* Nicholas Landry <nicholas.landry@uvm.edu>
* Leo Torres <leo@leotrs.com>
* Iacopo Iacopini <iacopiniiacopo@gmail.com>
* Maxime Lucas <maxime.lucas@centai.eu>
* Giovanni Petri <giovanni.petri@centai.eu>
* Alice Patania <apatania@uvm.edu>
* Alice Schwarze <alice.c.schwarze@dartmouth.edu>

The XGI library has copied or modified code from the HyperNetX and NetworkX libraries, the licenses of which can be found in our [license file](LICENSE.md)

## Funding
The XGI package has been supported by NSF Grant 2121905, ["HNDS-I: Using Hypergraphs to Study Spreading Processes in Complex Social Networks"](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2121905).

## Other Resources
This library may not meet your needs and if this is this case, consider checking out these other resources:
* [HyperNetX](https://pnnl.github.io/HyperNetX): A package in Python for representing, analyzing, and visualizing hypergraphs.
* [Reticula](https://docs.reticula.network/): A package with a Python wrapper of C++ functions for representing, analyzing, and visualizing temporal and static graphs and hypergraphs.
* [SimpleHypergraphs.jl](https://pszufe.github.io/SimpleHypergraphs.jl/v0.1/): A package in Julia for representing, analyzing, and generating hypergraphs.
* [HyperGraphs.jl](https://github.com/lpmdiaz/HyperGraphs.jl): A package in Julia for representing, analyzing, and generating hypergraphs which may be oriented and weighted.
* [hyperG](https://cran.r-project.org/package=HyperG): A package in R for storing and analyzing hypergraphs
* [NetworkX](https://networkx.org/): A package in Python for representing, analyzing, and visualizing networks.
