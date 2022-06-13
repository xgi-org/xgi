import pkg_resources

from . import (
    algorithms,
    classes,
    convert,
    drawing,
    generators,
    linalg,
    readwrite,
    utils,
    stats,
)
from .algorithms import *
from .classes import *
from .convert import *
from .drawing import *
from .generators import *
from .linalg import *
from .readwrite import *
from .utils import *
from .stats import *

__version__ = pkg_resources.require("xgi")[0].version
