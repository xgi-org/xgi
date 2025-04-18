"""Algorithms related to connected components of a hypergraph."""

from ..core.globalviews import subhypergraph
from ..exception import XGIError

__all__ = [
    "is_connected",
    "connected_components",
    "largest_connected_component",
    "number_connected_components",
    "node_connected_component",
    "largest_connected_hypergraph",
]


def is_connected(H, s=1):
    """
    A function to determine whether a hypergraph is connected.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, optional
        The overlap parameter

    Returns
    -------
    bool
        Whether the hypergraph is connected.

    See Also
    --------
    connected_components
    number_connected_components
    largest_connected_component
    largest_connected_hypergraph

    References
    ----------
    Aksoy, S.G., Joslyn, C., Ortiz Marrero, C. et al.
    Hypernetwork science via high-order hypergraph walks.
    EPJ Data Sci. 9, 16 (2020).
    https://doi.org/10.1140/epjds/s13688-020-00231-0

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(10, [0.5, 0.01], seed=1)
    >>> print(xgi.is_connected(H))
    True

    """
    return len(_plain_bfs(H, list(H.nodes)[0], s=s)) == len(H)


def connected_components(H, s=1):
    """
    A function to find the connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, optional
        The overlap parameter

    Returns
    -------
    iterable of sets
        An iterator where each entry is a component of the hypergraph.

    See Also
    --------
    is_connected
    number_connected_components
    largest_connected_component
    largest_connected_hypergraph

    References
    ----------
    Aksoy, S.G., Joslyn, C., Ortiz Marrero, C. et al.
    Hypernetwork science via high-order hypergraph walks.
    EPJ Data Sci. 9, 16 (2020).
    https://doi.org/10.1140/epjds/s13688-020-00231-0

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.1, 0.01], seed=1)
    >>> print([len(component) for component in xgi.connected_components(H)])
    [50]

    """
    seen = set()
    for v in H:
        if v not in seen:
            c = _plain_bfs(H, v, s=s)
            seen.update(c)
            yield c


def number_connected_components(H, s=1):
    """
    A function to find the number of connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, optional
        The overlap parameter

    Returns
    -------
    int
        The number of connected components of the hypergraph.

    See Also
    --------
    is_connected
    connected_components
    largest_connected_component
    largest_connected_hypergraph

    References
    ----------
    Aksoy, S.G., Joslyn, C., Ortiz Marrero, C. et al.
    Hypernetwork science via high-order hypergraph walks.
    EPJ Data Sci. 9, 16 (2020).
    https://doi.org/10.1140/epjds/s13688-020-00231-0

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.1, 0.01], seed=1)
    >>> print(xgi.number_connected_components(H))
    1

    """
    num_cc = 0
    seen = set()
    for v in H:
        if v not in seen:
            c = _plain_bfs(H, v, s=s)
            seen.update(c)
            num_cc += 1
    return num_cc


def largest_connected_component(H, s=1):
    """
    A function to find the largest connected component of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, optional
        The overlap parameter

    Returns
    -------
    set
        The largest connected component (a set of nodes) of the hypergraph.

    See Also
    --------
    connected_components
    largest_connected_hypergraph

    References
    ----------
    Aksoy, S.G., Joslyn, C., Ortiz Marrero, C. et al.
    Hypernetwork science via high-order hypergraph walks.
    EPJ Data Sci. 9, 16 (2020).
    https://doi.org/10.1140/epjds/s13688-020-00231-0

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.1, 0.01], seed=1)
    >>> print(len(xgi.largest_connected_component(H)))
    50

    """
    return max(connected_components(H, s=s), key=len)


def node_connected_component(H, n, s=1):
    """
    A function to find the connected component of which a node in the
    hypergraph is a part.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    n: hashable
        Node label
    s: int, optional
        The overlap parameter

    See Also
    --------
    connected_components

    Returns
    -------
    set
        Returns the connected component of which the specified node in the
        hypergraph is a part.

    References
    ----------
    Aksoy, S.G., Joslyn, C., Ortiz Marrero, C. et al.
    Hypernetwork science via high-order hypergraph walks.
    EPJ Data Sci. 9, 16 (2020).
    https://doi.org/10.1140/epjds/s13688-020-00231-0

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.1, 0.01], seed=1)
    >>> comp = xgi.node_connected_component(H, 0)
    >>> print(type(comp), len(comp))
    <class 'set'> 50

    """
    if n in H:
        return _plain_bfs(H, n, s=s)
    else:
        raise XGIError("Specified node is not in the hypergraph!")


def largest_connected_hypergraph(H, s=1, in_place=False):
    """
    A function to find the largest connected hypergraph from a data set.

    Parameters
    ----------
    H: Hypergraph
        The hypergraph of interest
    s: int, optional
        The overlap parameter
    in_place: bool, optional
        If False, creates a copy; if True, modifies the existing hypergraph.
        By default, True.

    Returns
    -------
    None
        If in_place: modifies the existing hypergraph

    Hypergraph
        If not in_place: the hypergraph induced on the nodes of the
        largest connected component.

    See Also
    --------
    connected_components
    largest_connected_component

    References
    ----------
    Aksoy, S.G., Joslyn, C., Ortiz Marrero, C. et al.
    Hypernetwork science via high-order hypergraph walks.
    EPJ Data Sci. 9, 16 (2020).
    https://doi.org/10.1140/epjds/s13688-020-00231-0

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(10, [0.1, 0.01], seed=1)
    >>> H_gcc = xgi.largest_connected_hypergraph(H)
    >>> print(H_gcc.num_nodes)
    6
    """
    connected_nodes = max(connected_components(H, s=s), key=len)
    if not in_place:
        return subhypergraph(H, nodes=connected_nodes).copy()
    else:
        H.remove_nodes_from(set(H.nodes).difference(connected_nodes))


def _plain_bfs(H, source, s=1):
    """A helper function to do an edge-first BFS search

    Parameters
    ----------
    H : xgi.Hypergraph
        The hypergraph
    source : hashable
        The ID of the starting node for the BFS
    s : int, optional
        The overlap of edges, by default 1

    Returns
    -------
    set
        A list of all nodes in the s-component.

    References
    ----------
    https://networkx.org/documentation/stable/_modules/networkx/algorithms/components/connected.html

    Aksoy, S.G., Joslyn, C., Ortiz Marrero, C. et al.
    Hypernetwork science via high-order hypergraph walks.
    EPJ Data Sci. 9, 16 (2020).
    https://doi.org/10.1140/epjds/s13688-020-00231-0
    """
    seen_edges = set()
    nodes = {source}
    nextlevel = set(H.edges(H.nodes.memberships(source)).filterby("size", s, "geq"))
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for e in thislevel:
            if e not in seen_edges:
                nodes.update(H.edges.members(e))
                seen_edges.add(e)
                nextlevel.update(H.edges.neighbors(e, s=s))
    return nodes
