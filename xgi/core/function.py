"""Functional interface to hypergraph methods and assorted utilities."""

from collections import Counter
from copy import deepcopy
from warnings import warn

from scipy.special import comb

from ..exception import IDNotFound, XGIError
from .hypergraph import Hypergraph

__all__ = [
    "set_node_attributes",
    "get_node_attributes",
    "set_edge_attributes",
    "get_edge_attributes",
    "convert_labels_to_integers",
]


def set_node_attributes(H, values, name=None):
    """Sets node attributes from a given value or dictionary of values.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to set node attributes
    values : scalar value, dict-like
        What the node attribute should be set to.  If `values` is
        not a dictionary, then it is treated as a single attribute value
        that is then applied to every node in `H`.  This means that if
        you provide a mutable object, like a list, updates to that object
        will be reflected in the node attribute for every node.
        The attribute name will be `name`.

        If `values` is a dict or a dict of dict, it should be keyed
        by node to either an attribute value or a dict of attribute key/value
        pairs used to update the node's attributes.
    name : string, optional
        Name of the node attribute to set if values is a scalar, by default None.

    See Also
    --------
    get_node_attributes
    set_edge_attributes
    ~xgi.core.hypergraph.Hypergraph.add_node
    ~xgi.core.hypergraph.Hypergraph.add_nodes_from

    Notes
    -----
    After computing some property of the nodes of a hypergraph, you may
    want to assign a node attribute to store the value of that property
    for each node.

    If you provide a list as the second argument, updates to the list
    will be reflected in the node attribute for each node.

    If you provide a dictionary of dictionaries as the second argument,
    the outer dictionary is assumed to be keyed by node to an inner
    dictionary of node attributes for that node.

    Note that if the dictionary contains nodes that are not in `G`, the
    values are silently ignored.

    """
    # Set node attributes based on type of `values`
    if name is not None:  # `values` must not be a dict of dict
        if isinstance(values, dict):  # `values` is a dict
            for n, v in values.items():
                try:
                    H._node_attr[n][name] = v
                except IDNotFound:
                    warn(f"Node {n} does not exist!")
        else:  # `values` is a constant
            for n in H:
                H._node_attr[n][name] = values
    else:  # `values` must be dict of dict
        try:
            for n, d in values.items():
                try:
                    H._node_attr[n].update(d)
                except IDNotFound:
                    warn(f"Node {n} does not exist!")
        except (TypeError, ValueError, AttributeError):
            raise XGIError("Must pass a dictionary of dictionaries")


def get_node_attributes(H, name=None):
    """Get the node attributes for a hypergraph

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to get node attributes from
    name : string, optional
       Attribute name. If None, then return the entire attribute dictionary.

    Returns
    -------
    dict of dict
        Dictionary of attributes keyed by node.

    See Also
    --------
    set_node_attributes
    get_edge_attributes

    """
    if name is None:
        return dict(H._node_attr)
    else:
        return {n: d[name] for n, d in H._node_attr.items() if name in d}


def set_edge_attributes(H, values, name=None):
    """Set the edge attributes from a value or a dictionary of values.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to set edge attributes
    values : scalar value, dict-like
        What the edge attribute should be set to.  If `values` is
        not a dictionary, then it is treated as a single attribute value
        that is then applied to every edge in `H`.  This means that if
        you provide a mutable object, like a list, updates to that object
        will be reflected in the edge attribute for each edge.  The attribute
        name will be `name`.
        If `values` is a dict or a dict of dict, it should be keyed
        by edge ID to either an attribute value or a dict of attribute
        key/value pairs used to update the edge's attributes.
    name : string, optional
        Name of the edge attribute to set if values is a scalar. By default, None.

    See Also
    --------
    set_node_attributes
    get_edge_attributes
    ~xgi.core.hypergraph.Hypergraph.add_edge
    ~xgi.core.hypergraph.Hypergraph.add_edges_from

    Notes
    -----
    Note that if the dict contains edge IDs that are not in `H`, they are
    silently ignored.

    """
    if name is not None:
        # `values` does not contain attribute names
        try:
            for e, value in values.items():
                try:
                    H._edge_attr[id][name] = value
                except IDNotFound:
                    warn(f"Edge {e} does not exist!")
        except AttributeError:
            # treat `values` as a constant
            for e in H.edges:
                H._edge_attr[e][name] = values
    else:
        try:
            for e, d in values.items():
                try:
                    H._edge_attr[e].update(d)
                except IDNotFound:
                    warn(f"Edge {e} does not exist!")
        except AttributeError:
            raise XGIError(
                "name property has not been set and a "
                "dict-of-dicts has not been provided."
            )


def get_edge_attributes(H, name=None):
    """Get the edge attributes of the hypergraph

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to get edge attributes from
    name : string, optional
       Attribute name. If None (default), then return the entire attribute dictionary.

    Returns
    -------
    dict
        Dictionary of attributes keyed by edge ID.

    See Also
    --------
    set_node_attributes
    get_node_attributes
    set_edge_attributes
    """
    if name is None:
        return dict(H._edge_attr)
    else:
        return {e: d[name] for e, d in H._edge_attr.items() if name in d}


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
    temp_H._hypergraph = deepcopy(H._hypergraph)

    temp_H.add_nodes_from((id, deepcopy(H.nodes[n])) for n, id in node_dict.items())
    set_node_attributes(
        temp_H, {n: {label_attribute: id} for id, n in node_dict.items()}
    )

    temp_H.add_edges_from(
        (
            {node_dict[n] for n in e},
            edge_dict[id],
            deepcopy(H.edges[id]),
        )
        for id, e in H.edges.members(dtype=dict).items()
    )
    set_edge_attributes(
        temp_H, {e: {label_attribute: id} for id, e in edge_dict.items()}
    )

    return temp_H
