# XGI
<img src='logo/logo.svg' width='150px' align="right" style="float:right;margin-left:10pt"></img>
Comple**X** **G**roup **I**nteractions (**XGI**) is a Python package for the representation, manipulation, and study of the structure, dynamics, and functions of complex systems with group (higher-order) interactions.

* [**Source**](../../)
* [**Bug reports**](../../issues)
* [**GitHub Discussions**](../../discussions)
* [**Documentation**](https://xgi.readthedocs.io/en/latest/)

## Table of Contents:
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [How to Cite](#how-to-cite)
  - [Code of Conduct](#code-of-conduct)
  - [License](#license)
  - [Funding](#funding)
  - [Other Resources](#other-resources)

## Installation
XGI runs on Python 3.7 or higher.

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

## Documentation

For more documentation, see our [Read The Docs](https://xgi.readthedocs.io/en/latest/) page.

## Contributing
Contributions are always welcome. Please report any bugs that you find [here](../../issues). Or, even better, fork the repository on [GitHub](../../) and create a pull request (PR). We welcome all changes, big or small, and we will help you make the PR if you are new to `git` (just ask on the issue and/or see our [contributing guidelines](CONTRIBUTING.md)).

## How to Cite

We acknowledge the importance of good software to support research, and we note
that research becomes more valuable when it is communicated effectively. To
demonstrate the value of XGI, we ask that you cite XGI in your work.
Currently, the best way to cite XGI is to go to our
[repository page](../../) (if you haven't already) and
click the "cite this repository" button on the right sidebar. This will generate
a citation in your preferred format, and will also integrate well with citation managers.

## Code of Conduct

Our full code of conduct, and how we enforce it, can be read in [our repository](CODE_OF_CONDUCT.md).

## License
Released under the 3-Clause BSD license (see [`LICENSE.md`](LICENSE.md))

Copyright (C) 2021 XGI Developers

Nicholas Landry <nicholas.landry@uvm.edu>

Leo Torres <leo@leotrs.com>

Iacopo Iacopini <iacopiniiacopo@gmail.com>

Maxime Lucas <maxime.lucas@centai.eu>

Giovanni Petri <giovanni.petri@centai.eu>

Alice Patania <apatania@uvm.edu>

Alice Schwarze <alice.c.schwarze@dartmouth.edu>

Martina Contisciani <martina.contisciani@tue.mpg.de>

The XGI library has copied or modified code from the HyperNetX and NetworkX libraries, the licenses of which can be found in our [license file](LICENSE.md)

## Funding
The XGI package has been supported by NSF Grant 2121905, ["HNDS-I: Using Hypergraphs to Study Spreading Processes in Complex Social Networks"](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2121905).

## Other resources
This library may not meet your needs and if this is this case, consider checking out these other resources:
* [HyperNetX](https://pnnl.github.io/HyperNetX): A package in Python for representing, analyzing, and visualizing hypergraphs.
* [Reticula](https://docs.reticula.network/): A package with a Python wrapper of C++ functions for representing, analyzing, and visualizing temporal and static graphs and hypergraphs.
* [SimpleHypergraphs.jl](https://pszufe.github.io/SimpleHypergraphs.jl/v0.1/): A package in Julia for representing, analyzing, and generating hypergraphs.
* [HyperGraphs.jl](https://github.com/lpmdiaz/HyperGraphs.jl): A package in Julia for representing, analyzing, and generating hypergraphs which may be oriented and weighted.
* [hyperG](https://cran.r-project.org/package=HyperG): A package in R for storing and analyzing hypergraphs
* [NetworkX](https://networkx.org/): A package in Python for representing, analyzing, and visualizing networks.
