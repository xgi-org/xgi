"""Functional interface to hypergraph methods and assorted utilities."""

from collections import Counter
from copy import deepcopy
from warnings import warn

from ..exception import IDNotFound, XGIError
from .hypergraph import Hypergraph

__all__ = [
    "num_edges_order",
    "max_edge_order",
    "is_possible_order",
    "is_uniform",
    "edge_neighborhood",
    "degree_counts",
    "degree_histogram",
    "unique_edge_sizes",
    "freeze",
    "is_frozen",
    "create_empty_copy",
    "set_node_attributes",
    "get_node_attributes",
    "set_edge_attributes",
    "get_edge_attributes",
    "is_empty",
    "maximal_simplices",
    "convert_labels_to_integers",
]

def num_edges_order(H, d=None):
    """The number of edges of order d.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.

    d : int | None, optional
        The order of edges to count. If None (default), counts
        for all orders. 
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

    """
    if H._edge:
        d_max = max(len(edge) for edge in H._edge.values()) - 1
    else:
        d_max = 0 if H._node else None
    return d_max


def is_possible_order(H, d):
    """Whether the specified order is between 1 and the maximum order.

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
    return (d >= 1) and (d <= d_max)


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
    edge_sizes = {len(members) for _, members in H._edge.items()}
    if 1 in edge_sizes:
        edge_sizes.remove(1)  # discard singleton edges

    if not edge_sizes or len(edge_sizes) != 1:
        return False

    return edge_sizes.pop() - 1  # order of all edges


def edge_neighborhood(H, n, include_self=False):
    """The edge neighborhood of the specified node.

    The edge neighborhood of a node `n` in a hypergraph `H` is an edgelist of all the edges
    containing `n` and its edges are all the edges in `H` that contain
    `n`.  Usually, the edge neighborhood does not include `n` itself.  This can be controlled
    with `include_self`.

    Parameters
    ----------
    H : Hypergraph
        THe hypergraph of interest
    n : node
        Node whose edge_neighborhood is needed.
    include_self : bool (default False)
        Whether the edge_neighborhood contains `n`.

    Returns
    -------
    list
        An edgelist of the edge_neighborhood of `n`.

    See Also
    --------
    neighbors

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
    """Returns a list of the frequency of each degree value.

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
        The unique edge sizes
    """
    return list({len(H.edges.members(edge)) for edge in H.edges})


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
    <xgi.classes.hypergraph.Hypergraph object at 0x...>
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
    <xgi.classes.hypergraph.Hypergraph object at 0x...>
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
    <xgi.classes.hypergraph.Hypergraph object at 0x...>
    >>> xgi.is_frozen(H)
    True

    """
    try:
        return H.frozen
    except AttributeError:
        return False


def create_empty_copy(H, with_data=True):
    """Create a new hypergraph with the nodes (and data) of a specified
    hypergraph.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to copy
    with_data : bool, optional
        Whether to keep the node and hypergraph data, by default True

    Returns
    -------
    Hypergraph object
        A hypergraph with the same nodes but without edges

    See Also
    --------
    is_empty
    empty_hypergraph

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> H_copy = xgi.create_empty_copy(H)
    >>> H_copy.nodes
    NodeView((1, 2, 3, 4))
    >>> H_copy.edges
    EdgeView(())

    """
    H_copy = H.__class__()
    H_copy.add_nodes_from(H.nodes)
    if with_data:
        set_node_attributes(H_copy, dict(H._node_attr))
        H_copy._hypergraph.update(H._hypergraph)
    return H_copy


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
        Name of the node attribute to set if values is a scalar, by default None

    See Also
    --------
    get_node_attributes
    set_edge_attributes
    get_edge_attributes

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
    set_edge_attributes
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
    name : string (optional, default=None)
        Name of the edge attribute to set if values is a scalar.

    See Also
    --------
    set_node_attributes
    get_node_attributes
    get_edge_attributes

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
                "name property has not been set and a dict-of-dicts has not been provided."
            )


def get_edge_attributes(H, name=None):
    """Get the edge attributes of the hypergraph

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to get edge attributes from
    name : string, optional
       Attribute name. If None, then return the entire attribute dictionary.

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


def is_empty(H):
    """Returns True if `H` has no edges.

    Parameters
    ----------
    H : Hypergraph object
        Hypergraph of interest

    Returns
    -------
    bool
        True if `H` has no edges, and False otherwise.

    See Also
    --------
    create_empty_copy
    empty_hypergraph

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> xgi.is_empty(H)
    False
    """
    return len(H.edges) == 0


def maximal_simplices(SC):
    """Return the IDs of the maximal simplices of the input.

    Parameters
    ----------
    SC : xgi SimplicialComplex

    Returns
    -------
    maximal_simplices : list(int)
        A list of IDs correspondent to the maximal simplices in `SC`.

    """
    # This import needs to happen when this function is called, not when it is
    # defined.  Otherwise, a circular import error would happen.
    from .simplicialcomplex import SimplicialComplex

    if not isinstance(SC, SimplicialComplex):
        raise XGIError("The input must be a SimplicialComplex")

    max_simplices = []

    for i in SC.edges:
        maximal = True
        for j in SC.edges:
            # i is a subface of j, I remove it
            if SC.edges.members(i) < SC.edges.members(j):
                maximal = False
                break
        if maximal:
            max_simplices.append(i)
    return max_simplices


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
