"""Functions to randomize hypergaphs

All the functions in this module return a Hypergraph class (i.e. a simple, undirected
hypergraph).
"""

import random
from copy import deepcopy

import xgi

__all__ = [
    "shuffle_hyperedges",
    "node_swap",
    "random_edge_shuffle",
    "run_markov_chain",
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

    Note
    ----
    By shuffling hyperedges in a simplicial complex, it will in general lose
    its "simpliciality" and become a hypergraph.

    Reference
    ---------
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
        if random.random() <= p:
            H.remove_edge(id_)
            new_hyperedge = tuple(random.sample(nodes, order + 1))
            while new_hyperedge in H._edge.values():
                new_hyperedge = tuple(random.sample(nodes, order + 1))
            H.add_edge(new_hyperedge)

    return H


def node_swap(H, nid1, nid2, id_temp=-1, order=None):
    """Swap nodes `nid1` and node `nid2` in all edges of order `order`.

    Parameters
    ----------
    H: HyperGraph
        Hypergraph to consider
    nid1: node ID
        ID of first node to swap
    nid2: node ID
        ID of second node to swap
    id_temp: node ID
        Temporary ID given to nodes when swapping
    order: {int, None}, default: None
        If None, consider all orders. If an integer,
        consider edges of that order.

    Returns
    -------
    HH: HyperGraph

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

    # make sure id_temps does not exist yet
    while id_temp in H.edges:
        id_temp -= 1

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

    new_edge_dict = deepcopy(edge_dict)
    HH = H.copy()

    # replace nid1 by temporary id in edges
    for key, members in edge_dict.items():
        if nid1 in members:
            members.remove(nid1)
            members.add(id_temp)
        new_edge_dict[key] = members

    # replace nid2 by nid1 in edges
    for key, members in new_edge_dict.items():
        if nid2 in members:
            members.remove(nid2)
            members.add(nid1)
        new_edge_dict[key] = members

    # replace temporary id by nid2 in edges
    for key, members in new_edge_dict.items():
        if id_temp in members:
            members.remove(id_temp)
            members.add(nid2)
        new_edge_dict[key] = members

    # update hypergraph with new edges
    HH.remove_edges_from(edge_dict)
    HH.add_edges_from(new_edge_dict)

    return HH


def random_edge_shuffle(H, e_id1=None, e_id2=None):
    """Randomly redistributes nodes between two hyperedges.

    The process is as follows:

    1. randomly select two hyperedges
    2. place all their nodes into a single bucket
    3. randomly redistribute the nodes between those two hyperedges

    Parameters
    ----------
    H : xgi.HyperGraph
        Hypergraph to shuffle two edges
    e_id1 : node ID, optional
        ID of first edge to shuffle.
    e_id2 : node ID, optional
        ID of second edge to shuffle.

    Note
    ----
    After shuffling, the sizes of the two hyperedges are unchanged.
    Edge IDs and attributes are also unchanged.
    If the same node appears in both hyperedges, then this is still true after reshuffling.
    If either `e_id1` or `e_id2` is not provided, then two random edges are selected.

    Reference
    ---------
    Philip S C., 2020.
    "Configuration models of random hypergraphs."
    Journal of Complex Networks, 8(3).
    https://doi.org/10.1093/comnet/cnaa018

    Example
    -------
    >>> random.seed(42)
    >>> H = xgi.Hypergraph([[1, 2, 3], [3, 4], [4, 5]])
    >>> xgi.random_edge_shuffle(H)
    >>> H.edges.members()
    [{2, 4, 5}, {3, 4}, {1, 3}]

    """
    if len(H._edge) < 2:
        raise ValueError("Hypergraph must have at least two edges.")

    # select two random edges
    if e_id1 is None or e_id2 is None:
        e_id1, e_id2 = random.sample(list(H._edge), 2)

    # get nodes in those edges
    nodes_e1 = H._edge[e_id1]
    nodes_e2 = H._edge[e_id2]

    # nodes in both edges should not be shuffled
    nodes_both = nodes_e1 & nodes_e2
    nodes_e1 -= nodes_both
    nodes_e2 -= nodes_both

    # put all nodes in a single bucket
    nodes = nodes_e1 | nodes_e2

    # randomly redistribute nodes between the two edges
    nodes_e1_new = set(random.sample(list(nodes), len(nodes_e1)))
    nodes_e2_new = nodes - nodes_e1_new

    # update edge memberships
    for n_id in nodes_e1_new & nodes_e2:
        H._node[n_id].remove(e_id2)
        H._node[n_id].add(e_id1)

    for n_id in nodes_e2_new & nodes_e1:
        H._node[n_id].remove(e_id1)
        H._node[n_id].add(e_id2)

    # add nodes in both edges back
    nodes_e1_new |= nodes_both
    nodes_e2_new |= nodes_both

    # update hypergraph
    H._edge[e_id1] = nodes_e1_new
    H._edge[e_id2] = nodes_e2_new


def run_markov_chain(S, n_steps, sample_interval, sample_fun):
    """Repeatedly shuffle edges as a Markov chain process, and samples a metric.

    Every `sample_interval` steps, the result of `sample_fun(S)` is collected.

    Parameters
    ----------
    S : xgi.HyperGraph
        Hypergraph to shuffle
    n_steps : int
        Number of steps to run the Markov chain for
    sample_interval : int
        Number of steps between each sample
    sample_fun : callable
        Function to call to sample a metric from the hypergraph

    Returns
    -------
    metrics : list
        List of metrics sampled from the hypergraph
    """
    metrics = []
    for i in range(n_steps):
        random_edge_shuffle(S)
        if i % sample_interval == 0:
            metrics.append(sample_fun(S))
    return metrics
