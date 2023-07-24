import pkg_resources

from . import (
    utils,
    core,
    algorithms,
    convert,
    drawing,
    dynamics,
    generators,
    linalg,
    readwrite,
    stats,
)
from .utils import *
from .core import *
from .algorithms import *
from .convert import *
from .drawing import *
from .dynamics import *
from .generators import *
from .linalg import *
from .readwrite import *
from .stats import *


__version__ = pkg_resources.require("xgi")[0].version
