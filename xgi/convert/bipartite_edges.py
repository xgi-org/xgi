from ..generators import empty_hypergraph

__all__ = ["from_bipartite_edgelist", "to_bipartite_edgelist"]


def from_bipartite_edgelist(edges, create_using=None):
    """Generate a hypergraph from a list of lists.

    Parameters
    ----------
    e : tuple, list, or array of tuples, lists, or arrays, each of size 2
        A bipartite edgelist
    create_using : Hypergraph constructor, optional
        The hypergraph to add the edges to, by default None

    Returns
    -------
    Hypergraph object
        The constructed hypergraph object

    See Also
    --------
    to_hyperedge_list
    """
    H = empty_hypergraph(create_using)
    for n, e in edges:
        H.add_node_to_edge(e, n)
    return H


def to_bipartite_edgelist(H):
    """Generate a hyperedge list from a hypergraph.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    list of sets
        The hyperedge list

    See Also
    --------
    from_hyperedge_list
    """
    return [(n, id) for id, e in H.edges.members(dtype=dict).items() for n in e]
