"""Edge statistics.

This module is part of the stats package, and it defines edge-level statistics.  That
is, each function defined in this module is assumed to define an edge-quantity mapping.
Each callable defined here is accessible via a `Network` object, or a
:class:`~xgi.classes.reportviews.EdgeView` object.  For more details, see the `tutorial
<https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

Examples
--------

>>> import xgi
>>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
>>> H.order()
{0: 2, 1: 3, 2: 2}
>>> H.edges.order.asdict()
{0: 2, 1: 3, 2: 2}

"""

__all__ = [
    "attrs",
    "order",
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
    >>> H = xgi.Hypergraph()
    >>> edges = [
    ...     ([0, 1], 'one', {'color': 'red'}),
    ...     ([1, 2], 'two', {'color': 'black', 'age': 30}),
    ...     ([2, 3, 4], 'three', {'color': 'blue', 'age': 40}),
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
        return {n: net._edge_attr[n].get(attr, missing) for n in bunch}
    elif attr is None:
        return {n: net._edge_attr[n] for n in bunch}
    else:
        raise ValueError('"attr" must be str or None')


def order(net, bunch, degree=None):
    """Edge order.

    The order of an edge is the number of nodes it contains minus 1.

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
    size

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
    >>> H.edges.order.asdict()
    {0: 2, 1: 3, 2: 2}

    """
    if degree is None:
        return {n: len(net._edge[n]) - 1 for n in bunch}
    else:
        return {
            n: len(n for n in net._edge[n] if len(net._node[n]) == degree) - 1
            for n in bunch
        }


def size(net, bunch, degree=None):
    """Edge size.

    The size of an edge is the number of nodes it contains.

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
    >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
    >>> H.edges.size.asdict()
    {0: 3, 1: 4, 2: 3}

    """
    if degree is None:
        return {n: len(net._edge[n]) for n in bunch}
    else:
        return {
            n: len(n for n in net._edge[n] if len(net._node[n]) == degree)
            for n in bunch
        }
