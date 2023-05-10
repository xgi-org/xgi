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

import numpy as np

import xgi

__all__ = [
    "attrs",
    "degree",
    "average_neighbor_degree",
    "local_clustering_coefficient",
    "clustering_coefficient",
    "two_node_clustering_coefficient",
    "clique_eigenvector_centrality",
    "h_eigenvector_centrality",
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
        neighbors = net.nodes.neighbors(n)
        result[n] = sum(len(net._node[nbr]) for nbr in neighbors)
        result[n] = result[n] / len(neighbors) if neighbors else 0
    return result


def clustering_coefficient(net, bunch):
    """Local clustering coefficient.

    This clustering coefficient is defined as the
    clustering coefficient of the unweighted pairwise
    projection of the hypergraph, i.e., `num / denom`,
    where `num` equals `A^3[n, n]` and `denom` equals
    `nu*(nu-1)/2`.  Here `A` is the adjacency matrix
    of the network and `nu` is the number of pairwise
    neighbors of `n`.

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
    >>> H.nodes.two_node_clustering_coefficient.asnumpy()
    array([0.41666667, 0.45833333, 0.58333333, 0.66666667, 0.66666667])

    """
    cc = xgi.clustering_coefficient(net)
    return {n: cc[n] for n in cc if n in bunch}


def local_clustering_coefficient(net, bunch):
    """Compute the local clustering coefficient.

    This clustering coefficient is based on the
    overlap of the edges connected to a given node,
    normalized by the size of the node's neighborhood.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.

    Returns
    -------
    dict
        keys are node IDs and values are the
        clustering coefficients.

    References
    ----------
    "Properties of metabolic graphs: biological organization or representation
    artifacts?"  by Wanding Zhou and Luay Nakhleh.
    https://doi.org/10.1186/1471-2105-12-132

    "Hypergraphs for predicting essential genes using multiprotein complex data"
    by Florian Klimm, Charlotte M. Deane, and Gesine Reinert.
    https://doi.org/10.1093/comnet/cnaa028

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(3, [1, 1])
    >>> H.nodes.local_clustering_coefficient.asdict()
    {0: 1.0, 1: 1.0, 2: 1.0}

    """
    cc = xgi.local_clustering_coefficient(net)
    return {n: cc[n] for n in cc if n in bunch}


def two_node_clustering_coefficient(net, bunch, kind="union"):
    """Return the clustering coefficients for
    each node in a Hypergraph.

    This definition averages over all of the
    two-node clustering coefficients involving the node.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    kind : str
        The type of two-node clustering coefficient.
        Types are:

        * "union"
        * "min"
        * "max"

    by default, "union".

    Returns
    -------
    dict
        nodes are keys, clustering coefficients are values.

    References
    ----------
    "Clustering Coefficients in Protein Interaction Hypernetworks"
    by Suzanne Gallagher and Debra Goldberg.
    DOI: 10.1145/2506583.2506635

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(3, [1, 1])
    >>> H.nodes.two_node_clustering_coefficient.asdict()
    {0: 0.5, 1: 0.5, 2: 0.5}
    """
    cc = xgi.two_node_clustering_coefficient(net, kind=kind)
    return {n: cc[n] for n in cc if n in bunch}


def clique_eigenvector_centrality(net, bunch, tol=1e-6):
    """Compute the clique motif eigenvector centrality of a hypergraph.

    Parameters
    ----------
    net : xgi.Hypergraph
        The hypergraph of interest.
    bunch : Iterable
        Nodes in `net`.
    tol : float > 0, default: 1e-6
        The desired L2 error in the centrality vector.

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
    c = xgi.clique_eigenvector_centrality(net, tol)
    return {n: c[n] for n in c if n in bunch}


def h_eigenvector_centrality(net, bunch, max_iter=10, tol=1e-6):
    """Compute the H-eigenvector centrality of a hypergraph.

    Parameters
    ----------
    net : xgi.Hypergraph
        The hypergraph of interest.
    bunch : Iterable
        Nodes in `net`.
    max_iter : int, default: 10
        The maximum number of iterations before the algorithm terminates.
    tol : float > 0, default: 1e-6
        The desired L2 error in the centrality vector.

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
    c = xgi.h_eigenvector_centrality(net, max_iter, tol)
    return {n: c[n] for n in c if n in bunch}


def node_edge_centrality(
    net,
    bunch,
    f=lambda x: np.power(x, 2),
    g=lambda x: np.power(x, 0.5),
    phi=lambda x: np.power(x, 2),
    psi=lambda x: np.power(x, 0.5),
    max_iter=100,
    tol=1e-6,
):
    """Computes node centralities.

    Parameters
    ----------
    net : Hypergraph
        The hypergraph of interest
    bunch : Iterable
        Edges in `net`
    f : lambda function, default: x^2
        The function f as described in Tudisco and Higham.
        Must accept a numpy array.
    g : lambda function, default: x^0.5
        The function g as described in Tudisco and Higham.
        Must accept a numpy array.
    phi : lambda function, default: x^2
        The function phi as described in Tudisco and Higham.
        Must accept a numpy array.
    psi : lambda function, default: x^0.5
        The function psi as described in Tudisco and Higham.
        Must accept a numpy array.
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
    c, _ = xgi.node_edge_centrality(net, f, g, phi, psi, max_iter, tol)
    return {n: c[n] for n in c if n in bunch}
