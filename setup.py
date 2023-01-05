import sys

import setuptools
from setuptools import setup

__version__ = "0.5.2"

if sys.version_info < (3, 7):
    sys.exit("XGI requires Python 3.7 or later.")

name = "xgi"

version = __version__

authors = "Nicholas Landry, Leo Torres, Maxime Lucas, Iacopo Iacopini, Giovanni Petri, Alice Patania, and Alice Schwarze"

author_email = "nicholas.landry@uvm.edu"

project_urls = {
    "Documentation": "https://xgi.readthedocs.io/en/latest/",
    "Bug Reports": "https://github.com/ComplexGroupInteractions/xgi/issues",
    "Source": "https://github.com/ComplexGroupInteractions/xgi",
    "PyPI": "https://pypi.org/project/xgi/",
    "GitHub Discussions": "https://github.com/ComplexGroupInteractions/xgi/discussions",
}

description = """XGI is a Python library for the representation
and analysis of complex systems with group (higher-order) interactions."""

with open("long_description.rst") as file:
    long_description = file.read()


def parse_requirements_file(filename):
    with open(filename) as fid:
        requires = [l.strip() for l in fid.readlines() if not l.startswith("#")]
    return requires


extras_require = {
    dep: parse_requirements_file("requirements/" + dep + ".txt")
    for dep in [
        "benchmarks",
        "developer",
        "documentation",
        "release",
        "test",
        "tutorial",
    ]
}

extras_require["all"] = list({item for dep in extras_require.values() for item in dep})

install_requires = parse_requirements_file("requirements/default.txt")

license = "3-Clause BSD license"

setup(
    name=name,
    packages=setuptools.find_packages(),
    version=version,
    author=authors,
    author_email=author_email,
    project_urls=project_urls,
    description=description,
    long_description=long_description,
    install_requires=install_requires,
    extras_require=extras_require,
)
