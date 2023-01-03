"""General utilities."""

from collections import defaultdict
from itertools import chain, combinations, count

__all__ = [
    "dual_dict",
    "powerset",
    "update_uid_counter",
    "find_triangles",
]


def dual_dict(edge_dict):
    """Given a dictionary with IDs as keys
    and lists as values, return the dual.

    Parameters
    ----------
    edge_dict : dict
        A dictionary where the keys are
        IDs and the values are lists of hashables

    Returns
    -------
    dict
        A dictionary with IDs as keys
        and lists as values, but the reverse of
        the original dict.

    Examples
    --------
    >>> import xgi
    >>> xgi.dual_dict({0 : [1, 2, 3], 1 : [0, 2]})
    {1: [0], 2: [0, 1], 3: [0], 0: [1]}

    """
    node_dict = defaultdict(list)
    for edge_id, members in edge_dict.items():
        for node in members:
            node_dict[node].append(edge_id)

    return dict(node_dict)


def powerset(
    iterable, include_empty=False, include_full=False, include_singletons=True
):
    """Returns all possible subsets of the elements in iterable, with options
    to include the empty set and the set containing all elements.

    Parameters
    ----------
    iterable : list-like
        List of elements
    include_empty: bool, default: False
        Whether to include the empty set
    include_singletons: bool, default: True
        Whether to include singletons
    include_full: bool, default: False
        Whether to include the set containing all elements of iterable

    Returns
    -------
    itertools.chain

    Notes
    -----
    include_empty overrides include_singletons if True: singletons will always
    be included if the empty set is.

    Examples
    --------
    >>> import xgi
    >>> list(xgi.powerset([1,2,3,4])) # doctest: +NORMALIZE_WHITESPACE
    [(1,), (2,), (3,), (4,), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),
     (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]

    """

    start = 1 if include_singletons else 2
    start = 0 if include_empty else start  # overrides include_singletons if True
    end = 1 if include_full else 0

    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(start, len(s) + end))


def update_uid_counter(H, new_id):
    """
    Helper function to make sure the uid counter is set correctly after
    adding an edge with a user-provided ID.

    If we don't set the start of self._edge_uid correctly, it will start at 0,
    which will overwrite any existing edges when calling add_edge().  First, we
    use the somewhat convoluted float(e).is_integer() instead of using
    isinstance(e, int) because there exist integer-like numeric types (such as
    np.int32) which fail the isinstance() check.

    Parameters
    ----------
    H : xgi.Hypergraph
        Hypergraph of which to update the uid counter
    id : any hashable type
        User-provided ID.

    """
    uid = next(H._edge_uid)
    if (
        not isinstance(new_id, str)
        and not isinstance(new_id, tuple)
        and float(new_id).is_integer()
        and uid <= new_id
    ):
        # tuple comes from merging edges and doesn't have as as_integer() method.
        start = int(new_id) + 1
        # we set the start at one plus the maximum edge ID that is an integer,
        # because count() only yields integer IDs.
    else:
        start = uid
    H._edge_uid = count(start=start)


def find_triangles(G):
    """Returns list of 3-node cliques present in a graph

    Parameters
    ----------
    G : networkx Graph
        Graph to consider

    Returns
    -------
    list of 3-node cliques (triangles)
    """

    triangles = set(
        frozenset((n, nbr, nbr2))
        for n in G
        for nbr, nbr2 in combinations(G[n], 2)
        if nbr in G[nbr2]
    )
    return [set(tri) for tri in triangles]
