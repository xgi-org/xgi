"""View of Graphs as SubGraph or read-only.

In some algorithms it is convenient to temporarily morph
a graph to exclude some nodes or edges. It should be better
to do that via a view than to remove and then re-add.
In other algorithms it is convenient to temporarily morph
a graph to reverse directed edges, or treat a directed graph
as undirected, etc. This module provides those graph views.

The resulting views are essentially read-only graphs that
report data from the orignal graph object. We provide an
attribute G._graph which points to the underlying graph object.

Note: Since graphviews look like graphs, one can end up with
view-of-view-of-view chains. Be careful with chains because
they become very slow with about 15 nested views.
For the common simple case of node induced subgraphs created
from the graph class, we short-cut the chain by returning a
subgraph of the original graph directly rather than a subgraph
of a subgraph. We are careful not to disrupt any edge filter in
the middle subgraph. In general, determining how to short-cut
the chain is tricky and much harder with restricted_views than
with induced subgraphs.
Often it is easiest to use .copy() to avoid chains.
"""

from hypergraph.exception import HypergraphError

import hypergraph as hg

__all__ = ["generic_hypergraph_view", "subhypergraph_view"]


def generic_hypergraph_view(H, create_using=None):
    if create_using is None:
        newH = H.__class__()
    else:
        newH = hg.empty_hypergraph(create_using)
    newH = hg.freeze(newH)

    # create view by assigning attributes from G
    newH._hypergraph = H._hypergraph
    newH._node = H._node
    newH._node_attr = H._node_attr
    newH._edge = H._edge
    newH._edge_attr = H._edge_attr
    return newH


def subhypergraph_view(H, filtered_nodes=None, filtered_edges=None):
    newH = hg.freeze(H.__class__())

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
        edge: H._edge[edge] for edge in edges if H._edge[edge].issubset(nodes)
    }
    newH._edge_attr = {edge: H._edge_attr[edge] for edge in newH._edge}

    # Add the filtered nodes with connections to the remaining edges after filtering
    newH._node = {node: H._node[node].intersection(newH._edge.keys()) for node in nodes}
    newH._node_attr = {node: H._node_attr[node] for node in nodes}
    return newH
