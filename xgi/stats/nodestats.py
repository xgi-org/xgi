"""Node statistics.

This module is part of the stats package, and it defines node-level statistics.  That
is, each function defined in this module is assumed to define a node-quantity mapping.
Each callable defined here is accessible via a `Network` object, or a
:class:`~xgi.core.views.NodeView` object.  For more details, see the `tutorial
<https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

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
    "z_eigenvector_centrality",
    "node_edge_centrality",
    "katz_centrality",
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
    """Clustering coefficient based on the pairwise projection of the hypergraph.

    See :func:`xgi.algorithms.clustering.clustering_coefficient` for the definition,
    formula, and references.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.

    Returns
    -------
    dict

    See Also
    --------
    ~xgi.algorithms.clustering.clustering_coefficient
    local_clustering_coefficient
    two_node_clustering_coefficient

    """
    cc = xgi.clustering_coefficient(net)
    return {n: cc[n] for n in cc if n in bunch}


def local_clustering_coefficient(net, bunch):
    """Local clustering coefficient based on edge overlap.

    See :func:`xgi.algorithms.clustering.local_clustering_coefficient` for the
    definition and references.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.

    Returns
    -------
    dict
        keys are node IDs and values are the clustering coefficients.

    See Also
    --------
    ~xgi.algorithms.clustering.local_clustering_coefficient
    clustering_coefficient
    two_node_clustering_coefficient

    """
    cc = xgi.local_clustering_coefficient(net)
    return {n: cc[n] for n in cc if n in bunch}


def two_node_clustering_coefficient(net, bunch, kind="union"):
    """Average over all two-node clustering coefficients involving each node.

    See :func:`xgi.algorithms.clustering.two_node_clustering_coefficient` for the
    definition and references.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    kind : str
        The type of two-node clustering coefficient: "union", "min", or "max".
        By default, "union".

    Returns
    -------
    dict
        nodes are keys, clustering coefficients are values.

    See Also
    --------
    ~xgi.algorithms.clustering.two_node_clustering_coefficient
    clustering_coefficient
    local_clustering_coefficient

    """
    cc = xgi.two_node_clustering_coefficient(net, kind=kind)
    return {n: cc[n] for n in cc if n in bunch}


def clique_eigenvector_centrality(net, bunch, tol=1e-6):
    """Clique motif eigenvector centrality of a hypergraph.

    See :func:`xgi.algorithms.centrality.clique_eigenvector_centrality` for the
    definition and references.

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

    See Also
    --------
    ~xgi.algorithms.centrality.clique_eigenvector_centrality

    """
    c = xgi.clique_eigenvector_centrality(net, tol)
    return {n: c[n] for n in c if n in bunch}


def h_eigenvector_centrality(net, bunch, max_iter=10, tol=1e-6):
    """H-eigenvector centrality of a hypergraph.

    See :func:`xgi.algorithms.centrality.h_eigenvector_centrality` for the definition
    and references.

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

    See Also
    --------
    ~xgi.algorithms.centrality.h_eigenvector_centrality

    """
    c = xgi.h_eigenvector_centrality(net, max_iter, tol)
    return {n: c[n] for n in c if n in bunch}


def z_eigenvector_centrality(net, bunch, max_iter=10, tol=1e-6):
    """Z-eigenvector centrality of a hypergraph.

    See :func:`xgi.algorithms.centrality.z_eigenvector_centrality` for the definition
    and references.

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

    See Also
    --------
    ~xgi.algorithms.centrality.z_eigenvector_centrality

    """
    c = xgi.z_eigenvector_centrality(net, max_iter, tol)
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
    """Node component of the nonlinear node-edge centrality.

    See :func:`xgi.algorithms.centrality.node_edge_centrality` for the definition,
    parameters, and references.

    Parameters
    ----------
    net : Hypergraph
        The hypergraph of interest.
    bunch : Iterable
        Nodes in `net`.

    Returns
    -------
    dict
        Node centralities.

    See Also
    --------
    ~xgi.algorithms.centrality.node_edge_centrality

    """
    c, _ = xgi.node_edge_centrality(net, f, g, phi, psi, max_iter, tol)
    return {n: c[n] for n in c if n in bunch}


def katz_centrality(net, bunch, cutoff=100):
    """Katz centrality of a hypergraph.

    See :func:`xgi.algorithms.centrality.katz_centrality` for the definition, formula,
    and references.

    Parameters
    ----------
    net : xgi.Hypergraph
        The hypergraph of interest.
    bunch : Iterable
        Nodes in `net`.
    cutoff : int
        Power at which to truncate the underlying series. Default 100.

    Returns
    -------
    dict
        Node IDs are keys and centrality values are values (1-normalized).

    Raises
    ------
    XGIError
        If the hypergraph is empty.

    See Also
    --------
    ~xgi.algorithms.centrality.katz_centrality

    """
    c = xgi.katz_centrality(net, cutoff=cutoff)
    return {n: c[n] for n in c if n in bunch}


def local_simplicial_fraction(net, bunch, min_size=2, exclude_min_size=True):
    """The local simplicial fraction.

    For each node, computes :func:`xgi.algorithms.simpliciality.simplicial_fraction`
    on the subhypergraph induced by the node and its neighbors.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    min_size: int, default: 2
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.
    exclude_min_size : bool, optional
        Whether to include minimal simplices when counting simplices, by default True

    Returns
    -------
    dict

    See Also
    --------
    ~xgi.algorithms.simpliciality.simplicial_fraction

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    s = dict()
    for n in bunch:
        nbrs = net.nodes.neighbors(n)
        if len(nbrs) == 0:
            s[n] = np.nan
        else:
            nbrs.add(n)
            sh = xgi.subhypergraph(net, nodes=nbrs)
            s[n] = xgi.simplicial_fraction(sh, min_size, exclude_min_size)
    return s


def local_edit_simpliciality(net, bunch, min_size=2, exclude_min_size=True):
    """The local edit simpliciality.

    For each node, computes :func:`xgi.algorithms.simpliciality.edit_simpliciality`
    on the subhypergraph induced by the node and its neighbors.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    min_size: int, default: 2
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.
    exclude_min_size : bool, optional
        Whether to include minimal simplices when counting simplices, by default True

    Returns
    -------
    dict

    See Also
    --------
    ~xgi.algorithms.simpliciality.edit_simpliciality

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    s = dict()
    for n in bunch:
        nbrs = net.nodes.neighbors(n)
        if len(nbrs) == 0:
            s[n] = np.nan
        else:
            nbrs.add(n)
            sh = xgi.subhypergraph(net, nodes=nbrs)
            s[n] = xgi.edit_simpliciality(sh, min_size, exclude_min_size)
    return s


def local_face_edit_simpliciality(net, bunch, min_size=2, exclude_min_size=True):
    """The local face edit simpliciality.

    For each node, computes
    :func:`xgi.algorithms.simpliciality.face_edit_simpliciality` on the subhypergraph
    induced by the node and its neighbors.

    Parameters
    ----------
    net : xgi.Hypergraph
        The network.
    bunch : Iterable
        Nodes in `net`.
    min_size: int, default: 2
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.
    exclude_min_size : bool, optional
        Whether to include minimal simplices when counting simplices, by default True

    Returns
    -------
    dict

    See Also
    --------
    ~xgi.algorithms.simpliciality.face_edit_simpliciality

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    s = dict()
    for n in bunch:
        nbrs = net.nodes.neighbors(n)
        if len(nbrs) == 0:
            s[n] = np.nan
        else:
            nbrs.add(n)
            sh = xgi.subhypergraph(net, nodes=nbrs)
            s[n] = xgi.face_edit_simpliciality(sh, min_size, exclude_min_size)
    return s
