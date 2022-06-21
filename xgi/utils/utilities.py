"""General utilities."""
from collections import defaultdict

import requests

from .. import convert
from ..classes import Hypergraph
from ..exception import XGIError

__all__ = ["get_dual", "load_xgi_data", "convert_labels_to_integers"]


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


def convert_labels_to_integers(H, label_attribute="label"):
    """Relabel node and edge IDs to be sequential integers.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest

    label_attribute : string, default: "label"
        The attribute name that stores the old node and edge labels

    Returns
    -------
    Hypergraph
        A new hypergraph with nodes and edges with sequential IDs starting at 0.
        The old IDs are stored in the "label" attribute for both nodes and edges.

    Notes
    -----
    The "relabeling" will occur even if the node/edge IDs are sequential.
    Because the old IDs are stored in the "label" attribute for both nodes and edges,
    the old "label" values (if they exist) will be overwritten.
    """
    node_dict = dict(zip(H.nodes, range(H.num_nodes)))
    edge_dict = dict(zip(H.edges, range(H.num_edges)))
    temp_H = Hypergraph()
    temp_H._hypergraph = H._hypergraph.copy()

    for node, id in node_dict.items():
        temp_H._node[id] = [edge_dict[e] for e in H._node[node]]
        temp_H._node_attr[id] = H._node_attr[node].copy()
        temp_H._node_attr[id][label_attribute] = node

    for edge, id in edge_dict.items():
        temp_H._edge[id] = [node_dict[n] for n in H._edge[edge]]
        temp_H._edge_attr[id] = H._edge_attr[edge].copy()
        temp_H._edge_attr[id][label_attribute] = edge

    return temp_H
