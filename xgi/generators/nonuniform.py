"""Generate random (non-uniform) hypergraphs."""
import math
import random
import warnings
from collections import defaultdict
from itertools import combinations

import networkx as nx
import numpy as np
from scipy.special import comb

from ..classes import SimplicialComplex
from .classic import empty_hypergraph, flag_complex_d2, ring_lattice

__all__ = [
    "chung_lu_hypergraph",
    "dcsbm_hypergraph",
    "random_hypergraph",
    "random_simplicial_complex",
    "random_flag_complex_d2",
    "random_flag_complex",
    "watts_strogatz_hypergraph",
]


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
                    j = j + math.floor(math.log(r) / math.log(1 - p))
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
    """A function to generate a DCSBM hypergraph.

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
                            j = j + math.floor(math.log(r) / math.log(1 - p))
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
    seed : integer or None (default)
            Seed for the random number generator.

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
    >>> H = xgi.random_hypergraph(50, [0.1, 0.01])

    """
    if seed is not None:
        np.random.seed(seed)

    if (np.any(np.array(ps) < 0)) or (np.any(np.array(ps) > 1)):
        raise ValueError("All elements of ps must be between 0 and 1 included.")

    nodes = range(N)
    hyperedges = []

    for i, p in enumerate(ps):
        d = i + 1  # order, ps[0] is prob of edges (d=1)

        potential_edges = combinations(nodes, d + 1)
        n_comb = comb(N, d + 1, exact=True)
        mask = np.random.random(size=n_comb) <= p  # True if edge to keep

        edges_to_add = [e for e, val in zip(potential_edges, mask) if val]

        hyperedges += edges_to_add

    H = empty_hypergraph()
    H.add_nodes_from(nodes)
    H.add_edges_from(hyperedges)

    return H


def random_simplicial_complex(N, ps, seed=None):
    """Generates a random hypergraph

    Generate N nodes, and connect any d+1 nodes
    by a simplex with probability ps[d-1]. For each simplex,
    add all its subfaces if they do not already exist.

    Parameters
    ----------
    N : int
        Number of nodes
    ps : list of float
        List of probabilities (between 0 and 1) to create a
        hyperedge at each order d between any d+1 nodes. For example,
        ps[0] is the wiring probability of any edge (2 nodes), ps[1]
        of any triangles (3 nodes).
    seed : int or None (default)
        The seed for the random number generator

    Returns
    -------
    Simplicialcomplex object
        The generated simplicial complex

    References
    ----------
    Described as 'random simplicial complex' in
    "Simplicial Models of Social Contagion", Nature Communications 10(1), 2485,
    by I. Iacopini, G. Petri, A. Barrat & V. Latora (2019).
    https://doi.org/10.1038/s41467-019-10431-6

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_simplicial_complex(20, [0.1, 0.01])

    """

    if seed is not None:
        np.random.seed(seed)

    if (np.any(np.array(ps) < 0)) or (np.any(np.array(ps) > 1)):
        raise ValueError("All elements of ps must be between 0 and 1 included.")

    nodes = range(N)
    simplices = []

    for i, p in enumerate(ps):
        d = i + 1  # order, ps[0] is prob of edges (d=1)

        potential_simplices = combinations(nodes, d + 1)
        n_comb = comb(N, d + 1, exact=True)
        mask = np.random.random(size=n_comb) <= p  # True if simplex to keep

        simplices_to_add = [e for e, val in zip(potential_simplices, mask) if val]

        simplices += simplices_to_add

    S = SimplicialComplex()
    S.add_nodes_from(nodes)
    S.add_simplices_from(simplices)

    return S


def random_flag_complex_d2(N, p, seed=None):
    """Generate a maximal simplicial complex (up to order 2) from a
    :math:`G_{N,p}` Erdős-Rényi random graph by filling all empty triangles with 2-simplices.

    Parameters
    ----------
    N : int
        Number of nodes
    p : float
        Probabilities (between 0 and 1) to create an edge
        between any 2 nodes
    seed : int or None (default)
        The seed for the random number generator

    Returns
    -------
    SimplicialComplex

    Notes
    -----
    Computing all cliques quickly becomes heavy for large networks.
    """
    if seed is not None:
        random.seed(seed)

    if (p < 0) or (p > 1):
        raise ValueError("p must be between 0 and 1 included.")

    G = nx.fast_gnp_random_graph(N, p, seed=seed)

    return flag_complex_d2(G)


def random_flag_complex(N, p, max_order=2, seed=None):
    """Generate a flag (or clique) complex from a
    :math:`G_{N,p}` Erdős-Rényi random graph by filling all cliques up to dimension max_order.

    Parameters
    ----------
    N : int
        Number of nodes
    p : float
        Probabilities (between 0 and 1) to create an edge
        between any 2 nodes
    max_order : int
        maximal dimension of simplices to add to the output simplicial complex
    seed : int or None (default)
        The seed for the random number generator

    Returns
    -------
    SimplicialComplex

    Notes
    -----
    Computing all cliques quickly becomes heavy for large networks.
    """

    if (p < 0) or (p > 1):
        raise ValueError("p must be between 0 and 1 included.")

    G = nx.fast_gnp_random_graph(N, p, seed=seed)

    nodes = G.nodes()
    edges = list(G.edges())

    # compute all triangles to fill
    max_cliques = list(nx.find_cliques(G))

    S = SimplicialComplex()
    S.add_nodes_from(nodes)
    S.add_simplices_from(max_cliques, max_order=max_order)

    return S


def watts_strogatz_hypergraph(n, d, k, l, p, seed=None):
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
