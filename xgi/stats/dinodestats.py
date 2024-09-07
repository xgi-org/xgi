"""Node statistics.

This module is part of the stats package, and it defines node-level statistics.  That
is, each function defined in this module is assumed to define a node-quantity mapping.
Each callable defined here is accessible via a `Network` object, or a
:class:`~xgi.core.views.NodeView` object.  For more details, see the `tutorial
<https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

Examples
--------

>>> import xgi
>>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
>>> H.degree()
{1: 2, 2: 1, 5: 1, 6: 1, 4: 1, 3: 1}
>>> H.nodes.degree.asdict()
{1: 2, 2: 1, 5: 1, 6: 1, 4: 1, 3: 1}

"""

__all__ = [
    "attrs",
    "degree",
    "in_degree",
    "out_degree",
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
    >>> H = xgi.DiHypergraph()
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

    The degree of a node is the number of edges it belongs to,
    regardless of whether it is in the head or the tail.

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

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.nodes.degree.asdict()
    {1: 2, 2: 1, 5: 1, 6: 1, 4: 1, 3: 1}
    """
    if order is None and weight is None:
        return {n: len(net._node[n]["in"].union(net._node[n]["out"])) for n in bunch}
    if order is None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node[n]["in"].union(net._node[n]["out"])
            )
            for n in bunch
        }
    if order is not None and weight is None:
        return {
            n: sum(
                1
                for e in net._node[n]["in"].union(net._node[n]["out"])
                if len(net._edge[e]["in"].union(net._edge[e]["out"])) == order + 1
            )
            for n in bunch
        }
    if order is not None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node[n]["in"].union(net._node[n]["out"])
                if len(net._edge[e]["in"].union(net._edge[e]["out"])) == order + 1
            )
            for n in bunch
        }


def in_degree(net, bunch, order=None, weight=None):
    """Node in-degree.

    The in-degree of a node is the number of edges for which
    the node is in the head (it is a receiver).

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

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.nodes.in_degree.asdict()
    {1: 1, 2: 0, 5: 1, 6: 1, 4: 0, 3: 1}
    """
    if order is None and weight is None:
        return {n: len(net._node[n]["in"]) for n in bunch}
    if order is None and weight:
        return {
            n: sum(net._edge_attr[e].get(weight, 1) for e in net._node[n]["in"])
            for n in bunch
        }
    if order is not None and weight is None:
        return {
            n: sum(
                1
                for e in net._node[n]["in"]
                if len(net._edge[e]["in"].union(net._edge[e]["out"])) == order + 1
            )
            for n in bunch
        }
    if order is not None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node[n]["in"]
                if len(net._edge[e]["in"].union(net._edge[e]["out"])) == order + 1
            )
            for n in bunch
        }


def out_degree(net, bunch, order=None, weight=None):
    """Node out-degree.

    The out-degree of a node is the number of edges for which
    the node is in the tail (it is a sender).

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

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.nodes.out_degree.asdict()
    {1: 1, 2: 1, 5: 0, 6: 0, 4: 1, 3: 0}
    """
    if order is None and weight is None:
        return {n: len(net._node[n]["out"]) for n in bunch}
    if order is None and weight:
        return {
            n: sum(net._edge_attr[e].get(weight, 1) for e in net._node[n]["out"])
            for n in bunch
        }
    if order is not None and weight is None:
        return {
            n: sum(
                1
                for e in net._node[n]["out"]
                if len(net._edge[e]["in"].union(net._edge[e]["out"])) == order + 1
            )
            for n in bunch
        }
    if order is not None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node[n]["out"]
                if len(net._edge[e]["in"].union(net._edge[e]["out"])) == order + 1
            )
            for n in bunch
        }
