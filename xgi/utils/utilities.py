"""General utilities."""
from collections import defaultdict

import requests

from .. import convert
from ..exception import XGIError

__all__ = ["get_dual", "load_xgi_data"]


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
    """_summary_

    Parameters
    ----------
    dataset : str
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository.

    nodetype : type, optional
        type to cast the node ID to
    edgetype : type, optional
        type to cast the edge ID to

    Returns
    -------
    Hypergraph
        The loaded hypergraph.

    Raises
    ------
    XGIError
       The specified dataset does not exist.
    """
    index_url = "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/index.json"
    index = requests.get(index_url).json()
    if dataset not in index:
        raise XGIError("Invalid dataset specifier!")

    r = requests.get(index[dataset]["url"])

    return convert.dict_to_hypergraph(r.json(), nodetype=nodetype, edgetype=edgetype)
