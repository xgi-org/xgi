"""Node statistics.

This module is part of the stats package, and it defines node-level statistics.  That
is, each function defined in this module is assumed to define a node-quantity mapping.
Each callable defined here is accessible via a `Network` object, or a
:class:`~xgi.classes.reportviews.NodeView` object.  For more details, see the `tutorial
<https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

Examples
--------

>>> import xgi
>>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
>>> H.degree()
{1: 1, 2: 2, 3: 3, 4: 2, 5: 2}
>>> H.nodes.degree.asdict()
{1: 1, 2: 2, 3: 3, 4: 2, 5: 2}

"""

from warnings import warn

import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import eigsh

import xgi

__all__ = [
    "attrs",
    "degree",
    "average_neighbor_degree",
    "clustering",
    "cec_centrality",
    "node_edge_centrality",
]


def attrs(net, bunch, attr=None, missing=None):
    """Access node attributes.

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
        Value to impute in case a node does not have an attribute with name `attr`.
        Default is None.

    Returns
    -------
    dict
        If attr is None, return a nested dict of the form `{node: {"attr": val}}`.
        Otherwise, return a simple dict of the form `{node: val}`.

    Notes
    -----
    When requesting all attributes (i.e. when `attr` is None), no value is imputed.

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
    >>> H.add_nodes_from([
    ...         (1, {"color": "red", "name": "horse"}),
    ...         (2, {"color": "blue", "name": "pony"}),
    ...         (3, {"color": "yellow", "name": "zebra"}),
    ...         (4, {"color": "red", "name": "orangutan", "age": 20}),
    ...         (5, {"color": "blue", "name": "fish", "age": 2}),
    ...     ])

    Access all attributes as different types.

    >>> H.nodes.attrs.asdict() # doctest: +NORMALIZE_WHITESPACE
    {1: {'color': 'red', 'name': 'horse'},
     2: {'color': 'blue', 'name': 'pony'},
     3: {'color': 'yellow', 'name': 'zebra'},
     4: {'color': 'red', 'name': 'orangutan', 'age': 20},
     5: {'color': 'blue', 'name': 'fish', 'age': 2}}
    >>> H.nodes.attrs.asnumpy() # doctest: +NORMALIZE_WHITESPACE
    array([{'color': 'red', 'name': 'horse'},
           {'color': 'blue', 'name': 'pony'},
           {'color': 'yellow', 'name': 'zebra'},
           {'color': 'red', 'name': 'orangutan', 'age': 20},
           {'color': 'blue', 'name': 'fish', 'age': 2}],
          dtype=object)

    Access a single attribute as different types.

    >>> H.nodes.attrs('color').asdict()
    {1: 'red', 2: 'blue', 3: 'yellow', 4: 'red', 5: 'blue'}
    >>> H.nodes.attrs('color').aslist()
    ['red', 'blue', 'yellow', 'red', 'blue']

    By default, None is imputed when a node does not have the requested attribute.

    >>> H.nodes.attrs('age').asdict()
    {1: None, 2: None, 3: None, 4: 20, 5: 2}

    Use `missing` to change the imputed value.

    >>> H.nodes.attrs('age', missing=100).asdict()
    {1: 100, 2: 100, 3: 100, 4: 20, 5: 2}

    """
    if isinstance(attr, str):
        return {n: net._node_attr[n].get(attr, missing) for n in bunch}
    elif attr is None:
        return {n: net._node_attr[n] for n in bunch}
    else:
        raise ValueError('"attr" must be str or None')


def degree(net, bunch, order=None, weight=None):
    """Node degree.

    The degree of a node is the number of edges it belongs to.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    order : int | None
        If not None (default), only count the edges of the given order.
    weight : str | None
        If not None, specifies the name of the edge attribute that determines the weight
        of each edge.

    Returns
    -------
    dict

    """
    if order is None and weight is None:
        return {n: len(net._node[n]) for n in bunch}
    if order is None and weight:
        return {
            n: sum(net._edge_attr[e].get(weight, 1) for e in net._node[n])
            for n in bunch
        }
    if order is not None and weight is None:
        return {
            n: len([e for e in net._node[n] if len(net._edge[e]) == order + 1])
            for n in bunch
        }
    if order is not None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node[n]
                if len(net._edge[e]) == order + 1
            )
            for n in bunch
        }


def average_neighbor_degree(net, bunch):
    """Average neighbor degree.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.

    Returns
    -------
    dict

    Examples
    --------
    >>> import xgi, numpy as np
    >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
    >>> np.round(H.nodes.average_neighbor_degree.asnumpy(), 3)
    array([2.5  , 2.   , 1.75 , 2.333, 2.333])

    """
    result = {}
    for n in bunch:
        neighbors = net.neighbors(n)
        result[n] = sum(len(net._node[nbr]) for nbr in neighbors)
        result[n] = result[n] / len(neighbors) if neighbors else 0
    return result


def clustering(net, bunch):
    """Local clustering coefficient.

    The clustering coefficient of a node `n` is defined as `num / denom`, where `num`
    equals `A^3[n, n]` and `denom` equals `d*(d-1)/2`.  Here `A` is the adjacency matrix
    of the network and `d` is the degree of `n`.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.

    Returns
    -------
    dict

    Notes
    -----
    This is a direct generalization of the definition of local clustering coefficient
    for graphs.  It has not been tested on hypergraphs.

    Examples
    --------
    >>> import xgi, numpy as np
    >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
    >>> np.round(H.nodes.clustering.asnumpy(), 3)
    array([0.   , 4.   , 1.333, 3.   , 3.   ])

    """
    adj, index = xgi.adjacency_matrix(net, index=True)
    node_to_index = {n: i for i, n in index.items()}
    mat = adj.dot(adj).dot(adj)
    result = {}
    for n in bunch:
        deg = len(net.nodes.memberships(n))
        denom = deg * (deg - 1) / 2
        if denom <= 0:
            result[n] = 0.0
        else:
            i = node_to_index[n]
            result[n] = mat[i, i] / denom / 2
    return result


def cec_centrality(net, bunch):
    """Compute the CEC centrality of a hypergraph.

    Parameters
    ----------
    net : xgi.Hypergraph
        The hypergraph of interest.
    bunch : Iterable
        Nodes in `net`.

    Returns
    -------
    dict
        Centrality, where keys are node IDs and values are centralities.

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    W, node_dict = xgi.clique_motif_matrix(net, index=True)
    _, v = eigsh(W.asfptype(), k=1, which="LM")

    return {node_dict[n]: v[n] for n in node_dict if node_dict[n] in bunch}





def node_edge_centrality(H, bunch, max_iter=100, tol=1e-6):
    """Computes node centralities.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    max_iter : int, default: 100
        Number of iterations at which the algorithm terminates
        if convergence is not reached.
    tol : float > 0, default: 1e-6
        The total allowable error in the node and edge centralities.

    Returns
    -------
    dict, dict
        The node centrality where keys are node IDs and values are associated
        centralities and the edge centrality where keys are the edge IDs and
        values are associated centralities.

    Notes
    -----
    In the paper from which this was taken, it includes general functions
    for both nodes and edges, nodes and edges may be weighted, and one can
    choose different norms for normalization, all of which are not yet
    implemented.

    This method does not output the node centralities even though they are computed.

    References
    ----------
    Node and edge nonlinear eigenvector centrality for hypergraphs,
    Francesco Tudisco & Desmond J. Higham,
    https://doi.org/10.1038/s42005-021-00704-2
    """
    x = np.ones(H.num_nodes) / H.num_nodes
    y = np.ones(H.num_edges) / H.num_edges

    I, node_dict, _ = xgi.incidence_matrix(H, index=True)

    check = np.inf

    f = lambda x: np.power(x, 2)
    g = lambda x: np.power(x, 0.5)

    iter = 0
    while iter < max_iter:
        u = np.multiply(x, g(I * f(y)))
        v = np.multiply(y, g(I.T * f(x)))
        new_x = u / norm(u)
        new_y = v / norm(v)

        check = norm(new_x - x) + norm(new_y - y)
        if check < tol:
            return {node_dict[n]: new_x[n] for n in node_dict if node_dict[n] in bunch}
        else:
            x = new_x.copy()
            y = new_y.copy()
    warn("Iteration did not converge!")
    return {node_dict[n]: new_x[n] for n in node_dict if node_dict[n] in bunch}
