import pkg_resources

from xgi import (
    algorithms,
    classes,
    convert,
    drawing,
    generators,
    linalg,
    readwrite,
    utils,
)
from xgi.algorithms import *
from xgi.classes import *
from xgi.convert import *
from xgi.drawing import *
from xgi.generators import *
from xgi.linalg import *
from xgi.readwrite import *

__version__ = pkg_resources.require("xgi")[0].version
