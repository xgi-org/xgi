"""Methods for converting to and from bipartite edgelists."""

from ..core import DiHypergraph, Hypergraph
from ..exception import XGIError

__all__ = ["from_bipartite_edgelist", "to_bipartite_edgelist"]


def from_bipartite_edgelist(edges):
    """Generate a hypergraph from a list of lists.

    Parameters
    ----------
    e : tuple, list, or array of tuples, lists, or arrays, each of size 2
        A bipartite edgelist

    Returns
    -------
    Hypergraph object
        The constructed hypergraph object

    See Also
    --------
    to_bipartite_edgelist
    ~xgi.convert.hyperedges.from_hyperedge_list
    ~xgi.convert.hyperedges.to_hyperedge_list
    """
    if len(edges[0]) == 3:  # directed
        H = DiHypergraph()
        for n, e, d in edges:
            H.add_node_to_edge(e, n, d)
        return H
    elif len(edges[0]) == 2:  # undirected
        H = Hypergraph()
        for n, e in edges:
            H.add_node_to_edge(e, n)
        return H
    else:
        raise XGIError(
            "Each list element must have two entries for directed "
            "and three entries for directed."
        )


def to_bipartite_edgelist(H):
    """Generate a hyperedge list from a hypergraph.

    Parameters
    ----------
    H : Hypergraph, SimplicialComplex, or DiHypergraph object
        The network of interest

    Returns
    -------
    list of sets
        The hyperedge list

    See Also
    --------
    from_bipartite_edgelist
    ~xgi.convert.hyperedges.to_hyperedge_list
    ~xgi.convert.hyperedges.from_hyperedge_list
    """
    if isinstance(H, DiHypergraph):
        edgelist = []
        for e, edge in H._edge.items():
            for n in edge["in"]:
                edgelist.append((n, e, "in"))
            for n in edge["out"]:
                edgelist.append((n, e, "out"))
        return edgelist

    return [(n, e) for e, edge in H.edges.members(dtype=dict).items() for n in edge]
