import math
import random
import warnings
from collections import defaultdict
from itertools import combinations

import numpy as np
import xgi
from xgi.utils import py_random_state

__all__ = [
    "chung_lu_hypergraph",
    "dcsbm_hypergraph",
    "random_hypergraph",
]


@py_random_state(2)
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
    seed : integer, random_state, or None (default)
            Indicator of random number generation state.

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

    # sort dictionary by degree in decreasing order
    Nlabels = [n for n, _ in sorted(k1.items(), key=lambda d: d[1], reverse=True)]
    Mlabels = [m for m, _ in sorted(k2.items(), key=lambda d: d[1], reverse=True)]

    m = len(k2)

    if sum(k1.values()) != sum(k2.values()):
        warnings.warn(
            "The sum of the degree sequence does not match the sum of the size sequence"
        )

    S = sum(k1.values())

    H = xgi.empty_hypergraph()
    H.add_nodes_from(Nlabels)

    for u in Nlabels:
        j = 0
        v = Mlabels[j]  # start from beginning every time
        p = min((k1[u] * k2[v]) / S, 1)

        while j < m:
            if p != 1:
                r = seed.random()
                j = j + math.floor(math.log(r) / math.log(1 - p))
            if j < m:
                v = Mlabels[j]
                q = min((k1[u] * k2[v]) / S, 1)
                r = seed.random()
                if r < q / p:
                    # no duplicates
                    H.add_node_to_edge(u, v)
                p = q
                j = j + 1

    return H


@py_random_state(2)
def dcsbm_hypergraph(k1, k2, g1, g2, omega, seed=None):
    """A function to generate a DCSBM hypergraph.

    Parameters
    ----------
    k1 : dictionary
        This is a dictionary where the keys are node ids
        and the values are node degrees.
    k2 : dictionary
        This is a dictionary where the keys are edge ids
        and the values are edge degrees also known as edge sizes.
    g1 : dictionary
        This a dictionary where the keys are node ids
        and the values are the group ids to which the node belongs.
        The keys must match the keys of k1.
    g2 : dictionary
        This a dictionary where the keys are edge ids
        and the values are the group ids to which the edge belongs.
        The keys must match the keys of k2.
    omega : 2D numpy array
        This is a matrix with entries which specify the number of edges
        between a given node community and edge community.
        The number of rows must match the number of node communities
        and the number of columns must match the number of edge
        communities.
    seed : integer, random_state, or None (default)
            Indicator of random number generation state.

    Returns
    -------
    Hypergraph object
        The generated hypergraph

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
    >>> import xgi
    >>> import random
    >>> n = 100
    >>> k1 = {i : random.randint(1, 100) for i in range(n)}
    >>> k2 = {i : sorted(k1.values())[i] for i in range(n)}
    >>> g1 = {i : random.choice([0, 1]) for i in range(n)}
    >>> g2 = {i : random.choice([0, 1]) for i in range(n)}
    >>> omega = np.array([[100, 10], [10, 100]])
    >>> H = xgi.dcsbm_hypergraph(k1, k2, g1, g2, omega)

    """

    # sort dictionary by degree in decreasing order
    Nlabels = [n for n, _ in sorted(k1.items(), key=lambda d: d[1], reverse=True)]
    Mlabels = [m for m, _ in sorted(k2.items(), key=lambda d: d[1], reverse=True)]

    # these checks verify that the sum of node and edge degrees and the sum of node degrees
    # and the sum of community connection matrix differ by less than a single edge.
    if abs(sum(k1.values()) - sum(k2.values())) > 1:
        warnings.warn(
            "The sum of the degree sequence does not match the sum of the size sequence"
        )

    if abs(sum(k1.values()) - np.sum(omega)) > 1:
        warnings.warn(
            "The sum of the degree sequence does not match the entries in the omega matrix"
        )

    # get indices for each community
    community1Indices = defaultdict(list)
    for label in Nlabels:
        group = g1[label]
        community1Indices[group].append(label)

    community2Indices = defaultdict(list)
    for label in Mlabels:
        group = g2[label]
        community2Indices[group].append(label)

    H = xgi.empty_hypergraph()
    H.add_nodes_from(Nlabels)

    kappa1 = defaultdict(lambda: 0)
    kappa2 = defaultdict(lambda: 0)
    for id, g in g1.items():
        kappa1[g] += k1[id]
    for id, g in g2.items():
        kappa2[g] += k2[id]

    for group1 in community1Indices.keys():
        for group2 in community2Indices.keys():
            # for each constant probability patch
            try:
                groupConstant = omega[group1, group2] / (
                    kappa1[group1] * kappa2[group2]
                )
            except:
                groupConstant = 0

            for u in community1Indices[group1]:
                j = 0
                v = community2Indices[group2][j]  # start from beginning every time
                # max probability
                p = min(k1[u] * k2[v] * groupConstant, 1)
                while j < len(community2Indices[group2]):
                    if p != 1:
                        r = seed.random()
                        try:
                            j = j + math.floor(math.log(r) / math.log(1 - p))
                        except:
                            j = np.inf
                    if j < len(community2Indices[group2]):
                        v = community2Indices[group2][j]
                        q = min((k1[u] * k2[v]) * groupConstant, 1)
                        r = seed.random()
                        if r < q / p:
                            # no duplicates
                            H.add_node_to_edge(u, v)
                        p = q
                        j = j + 1
    return H


@py_random_state(2)
def random_hypergraph(N, ps, seed=None):
    """Generates a random hypergraph

    Generate N nodes, and connect any d+1 nodes
    by a hyperedge with probability ps[d-1].

    Parameters
    ----------
    N : int
        Number of nodes
    ps : list of float
        List of probabilities (between 0 and 1) to create a
        hyperedge at each order d between any d+1 nodes. For example,
        ps[0] is the wiring probability of any edge (2 nodes), ps[1]
        of any triangles (3 nodes).
    seed : integer, random_state, or None (default)
            Indicator of random number generation state.

    Returns
    -------
    Hypergraph object
        The generated hypergraph
    
    References
    ----------
    Described as 'random hypergraph' by M. Dewar et al. in https://arxiv.org/abs/1703.07686

    Example
    -------
    >>> import xgi
    >>> N = 100
    >>> ps = [0.1, 0.01]
    >>> H = xgi.random_hypergraph(N, ps)

    """

    if (np.any(np.array(ps) < 0)) or (np.any(np.array(ps) > 1)):
        raise ValueError("All elements of ps must be between 0 and 1 included.")

    nodes = range(N)  # list(G.nodes())
    hyperedges = []  # hyperedges = list(G.edges())

    for i, p in enumerate(ps):
        d = i + 1  # order, ps[0] is prob of edges (d=1)

        for hyperedge in combinations(nodes, d + 1):
            if seed.random() <= p:
                hyperedges.append(hyperedge)

    hyperedges += [[i] for i in nodes]  # add singleton edges

    H = xgi.empty_hypergraph()
    H.add_nodes_from(nodes)
    H.add_edges_from(hyperedges)

    return H
