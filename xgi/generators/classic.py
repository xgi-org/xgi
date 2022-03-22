"""Generators for some classic hypergraphs. All the functions
in this module return a Hypergraph class (i.e. a simple, undirected hypergraph).
"""

from itertools import combinations

from xgi.classes import Hypergraph

__all__ = ["empty_hypergraph", "star_clique"]


def empty_hypergraph(create_using=None, default=Hypergraph):
    """Returns the empty hypergraph with zero nodes and edges.

    Parameters
    ----------
    create_using : Hypergraph Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty hypergraph.
    default : Hypergraph constructor (optional, default = xgi.Hypergraph)
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
    >>> H.num_nodes
    0
    >>> H.num_edges
    0
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
    H : xgi.Hypergraph

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
