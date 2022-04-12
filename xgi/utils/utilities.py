"""General utilities."""
from collections import defaultdict

__all__ = ['XGICounter', 'get_dual']

class XGICounter:
    """
    A class for a universal counter
    when generating uids.
    """

    def __init__(self):
        """Initialize counter to 0."""
        self._count = 0

    def __call__(self):
        """Return integer then increment counter

        Returns
        -------
        int
            the value before it was incremented

        Examples
        --------
        >>> from hypergraph import HypergraphCounter
        >>> counter = HypergraphCounter()
        >>> counter()
        0
        >>> counter()
        1
        """
        temp = self._count
        self._count += 1
        return temp


def get_dual(edge_dict):
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
    >>> xgi.get_dual({0 : [1, 2, 3], 1 : [0, 2]})
    {1: [0], 2: [0, 1], 3: [0], 0: [1]}
    """
    node_dict = defaultdict(list)
    for edge_id, members in edge_dict.items():
        for node in members:
            node_dict[node].append(edge_id)

    return dict(node_dict)
