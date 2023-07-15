"""General utilities."""

from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from itertools import chain, combinations, count

import requests
from numpy import infty

from xgi.exception import IDNotFound, XGIError

__all__ = [
    "IDDict",
    "dual_dict",
    "powerset",
    "update_uid_counter",
    "find_triangles",
    "request_json_from_url",
    "request_json_from_url_cached",
    "subfaces",
    "convert_labels_to_integers",
]


class IDDict(dict):
    """A dict that holds (node or edge) IDs.

    For internal use only.  Adds input validation functionality to the internal dicts
    that hold nodes and edges in a network.

    """

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError as e:
            raise IDNotFound(f"ID {item} not found") from e

    def __setitem__(self, item, value):
        if item is None:
            raise XGIError("None cannot be a node or edge")
        try:
            return dict.__setitem__(self, item, value)
        except TypeError as e:
            raise TypeError(f"ID {item} not a valid type") from e

    def __delitem__(self, item):
        try:
            return dict.__delitem__(self, item)
        except KeyError as e:
            raise IDNotFound(f"ID {item} not found") from e


def dual_dict(edge_dict):
    """Given a dictionary with IDs as keys
    and sets as values, return the dual.

    Parameters
    ----------
    edge_dict : dict
        A dictionary where the keys are
        IDs and the values are sets of hashables

    Returns
    -------
    dict
        A dictionary with IDs as keys
        and sets as values, but the reverse of
        the original dict.

    Examples
    --------
    >>> import xgi
    >>> xgi.dual_dict({0 : [1, 2, 3], 1 : [0, 2]})
    {1: {0}, 2: {0, 1}, 3: {0}, 0: {1}}

    """
    node_dict = defaultdict(set)
    for edge_id, members in edge_dict.items():
        for node in members:
            node_dict[node].add(edge_id)

    return dict(node_dict)


def powerset(
    iterable, include_empty=False, include_full=False, include_singletons=True
):
    """Returns all possible subsets of the elements in iterable, with options
    to include the empty set and the set containing all elements.

    Parameters
    ----------
    iterable : list-like
        List of elements
    include_empty: bool, default: False
        Whether to include the empty set
    include_singletons: bool, default: True
        Whether to include singletons
    include_full: bool, default: False
        Whether to include the set containing all elements of iterable

    Returns
    -------
    itertools.chain

    Notes
    -----
    include_empty overrides include_singletons if True: singletons will always
    be included if the empty set is.

    Examples
    --------
    >>> import xgi
    >>> list(xgi.powerset([1,2,3,4])) # doctest: +NORMALIZE_WHITESPACE
    [(1,), (2,), (3,), (4,), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),
     (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]

    """

    start = 1 if include_singletons else 2
    start = 0 if include_empty else start  # overrides include_singletons if True
    end = 1 if include_full else 0

    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(start, len(s) + end))


def update_uid_counter(H, new_id):
    """
    Helper function to make sure the uid counter is set correctly after
    adding an edge with a user-provided ID.

    If we don't set the start of self._edge_uid correctly, it will start at 0,
    which will overwrite any existing edges when calling add_edge().  First, we
    use the somewhat convoluted float(e).is_integer() instead of using
    isinstance(e, int) because there exist integer-like numeric types (such as
    np.int32) which fail the isinstance() check.

    Parameters
    ----------
    H : xgi.Hypergraph
        Hypergraph of which to update the uid counter
    id : any hashable type
        User-provided ID.

    """
    uid = next(H._edge_uid)
    if (
        not isinstance(new_id, str)
        and not isinstance(new_id, tuple)
        and float(new_id).is_integer()
        and uid <= new_id
    ):
        # tuple comes from merging edges and doesn't have as as_integer() method.
        start = int(new_id) + 1
        # we set the start at one plus the maximum edge ID that is an integer,
        # because count() only yields integer IDs.
    else:
        start = uid
    H._edge_uid = count(start=start)


def find_triangles(G):
    """Returns list of 3-node cliques present in a graph

    Parameters
    ----------
    G : networkx Graph
        Graph to consider

    Returns
    -------
    list of 3-node cliques (triangles)
    """

    triangles = set(
        frozenset((n, nbr, nbr2))
        for n in G
        for nbr, nbr2 in combinations(G[n], 2)
        if nbr in G[nbr2]
    )
    return [set(tri) for tri in triangles]


def min_where(dicty, where):
    """
    Finds the minimum value of a dictonary `dicty`. The dictonary `where`
    indicates which keys to take into account. The minimum is eventualy
    infinite.

    Parameters
    ----------
    dicty : dict
        Dictionary of values (int, float...) from which to find
        the minimum.
    where : dict
        Dictionary of booleans that has the same keys as `dicty`.
        The minimum will be searched among the values for which
        `where[key]` is TRUE.

    Return
    ------
    min_val : float or np.Inf
        Minimum value found in `dicty`. Is set to np.infty if `where` indicated
        nowhere or if all values are `np.infty`.
    """

    min_val = infty
    for key in dicty.keys():
        if where[key]:
            if dicty[key] < min_val:
                min_val = dicty[key]
            else:
                pass
        else:
            pass
    return min_val


def request_json_from_url(url):
    """HTTP request json file and return as dict.

    Parameters
    ----------
    url : str
        The url where the json file is located.

    Returns
    -------
    dict
        A dictionary of the JSON requested.

    Raises
    ------
    XGIError
        If the connection fails or if there is a bad HTTP request.
    """

    try:
        r = requests.get(url)
    except requests.ConnectionError:
        raise XGIError("Connection Error!")

    if r.ok:
        return r.json()
    else:
        raise XGIError(f"Error: HTTP response {r.status_code}")


@lru_cache(maxsize=None)
def request_json_from_url_cached(url):
    """HTTP request json file and return as dict.

    Parameters
    ----------
    url : str
        The url where the json file is located.

    Returns
    -------
    dict
        A dictionary of the JSON requested.

    Raises
    ------
    XGIError
        If the connection fails or if there is a bad HTTP request.
    """

    try:
        r = requests.get(url)
    except requests.ConnectionError:
        raise XGIError("Connection Error!")

    if r.ok:
        return r.json()
    else:
        raise XGIError(f"Error: HTTP response {r.status_code}")


def subfaces(edges, order=None):
    """Returns the subfaces of a list of hyperedges

    Parameters
    ---------
    edges: list of edges
        Edges to consider, as tuples of nodes
    order: {None, -1, int}, optional
        If None, compute subfaces recursively down to nodes.
        If -1, compute subfaces the order below (e.g. edges for a triangle).
        If d > 0, compute the subfaces of order d.
        By default, None.

    Returns
    -------
    faces: list of sets
        List of hyperedges that are subfaces of input hyperedges.

    Raises
    ------
    XGIError
        Raises error when order is larger than the max order of input edges

    Notes
    -----
    Hyperedges in the returned list are not unique, they may appear more than once
    if they are subfaces or more than one edge from the input edges.

    Examples
    --------
    >>> import xgi
    >>> edges = [{1,2,3,4}, {3,4,5}]
    >>> xgi.subfaces(edges) # doctest: +NORMALIZE_WHITESPACE
    [(1,), (2,), (3,), (4,), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (1, 2, 3),
     (1, 2, 4), (1, 3, 4), (2, 3, 4), (3,), (4,), (5,), (3, 4), (3, 5), (4, 5)]
    >>> xgi.subfaces(edges, order=-1)
    [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4), (3, 4), (3, 5), (4, 5)]
    >>> xgi.subfaces(edges, order=2)
    [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4), (3, 4, 5)]

    """

    max_order = len(max(edges, key=len)) - 1
    if order and order > max_order:
        raise XGIError(
            "order must be less or equal to the maximum "
            f"order among the edges: {max_order}."
        )

    faces = []
    for edge in edges:
        size = len(edge)

        if size <= 1:  # down from a node is an empty tuple
            continue

        if order is None:  # add all subfaces down to nodes
            faces_to_add = list(powerset(edge))
        elif order == -1:  # add subfaces of order below
            faces_to_add = list(combinations(edge, size - 1))
        elif order >= 0:  # add subfaces of order d
            faces_to_add = list(combinations(edge, order + 1))

        faces += faces_to_add
    return faces


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
    from ..core import Hypergraph

    node_dict = dict(zip(H.nodes, range(H.num_nodes)))
    edge_dict = dict(zip(H.edges, range(H.num_edges)))
    temp_H = Hypergraph()
    temp_H._hypergraph = deepcopy(H._hypergraph)

    temp_H.add_nodes_from((id, deepcopy(H.nodes[n])) for n, id in node_dict.items())
    temp_H.set_node_attributes(
        {n: {label_attribute: id} for id, n in node_dict.items()}
    )

    temp_H.add_edges_from(
        (
            {node_dict[n] for n in e},
            edge_dict[id],
            deepcopy(H.edges[id]),
        )
        for id, e in H.edges.members(dtype=dict).items()
    )
    temp_H.set_edge_attributes(
        {e: {label_attribute: id} for id, e in edge_dict.items()}
    )

    return temp_H
