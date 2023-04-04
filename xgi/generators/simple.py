"""Generators for some simple hypergraphs.

All the functions in this module return a Hypergraph class (i.e. a simple, undirected
hypergraph).

"""

import random
from collections import defaultdict
from itertools import combinations

import networkx as nx

from ..classes.function import subfaces
from ..exception import XGIError
from ..utils.utilities import find_triangles
from .classic import empty_hypergraph

__all__ = [
    "star_clique",
    "flag_complex",
    "flag_complex_d2",
    "sunflower",
]


def star_clique(n_star, n_clique, d_max):
    """Generate a star-clique structure

    That is a star network and a clique network,
    connected by one pairwise edge connecting the centre of the star to the clique.
    network, the each clique is promoted to a hyperedge
    up to order d_max.

    Parameters
    ----------
    n_star : int
        Number of legs of the star
    n_clique : int
        Number of nodes in the clique
    d_max : int
        Maximum order up to which to promote
        cliques to hyperedges

    Returns
    -------
    H : Hypergraph

    Examples
    --------
    >>> import xgi
    >>> H = xgi.star_clique(6, 7, 2)

    Notes
    -----
    The total number of nodes is n_star + n_clique.

    """

    if n_star <= 0:
        raise ValueError("n_star must be an integer > 0.")
    if n_clique <= 0:
        raise ValueError("n_clique must be an integer > 0.")
    if d_max < 0:
        raise ValueError("d_max must be an integer >= 0.")
    elif d_max > n_clique - 1:
        raise ValueError("d_max must be <= n_clique - 1.")

    nodes_star = range(n_star)
    nodes_clique = range(n_star, n_star + n_clique)
    nodes = list(nodes_star) + list(nodes_clique)

    H = empty_hypergraph()
    H.add_nodes_from(nodes)

    # add star edges (center of the star is 0-th node)
    H.add_edges_from([(nodes_star[0], nodes_star[i]) for i in range(1, n_star)])

    # connect clique and star by adding last star leg
    H.add_edge((nodes_star[0], nodes_clique[0]))

    # add clique hyperedges up to order d_max
    H.add_edges_from(
        [e for d in range(1, d_max + 1) for e in combinations(nodes_clique, d + 1)]
    )

    return H


def flag_complex(G, max_order=2, ps=None, seed=None):
    """Generate a flag (or clique) complex from a
    NetworkX graph by filling all cliques up to dimension max_order.

    Parameters
    ----------
    G : Networkx Graph

    max_order : int
        maximal dimension of simplices to add to the output simplicial complex
    ps: list of float
        List of probabilities (between 0 and 1) to create a
        hyperedge from a clique, at each order d. For example,
        ps[0] is the probability of promoting any 3-node clique (triangle) to
        a 3-hyperedge.
    seed: int or None (default)
        The seed for the random number generator

    Returns
    -------
    S : SimplicialComplex

    Notes
    -----
    Computing all cliques quickly becomes heavy for large networks. `flag_complex_d2`
    is faster to compute up to order 2.

    See also
    --------
    flag_complex_d2

    """
    # This import needs to happen when this function is called, not when it is
    # defined.  Otherwise, a circular import error would happen.
    from ..classes import SimplicialComplex

    if seed is not None:
        random.seed(seed)

    nodes = G.nodes()
    edges = G.edges()

    # compute all maximal cliques to fill
    max_cliques = list(nx.find_cliques(G))

    S = SimplicialComplex()
    S.add_nodes_from(nodes)
    S.add_simplices_from(edges)
    if not ps:  # promote all cliques
        S.add_simplices_from(max_cliques, max_order=max_order)
        return S

    if max_order:  # compute subfaces of order max_order (allowed max cliques)
        max_cliques_to_add = subfaces(max_cliques, order=max_order)
    else:
        max_cliques_to_add = max_cliques

    # store max cliques per order
    cliques_d = defaultdict(list)
    for x in max_cliques_to_add:
        cliques_d[len(x)].append(x)

    # promote cliques with a given probability
    for i, p in enumerate(ps[: max_order - 1]):
        d = i + 2  # simplex order
        cliques_d_to_add = [el for el in cliques_d[d + 1] if random.random() <= p]
        S.add_simplices_from(cliques_d_to_add, max_order=max_order)

    return S


def flag_complex_d2(G, p2=None, seed=None):
    """Generate a flag (or clique) complex from a
    NetworkX graph by filling all cliques up to dimension 2.

    Parameters
    ----------
    G : networkx Graph
        Graph to consider
    p2: float
        Probability (between 0 and 1) of filling empty triangles in graph G
    seed: int or None (default)
        The seed for the random number generator

    Returns
    -------
    S : xgi.SimplicialComplex

    Notes
    -----
    Computing all cliques quickly becomes heavy for large networks. This
    is faster than `flag_complex` to compute up to order 2.

    See also
    --------
    flag_complex
    """
    # This import needs to happen when this function is called, not when it is
    # defined.  Otherwise, a circular import error would happen.
    from ..classes import SimplicialComplex

    if seed is not None:
        random.seed(seed)

    nodes = G.nodes()
    edges = G.edges()

    S = SimplicialComplex()
    S.add_nodes_from(nodes)
    S.add_simplices_from(edges)

    triangles_empty = find_triangles(G)

    if p2 is not None:
        triangles = [el for el in triangles_empty if random.random() <= p2]
    else:
        triangles = triangles_empty

    S.add_simplices_from(triangles)

    return S


def sunflower(l, c, m):
    """Create a sunflower hypergraph.

    This creates an m-uniform hypergraph
    according to the sunflower model.

    Parameters
    ----------
    l : int
        Number of petals
    c : int
        Size of the core
    m : int
        Size of each edge

    Raises
    ------
    XGIError
        If the edge size is smaller than the core.

    Returns
    -------

    """
    from ..classes import Hypergraph

    if m < c:
        raise XGIError("m cannot be smaller than c.")

    core_nodes = list(range(c))

    H = Hypergraph()
    start_label = c
    while start_label + (m - c) <= c + (m - c) * l:
        H.add_edge(core_nodes + [start_label + i for i in range(m - c)])
        start_label = start_label + (m - c)

    return H
