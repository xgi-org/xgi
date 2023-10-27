"""Method for projecting a hypergraph to a graph."""

import networkx as nx

from ..linalg import adjacency_matrix

__all__ = ["to_graph"]


def to_graph(H):
    """Graph projection (1-skeleton) of the hypergraph H.
    Weights are not considered.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    G : networkx.Graph
        The graph projection
    """

    A = adjacency_matrix(H)  # This is unweighted by design
    G = nx.from_scipy_sparse_array(A)
    G = nx.relabel_nodes(G, {i: node for i, node in enumerate(H.nodes)})
    return G
