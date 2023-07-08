"""Functional interface to hypergraph methods and assorted utilities."""

from collections import Counter
from copy import deepcopy
from warnings import warn

from scipy.special import comb

from ..exception import IDNotFound, XGIError
from .hypergraph import Hypergraph

__all__ = [
    "freeze",
    "is_frozen",
    "set_node_attributes",
    "get_node_attributes",
    "set_edge_attributes",
    "get_edge_attributes",
    "convert_labels_to_integers",
]



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
    list()
        The unique edge sizes in ascending order by size.
    """
    return sorted(set(H.edges.size.asnumpy()))


def frozen(*args, **kwargs):
    """Dummy method that raises an error when trying to modify frozen hypergraphs

    Raises
    ------
    XGIError
        Raises error when user tries to modify the hypergraph

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> xgi.freeze(H) # doctest: +ELLIPSIS
    <xgi.core.hypergraph.Hypergraph object at 0x...>
    >>> H.add_node(5)
    Traceback (most recent call last):
    xgi.exception.XGIError: Frozen hypergraph can't be modified

    """
    raise XGIError("Frozen hypergraph can't be modified")


def freeze(H):
    """Method for freezing a hypergraph which prevents it from being modified

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to freeze

    Returns
    -------
    Hypergraph object
        The hypergraph with all the functions that can modify the hypergraph
        set to the frozen method

    See Also
    --------
    frozen : Method that raises an error when a user tries to modify the hypergraph
    is_frozen : Check whether a hypergraph is frozen

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> xgi.freeze(H) # doctest: +ELLIPSIS
    <xgi.core.hypergraph.Hypergraph object at 0x...>
    >>> H.add_node(5)
    Traceback (most recent call last):
    xgi.exception.XGIError: Frozen hypergraph can't be modified

    """
    H.add_node = frozen
    H.add_nodes_from = frozen
    H.remove_node = frozen
    H.remove_nodes_from = frozen
    H.add_edge = frozen
    H.add_edges_from = frozen
    H.add_weighted_edges_from = frozen
    H.remove_edge = frozen
    H.remove_edges_from = frozen
    H.add_node_to_edge = frozen
    H.remove_node_from_edge = frozen
    H.clear = frozen
    H.frozen = True
    return H


def is_frozen(H):
    """Checks whether a hypergraph is frozen

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to check

    Returns
    -------
    bool
        True if hypergraph is frozen, false if not.

    See Also
    --------
    freeze : A method to prevent a hypergraph from being modified.

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> xgi.freeze(H) # doctest: +ELLIPSIS
    <xgi.core.hypergraph.Hypergraph object at 0x...>
    >>> xgi.is_frozen(H)
    True

    """
    try:
        return H.frozen
    except AttributeError:
        return False


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
