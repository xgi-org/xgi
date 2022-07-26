"""Generators for some classic hypergraphs.

All the functions in this module return a Hypergraph class (i.e. a simple, undirected
hypergraph).

"""

from itertools import combinations

import networkx as nx
import numpy as np

from ..classes import SimplicialComplex
from ..utils import py_random_state

__all__ = [
    "empty_hypergraph",
    "empty_simplicial_complex",
    "star_clique",
    "flag_complex",
]


def _empty_network(create_using, default):
    """Return an empty network.

    See Also
    --------
    empty_hypergraph
    empty_simplicial_complex

    """
    if create_using is None:
        H = default()
    elif hasattr(create_using, "_node"):
        # create_using is a Hypergraph object
        create_using.clear()
        H = create_using
    else:
        # try create_using as constructor
        H = create_using()
    return H


def empty_hypergraph(create_using=None, default=None):
    """Returns the empty hypergraph with zero nodes and edges.

    Parameters
    ----------
    create_using : Hypergraph Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty hypergraph.
    default : Hypergraph constructor (default None)
        The constructor to use if create_using is None.
        If None, then xgi.Hypergraph is used.

    Returns
    -------
    Hypergraph object
        An empty hypergraph

    Examples
    --------
    >>> import xgi
    >>> H = xgi.empty_hypergraph()
    >>> H.num_nodes, H.num_edges
    (0, 0)

    """
    # this import needs to happen when the function runs, not when the module is first
    # imported, to avoid circular imports
    import xgi

    if default is None:
        default = xgi.Hypergraph
    return _empty_network(create_using, default)


def empty_simplicial_complex(create_using=None, default=None):
    """Returns the empty simplicial complex with zero nodes and simplices.

    Parameters
    ----------
    create_using : SimplicialComplex Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty simplicial complex.
    default : SimplicialComplex constructor (default None)
        The constructor to use if create_using is None.
        If None, then xgi.SimplicialComplex is used.

    Returns
    -------
    SimplicialComplex
        An empty simplicial complex.

    Examples
    --------
    >>> import xgi
    >>> H = xgi.empty_simplicial_complex()
    >>> H.num_nodes, H.num_edges
    (0, 0)

    """
    # this import needs to happen when the function runs, not when the module is first
    # imported, to avoid circular imports
    import xgi

    if default is None:
        default = xgi.SimplicialComplex
    return _empty_network(create_using, default)


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


@py_random_state("seed")
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

    Returns
    -------
    S : SimplicialComplex

    Notes
    -----
    Computing all cliques quickly becomes heavy for large networks.

    """
    # This import needs to happen when this function is called, not when it is
    # defined.  Otherwise, a circular import error would happen.

    nodes = G.nodes()
    edges = G.edges()

    # compute all triangles to fill
    max_cliques = list(nx.find_cliques(G))

    S = SimplicialComplex()
    S.add_nodes_from(nodes)
    S.add_simplices_from(edges)
    if not ps: # promote all cliques
        S.add_simplices_from(max_cliques, max_order=max_order)
    else: # promote cliques with a given probability
        for i, p in enumerate(ps[:max_order - 1]):
            d = i + 2 # simplex order
            cliques_d = [x for x in max_cliques if len(x) == d + 1]
            cliques_d_to_add = []
            for el in cliques_d:
                if seed.random() <= p:
                    cliques_d_to_add.append(el)
            S.add_simplices_from(cliques_d_to_add, max_order=max_order)

    return S
