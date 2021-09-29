from setuptools import setup
import sys

__version__ = "0.0"

if sys.version_info < (3, 7):
    sys.exit("Hypergraph requires Python 3.7 or later.")

name="hypergraph"

packages=[
"hypergraph",
"hypergraph.algorithms",
"hypergraph.classes",
"hypergraph.generators",
"hypergraph.linalg",
"hypergraph.readwrite",
"hypergraph.utils",
]

version=__version__

authors="Nicholas Landry and Leo Torres"

author_email = "nicholas.landry@colorado.edu"

url="https://github.com/nwlandry/Hypergraph"

description="Hypergraph is a Python library for hypergraphs."

install_requires=[
"networkx>=2.2,<3.0",
"numpy>=1.15.0,<2.0",
"scipy>=1.1.0,<2.0",
"pandas>=0.23",
]

license="3-Clause BSD license"

extras_require={
"testing": ["pytest>=4.0"],
"tutorials": ["jupyter>=1.0"],
"documentation": ["sphinx>=1.8.2", "nb2plots>=0.6", "sphinx-rtd-theme>=0.4.2"],
"all": ["sphinx>=1.8.2","nb2plots>=0.6","sphinx-rtd-theme>=0.4.2","pytest>=4.0","jupyter>=1.0"],
}

setup(
name=name,
packages=packages,
version=version,
author=authors,
author_email=author_email,
url=url,
description=description,
install_requires=install_requires,
extras_require=extras_require,
)