from setuptools import setup
import sys
from xgi.utils.utilities import parse_requirements_file

__version__ = "0.1.1"

if sys.version_info < (3, 7):
    sys.exit("XGI requires Python 3.7 or later.")

name = "xgi"

packages = [
    "xgi",
    "xgi.algorithms",
    "xgi.classes",
    "xgi.generators",
    "xgi.linalg",
    "xgi.readwrite",
    "xgi.utils",
]

version = "0.1.1"

authors = "Nicholas Landry and Leo Torres"

author_email = "nicholas.landry@colorado.edu"

url = "https://github.com/ComplexGroupInteractions/xgi"

description = """XGI is a Python library for the representation
and analysis of complex systems with group (higher-order) interactions."""

with open("long_description.rst") as file:
    long_description = file.read()

extras_require = {
    dep: parse_requirements_file("requirements/" + dep + ".txt")
    for dep in ["developer", "documentation", "release", "test", "tutorial"]
}

extras_require["all"] = list({item for dep in extras_require.values() for item in dep})

install_requires = parse_requirements_file("requirements/default.txt")

license = "3-Clause BSD license"

setup(
    name=name,
    packages=packages,
    version=version,
    author=authors,
    author_email=author_email,
    url=url,
    description=description,
    long_description=long_description,
    install_requires=install_requires,
    extras_require=extras_require,
)
