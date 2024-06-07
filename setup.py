import codecs
import os.path
import sys

import setuptools
from setuptools import setup

name = "xgi"


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


if sys.version_info < (3, 8):
    sys.exit("XGI requires Python 3.8 or later.")

version = get_version("xgi/__init__.py")

authors = "XGI Developers"

author_email = "nicholas.landry@uvm.edu"

project_urls = {
    "Documentation": "https://xgi.readthedocs.io/en/stable/",
    "Bug Reports": "https://github.com/xgi-org/xgi/issues",
    "Source": "https://github.com/xgi-org/xgi",
    "PyPI": "https://pypi.org/project/xgi/",
    "GitHub Discussions": "https://github.com/xgi-org/xgi/discussions",
}

description = """XGI is a Python package for higher-order networks."""

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
