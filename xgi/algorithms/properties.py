"""Functional interface to hypergraph methods and assorted utilities."""

from collections import Counter

from scipy.special import comb

from ..exception import XGIError

__all__ = [
    "num_edges_order",
    "max_edge_order",
    "is_uniform",
    "is_possible_order",
    "edge_neighborhood",
    "degree_counts",
    "degree_histogram",
    "unique_edge_sizes",
    "density",
    "incidence_density",
]


def num_edges_order(H, d=None):
    """The number of edges of order d.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.

    d : int, optional
        The order of edges to count. If None (default), counts
        for all orders.

    Returns
    -------
    int
        The number of edges of order d

    See Also
    --------
    max_edge_order
    """

    if d is not None:
        return len(H.edges.filterby("order", d))
    else:
        return H.num_edges


def max_edge_order(H):
    """The maximum order of edges in the hypergraph.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.

    Returns
    -------
    int
        Maximum order of edges in hypergraph.

    See Also
    --------
    num_edges_order
    """
    if H._edge:
        d_max = max(len(edge) for edge in H._edge.values()) - 1
    else:
        d_max = 0 if H._node else None
    return d_max


def is_possible_order(H, d):
    """Whether the specified order is between 0 (singletons) and the maximum order.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.
    d : int
        Order for which to check.

    Returns
    -------
    bool
        Whether `d` is a possible order.

    """
    d_max = max_edge_order(H)
    return (d >= 0) and (d <= d_max)


def is_uniform(H):
    """Order of uniformity if the hypergraph is uniform, or False.

    A hypergraph is uniform if all its edges have the same order.

    Returns d if the hypergraph is d-uniform, that is if all edges
    in the hypergraph (excluding singletons) have the same degree d.
    Returns False if not uniform.

    Returns
    -------
    d : int or False
        If the hypergraph is d-uniform, return d, or False otherwise.

    Examples
    --------
    This function can be used as a boolean check:

    >>> import xgi
    >>> H = xgi.Hypergraph([(0, 1, 2), (1, 2, 3), (2, 3, 4)])
    >>> xgi.is_uniform(H)
    2
    >>> if xgi.is_uniform(H): print('H is uniform!')
    H is uniform!

    """
    edge_sizes = unique_edge_sizes(H)
    if 1 in edge_sizes:
        edge_sizes.remove(1)  # discard singleton edges

    if not edge_sizes or len(edge_sizes) != 1:
        return False

    return int(edge_sizes.pop() - 1)  # order of all edges


def edge_neighborhood(H, n, include_self=False):
    """The edge neighborhood of the specified node.

    The edge neighborhood of a node `n` in a hypergraph `H` is an edgelist of all the
    edges containing `n` and its edges are all the edges in `H` that contain `n`.
    Usually, the edge neighborhood does not include `n` itself.  This can be controlled
    with `include_self`.

    Parameters
    ----------
    H : Hypergraph
        THe hypergraph of interest
    n : node
        Node whose edge_neighborhood is needed.
    include_self : bool, optional
        Whether the edge_neighborhood contains `n`.
        By default, False.
    Returns
    -------
    list
        An edgelist of the edge_neighborhood of `n`.

    See Also
    --------
    ~xgi.core.views.IDView.neighbors

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph([[1, 2, 3], [3, 4], [4, 5, 6]])
    >>> H.nodes.neighbors(3)
    {1, 2, 4}
    >>> xgi.edge_neighborhood(H, 3)
    [{1, 2}, {4}]
    >>> xgi.edge_neighborhood(H, 3, include_self=True)
    [{1, 2, 3}, {3, 4}]

    """
    if include_self:
        return [H.edges.members(e) for e in H.nodes.memberships(n)]
    else:
        return [H.edges.members(e) - {n} for e in H.nodes.memberships(n)]


def degree_counts(H, order=None):
    """Returns a list of the the number of occurrences of each degree value.

    The counts correspond to degrees from 0 to max(degree).

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest
    order: int, optional
        Order of edges to take into account. If None (default),
        consider all edges.

    Returns
    -------
    list
        A list of frequencies of degrees.
        The degree values are the index in the list.

    Notes
    -----
    Note: the bins are width one, hence len(list) can be large
    (Order(num_edges))

    The degree is defined as the number of edges to which a node belongs.
    A node belonging only to a singleton edge will thus have degree 1 and
    contribute accordingly to the degree count.

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> xgi.degree_counts(H)
    [0, 3, 1]

    """
    counts = Counter(H.degree(order=order).values())
    return [counts.get(i, 0) for i in range(max(counts) + 1)]


def degree_histogram(H):
    """Returns a degree histogram including bin centers (degree values).

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    tuple of lists
        First entry is observed degrees (bin centers),
            second entry is degree count (histogram height)
    Notes
    -----
    Note: the bins are width one, hence there will be an entry
    for every observed degree.

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> xgi.degree_histogram(H)
    ([1, 2], [3, 1])

    """
    counts = Counter(H.degree().values())
    degrees = []
    heights = []
    for d, c in sorted(counts.items(), key=lambda kv: kv[0]):
        degrees.append(d)
        heights.append(c)
    return degrees, heights


def unique_edge_sizes(H):
    """A function that returns the unique edge sizes.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    list of int
        The unique edge sizes in ascending order by size.
    """
    return sorted(set(H.edges.size.aslist()))


def density(H, order=None, max_order=None, ignore_singletons=False):
    r"""Hypergraph density.

    The density of a hypergraph is the number of existing edges divided by the number of
    possible edges.

    Let `H` have :math:`n` nodes and :math:`m` hyperedges. Then,

    * `density(H) =` :math:`\frac{m}{2^n - 1}`,
    * `density(H, ignore_singletons=True) =` :math:`\frac{m}{2^n - 1 - n}`.

    Here, :math:`2^n` is the total possible number of hyperedges on `H`, from which we
    subtract :math:`1` because the empty hyperedge is not considered.  We subtract an
    additional :math:`n` when singletons are not considered.

    Now assume `H` has :math:`a` edges with order :math:`1` and :math:`b` edges with
    order :math:`2`.  Then,

    * `density(H, order=1) =` :math:`\frac{a}{{n \choose 2}}`,
    * `density(H, order=2) =` :math:`\frac{b}{{n \choose 3}}`,
    * `density(H, max_order=1) =` :math:`\frac{a}{{n \choose 1} + {n \choose 2}}`,
    * `density(H, max_order=1, ignore_singletons=True) =` :math:`\frac{a}{{n \choose 2}}`,
    * `density(H, max_order=2) =` :math:`\frac{m}{{n \choose 1} + {n \choose 2} + {n \choose 3}}`,
    * `density(H, max_order=2, ignore_singletons=True) =` :math:`\frac{m}{{n \choose 2} + {n \choose 3}}`,

    Parameters
    ---------
    order : int, optional
        If not None, only count edges of the specified order.
        By default, None.

    max_order : int, optional
        If not None, only count edges of order up to this value, inclusive.
        By default, None.

    ignore_singletons : bool, optional
        Whether to consider singleton edges.  Ignored if `order` is not None and
        different from :math:`0`. By default, False.

    See Also
    --------
    :func:`incidence_density`

    Notes
    -----
    If both `order` and `max_order` are not None, `max_order` is ignored.

    """
    n = H.num_nodes
    if n < 1:
        raise XGIError("Density not defined for empty hypergraph")
    if H.num_edges < 1:
        return 0.0

    def order_filter(val, mode):
        return H.edges.filterby("order", val, mode=mode)

    if order is None and max_order is None:
        numer = H.num_edges
        denom = 2**n - 1
        if ignore_singletons:
            numer -= len(order_filter(0, mode="eq"))
            denom -= n

    elif order is None and max_order is not None:
        if max_order >= n:
            raise ValueError("max_order must be smaller than the number of nodes")
        numer = len(order_filter(max_order, "leq"))
        denom = sum(comb(n, _ord + 1, exact=True) for _ord in range(max_order + 1))
        if ignore_singletons:
            numer -= len(order_filter(0, mode="eq"))
            denom -= n

    elif order is not None:  # ignore max_order
        if order >= n:
            raise ValueError("order must be smaller than the number of nodes")
        if ignore_singletons and order == 0:
            return 0.0
        numer = len(order_filter(order, mode="eq"))
        denom = comb(n, order + 1, exact=True)

    try:
        return float(numer) / denom
    except ZeroDivisionError:
        return 0.0


def incidence_density(H, order=None, max_order=None, ignore_singletons=False):
    r"""Density of the incidence matrix.

    The incidence matrix of a hypergraph contains one row per node and one column per
    edge.  An entry is non-zero when the corresponding node is a member of the
    corresponding edge.  The density of this matrix is the number of non-zero entries
    divided by the total number of entries.

    Parameters
    ---------
    order : int, optional
        If not None, only count edges of the specified order.
        By default, None.

    max_order : int, optional
        If not None, only count edges of order up to this value, inclusive.
        By default, None.

    ignore_singletons : bool, optional
        Whether to consider singleton edges.  Ignored if `order` is not None and
        different from :math:`0`. By default, False.

    See Also
    --------
    :func:`density`

    Notes
    -----
    If both `order` and `max_order` are not None, `max_order` is ignored.

    The parameters `order`, `max_order` and `ignore_singletons` have a similar effect on
    the denominator as they have in :func:`density`.

    """
    n = H.num_nodes
    if n < 1:
        raise XGIError("Density not defined for empty hypergraph")
    if H.num_edges < 1:
        return 0.0

    edges_to_count = H.edges
    if order is None and max_order is None:
        if ignore_singletons:
            edges_to_count = edges_to_count.filterby("order", 0, "gt")

    elif order is None and max_order is not None:
        if max_order >= n:
            raise ValueError("max_order must be smaller than the number of nodes")
        edges_to_count = edges_to_count.filterby("order", max_order, "leq")
        if ignore_singletons:
            edges_to_count = edges_to_count.filterby("order", 0, "gt")

    elif order is not None:  # ignore max_order
        if order >= n:
            raise ValueError("order must be smaller than the number of nodes")
        if ignore_singletons and order == 0:
            return 0.0
        edges_to_count = edges_to_count.filterby("order", order, "eq")

    denom = n * len(edges_to_count)
    numer = edges_to_count.size.asnumpy().sum()  # size, not order
    try:
        # cast both to float because sometimes 0 / 0.0 may issue a warning instead of
        # raising ZeroDivisionError
        return float(numer) / float(denom)
    except ZeroDivisionError:
        return 0.0
