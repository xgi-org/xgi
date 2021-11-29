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

__all__ = ["generic_hypergraph_view", "subhypergraph_view"]


def generic_hypergraph_view(H, create_using=None):
    """Create a read-only view of the hypergraph

    The read-only view shares the same memory as the original hypergraph
    and "freezes" the hypergraph by removing the methods that can modify
    the hypergraph.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None

    Returns
    -------
    Hypergraph object
        A read-only view of the hypergraph
    """
    if create_using is None:
        newH = H.__class__()
    else:
        newH = xgi.empty_hypergraph(create_using)
    newH = xgi.freeze(newH)

    # create view by assigning attributes from G
    newH._hypergraph = H._hypergraph
    newH._node = H._node
    newH._node_attr = H._node_attr
    newH._edge = H._edge
    newH._edge_attr = H._edge_attr
    return newH


def subhypergraph_view(H, filtered_nodes=None, filtered_edges=None):
    """View of `H` applying a filter on nodes and edges.

    `subhypergraph_view` provides a read-only view of the induced subhypergraph that
    includes nodes, edges, or both based on what the user specifies. This function
    automatically filters out edges that are not subsets of the nodes. This function
    may create isolated nodes.

    Parameters
    ----------
    H : hypergraph.Hypergraph
        A hypergraph
    filtered_nodes : list or set, default: None
        A list of the nodes desired for the subhypergraph.
        If None, uses all the nodes.
    filtered_edges : list or set, default: None
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
    nodes = (
        H.nodes
        if filtered_nodes is None
        else {node for node in filtered_nodes if node in H.nodes}
    )
    edges = (
        H.edges
        if filtered_edges is None
        else {edge for edge in filtered_edges if edge in H.edges}
    )

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
