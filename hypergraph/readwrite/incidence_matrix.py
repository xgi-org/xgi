import hypergraph as hg
import numpy as np

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

    Example
    -------
        >>> import hypergraph as hg
        >>> H = hg.read_incidence_matrix("test.csv", delimiter=",")
    """
    return hg.from_incidence_matrix(
        np.loadtxt(path, comments=comments, delimiter=delimiter, encoding=encoding),
        create_using=create_using,
    )


def write_incidence_matrix(H, path, delimiter=" ", encoding="utf-8"):
    """Write a Hypergraph object to a file
    as an incidence matrix.

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

    Example
    -------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> hg.write_incidence_matrix(H, "test.csv", delimiter=",")
    """
    I = hg.incidence_matrix(H, sparse=False)
    np.savetxt(path, I, delimiter=delimiter, newline="\n", encoding=encoding)
