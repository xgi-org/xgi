import networkx as nx
import hypergraph as hg
from hypergraph.exception import HypergraphError
import scipy.sparse as sparse
import random

__all__ = [
    "is_connected",
    "connected_components",
    "number_connected_components",
    "node_connected_component",
    "is_connected_bfs",
]


def is_connected(H, s=1):
    """
    A function to determine whether a hypergraph is s-connected.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, default: 1
        Specifies the s-connected level

    Returns
    -------
    is_connected: boolean
        Specifies whether the hypergraph is s-connected.

    Example
    -------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> print(hg.is_connected(H))
    """
    data = sparse.find(hg.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.is_connected(nx.Graph(zip(rows, cols)))


def connected_components(H, s=1):
    """
    A function to find the s-connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, default: 1
        Specifies the s-connected level

    Returns
    -------
    components: iteratble of lists
        A list where each entry is an s-component of the hypergraph.

    Example
    -------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> print([len(component) for component in hg.connected_components(H)])
    """
    data = sparse.find(hg.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.connected_components(nx.Graph(zip(rows, cols)))


def number_connected_components(H, s=1):
    """
    A function to find the number of s-connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, default: 1
        Specifies the s-connected level

    Returns
    -------
    num_components: int
        Returns the number of s-connected components of a hypergraph.

    Example
    -------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> print(hg.number_connected_components(H))
    """
    return len(connected_components(H, s=s))


def node_connected_component(H, n, s=1):
    """
    A function to find the s-connected component of which a node in the
    hypergraph is a part.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    n: hashable
        Node label
    s: int, default: 1
        Specifies the s-connected level

    Returns
    -------
    component: list
        Returns the s-connected component of which the specified node in the
        hypergraph is a part.

    Example
    -------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> print(hg.node_connected_component(H, 0))
    """
    data = sparse.find(hg.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.node_connected_component(nx.Graph(zip(rows, cols)), n)


def is_connected_bfs(H):
    """
    A function to determine whether a hypergraph is connected.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

    Returns
    -------
    is_connected: boolean
        Specifies whether the hypergraph is s-connected.

    Example
    -------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> print(hg.is_connected(H))

    Notes
    -----
    This currently does not check for s-connectedness.
    """
    return len(_plain_bfs(H, random.choice(list(H.nodes)))) == len(H)


def _plain_bfs(H, source):
    """A fast BFS node generator"""
    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                nextlevel.update(H.neighbors(v))
    return seen
