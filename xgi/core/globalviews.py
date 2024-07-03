"""View of Hypergraphs as a subhypergraph or read-only.

In some algorithms it is convenient to temporarily morph a hypergraph to exclude some
nodes or edges. It should be better to do that via a view than to remove and then
re-add. This module provides those graph views.

The resulting views are essentially read-only graphs that report data from the original
graph object.

Note: Since globalviews look like hypergraphs, one can end up with
view-of-view-of-view chains. Be careful with chains because they become very slow with
about 15 nested views. Often it is easiest to use .copy() to avoid chains.

"""

__all__ = ["subhypergraph"]


def subhypergraph(H, nodes=None, edges=None, keep_isolates=True):
    """View of `H` applying a filter on nodes and edges.

    `subhypergraph_view` provides a read-only view of the induced subhypergraph that
    includes nodes, edges, or both based on what the user specifies. This function
    automatically filters out edges that are not subsets of the nodes. This function may
    create isolated nodes.

    If the user only specifies the nodes to include, the function returns an induced
    subhypergraph on the nodes.

    If the user only specifies the edges to include, the function returns all of the
    nodes and the specified edges.

    If the user specifies both nodes and edges to include in the subhypergraph, then the
    function returns a subhypergraph with the specified nodes and edges from the list of
    specified hyperedges that are induced by the specified nodes.

    Parameters
    ----------
    H : hypergraph.Hypergraph
        A hypergraph
    nodes : list or set, optional
        A list of the nodes desired for the subhypergraph.
        If None (default), uses all the nodes.
    edges : list or set, optional
        A list of the edges desired for the subhypergraph.
        If None (default), uses all the edges.
    keep_isolates : bool, optional
        Whether to keep isolated nodes in the subhypergraph.
        By default, True.

    Returns
    -------
    Hypergraph object
        A read-only hypergraph view of the input hypergraph.

    """
    new = H.__class__()

    new._net_attr = H._net_attr.copy()
    nodes = set(H.nodes) if nodes is None else (set(nodes) & set(H.nodes))
    edges = set(H.edges) if edges is None else (set(edges) & set(H.edges))

    new.add_nodes_from((uid, attr) for uid, attr in H.nodes.items() if uid in nodes)
    new.add_edges_from(
        (H.edges.members(uid), uid, attr)
        for uid, attr in H.edges.items()
        if uid in edges and set(H.edges.members(uid)).issubset(nodes)
    )

    if not keep_isolates:
        new.remove_nodes_from(new.nodes.isolates())

    new.freeze()
    return new
