"""Generators for some classic hypergraphs.

All the functions in this module return a Hypergraph class (i.e. a simple, undirected
hypergraph).

"""

from itertools import chain, combinations

from ..utils import powerset

__all__ = [
    "empty_hypergraph",
    "empty_dihypergraph",
    "empty_simplicial_complex",
    "trivial_hypergraph",
    "complete_hypergraph",
    "complement",
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
    elif hasattr(create_using, "_node") or hasattr(create_using, "_node_in"):
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


def empty_dihypergraph(create_using=None, default=None):
    """Returns the empty dihypergraph with zero nodes and edges.

    Parameters
    ----------
    create_using : DiHypergraph Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty dihypergraph.
    default : DiHypergraph constructor (default None)
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
    >>> H = xgi.empty_dihypergraph()
    >>> H.num_nodes, H.num_edges
    (0, 0)

    """
    # this import needs to happen when the function runs, not when the module is first
    # imported, to avoid circular imports
    import xgi

    if default is None:
        default = xgi.DiHypergraph
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
    """Returns a hypergraph with `n` nodes and zero edges.

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


def complete_hypergraph(N, order=None, max_order=None, include_singletons=False):
    """Generate a complete hypergraph, i.e. one that contains all possible hyperdges
    at a given `order` or up to a `max_order`.

    Parameters
    ----------

    N : int
        Number of nodes
    order : int or None
        If not None (default), specifies the single order for which to generate
        hyperedges
    max_order : int or None
        If not None (default), specifies the maximum order for which to generate
        hyperedges
    include_singletons : bool
        Whether to include singleton edges (default: False). This argument is discarded
        if max_order is None.

    Return
    ------
    Hypergraph object
        A complete hypergraph with `N` nodes

    Notes
    ----
    Only one of `order` and `max_order` can be specified by and int (not None).
    Additionally, at least one of either must be specified.

    The number of possible edges grows exponentially as :math:`2^N` for large `N` and
    quickly becomes impractically long to compute, especially when using
    `max_order`. For example, `N=100` and `max_order=5` already yields :math:`10^8`
    edges. Increasing `N=1000` makes it :math:`10^{13}`. `N=100` and with a larger
    `max_order=6` yields :math:`10^9` edges.

    """
    # this import needs to happen when the function runs, not when the module is first
    # imported, to avoid circular imports
    import xgi

    if (order is None) and (max_order is None):
        raise ValueError(
            "At least one among order and max_order must be specified (not None)"
        )
    if (order is not None) and (max_order is not None):
        raise ValueError(
            "Both order and max_order cannot be specified (not None) at the same time."
        )

    H = xgi.Hypergraph()

    nodes = range(N)
    H.add_nodes_from(nodes)

    if order is not None:
        edges = combinations(nodes, order + 1)
    elif max_order is not None:
        start = 1 if include_singletons else 2
        end = max_order + 1
        assert end >= start  # can be equal because adding +1 to end below

        s = list(nodes)
        edges = chain.from_iterable(combinations(s, r) for r in range(start, end + 1))

    H.add_edges_from(edges)

    return H


def complement(H):
    """Returns the complement of hypergraph H.

    The complement Hc of a hypergraph H has the same nodes (same indexes) as H and
    contains every possible hyperedge linking these nodes, except those present in H.
    Also, the maximum hyperedge size in Hc is the same as in H.
    Hyperedges of size one are taken into account.

    Parameters
    ----------
    H : xgi.Hypergraph
        Hypergraph to complement.

    Returns
    -------
    Hc : xgi.Hypergraph
        Complement of H.
    """

    from ..algorithms import max_edge_order

    N = len(H.nodes)
    M = len(H.edges)

    if N == 0:
        return empty_hypergraph()
    else:

        node_dict = dict(zip(H.nodes, range(N)))
        num_dict = {idx: n for n, idx in node_dict.items()}

        # parsing list of edges into set of strings
        edges = set()
        for st in H.edges.members():
            lst = [node_dict[n] for n in st]  # we let go node IDs
            lst.sort()
            string = ",".join(str(idx) for idx in lst)
            edges.add(string)

        # parsing list of possible edges into set of strings
        max_edge_size = max_edge_order(H) + 1
        possible_edges = set()
        iterator = powerset(
            range(N),
            include_empty=False,
            include_singletons=True,
            max_size=max_edge_size,
        )
        for subset in iterator:
            lst = list(subset)
            lst.sort()
            string = ",".join(str(idx) for idx in lst)
            possible_edges.add(string)

        # performing set difference
        to_add = possible_edges.difference(edges)

        Hc = empty_hypergraph()
        Hc.add_nodes_from(H.nodes)

        for string in to_add:
            lst = string.split(",")
            nodes = [num_dict[int(idx)] for idx in lst]
            Hc.add_edge(nodes)

        return Hc
