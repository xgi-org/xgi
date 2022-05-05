"""View of Hypergraphs as a subhypergraph or read-only.

In some algorithms it is convenient to temporarily morph
a hypergraph to exclude some nodes or edges. It should be better
to do that via a view than to remove and then re-add. This module provides those graph views.

The resulting views are essentially read-only graphs that
report data from the original graph object.

Note: Since hypergraphviews look like hypergraphs, one can end up with
view-of-view-of-view chains. Be careful with chains because
they become very slow with about 15 nested views. Often it is easiest to use .copy() to avoid chains.
"""


import xgi

__all__ = ["subhypergraph"]


def subhypergraph(H, nodes=None, edges=None):
    """View of `H` applying a filter on nodes and edges.

    `subhypergraph_view` provides a read-only view of the induced subhypergraph that
    includes nodes, edges, or both based on what the user specifies. This function
    automatically filters out edges that are not subsets of the nodes. This function
    may create isolated nodes.

    If the user only specifies the nodes to include, the function returns
    an induced subhypergraph on the nodes.

    If the user only specifies the edges to include, the function returns all of the nodes
    and the specified edges.

    If the user specifies both nodes and edges to include in the subhypergraph, then the
    function returns a subhypergraph with the specified nodes and edges from the list of specified
    hyperedges that are induced by the specified nodes.

    Parameters
    ----------
    H : hypergraph.Hypergraph
        A hypergraph
    nodes : list or set, default: None
        A list of the nodes desired for the subhypergraph.
        If None, uses all the nodes.
    edges : list or set, default: None
        A list of the edges desired for the subhypergraph.
        If None, uses all the edges.

    Returns
    -------
    Hypergraph object
        A read-only hypergraph view of the input hypergraph.
    """
    newH = xgi.freeze(H.__class__())

    # create view by assigning attributes from G
    newH._hypergraph = H._hypergraph
    # intersection of the selected nodes and edges with the existing edges
    nodes = H.nodes if nodes is None else {node for node in nodes if node in H.nodes}
    edges = H.edges if edges is None else {edge for edge in edges if edge in H.edges}

    # Add edges that are a subset of the filtered nodes
    newH._edge = {
        edge: H._edge[edge] for edge in edges if set(H._edge[edge]).issubset(nodes)
    }
    newH._edge_attr = {edge: H._edge_attr[edge] for edge in newH._edge}

    # Add the filtered nodes with connections to the remaining edges after filtering
    newH._node = {
        node: set(H._node[node]).intersection(newH._edge.keys()) for node in nodes
    }
    newH._node_attr = {node: H._node_attr[node] for node in nodes}
    return newH
