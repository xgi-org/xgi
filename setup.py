from setuptools import setup
import sys

__version__ = "0.0"

if sys.version_info < (3, 7):
    sys.exit("Hypergraph requires Python 3.7 or later.")

setup(
    name="hypergraph",
    packages=[
        "hypergraph",
        "hypergraph.algorithms",
        "hypergraph.classes",
        "hypergraph.generators",
        "hypergraph.linalg",
        "hypergraph.readwrite",
        "hypergraph.utils",
    ],
    version=__version__,
    author="Nicholas Landry",
    description="Hypergraph is a Python library for hypergraphs.",
    install_requires=[
        "networkx>=2.2,<3.0",
        "numpy>=1.15.0,<2.0",
        "scipy>=1.1.0,<2.0",
        "pandas>=0.23",
        "celluloid>=0.2.0",
    ],
    license="3-Clause BSD license",
    extras_require={
        "testing": ["pytest>=4.0"],
        "tutorials": ["jupyter>=1.0"],
        "documentation": ["sphinx>=1.8.2", "nb2plots>=0.6", "sphinx-rtd-theme>=0.4.2"],
        "all": [
            "sphinx>=1.8.2",
            "nb2plots>=0.6",
            "sphinx-rtd-theme>=0.4.2",
            "pytest>=4.0",
            "jupyter>=1.0",
        ],
    },
)