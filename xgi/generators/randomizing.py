"""Functions to randomize hypergaphs

All the functions in this module return a Hypergraph class (i.e. a simple, undirected
hypergraph).
"""

import numpy as np

import xgi

__all__ = [
    "shuffle_hyperedges",
    "node_swap",
]


def shuffle_hyperedges(S, order, p, seed=None):
    """Shuffle existing hyperdeges of order `order` with probablity `p`.

    Parameters
    ----------
    S : xgi.Hypergraph
        Hypergraph
    order : int
        Order of hyperedges to shuffle
    p : float
        Probability of shuffling each hyperedge
    seed : int, numpy.random.Generator, or None, optional
        The seed for the random number generator. By default, None.

    Returns
    -------
    H: xgi.Hypergraph
        Hypergraph with edges of order d shuffled

    Note
    ----
    By shuffling hyperedges in a simplicial complex, it will in general lose
    its "simpliciality" and become a hypergraph.

    References
    ----------
    Zhang, Y.*, Lucas, M.* and Battiston, F., 2023.
    "Higher-order interactions shape collective dynamics differently
    in hypergraphs and simplicial complexes."
    Nature Communications, 14(1), p.1605.
    https://doi.org/10.1038/s41467-023-37190-9

    Example
    -------
    >>> S = xgi.random_simplicial_complex(50, [0.1, 0.01, 0.001], seed=1)
    >>> H = xgi.shuffle_hyperedges(S, order=2, p=0.5)

    """

    rng = np.random.default_rng(seed)

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

    nodes = list(S.nodes)
    d_hyperedges = H.edges.filterby("order", order).members(dtype=dict)

    for id_, members in d_hyperedges.items():
        if rng.random() <= p:
            H.remove_edge(id_)
            new_hyperedge = tuple(rng.choice(nodes, size=order + 1, replace=False))
            while new_hyperedge in H._edge.values():
                new_hyperedge = tuple(rng.choice(nodes, size=order + 1, replace=False))
            H.add_edge(new_hyperedge)

    return H


def node_swap(H, nid1, nid2, order=None):
    """Swap nodes `nid1` and node `nid2` in all edges of order `order`.

    Parameters
    ----------
    H: Hypergraph
        Hypergraph to consider
    nid1: node ID
        ID of first node to swap
    nid2: node ID
        ID of second node to swap
    order: {int, None}, default: None
        If None, consider all orders. If an integer,
        consider edges of that order.

    Returns
    -------
    HH: Hypergraph

    Reference
    ---------
    Zhang, Y.*, Lucas, M.* and Battiston, F., 2023.
    "Higher-order interactions shape collective dynamics differently
    in hypergraphs and simplicial complexes."
    Nature Communications, 14(1), p.1605.
    https://doi.org/10.1038/s41467-023-37190-9

    """

    # check that node ids are in hypergraph
    if not nid1 in H:
        raise ValueError(f"Node {nid1} is not in hypergraph H")
    if not nid2 in H:
        raise ValueError(f"Node {nid2} is not in hypergraph H")

    if order is not None:
        if (order + 1) not in xgi.unique_edge_sizes(H):
            raise ValueError(
                f"There is no hyperedge of order {order} is this hypergraph."
            )

    # get edges of given order
    if order:
        edge_dict = H.edges.filterby("order", order).members(dtype=dict).copy()
    else:  # includes order 0
        edge_dict = H.edges.members(dtype=dict).copy()

    # check that node ids exist in those edges
    if H.nodes.degree(order=order)[nid1] == 0:
        raise ValueError(
            f"Node {nid1} is not part of any hyperedge of the specified order"
        )
    if H.nodes.degree(order=order)[nid2] == 0:
        raise ValueError(
            f"Node {nid2} is not part of any hyperedge of the specified order"
        )

    HH = H.copy()

    # single-pass swap using a mapping dict
    swap_map = {nid1: nid2, nid2: nid1}
    new_edge_dict = {
        key: {swap_map.get(n, n) for n in members} for key, members in edge_dict.items()
    }

    # update hypergraph with new edges
    HH.remove_edges_from(edge_dict)
    HH.add_edges_from(new_edge_dict)

    return HH
