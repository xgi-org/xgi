"""XGI exception hierarchy.

XGIException
├── XGIError        — domain-specific hypergraph errors (e.g. modifying a frozen network)
└── IDNotFound      — also inherits KeyError; raised when a node or edge ID is missing

Use ``ValueError`` (not ``XGIError``) for invalid arguments in public API functions.
Reserve ``XGIError`` for cases where the hypergraph itself is in a state that
prevents the operation.
"""


class XGIException(Exception):
    """Base class for exceptions in XGI."""


class XGIError(XGIException):
    """Exception for a serious error in XGI"""


class IDNotFound(XGIException, KeyError):
    """Raised when a node or edge is not in the hypergraph."""


def frozen(*args, **kwargs):
    """Dummy method that raises an error when trying to modify frozen networks

    Raises
    ------
    XGIError
        Raises error when user tries to modify the network

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> H.freeze()
    >>> H.add_node(5)
    Traceback (most recent call last):
    xgi.exception.XGIError: Frozen higher-order network can't be modified

    """
    raise XGIError("Frozen higher-order network can't be modified")
