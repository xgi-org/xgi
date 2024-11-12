"""Generate random (non-uniform) hypergraphs."""

import random
import warnings
from collections import defaultdict
from itertools import combinations
from math import floor, log
from warnings import warn

import numpy as np
from scipy.special import comb

from .classic import empty_hypergraph
from .lattice import ring_lattice
from .uniform import _index_to_edge_comb

__all__ = [
    "fast_random_hypergraph",
    "random_hypergraph",
    "chung_lu_hypergraph",
    "dcsbm_hypergraph",
    "watts_strogatz_hypergraph",
]


def fast_random_hypergraph(n, ps, order=None, seed=None):
    """Generates a random hypergraph with a fast algorithm.

    Generate `n` nodes, and connect any `d+1` nodes
    by a hyperedge with probability `ps[d-1]`.

    This uses a fast method for generating hyperedges.
    See the references for more details.

    Parameters
    ----------
    n : int
        Number of nodes
    ps : list of float, or float
        List of probabilities (between 0 and 1) to create a
        hyperedge at each order d between any d+1 nodes (when `order` is `None`). For example,
        ps[0] is the wiring probability of any edge (2 nodes), ps[1]
        of any triangles (3 nodes). If a float, generate a uniform hypergraph.
        See `order` for advanced options when it is not `None`.
    order: int, list of ints, or array of ints or None (default)
        If None (default), ignored. If list or array, generates a hypergraph
        with edges of orders `order[0]`, `order[1]`, etc.
        (The length of `ps` must match the length of `order` in this case).
    seed : integer or None (default)
            Seed for the random number generator.

    Returns
    -------
    Hypergraph object
        The generated hypergraph

    References
    ----------
    M. Dewar et al.
    "Subhypergraphs in non-uniform random hypergraphs"
    https://arxiv.org/abs/1703.07686

    Nicholas W. Landry and Juan G. Restrepo,
    "Opinion disparity in hypergraphs with community structure",
    Phys. Rev. E **108**, 034311 (2024).
    https://doi.org/10.1103/PhysRevE.108.034311

    See Also
    --------
    random_hypergraph

    Example
    -------
    >>> import xgi
    >>> H = xgi.fast_random_hypergraph(50, [0.1, 0.01])
    """
    if seed is not None:
        random.seed(seed)

    ps, order = _check_input_args(ps, order)

    nodes = range(n)

    H = empty_hypergraph()
    H.add_nodes_from(nodes)

    for d, p in zip(order, ps):
        if p == 1:
            H.add_edges_from([e for e in combinations(nodes, d + 1)])
        elif p > 0:
            r = random.random()
            index = floor(log(r) / log(1 - p)) - 1  # -1 b/c zero indexing
            max_index = comb(n, d + 1, exact=True)

            while index <= max_index:
                e = set(_index_to_edge_comb(index, n, d + 1))
                H.add_edge(e)
                # We no longer subtract 1 because if we did, the minimum
                # value of the right-hand side would be zero, meaning that
                # we sample the same index multiple times.
                r = random.random()
                index += floor(log(r) / log(1 - p))
    return H


def random_hypergraph(n, ps, order=None, seed=None):
    """Generates a random hypergraph

    Generate N nodes, and connect any d+1 nodes
    by a hyperedge with probability ps[d-1].

    Parameters
    ----------
    n : int
        Number of nodes
    ps : list of float, or float
        List of probabilities (between 0 and 1) to create a
        hyperedge at each order d between any d+1 nodes (when `order` is None). For example,
        ps[0] is the wiring probability of any edge (2 nodes), ps[1]
        of any triangles (3 nodes). If a float, generate a uniform hypergraph
        (in this case, order must be specified)
        See `order` for advanced options when it is not `None`.
    order: int, list of ints, or array of ints or None (default)
        If None, ignore. If list or array, generates a hypergraph
        with edges of orders `order[0]`, `order[1]`, etc.
        (The length of `ps` must match the length of `order` in this case).
    seed : integer, random_state, or None (default)
            Indicator of random number generation state.

    Returns
    -------
    Hypergraph object
        The generated hypergraph

    References
    ----------
    Described as 'random hypergraph' by M. Dewar et al. in https://arxiv.org/abs/1703.07686

    Warns
    -----
    warnings.warn
        Because `fast_random_hypergraph` is a much faster method for generating random hypergraphs.

    See Also
    --------
    fast_random_hypergraph

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.1, 0.01])

    """
    warn("This method is much slower than fast_random_hypergraph")
    if seed is not None:
        random.seed(seed)

    ps, order = _check_input_args(ps, order)

    nodes = range(n)
    H = empty_hypergraph()
    H.add_nodes_from(nodes)

    for d, p in zip(order, ps):
        for edge in combinations(nodes, d + 1):
            if random.random() <= p:
                H.add_edge(edge)
    return H


def _check_input_args(ps, order):
    """Check input args for random_hypergraph and fast_random_hypergraph"""
    if order is None:
        if not isinstance(ps, (list, np.ndarray)):
            raise ValueError(
                "If order is not specified, ps must be a list or numpy array!"
            )
        order = [i + 1 for i in range(len(ps))]
    else:
        if isinstance(order, int):
            if not isinstance(ps, float):
                raise ValueError("If order is an int, ps must be a float")
            else:
                order = [order]
                ps = [ps]
        elif isinstance(order, (list, np.ndarray)) and isinstance(
            ps, (list, np.ndarray)
        ):
            if len(ps) != len(order):
                raise ValueError("The length ps must match the length of order")
        else:
            raise ValueError("Invalid entries!")

    ps = np.array(ps)
    order = np.array(order)

    if (np.any(np.array(ps) < 0)) or (np.any(np.array(ps) > 1)):
        raise ValueError("All elements of ps must be between 0 and 1 included.")

    if (order < 0).any():
        raise ValueError("All elements of ps must be between 0 and 1 included.")

    return ps, order


def chung_lu_hypergraph(k1, k2, seed=None):
    """A function to generate a Chung-Lu hypergraph

    Parameters
    ----------
    k1 : dictionary
        Dictionary where the keys are node ids
        and the values are node degrees.
    k2 : dictionary
        Dictionary where the keys are edge ids
        and the values are edge sizes.
    seed : integer or None (default)
            The seed for the random number generator.

    Returns
    -------
    Hypergraph object
        The generated hypergraph

    Warns
    -----
    warnings.warn
        If the sums of the edge sizes and node degrees are not equal, the
        algorithm still runs, but raises a warning.

    Notes
    -----
    The sums of k1 and k2 should be the same. If they are not the same,
    this function returns a warning but still runs.

    References
    ----------
    Implemented by Mirah Shi in HyperNetX and described for
    bipartite networks by Aksoy et al. in https://doi.org/10.1093/comnet/cnx001

    Example
    -------
    >>> import xgi
    >>> import random
    >>> n = 100
    >>> k1 = {i : random.randint(1, 100) for i in range(n)}
    >>> k2 = {i : sorted(k1.values())[i] for i in range(n)}
    >>> H = xgi.chung_lu_hypergraph(k1, k2)

    """
    if seed is not None:
        random.seed(seed)

    # sort dictionary by degree in decreasing order
    node_labels = [n for n, _ in sorted(k1.items(), key=lambda d: d[1], reverse=True)]
    edge_labels = [m for m, _ in sorted(k2.items(), key=lambda d: d[1], reverse=True)]

    m = len(k2)

    if sum(k1.values()) != sum(k2.values()):
        warnings.warn(
            "The sum of the degree sequence does not match the sum of the size sequence"
        )

    S = sum(k1.values())

    H = empty_hypergraph()
    H.add_nodes_from(node_labels)

    for u in node_labels:
        j = 0
        v = edge_labels[j]  # start from beginning every time
        p = min((k1[u] * k2[v]) / S, 1)

        while j < m:
            if p != 1:
                r = random.random()
                try:
                    j = j + floor(log(r) / log(1 - p))
                except ZeroDivisionError:
                    j = np.inf

            if j < m:
                v = edge_labels[j]
                q = min((k1[u] * k2[v]) / S, 1)
                r = random.random()
                if r < q / p:
                    # no duplicates
                    H.add_node_to_edge(v, u)
                p = q
                j = j + 1

    return H


def dcsbm_hypergraph(k1, k2, g1, g2, omega, seed=None):
    """A function to generate a Degree-Corrected Stochastic Block Model
    (DCSBM) hypergraph.

    Parameters
    ----------
    k1 : dict
        This is a dictionary where the keys are node ids
        and the values are node degrees.
    k2 : dict
        This is a dictionary where the keys are edge ids
        and the values are edge sizes.
    g1 : dict
        This a dictionary where the keys are node ids
        and the values are the group ids to which the node belongs.
        The keys must match the keys of k1.
    g2 : dict
        This a dictionary where the keys are edge ids
        and the values are the group ids to which the edge belongs.
        The keys must match the keys of k2.
    omega : 2D numpy array
        This is a matrix with entries which specify the number of edges
        between a given node community and edge community.
        The number of rows must match the number of node communities
        and the number of columns must match the number of edge
        communities.
    seed : int or None (default)
        Seed for the random number generator.

    Returns
    -------
    Hypergraph

    Warns
    -----
    warnings.warn
        If the sums of the edge sizes and node degrees are not equal, the
        algorithm still runs, but raises a warning.
        Also if the sum of the omega matrix does not match the sum of degrees,
        a warning is raised.

    Notes
    -----
    The sums of k1 and k2 should be the same. If they are not the same, this function
    returns a warning but still runs. The sum of k1 (and k2) and omega should be the
    same. If they are not the same, this function returns a warning but still runs and
    the number of entries in the incidence matrix is determined by the omega matrix.

    References
    ----------
    Implemented by Mirah Shi in HyperNetX and described for bipartite networks by
    Larremore et al. in https://doi.org/10.1103/PhysRevE.90.012805

    Examples
    --------
    >>> import xgi; import random; import numpy as np
    >>> n = 50
    >>> k1 = {i : random.randint(1, n) for i in range(n)}
    >>> k2 = {i : sorted(k1.values())[i] for i in range(n)}
    >>> g1 = {i : random.choice([0, 1]) for i in range(n)}
    >>> g2 = {i : random.choice([0, 1]) for i in range(n)}
    >>> omega = np.array([[n//2, 10], [10, n//2]])
    >>> # H = xgi.dcsbm_hypergraph(k1, k2, g1, g2, omega)

    """
    if seed is not None:
        random.seed(seed)

    # sort dictionary by degree in decreasing order
    node_labels = [n for n, _ in sorted(k1.items(), key=lambda d: d[1], reverse=True)]
    edge_labels = [m for m, _ in sorted(k2.items(), key=lambda d: d[1], reverse=True)]

    # Verify that the sum of node and edge degrees and the sum of node degrees and the
    # sum of community connection matrix differ by less than a single edge.
    if abs(sum(k1.values()) - sum(k2.values())) > 1:
        warnings.warn(
            "The sum of the degree sequence does not match the sum of the size sequence"
        )

    if abs(sum(k1.values()) - np.sum(omega)) > 1:
        warnings.warn(
            "The sum of the degree sequence does not "
            "match the entries in the omega matrix"
        )

    # get indices for each community
    community1_nodes = defaultdict(list)
    for label in node_labels:
        group = g1[label]
        community1_nodes[group].append(label)

    community2_nodes = defaultdict(list)
    for label in edge_labels:
        group = g2[label]
        community2_nodes[group].append(label)

    H = empty_hypergraph()
    H.add_nodes_from(node_labels)

    kappa1 = defaultdict(lambda: 0)
    kappa2 = defaultdict(lambda: 0)
    for id, g in g1.items():
        kappa1[g] += k1[id]
    for id, g in g2.items():
        kappa2[g] += k2[id]

    for group1 in community1_nodes.keys():
        for group2 in community2_nodes.keys():
            # for each constant probability patch
            try:
                group_constant = omega[group1, group2] / (
                    kappa1[group1] * kappa2[group2]
                )
            except ZeroDivisionError:
                group_constant = 0

            for u in community1_nodes[group1]:
                j = 0
                v = community2_nodes[group2][j]  # start from beginning every time
                # max probability
                p = min(k1[u] * k2[v] * group_constant, 1)
                while j < len(community2_nodes[group2]):
                    if p != 1:
                        r = random.random()
                        try:
                            j = j + floor(log(r) / log(1 - p))
                        except ZeroDivisionError:
                            j = np.inf
                    if j < len(community2_nodes[group2]):
                        v = community2_nodes[group2][j]
                        q = min((k1[u] * k2[v]) * group_constant, 1)
                        r = random.random()
                        if r < q / p:
                            # no duplicates
                            H.add_node_to_edge(v, u)
                        p = q
                        j = j + 1
    return H


def watts_strogatz_hypergraph(n, d, k, l, p, seed=None):
    """Generates a Watts-Strogatz hypergraph

    Parameters
    ----------
    n : int
        Number of nodes
    d : int
        Edge size
    k : int
        Number of edges of which a node is a part. Should be a multiple of 2.
    l : int
        Overlap between edges
    p : float
        The rewiring probability
    seed : int, optional
        The seed for the random number generator, by default None

    Returns
    -------
    xgi.Hypergraph
        THe Watts-Strogatz hypergraph

    See Also
    --------
    ~lattice.ring_lattice

    References
    ----------
    Tanu Raghav, Stefano Boccaletti, and Sarika Jalan,
    Smallworldness in hypergraphs,
    https://doi.org/10.1088/2632-072X/acf430
    """
    if seed is not None:
        np.random.seed(seed)
    H = ring_lattice(n, d, k, l)
    to_remove = []
    to_add = []
    for e in H.edges:
        if np.random.random() < p:
            to_remove.append(e)
            node = min(H.edges.members(e))
            neighbors = np.random.choice(H.nodes, size=d - 1)
            to_add.append(np.append(neighbors, node))
    H.remove_edges_from(to_remove)
    H.add_edges_from(to_add)
    return H
