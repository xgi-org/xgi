"""Directed edge statistics.

This module is part of the stats package, and it defines edge-level statistics.  That
is, each function defined in this module is assumed to define an edge-quantity mapping.
Each callable defined here is accessible via a `Network` object, or a
:class:`~xgi.core.views.DiEdgeView` object.  For more details, see the `tutorial
<https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

Examples
--------

>>> import xgi
>>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
>>> H.order()
{0: 3, 1: 2}
>>> H.edges.order.asdict()
{0: 3, 1: 2}

"""

__all__ = [
    "attrs",
    "order",
    "size",
    "head_order",
    "head_size",
    "tail_order",
    "tail_size",
]


def attrs(net, bunch, attr=None, missing=None):
    """Access edge attributes.

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
        Value to impute in case an edge does not have an attribute with name `attr`.
        Default is None.

    Returns
    -------
    dict
        If attr is None, return a nested dict of the form `{edge: {"attr": val}}`.
        Otherwise, return a simple dict of the form `{edge: val}`.

    Notes
    -----
    When requesting all attributes (i.e. when `attr` is None), no value is imputed.

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph()
    >>> edges = [
    ...     ([{0, 1}, {2, 4}], 'one', {'color': 'red'}),
    ...     ([{1, 2}, {2, 0}], 'two', {'color': 'black', 'age': 30}),
    ...     ([{2, 3, 4}, {1}], 'three', {'color': 'blue', 'age': 40}),
    ... ]
    >>> H.add_edges_from(edges)

    Access all attributes as different types.

    >>> H.edges.attrs.asdict() # doctest: +NORMALIZE_WHITESPACE
    {'one': {'color': 'red'},
     'two': {'color': 'black', 'age': 30},
     'three': {'color': 'blue', 'age': 40}}
    >>> H.edges.attrs.asnumpy() # doctest: +NORMALIZE_WHITESPACE
    array([{'color': 'red'},
           {'color': 'black', 'age': 30},
           {'color': 'blue', 'age': 40}],
           dtype=object)

    Access a single attribute as different types.

    >>> H.edges.attrs('color').asdict()
    {'one': 'red', 'two': 'black', 'three': 'blue'}
    >>> H.edges.attrs('color').aslist()
    ['red', 'black', 'blue']

    By default, None is imputed when a node does not have the requested attribute.

    >>> H.edges.attrs('age').asdict()
    {'one': None, 'two': 30, 'three': 40}

    Use `missing` to change the imputed value.

    >>> H.edges.attrs('age', missing=100).asdict()
    {'one': 100, 'two': 30, 'three': 40}

    """
    if isinstance(attr, str):
        return {e: net._edge_attr[e].get(attr, missing) for e in bunch}
    elif attr is None:
        return {e: net._edge_attr[e] for e in bunch}
    else:
        raise ValueError('"attr" must be str or None')


def order(net, bunch, degree=None):
    """Edge order.

    The order of a directed edge is the number of nodes
    contained in the union of the head and the tail minus 1.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Edges in `net`.
    degree : int | None
        If not None (default), count only those member nodes with the specified degree.

    Returns
    -------
    dict

    See Also
    --------
    size

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.edges.order.asdict()
    {0: 3, 1: 2}
    """
    if degree is None:
        return {
            e: len(net._edge[e]["in"].union(net._edge[e]["out"])) - 1 for e in bunch
        }
    else:
        return {
            e: sum(
                len(net._node[n]["in"].union(net._node[n]["out"])) == degree
                for n in net._edge[e]["in"].union(net._edge[e]["out"])
            )
            - 1
            for e in bunch
        }


def size(net, bunch, degree=None):
    """Edge size.

    The size of a directed edge is the number of nodes
    contained in the union of the head and the tail.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Edges in `net`.

    Returns
    -------
    dict

    See Also
    --------
    order

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.edges.size.asdict()
    {0: 4, 1: 3}
    """
    if degree is None:
        return {e: len(net._edge[e]["in"].union(net._edge[e]["out"])) for e in bunch}
    else:
        return {
            e: sum(
                1
                for n in net._edge[e]["in"].union(net._edge[e]["out"])
                if len(net._node[n]["in"].union(net._node[n]["out"])) == degree
            )
            for e in bunch
        }


def tail_order(net, bunch, degree=None):
    """Tail order.

    The order of the tail is the number of nodes it contains minus 1.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Edges in `net`.

    Returns
    -------
    dict

    See Also
    --------
    order

    Examples
    --------
    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.edges.tail_order.asdict()
    {0: 1, 1: 0}

    """
    if degree is None:
        return {e: len(net._edge[e]["in"]) - 1 for e in bunch}
    else:
        return {
            e: sum(
                1
                for n in net._edge[e]["in"]
                if len(net._node[n]["in"].union(net._node[n]["out"])) == degree
            )
            - 1
            for e in bunch
        }


def tail_size(net, bunch, degree=None):
    """Tail size.

    The size of the tail is the number of nodes it contains.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Edges in `net`.

    Returns
    -------
    dict

    See Also
    --------
    order

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.edges.tail_size.asdict()
    {0: 2, 1: 1}
    """
    if degree is None:
        return {e: len(net._edge[e]["in"]) for e in bunch}
    else:
        return {
            e: sum(
                1
                for n in net._edge[e]["in"]
                if len(net._node[n]["in"].union(net._node[n]["out"])) == degree
            )
            for e in bunch
        }


def head_order(net, bunch, degree=None):
    """Head order.

    The order of the head is the number of nodes it contains minus 1.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Edges in `net`.

    Returns
    -------
    dict

    See Also
    --------
    order

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.edges.head_order.asdict()
    {0: 1, 1: 1}
    """
    if degree is None:
        return {e: len(net._edge[e]["out"]) - 1 for e in bunch}
    else:
        return {
            e: sum(
                1
                for n in net._edge[e]["out"]
                if len(net._node[n]["in"].union(net._node[n]["out"])) == degree
            )
            - 1
            for e in bunch
        }


def head_size(net, bunch, degree=None):
    """Head size.

    The size of the head is the number of nodes it contains.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Edges in `net`.

    Returns
    -------
    dict

    See Also
    --------
    order

    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])
    >>> H.edges.head_size.asdict()
    {0: 2, 1: 2}
    """
    if degree is None:
        return {e: len(net._edge[e]["out"]) for e in bunch}
    else:
        return {
            e: sum(
                1
                for n in net._edge[e]["out"]
                if len(net._node[n]["in"].union(net._node[n]["out"])) == degree
            )
            for e in bunch
        }
