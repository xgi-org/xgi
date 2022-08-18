import pkg_resources

from . import (
    utils,
    classes,
    algorithms,
    convert,
    drawing,
    generators,
    linalg,
    readwrite,
    stats,
)
from .utils import *
from .classes import *
from .algorithms import *
from .convert import *
from .drawing import *
from .generators import *
from .linalg import *
from .readwrite import *
from .stats import *


__version__ = pkg_resources.require("xgi")[0].version
