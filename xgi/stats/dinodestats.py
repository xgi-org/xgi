"""Node statistics.

This module is part of the stats package, and it defines node-level statistics.  That
is, each function defined in this module is assumed to define a node-quantity mapping.
Each callable defined here is accessible via a `Network` object, or a
:class:`~xgi.classes.reportviews.NodeView` object.  For more details, see the `tutorial
<https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

Examples
--------

>>> import xgi
>>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
>>> H.degree()
{1: 1, 2: 2, 3: 3, 4: 2, 5: 2}
>>> H.nodes.degree.asdict()
{1: 1, 2: 2, 3: 3, 4: 2, 5: 2}

"""

import numpy as np

import xgi

__all__ = [
    "attrs",
    "degree",
    "average_neighbor_degree",
    "local_clustering_coefficient",
    "clustering_coefficient",
    "two_node_clustering_coefficient",
    "clique_eigenvector_centrality",
    "h_eigenvector_centrality",
    "node_edge_centrality",
]


def attrs(net, bunch, attr=None, missing=None):
    """Access node attributes.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    attr : str | None (default)
        If None, return all attributes.  Otherwise, return a single attribute with name
        `attr`.
    missing : Any
        Value to impute in case a node does not have an attribute with name `attr`.
        Default is None.

    Returns
    -------
    dict
        If attr is None, return a nested dict of the form `{node: {"attr": val}}`.
        Otherwise, return a simple dict of the form `{node: val}`.

    Notes
    -----
    When requesting all attributes (i.e. when `attr` is None), no value is imputed.

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
    >>> H.add_nodes_from([
    ...         (1, {"color": "red", "name": "horse"}),
    ...         (2, {"color": "blue", "name": "pony"}),
    ...         (3, {"color": "yellow", "name": "zebra"}),
    ...         (4, {"color": "red", "name": "orangutan", "age": 20}),
    ...         (5, {"color": "blue", "name": "fish", "age": 2}),
    ...     ])

    Access all attributes as different types.

    >>> H.nodes.attrs.asdict() # doctest: +NORMALIZE_WHITESPACE
    {1: {'color': 'red', 'name': 'horse'},
     2: {'color': 'blue', 'name': 'pony'},
     3: {'color': 'yellow', 'name': 'zebra'},
     4: {'color': 'red', 'name': 'orangutan', 'age': 20},
     5: {'color': 'blue', 'name': 'fish', 'age': 2}}
    >>> H.nodes.attrs.asnumpy() # doctest: +NORMALIZE_WHITESPACE
    array([{'color': 'red', 'name': 'horse'},
           {'color': 'blue', 'name': 'pony'},
           {'color': 'yellow', 'name': 'zebra'},
           {'color': 'red', 'name': 'orangutan', 'age': 20},
           {'color': 'blue', 'name': 'fish', 'age': 2}],
          dtype=object)

    Access a single attribute as different types.

    >>> H.nodes.attrs('color').asdict()
    {1: 'red', 2: 'blue', 3: 'yellow', 4: 'red', 5: 'blue'}
    >>> H.nodes.attrs('color').aslist()
    ['red', 'blue', 'yellow', 'red', 'blue']

    By default, None is imputed when a node does not have the requested attribute.

    >>> H.nodes.attrs('age').asdict()
    {1: None, 2: None, 3: None, 4: 20, 5: 2}

    Use `missing` to change the imputed value.

    >>> H.nodes.attrs('age', missing=100).asdict()
    {1: 100, 2: 100, 3: 100, 4: 20, 5: 2}

    """
    if isinstance(attr, str):
        return {n: net._node_attr[n].get(attr, missing) for n in bunch}
    elif attr is None:
        return {n: net._node_attr[n] for n in bunch}
    else:
        raise ValueError('"attr" must be str or None')


def degree(net, bunch, order=None, weight=None):
    """Node degree.

    The degree of a node is the number of edges it belongs to.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    order : int | None
        If not None (default), only count the edges of the given order.
    weight : str | None
        If not None, specifies the name of the edge attribute that determines the weight
        of each edge.

    Returns
    -------
    dict

    """
    if order is None and weight is None:
        return {n: len(net._node_in[n].union(net._node_out[n])) for n in bunch}
    if order is None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node_in[n].union(net._node_out[n])
            )
            for n in bunch
        }
    if order is not None and weight is None:
        return {
            n: len(
                [
                    e
                    for e in net._node_in[n].union(net._node_out[n])
                    if len(net._edge_in[e].union(net._edge_out[e])) == order + 1
                ]
            )
            for n in bunch
        }
    if order is not None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node_in[n].union(net._node_out[n])
                if len(net._edge_in[e].union(net._edge_out[e])) == order + 1
            )
            for n in bunch
        }


def in_degree(net, bunch, order=None, weight=None):
    """Node degree.

    The degree of a node is the number of edges it belongs to.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    order : int | None
        If not None (default), only count the edges of the given order.
    weight : str | None
        If not None, specifies the name of the edge attribute that determines the weight
        of each edge.

    Returns
    -------
    dict

    """
    if order is None and weight is None:
        return {n: len(net._node_in[n]) for n in bunch}
    if order is None and weight:
        return {
            n: sum(net._edge_attr[e].get(weight, 1) for e in net._node_in[n])
            for n in bunch
        }
    if order is not None and weight is None:
        return {
            n: len(
                [
                    e
                    for e in net._node_in[n]
                    if len(net._edge_in[e].union(net._edge_out[e])) == order + 1
                ]
            )
            for n in bunch
        }
    if order is not None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node_in[n]
                if len(net._edge_in[e].union(net._edge_out[e])) == order + 1
            )
            for n in bunch
        }


def out_degree(net, bunch, order=None, weight=None):
    """Node degree.

    The degree of a node is the number of edges it belongs to.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    order : int | None
        If not None (default), only count the edges of the given order.
    weight : str | None
        If not None, specifies the name of the edge attribute that determines the weight
        of each edge.

    Returns
    -------
    dict

    """
    if order is None and weight is None:
        return {n: len(net._node_out[n]) for n in bunch}
    if order is None and weight:
        return {
            n: sum(net._edge_attr[e].get(weight, 1) for e in net._node_out[n])
            for n in bunch
        }
    if order is not None and weight is None:
        return {
            n: len(
                [
                    e
                    for e in net._node_out[n]
                    if len(net._edge_in[e].union(net._edge_out[e])) == order + 1
                ]
            )
            for n in bunch
        }
    if order is not None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node[n]
                if len(net._edge_in[e].union(net._edge_out[e])) == order + 1
            )
            for n in bunch
        }
