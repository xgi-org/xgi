"""General utilities."""
import json
from collections import defaultdict

import requests

import xgi
from xgi.exception import XGIError

__all__ = ["XGICounter", "get_dual", "load_xgi_data"]

dataset_urls = {
    "congress-bills": "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/data/congress-bills/congress-bills.json",
    "tags-ask-ubuntu": "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/data/tags-ask-ubuntu/tags-ask-ubuntu.json",
    "email-eu": "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/data/email-Eu/email-Eu.json",
    "email-enron": "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/data/email-Enron/email-Enron.json",
}


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


def load_xgi_data(dataset, nodetype=None, edgetype=None):

    if dataset not in dataset_urls:
        raise XGIError("Invalid dataset specifier!")

    r = requests.get(dataset_urls[dataset])

    return xgi.read_hypergraph_json(r.json(), nodetype=nodetype, edgetype=edgetype)
