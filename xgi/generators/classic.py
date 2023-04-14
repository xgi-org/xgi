"""Generators for some classic hypergraphs.

All the functions in this module return a Hypergraph class (i.e. a simple, undirected
hypergraph).

"""

__all__ = [
    "empty_hypergraph",
    "empty_simplicial_complex",
    "trivial_hypergraph",
]


def _empty_network(create_using, default):
    """Return an empty network.

    See Also
    --------
    empty_hypergraph
    empty_simplicial_complex

    """
    if create_using is None:
        H = default()
    elif hasattr(create_using, "_node"):
        # create_using is a Hypergraph object
        create_using.clear()
        H = create_using
    else:
        # try create_using as constructor
        H = create_using()
    return H


def empty_hypergraph(create_using=None, default=None):
    """Returns the empty hypergraph with zero nodes and edges.

    Parameters
    ----------
    create_using : Hypergraph Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty hypergraph.
    default : Hypergraph constructor (default None)
        The constructor to use if create_using is None.
        If None, then xgi.Hypergraph is used.

    Returns
    -------
    Hypergraph object
        An empty hypergraph

    See also
    --------
    empty_simplicial_complex
    trivial_hypergraph

    Examples
    --------
    >>> import xgi
    >>> H = xgi.empty_hypergraph()
    >>> H.num_nodes, H.num_edges
    (0, 0)

    """
    # this import needs to happen when the function runs, not when the module is first
    # imported, to avoid circular imports
    import xgi

    if default is None:
        default = xgi.Hypergraph
    return _empty_network(create_using, default)


def empty_simplicial_complex(create_using=None, default=None):
    """Returns the empty simplicial complex with zero nodes and simplices.

    Parameters
    ----------
    create_using : SimplicialComplex Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty simplicial complex.
    default : SimplicialComplex constructor (default None)
        The constructor to use if create_using is None.
        If None, then xgi.SimplicialComplex is used.

    Returns
    -------
    SimplicialComplex
        An empty simplicial complex.

    See also
    --------
    empty_hypergraph
    trivial_hypergraph

    Examples
    --------
    >>> import xgi
    >>> H = xgi.empty_simplicial_complex()
    >>> H.num_nodes, H.num_edges
    (0, 0)

    """
    # this import needs to happen when the function runs, not when the module is first
    # imported, to avoid circular imports
    import xgi

    if default is None:
        default = xgi.SimplicialComplex
    return _empty_network(create_using, default)


def trivial_hypergraph(n=1, create_using=None, default=None):
    """Returns a hypergraph with `n` node and zero edges.

    Parameters
    ----------
    n : int, optional
        Number of nodes (default is 1)
    create_using : Hypergraph Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty hypergraph.
    default : Hypergraph constructor (default None)
        The constructor to use if create_using is None.
        If None, then xgi.Hypergraph is used.

    Returns
    -------
    Hypergraph object
        A trivial hypergraph with `n` nodes

    See also
    --------
    empty_hypergraph
    empty_simplicial_complex

    Examples
    --------
    >>> import xgi
    >>> H = xgi.trivial_hypergraph()
    >>> H.num_nodes, H.num_edges
    (1, 0)

    """
    # this import needs to happen when the function runs, not when the module is first
    # imported, to avoid circular imports
    import xgi

    if default is None:
        default = xgi.Hypergraph
    H = _empty_network(create_using, default)
    nodes = range(n)
    H.add_nodes_from(nodes)

    return H
