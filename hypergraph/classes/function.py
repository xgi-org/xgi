"""Functional interface to graph methods and assorted utilities.
"""

from collections import Counter
import hypergraph as hg
from hypergraph.exception import HypergraphError

__all__ = [
    "nodes",
    "edges",
    "neighbors",
    "degree",
    "degree_histogram",
    "number_of_nodes",
    "number_of_edges",
    "has_edge",
    "freeze",
    "is_frozen",
    "create_empty_copy",
    "set_node_attributes",
    "get_node_attributes",
    "set_edge_attributes",
    "get_edge_attributes",
    "is_empty",
]


def nodes(H):
    """Returns an iterator over the hypergraph nodes.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    NodeView object
        The nodes of the hypergraph

    Examples
    --------
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.nodes(H)
    NodeView([1, 2, 3, 4])
    """
    return H.nodes

def has_edge_id(H, id):
    """Returns True if the edge id is in the hypergraph.

    This is the same as `v in H.edges` without KeyError exceptions.

    Parameters
    ----------
    id : hashable
        Edge id

    Returns
    -------
    bool
        True if edge is in the hypergraph, False otherwise.
    """
    try:
        return id in H._edge
    except KeyError:
        return False

def has_edge(H, edge):
    """Specifies whether an edge appears in the hypergraph as a different ID.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest
    edge : list or set
        A container of hashables that specifies an edge

    Returns
    -------
    bool
        Returns True if the set appears as an edge in the hypergraph.

    Examples
    --------
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.has_edge(H, [1, 2])
    True
    >>> hg.has_edge(H, [1, 3])
    False
    """
    return set(edge) in [set(H.edges(e)) for e in H.edges]


def edges(H, nbunch=None):
    """Returns an edge view of edges incident to nodes in nbunch.

    Return all edges if nbunch is unspecified or nbunch=None.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest
    nbunch : iterable, optional
        a list of edge IDs, by default None

    Returns
    -------
    EdgeView object
        The edges of a hypergraph

    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.edges(H)
    EdgeView([0, 1])
    """
    return H.edges(nbunch)


def neighbors(H, n):
    """Returns the neighbors of a node.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest
    n : hashable
        The node id

    Returns
    -------
    set
        The neighbors of that node

    Examples
    --------
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.neighbors(H, 1)
    {2}
    >>> hg.neighbors(H, 2)
    {1, 3, 4}
    """
    return H.neighbors(n)


def degree(H, nbunch=None, weight=None):
    """Returns a degree view of single node or of nbunch of nodes.
    If nbunch is omitted, then return degrees of *all* nodes.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest
    nbunch : iterable, optional
        a list of node IDs, by default None
    weight : string or bool, optional
        The name of the wieght attribute, by default None

    Returns
    -------
    DegreeView object
        The degrees of the hypergraph

    Examples
    --------
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.degree(H)
    DegreeView({1 : 1, 2 : 2, 3 : 1, 4 : 1})
    """
    return H.degree(nbunch, weight)


def number_of_nodes(H):
    """Returns the number of nodes in the hypergraph.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    int
        number of nodes in the hypergraph

    Examples
    --------
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.number_of_nodes(H)
    4
    """
    return H.number_of_nodes()


def number_of_edges(H):
    """Returns the number of edges in the hypergraph.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    int
        number of edges in the hypergraph

    Examples
    --------
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.number_of_edges(H)
    2
    """
    return H.number_of_edges()


def degree_histogram(H):
    """Returns a list of the frequency of each degree value.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    list
        A list of frequencies of degrees.
        The degree values are the index in the list.

    Notes
    -----
    Note: the bins are width one, hence len(list) can be large
    (Order(number_of_edges))

    Examples
    --------
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.degree_histogram(H)
    [0, 3, 1]
    """
    counts = Counter(d for n, d in H.degree())
    return [counts.get(i, 0) for i in range(max(counts) + 1)]


def frozen(*args, **kwargs):
    """Dummy method that raises an error when trying to modify frozen hypergraphs

    Raises
    ------
    hg.HypergraphError
        Raises error when user tries to modify the hypergraph

    Examples
    --------
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.freeze(H)
    >>> H.add_node(5)
    HypergraphError: "Frozen hypergraph can't be modified"
    """
    raise hg.HypergraphError("Frozen hypergraph can't be modified")


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
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.freeze(H)
    >>> H.add_node(5)
    HypergraphError: "Frozen hypergraph can't be modified"
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
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.freeze(H)
    >>> hg.is_frozen(H)
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
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> H_copy = hg.creat_empty_copy(H)
    >>> H_copy.nodes
    NodeView([1, 2, 3, 4])
    >>> H_copy.edges
    EdgeView([])
    """
    H = H.__class__()
    H.add_nodes_from(H.nodes(data=with_data))
    if with_data:
        H._hypergraph.update(H._hypergraph)
    return H


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
        try:  # `values` is a dict
            for n, v in values.items():
                try:
                    H._node_attr[n][name] = values[n]
                except KeyError:
                    pass
        except AttributeError:  # `values` is a constant
            for n in H:
                H._node_attr[n][name] = values
    else:  # `values` must be dict of dict
        for n, d in values.items():
            try:
                H._node_attr[n].update(d)
            except KeyError:
                pass


def get_node_attributes(H, name):
    """Get the node attributes for a hypergraph

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to get node attributes from
    name : string
       Attribute name

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
    return {n: d[name] for n, d in H._node_attr.items() if name in d}


def set_edge_attributes(H, values, name=None):
    """Set the edge attributes from a value or a dictionary of values

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
            for id, value in values.items():
                try:
                    H._edge_attr[id][name] = value
                except KeyError:
                    pass
        except AttributeError:
            # treat `values` as a constant
            for id in H.edges:
                H._edge_attr[id][name] = values
    else:
        # `values` consists of doct-of-dict {edge: {attr: value}} shape
        for id, value in values.items():
            try:
                H._edge_attr[id].update(values)
            except KeyError:
                pass


def get_edge_attributes(H, name):
    """Get the edge attributes of the hypergraph

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph to get edge attributes from
    name : string
       Attribute name

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
    edge_data = H.edges.data
    return {id: edge_data[edge][name] for edge in edge_data if name in edge_data[edge]}


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
    >>> import hypergraph as hg
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = hg.Hypergraph(hyperedge_list)
    >>> hg.is_empty(H)
    False
    """
    return len(H.edges) == 0
