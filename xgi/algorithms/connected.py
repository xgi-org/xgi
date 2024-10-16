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


def is_connected(H):
    """
    A function to determine whether a hypergraph is connected.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

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

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(10, [0.5, 0.01], seed=1)
    >>> print(xgi.is_connected(H))
    True

    """
    return len(_plain_bfs(H, list(H.nodes)[0])) == len(H)


def connected_components(H):
    """
    A function to find the connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

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
            c = _plain_bfs(H, v)
            seen.update(c)
            yield c


def number_connected_components(H):
    """
    A function to find the number of connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

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
            c = _plain_bfs(H, v)
            seen.update(c)
            num_cc += 1
    return num_cc


def largest_connected_component(H):
    """
    A function to find the largest connected component of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

    Returns
    -------
    set
        The largest connected component (a set of nodes) of the hypergraph.

    See Also
    --------
    connected_components
    largest_connected_hypergraph

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.1, 0.01], seed=1)
    >>> print(len(xgi.largest_connected_component(H)))
    50

    """
    return max(connected_components(H), key=len)


def node_connected_component(H, n):
    """
    A function to find the connected component of which a node in the
    hypergraph is a part.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    n: hashable
        Node label

    See Also
    --------
    connected_components

    Returns
    -------
    set
        Returns the connected component of which the specified node in the
        hypergraph is a part.

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(50, [0.1, 0.01], seed=1)
    >>> comp = xgi.node_connected_component(H, 0)
    >>> print(type(comp), len(comp))
    <class 'set'> 50

    """
    if n in H:
        return _plain_bfs(H, n)
    else:
        raise XGIError("Specified node is not in the hypergraph!")


def largest_connected_hypergraph(H, in_place=False):
    """
    A function to find the largest connected hypergraph from a data set.

    Parameters
    ----------
    H: Hypergraph
        The hypergraph of interest
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

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(10, [0.1, 0.01], seed=1)
    >>> H_gcc = xgi.largest_connected_hypergraph(H)
    >>> print(H_gcc.num_nodes)
    6

    """
    connected_nodes = max(connected_components(H), key=len)
    if not in_place:
        return subhypergraph(H, nodes=connected_nodes).copy()
    else:
        H.remove_nodes_from(set(H.nodes).difference(connected_nodes))


def _plain_bfs(H, source):
    """A fast BFS node generator

    Source:
    https://networkx.org/documentation/stable/_modules/networkx/algorithms/components/connected.html
    """
    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                nextlevel.update(H.nodes.neighbors(v))
    return seen
