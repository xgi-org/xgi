"""General utilities."""

from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from itertools import chain, combinations, count

import numpy as np
import pandas as pd
import requests

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
    "hist",
    "binomial_sequence",
    "get_network_type",
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

    def __add__(self, dict):
        d = dict.copy()
        d.update(self)
        return d


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
    iterable,
    include_empty=False,
    include_full=False,
    include_singletons=True,
    max_size=None,
):
    """Returns all possible subsets of the elements in iterable, with options
    to include the empty set and the set containing all elements, and to set
    the maximum subset size.

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
    max_size: int, default: None
        Maximum size of the returned subsets.

    Returns
    -------
    itertools.chain

    Notes
    -----
    include_empty overrides include_singletons if True: singletons will always
    be included if the empty set is.
    Likewise, max_size will override other arguments: if set to -1, no subset
    will be returned.

    Examples
    --------
    >>> import xgi
    >>> list(xgi.powerset([1,2,3,4])) # doctest: +NORMALIZE_WHITESPACE
    [(1,), (2,), (3,), (4,), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),
     (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]

    """

    start = 1 if include_singletons else 2
    start = 0 if include_empty else start  # overrides include_singletons if True

    s = list(iterable)

    if max_size is None:
        max_size = len(s) if include_full else len(s) - 1
    else:
        max_size = min(max_size, len(s))

    return chain.from_iterable(combinations(s, r) for r in range(start, max_size + 1))


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
    min_val : float or np.inf
        Minimum value found in `dicty`. Is set to np.inf if `where` indicated
        nowhere or if all values are `np.inf`.
    """

    min_val = np.inf
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


def convert_labels_to_integers(net, label_attribute="label", in_place=False):
    """Relabel node and edge IDs to be sequential integers.

    Parameters
    ----------
    net : Hypergraph, DiHypergraph, or SimplicialComplex
        The higher-order network of interest

    label_attribute : string, default: "label"
        The attribute name that stores the old node and edge labels

    in_place : bool, optional
        Whether the relabeling should modify the network in-place or return a new
        network.

    Returns
    -------
    Hypergraph, DiHypergraph, or SimplicialComplex
        A new higher-order network with nodes and edges with sequential IDs starting at 0.
        The old IDs are stored in the "label" attribute for both nodes and edges.

    Notes
    -----
    The "relabeling" will occur even if the node/edge IDs are sequential.
    Because the old IDs are stored in the "label" attribute for both nodes and edges,
    the old "label" values (if they exist) will be overwritten.
    """
    from ..core import DiHypergraph, Hypergraph, SimplicialComplex

    node_dict = dict(zip(net.nodes, range(net.num_nodes)))
    edge_dict = dict(zip(net.edges, range(net.num_edges)))

    if not in_place:
        net = net.copy()

    node_attrs = net._node_attr.copy()
    edge_attrs = net._edge_attr.copy()
    edges = net._edge.copy()
    net.clear(remove_net_attr=False)
    net.add_nodes_from((id, deepcopy(node_attrs[n])) for n, id in node_dict.items())
    net.set_node_attributes({id: {label_attribute: n} for n, id in node_dict.items()})
    if isinstance(net, SimplicialComplex):
        net.add_simplices_from(
            (
                {node_dict[n] for n in edge},
                edge_dict[e],
                deepcopy(edge_attrs[e]),
            )
            for e, edge in edges.items()
        )
    elif isinstance(net, Hypergraph):
        net.add_edges_from(
            (
                {node_dict[n] for n in edge},
                edge_dict[e],
                deepcopy(edge_attrs[e]),
            )
            for e, edge in edges.items()
        )
    elif isinstance(net, DiHypergraph):
        net.add_edges_from(
            (
                [
                    {node_dict[n] for n in edge["in"]},
                    {node_dict[n] for n in edge["out"]},
                ],
                edge_dict[e],
                deepcopy(edge_attrs[e]),
            )
            for e, edge in edges.items()
        )

    net.set_edge_attributes({id: {label_attribute: e} for e, id in edge_dict.items()})

    if not in_place:
        return net


def hist(vals, bins=10, bin_edges=False, density=False, log_binning=False):
    """Return the distribution of a numpy array.

    Parameters
    ----------
    vals : numpy.ndarray
        The array of values
    bins : int, list, or numpy.ndarray
        The number of bins or the bin edges.
        By default, 10.
    bin_edges : bool
        Whether to also output the min and max of each bin,
        by default, False.
    density : bool
        Whether to normalize the resulting distribution.
        By default, False.
    log_binning : bool
        Whether to bin the values with log-sized bins.
        By default, False.

    Returns
    -------
    ~pandas.DataFrame
        A two-column table with "bin_center" and "value" columns,
        where "value" is a count or a probability. If `bin_edges`
        is True, outputs two additional columns, `bin_lo` and `bin_hi`,
        which outputs the left and right bin edges respectively.

    Notes
    -----
    Originally from https://github.com/jkbren/networks-and-dataviz

    """
    # We need to define the support of our distribution
    lower_bound = np.min(vals)
    upper_bound = np.max(vals)

    if log_binning:
        lower_bound = np.log10(lower_bound) if lower_bound > 0 else 0.0
        upper_bound = np.log10(upper_bound)

    # And the bins
    if isinstance(bins, int):
        if log_binning:
            bins = np.logspace(lower_bound, upper_bound, bins + 1, base=10)
        else:
            bins = np.linspace(lower_bound, upper_bound, bins + 1)
    elif not isinstance(bins, (list, np.ndarray)):
        raise XGIError("Bins must be an integer, a list, or a numpy array.")

    # Then we can compute the histogram using numpy
    y, __ = np.histogram(vals, bins=bins, density=density)
    # Now, we need to compute for each y the bin centers
    x = bins[1:] - np.diff(bins) / 2.0

    if bin_edges:
        return pd.DataFrame.from_dict(
            {"bin_center": x, "value": y, "bin_lo": bins[:-1], "bin_hi": bins[1:]}
        )
    else:
        return pd.DataFrame.from_dict({"bin_center": x, "value": y})


def binomial_sequence(k, N):
    """Returns the set of all the distinct strings (order counts) with k ones
    and N-k zeros. binomial_sequence(2, 4) will output '1010', '1100', '0011', '0110',
    '0101' and '1001'.

    Parameters
    ----------
    k : int
        Number of ones in the strings. Must be greater or equal to zero.
    N : int
        Length of the strings. Must be positive as well.

    Returns
    -------
    res : set
        Set containing all the strings (they are distinct). The empty set is
        returned if N = 0 or if k > N.
    """

    if k < 0 or N < 0:
        raise ValueError("binomial_sequence must be given positive integers.")

    res = set()

    if k == 0:
        # seq = str()
        # for i in range(N):
        #    seq += "0"
        # res.add(seq)
        res = {"0" * N}
    elif N == 0:
        pass
    else:  # k and N are greater than zero
        for seq in binomial_sequence(k, N - 1):
            res.add(seq + "0")
        for seq in binomial_sequence(k - 1, N - 1):
            res.add(seq + "1")
    return res


def get_network_type(H):
    return str(type(H)).split(".")[-1].split("'")[0].lower()
