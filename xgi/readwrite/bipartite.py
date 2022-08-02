"""Read from and write to bipartite formats."""

from ..exception import XGIError
from ..generators import empty_hypergraph

__all__ = [
    "read_bipartite_edgelist",
    "write_bipartite_edgelist",
    "parse_bipartite_edgelist",
]


def generate_bipartite_edgelist(H, delimiter=" "):
    """
    A helper function to generate a bipartite edge list from a Hypergraph object.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    delimiter: char, default: space (" ")
        Specifies the delimiter between hyperedge members

    Yields
    -------
    A iterator of strings
        Each entry is a line to be written to the output file.
    """
    for id in H.edges:
        for node in H.edges.members(id):
            yield delimiter.join(map(str, [node, id]))


def write_bipartite_edgelist(H, path, delimiter=" ", encoding="utf-8"):
    """Write a Hypergraph object to a file
    as a bipartite edgelist.

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
    read_bipartite_edgelist

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.01, 0.001])
    >>> # xgi.write_bipartite_edgelist(H, "test.csv", delimiter=",")

    """
    with open(path, "wb") as file:
        for line in generate_bipartite_edgelist(H, delimiter):
            line += "\n"
            file.write(line.encode(encoding))


def read_bipartite_edgelist(
    path,
    comments="#",
    delimiter=None,
    create_using=None,
    nodetype=None,
    edgetype=None,
    dual=False,
    encoding="utf-8",
):
    """Read a file containing a bipartite edge list and
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
    edgetype: type
        type that the edge labels will be cast to
    dual: bool, default: False
        Specifies whether the node IDs are in the second column. If False,
        the node IDs are in the first column.
    encoding: string, default: "utf-8"
        Encoding of the file

    Returns
    -------
    A Hypergraph object
        The loaded hypergraph

    See Also
    --------
    write_bipartite_edgelist

    Example
    -------
    >>> import xgi
    >>> # H = xgi.read_bipartite_edgelist("test.csv", delimiter=",")

    """
    with open(path, "rb") as file:
        lines = (
            line if isinstance(line, str) else line.decode(encoding) for line in file
        )
        return parse_bipartite_edgelist(
            lines,
            comments=comments,
            delimiter=delimiter,
            create_using=create_using,
            nodetype=nodetype,
            edgetype=edgetype,
            dual=dual,
        )


def parse_bipartite_edgelist(
    lines,
    comments="#",
    delimiter=None,
    create_using=None,
    nodetype=None,
    edgetype=None,
    dual=False,
):
    """
    A helper function to read a iterable of strings containing a bipartite edge list and
    convert it to a Hypergraph object.

    Reads the first two entries of each line and assumes that the first entry is a node
    ID and that the second entry is an edge ID. Raises error if there are fewer than two
    entries.

    Parameters
    ----------
    lines: iterable of strings
        Lines where each line is a bipartite edge
    comments: string, default: "#"
        The token that denotes comments to ignore
    delimiter: char, default: space (" ")
        Specifies the delimiter between hyperedge members
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None
    nodetype: type
        type that the node labels will be cast to
    edgetype: type
        type that the edge labels will be cast to
    data: bool, default: False
        Specifies whether there is a dictionary of data at the end of the line.

    Raises
    ------
    XGIError
        If a line contains fewer than two entries
    TypeError
        If node types fail to be converted

    Returns
    -------
    Hypergraph
        The loaded hypergraph.

    """
    H = empty_hypergraph(create_using)

    node_index = 1 if dual else 0
    edge_index = 0 if dual else 1

    for line in lines:
        if comments is not None:
            p = line.find(comments)
            if p >= 0:
                line = line[:p]
            if not line:
                continue
        s = line.strip().split(delimiter)
        if len(s) < 2:
            raise XGIError("Each line must contain at least two entries!")
        # no data or data type specified

        # convert node types
        if nodetype is not None:
            try:
                node = nodetype(s[node_index])
            except ValueError as e:
                raise TypeError(
                    f"Failed to convert the node with ID {s[node_index]} to type {nodetype}."
                ) from e
        else:
            node = s[node_index]

        # convert edge types
        if edgetype is not None:
            try:
                edge = edgetype(s[edge_index])
            except ValueError as e:
                raise TypeError(
                    f"Failed to convert the edge with ID {s[edge_index]} to type {edgetype}."
                ) from e
        else:
            edge = s[edge_index]

        H.add_node_to_edge(edge, node)
    return H
