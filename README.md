<img src='https://github.com/xgi-org/xgi/blob/main/logo/logo.svg' alt="XGI" width='50%'></img>

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Supports Python versions 3.9 and above.](https://img.shields.io/badge/Python%20versions%20supported-3.9%2B-forest
)](https://www.repostatus.org/#active)
[![Test Status](https://github.com/xgi-org/xgi/workflows/test/badge.svg?branch=main)](https://github.com/xgi-org/xgi/actions?query=workflow%3A%22test%22)
[![codecov](https://codecov.io/gh/xgi-org/xgi/branch/main/graph/badge.svg?token=BI6TX2WDSG)](https://codecov.io/gh/xgi-org/xgi)
[![Good First Issue](https://img.shields.io/badge/contribute-Good%20First%20Issue-forest)](https://github.com/xgi-org/xgi/issues?q=is%3Aopen+is%3Aissue+label%3A%22Good+First+Issue%22)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.05162/status.svg)](https://doi.org/10.21105/joss.05162)
[![pyOpenSci](https://tinyurl.com/y22nb8up)](https://github.com/pyOpenSci/software-review/issues/115)

* [**Source**](https://github.com/xgi-org/xgi)
* [**Bug reports**](https://github.com/xgi-org/xgi/issues)
* [**GitHub Discussions**](https://github.com/xgi-org/xgi/discussions)
* [**Documentation**](https://xgi.readthedocs.io)
* [**Contribute**](https://xgi.readthedocs.io/en/stable/contribute.html)
* [**Projects using XGI**](https://xgi.readthedocs.io/en/stable/using-xgi.html)

Sign up for our [mailing list](http://eepurl.com/igE6ez) and follow XGI on [Twitter](https://twitter.com/xginets) or [Mastodon](https://mathstodon.xyz/@xginets)!

### Table of Contents: ###
- [What is XGI?](#what-is-xgi)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [XGI-DATA](#xgi-data)
- [How to Contribute](#how-to-contribute)
- [How to Cite](#how-to-cite)
- [License](#license)
- [Funding](#funding)
- [Other Resources](#other-resources)

## What is XGI?<a id="what-is-xgi"></a>

Comple**X** **G**roup **I**nteractions (**XGI**) is a Python package for higher-order networks (If you want more information on what higher-order networks are, see our [brief introduction](https://xgi.readthedocs.io/en/stable/higher-order.html)).

**XGI is a software designed to streamline working with higher-order networks from start to finish**. XGI can
* Create synthetic datasets from many **generative models**
* **Read and write** higher-order datasets in a user-friendly way
* Represent **hypergraphs, directed hypergraphs, and simplicial complexes** with efficient and flexible data structures
* Analyze higher-order networks with **measures and algorithms**
* **Manipulate node and edge statistics** in a flexible and customizable way.
* Draw higher-order networks in a variety of **visually striking ways** (See our [gallery](https://xgi.readthedocs.io/en/stable/gallery.html) for several examples.)

## Installation<a id="installation"></a>
XGI runs on Python 3.9 or higher.

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
pip install -e ."[all]"
````
For more installation options, see the [guide](https://github.com/xgi-org/xgi/blob/main/requirements/README.md).


## Getting Started<a id="getting-started"></a>
To get started, take a look at the [user guides](https://xgi.readthedocs.io/en/stable/user_guides.html) illustrating the library's basic functionality.


## XGI-DATA<a id="xgi-data"></a>
A number of higher-order datasets are available in the [XGI-DATA repository](https://github.com/xgi-org/xgi-data) and can be easily accessed with the `load_xgi_data()` function.


## How to Contribute<a id="how-to-contribute"></a>
If you want to contribute to this project, please make sure to read the
[contributing guidelines](https://github.com/xgi-org/xgi/blob/main/HOW_TO_CONTRIBUTE.md). We expect respectful and kind interactions by all contributors and users as laid out in our [code of conduct](https://github.com/xgi-org/xgi/blob/main/CODE_OF_CONDUCT.md).

The XGI community always welcomes contributions, no matter how small. We're happy to help troubleshoot XGI issues you run into, assist you if you would like to add functionality or fixes to the codebase, or answer any questions you may have.

Some concrete ways that you can get involved:

* **Get XGI updates** by following the XGI [Twitter](https://twitter.com/xginets) account, signing up for our [mailing list](http://eepurl.com/igE6ez), or starring this repository.
* **Spread the word** when you use XGI by sharing with your colleagues and friends.
* **Request a new feature or report a bug** by raising a [new issue](https://github.com/xgi-org/xgi/issues/new).
* **Create a Pull Request (PR)** to address an [open issue](https://github.com/xgi-org/xgi/issues) or add a feature.
* **Join our [Zulip channel](https://xgi.zulipchat.com/join/7agfwo7dh7jo56ppnk5kc23r/)** to be a part of the daily goings-on of XGI.


## How to Cite<a id="how-to-cite"></a>
We acknowledge the importance of good software to support research, and we note that research becomes more valuable when it is communicated effectively. To demonstrate the value of XGI, we ask that you cite the XGI [paper](https://doi.org/10.21105/joss.05162) in your work. You can cite XGI either by going to our repository page [repository page](https://github.com/xgi-org/xgi) (if you haven't already) and clicking the "cite this repository" button on the right sidebar (which will generate a citation in your preferred format) or by copying the following BibTeX entry:
```
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
```

## License<a id="license"></a>
Released under the 3-Clause BSD license (see [`LICENSE.md`](https://github.com/xgi-org/xgi/blob/main/LICENSE.md))

Copyright (C) 2021-2024 XGI Developers

## Funding<a id="funding"></a>
The XGI package has been supported by NSF Grant 2121905, ["HNDS-I: Using Hypergraphs to Study Spreading Processes in Complex Social Networks"](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2121905).

## Other Resources<a id="other-resources"></a>
This library may not meet your needs and if this is this case, consider checking out our [list of other resources](https://github.com/xgi-org/xgi/blob/main/OTHER_RESOURCES.md).
