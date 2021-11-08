import csv
import hypergraph as hg
from hypergraph.exception import HypergraphError
from ast import literal_eval

__all__ = [
    "read_bipartite_edgelist",
    "write_bipartite_edgelist",
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
        for node in H.edges[id]:
            yield delimiter.join(map(str, [node, id]))


def write_bipartite_edgelist(H, path, delimiter=" ", data=True, encoding="utf-8"):
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
    data: bool, default: True
        Specifies whether to output the edge attributes
    encoding: string, default: "utf-8"
        Encoding of the file

    See Also
    --------
    read_bipartite_edgelist

    Example
    -------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> hg.write_edgelist(H, "test.csv", delimiter=",")
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
    data=False,
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
    data: bool, default: False
        Specifies whether there is a dictionary of data at the end of the line.
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
        >>> import hypergraph as hg
        >>> H = hg.read_edgelist("test.csv", delimiter=",")
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
        )


def parse_bipartite_edgelist(
    lines, comments="#", delimiter=None, create_using=None, nodetype=None
):
    """
    A helper function to read a iterable of strings containing a bipartite edge list and
    convert it to a Hypergraph object.

    Parameters
    ----------
    lines: iterable of strings
        Lines where each line is an edge
    comments: string, default: "#"
        The token that denotes comments to ignore
    delimiter: char, default: space (" ")
        Specifies the delimiter between hyperedge members
    create_using:
    nodetype: type
        type that the node labels will be cast to
    data: bool, default: False
        Specifies whether there is a dictionary of data at the end of the line.

    Returns
    -------
    A Hypergraph object
        The loaded hypergraph
    """
    H = hg.empty_hypergraph(create_using)
    for line in lines:
        if comments is not None:
            p = line.find(comments)
            if p >= 0:
                line = line[:p]
            if not line:
                continue
        s = line.strip().split(delimiter)
        if len(s) != 2:
            raise HypergraphError("Each line must contain two entries!")
        # no data or data type specified

        if nodetype is not None:
            try:
                H.add_node_to_edge(s[1], nodetype(s[0]))
            except Exception as e:
                raise TypeError(f"Failed to convert nodes to type {nodetype}.") from e
        else:
            H.add_node_to_edge(s[1], s[0])
    return H
