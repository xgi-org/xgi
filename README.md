# Hypergraph

Hypergraph is a Python package for the representation, manipulation, and study of the structure, dynamics, and functions of hypergraphs.

* **Source:** https://github.com/nwlandry/Hypergraph
* **Bug reports:** https://github.com/nwlandry/Hypergraph/issues
* **GitHub Discussions:** https://github.com/nwlandry/Hypergraph/discussions

## Table of Contents:
  - [Installation](#installation)
  - [Usage](#usage)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [How to cite](#how-to-cite)
  - [Code of Conduct](#code-of-conduct)
  - [License](#license)

## Installation

Hypergraph runs on Python 3.9 or higher.

Install the latest version of Hypergraph:
* Clone this repository
* Navigate to the folder on your local machine
* Run the following command:
```sh
pip install -e .["all"]
```

## Usage

The following is an example of constructing a hypergraph from a hyperedge list and getting its incidence matrix:

```python
import hypergraph as hg
import random

n = 1000
m = 10000
min_edge_size = 2
max_edge_size = 25
hyperedge_list = [random.sample(range(n), random.choice(range(min_edge_size,max_edge_size+1))) for i in range(m)]

H = hg.Hypergraph(hyperedge_list)

I = hg.incidence_matrix(H)
```

## Documentation

Documentation is in progress.

## Contributing
Is always welcome. Please report any bugs that you find [here](https://github.com/nwlandry/Hypergraph/issues). Or, even better, fork the repository on [GitHub](https://github.com/nwlandry/Hypergraph) and create a pull request (PR). We welcome all changes, big or small, and we will help you make the PR if you are new to `git` (just ask on the issue and/or see `CONTRIBUTING.md`).

## How to Cite

We acknowledge the importance of good software to support research, and we note
that research becomes more valuable when it is communicated effectively. To
demonstrate the value of Hypergraph, we ask that you cite Hypergraph in your work.
Currently, the best way to cite Hypergraph is to go to our
[repository page](https://github.com/nwlandry/Hypergraph) (if you haven't already) and
click the "cite this repository" button on the right sidebar. This will generate
a citation in your preferred format, and will also integrate well with citation managers.

## Code of Conduct

Our full code of conduct, and how we enforce it, can be read in [our repository](https://github.com/nwlandry/Hypergraph/blob/main/CODE_OF_CONDUCT.md).
### License
Released under the 3-Clause BSD license (see `license.md`)

Copyright (C) 2021 Hypergraph Developers
Nicholas Landry <nicholas.landry@colorado.edu>
Leo Torres <leo@leotrs.com>

The Hypergraph library has copied or modified code from the HyperNetX and NetworkX libraries, the licenses of which can be found in our [license file](https://github.com/nwlandry/Hypergraph/blob/main/license.md)