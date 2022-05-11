class XGIException(Exception):
    """Base class for exceptions in XGI."""


class XGIError(XGIException):
    """Exception for a serious error in XGI"""


class IDNotFound(KeyError):
    """Raised when a node or edge is not in the hypergraph."""
