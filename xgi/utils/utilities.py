"""General utilities."""

from collections import defaultdict
from itertools import chain, combinations

__all__ = ["dual_dict", "powerset"]


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


def powerset(iterable, include_empty=False, include_full=False):
    """Returns all possible subsets of the elements in iterable, with options
    to include the empty set and the set containing all elements.

    Parameters
    ----------
    iterable : list-like
        List of elements
    include_empty: bool, default: False
        Whether to include the empty set
    include_full: bool, default: False
        Whether to include the set containing all elements of iterable

    Returns
    -------
    itertools.chain

    Examples
    --------
    >>> import xgi
    >>> list(xgi.powerset([1,2,3,4])) # doctest: +NORMALIZE_WHITESPACE
    [(1,), (2,), (3,), (4,), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),
     (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]

    """

    start = 0 if include_empty else 1
    end = 1 if include_full else 0

    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(start, len(s) + end))
