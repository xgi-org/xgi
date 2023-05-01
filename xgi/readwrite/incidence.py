"""Read from and write to incidece matrices."""

import numpy as np

from ..convert import from_incidence_matrix
from ..linalg import incidence_matrix

__all__ = [
    "read_incidence_matrix",
    "write_incidence_matrix",
]


def read_incidence_matrix(
    path, comments="#", delimiter=None, create_using=None, encoding="utf-8"
):
    """Read a file containing an incidence matrix and
    convert it to a Hypergraph object.

    Parameters
    ----------
    path: string
        The path of the file to read from
    comments: string, default: "#"
        The token that denotes comments in the file
    delimiter: char, default: space (" ")
        Specifies the delimiter between hyperedge members
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None
    nodetype: type
        type that the node labels will be cast to
    encoding: string, default: "utf-8"
        Encoding of the file

    Returns
    -------
    A Hypergraph object
        The loaded hypergraph

    See Also
    --------
    write_incidence_matrix

    Examples
    --------
    >>> import xgi
    >>> # H = xgi.read_incidence_matrix("test.csv", delimiter=",")

    """
    return from_incidence_matrix(
        np.loadtxt(path, comments=comments, delimiter=delimiter, encoding=encoding),
        create_using=create_using,
    )


def write_incidence_matrix(H, path, delimiter=" ", encoding="utf-8"):
    """Write a Hypergraph object to a file as an incidence matrix.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    path: string
        The path of the file to write to
    delimiter: char, default: space (" ")
        Specifies the delimiter between hyperedge members
    encoding: string, default: "utf-8"
        Encoding of the file

    See Also
    --------
    read_incidence_matrix

    Examples
    --------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.01, 0.001])
    >>> # xgi.write_incidence_matrix(H, "test.csv", delimiter=",")

    """
    eye = incidence_matrix(H, sparse=False)
    np.savetxt(path, eye, delimiter=delimiter, newline="\n", encoding=encoding)
