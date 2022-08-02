"""Read from and write to edgelists."""

from ..generators import empty_hypergraph

__all__ = [
    "read_edgelist",
    "write_edgelist",
    "parse_edgelist",
]


def generate_edgelist(H, delimiter=" "):
    """
    A helper function to generate a hyperedge list from a Hypergraph object.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    delimiter: char, default: space (" ")
        Specifies the delimiter between hyperedge members

    Yields
    -------
    iterator of strings
        Each entry is a line for the file to write.
    """
    for id in H.edges:
        e = H.edges.members(id)
        yield delimiter.join(map(str, e))


def write_edgelist(H, path, delimiter=" ", encoding="utf-8"):
    """Create a file containing a hyperedge list from a Hypergraph object.

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

    Examples
    --------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.01, 0.001])
    >>> # xgi.write_edgelist(H, "test.csv", delimiter=",")

    """
    with open(path, "wb") as file:
        for line in generate_edgelist(H, delimiter):
            line += "\n"
            file.write(line.encode(encoding))


def read_edgelist(
    path,
    comments="#",
    delimiter=None,
    create_using=None,
    nodetype=None,
    encoding="utf-8",
):
    """Read a file containing a hyperedge list and
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
    Hypergraph object
        The loaded hypergraph

    See Also
    --------
    read_weighted_edgelist

    Examples
    --------
    >>> import xgi
    >>> # H = xgi.read_edgelist("test.csv", delimiter=",")

    """
    with open(path, "rb") as file:
        lines = (
            line if isinstance(line, str) else line.decode(encoding) for line in file
        )
        return parse_edgelist(
            lines,
            comments=comments,
            delimiter=delimiter,
            create_using=create_using,
            nodetype=nodetype,
        )


def parse_edgelist(
    lines, comments="#", delimiter=None, create_using=None, nodetype=None
):
    """
    A helper function to read a iterable of strings containing a hyperedge list and
    convert it to a Hypergraph object.

    Parameters
    ----------
    lines: iterable of strings
        Lines where each line is an edge
    comments: string, default: "#"
        The token that denotes comments to ignore
    delimiter: char, default: space (" ")
        Specifies the delimiter between hyperedge members
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None
    nodetype: type
        type that the node labels will be cast to

    Returns
    -------
    Hypergraph object
        The loaded hypergraph

    """
    H = empty_hypergraph(create_using)
    for line in lines:
        if comments is not None:
            p = line.find(comments)
            if p >= 0:
                line = line[:p]
            if not line:
                continue
        edge = line.strip().split(delimiter)

        if nodetype is not None:
            try:
                edge = [nodetype(node) for node in edge]
            except ValueError as e:
                raise TypeError(f"Failed to convert nodes to type {nodetype}.") from e

        H.add_edge(edge)
    return H
