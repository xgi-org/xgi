"""Functions to randomize hypergaphs

All the functions in this module return a Hypergraph class (i.e. a simple, undirected
hypergraph).

"""

import random

import xgi

__all__ = [
    "shuffle_hyperedges",
]


def shuffle_hyperedges(S, order, p):
    """Shuffle existing hyperdeges of order `order` with probablity `p`.

    Parameters
    ----------
    S : xgi.HyperGraph
        Hypergraph
    order : int
        Order of hyperedges to shuffle
    p : float
        Probability of shuffling each hyperedge

    Returns
    -------
    H: xgi.HyperGraph
        Hypergraph with edges of order d shuffled

    Reference
    ---------
    Zhang, Y., Lucas, M. and Battiston, F., 2023.
    "Higher-order interactions shape collective dynamics differently
    in hypergraphs and simplicial complexes."
    Nature Communications, 14(1), p.1605.
    https://doi.org/10.1038/s41467-023-37190-9

    Example
    -------


    """

    if (order + 1) not in xgi.unique_edge_sizes(S):
        raise ValueError(f"There is no hyperedge of order {order} is this hypergraph.")
    if (p < 0) or (p > 1):
        raise ValueError("p must be between 0 and 1 included.")

    # convert to Hypergraph to be able to shuffle edges
    if isinstance(S, xgi.Hypergraph):
        H = xgi.Hypergraph()
        H.add_nodes_from(S.nodes)
        H.add_edges_from(S._edge)
    else:
        H = S.copy()

    nodes = S.nodes
    d_hyperedges = H.edges.filterby("order", order).members(dtype=dict)

    for id_, members in d_hyperedges.items():
        if random.random() <= p:
            H.remove_edge(id_)
            new_hyperedge = tuple(random.sample(nodes, order + 1))
            while new_hyperedge in H._edge.values():
                new_hyperedge = tuple(random.sample(nodes, order + 1))
            H.add_edge(new_hyperedge)

    assert H.num_nodes == S.num_nodes
    assert xgi.num_edges_order(H, 1) == xgi.num_edges_order(S, 1)
    assert xgi.num_edges_order(H, 2) == xgi.num_edges_order(S, 2)

    return H
