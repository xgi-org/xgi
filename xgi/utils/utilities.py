"""General utilities."""
from collections import defaultdict

import requests

import xgi
from xgi.exception import XGIError

__all__ = ["XGICounter", "get_dual", "load_xgi_data"]


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


dataset_urls = {
    "congress-bills": "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/data/congress-bills/congress-bills.json",
    "tags-ask-ubuntu": "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/data/tags-ask-ubuntu/tags-ask-ubuntu.json",
    "email-eu": "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/data/email-Eu/email-Eu.json",
    "email-enron": "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/data/email-Enron/email-Enron.json",
}


def load_xgi_data(dataset, nodetype=None, edgetype=None):
    """_summary_

    Parameters
    ----------
    dataset : str
        Dataset name. Valid options are the following:

        * congress-bills
        * email-enron
        * email-eu
        * tags-ask-ubuntu

    nodetype : type, optional
        type to cast the node ID to
    edgetype : type, optional
        type to cast the edge ID to

    Returns
    -------
    xgi.Hypergraph
        The loaded hypergraph

    Raises
    ------
    XGIError
       The specified dataset does not exist.
    """
    if dataset not in dataset_urls:
        raise XGIError("Invalid dataset specifier!")

    r = requests.get(dataset_urls[dataset])

    return _dict_to_hypergraph(r.json(), nodetype=nodetype, edgetype=edgetype)


def _dict_to_hypergraph(hypergraph_dict, nodetype=None, edgetype=None):
    """
    A function to read a file in a standardized JSON format.

    Parameters
    ----------
    hypergraph_dict: dict
        A dictionary in the hypergraph JSON format
    nodetype: type, optional
        type that the node IDs will be cast to
    edgetype: type, optional
        type that the edge IDs will be cast to

    Returns
    -------
    A Hypergraph object
        The loaded hypergraph

    Raises
    ------
    XGIError
        If the JSON is not in a format that can be loaded.

    See Also
    --------
    read_hypergraph_json
    """

    H = xgi.empty_hypergraph()
    try:
        H._hypergraph.update(hypergraph_dict["hypergraph-data"])
    except KeyError:
        raise XGIError("Failed to get hypergraph data attributes.")

    try:
        for id, dd in hypergraph_dict["node-data"].items():
            if nodetype is not None:
                try:
                    id = nodetype(id)
                except Exception as e:
                    raise TypeError(
                        f"Failed to convert edge IDs to type {nodetype}."
                    ) from e
            H.add_node(id, **dd)
    except KeyError:
        raise XGIError("Failed to import node attributes.")

    try:
        for id, edge in hypergraph_dict["edge-dict"].items():
            if edgetype is not None:
                try:
                    id = edgetype(id)
                except Exception as e:
                    raise TypeError(
                        f"Failed to convert the edge with ID {id} to type {edgetype}."
                    ) from e

            if nodetype is not None:
                try:
                    edge = [nodetype(n) for n in edge]
                except Exception as e:
                    raise TypeError(
                        f"Failed to convert nodes to type {nodetype}."
                    ) from e
            H.add_edge(edge, id)
    except:
        raise XGIError("Failed to import edge dictionary.")

    try:
        xgi.set_edge_attributes(
            H,
            hypergraph_dict["edge-data"]
            if edgetype is None
            else {edgetype(e): dd for e, dd in hypergraph_dict["edge-data"].items()},
        )
    except KeyError:
        raise XGIError("Failed to import edge attributes.")

    return H
