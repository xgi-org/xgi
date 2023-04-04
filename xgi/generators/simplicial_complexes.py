"""Generators for some simplicial complexes.

All the functions in this module return a SimplicialComplex class.

"""

import random
from collections import defaultdict

import networkx as nx

from ..classes.function import subfaces
from ..utils.utilities import find_triangles

__all__ = [
    "flag_complex",
    "flag_complex_d2",
]


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
