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
    {0: 0.3333333333333333, 1: 0.3333333333333333, 2: 0.3333333333333333}

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

    The H-eigenvector terminology comes from Qi (2005) which
    defines a "tensor H-eigenpair".

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

    Scalable Tensor Methods for Nonuniform Hypergraphs,
    Sinan Aksoy, Ilya Amburg, Stephen Young,
    https://doi.org/10.1137/23M1584472

    Liqun Qi
    "Eigenvalues of a real supersymmetric tensor"
    Journal of Symbolic Computation, **40**, *6* (2005).
    https://doi.org/10.1016/j.jsc.2005.05.007.
    """
    c = xgi.h_eigenvector_centrality(net, max_iter, tol)
    return {n: c[n] for n in c if n in bunch}


def z_eigenvector_centrality(net, bunch, max_iter=10, tol=1e-6):
    r"""Compute the Z-eigenvector centrality of a hypergraph.

    The Z-eigenvector terminology comes from Qi (2005) which
    defines a "tensor Z-eigenpair".

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

    Liqun Qi
    "Eigenvalues of a real supersymmetric tensor"
    Journal of Symbolic Computation, **40**, *6* (2005).
    https://doi.org/10.1016/j.jsc.2005.05.007.
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
    """Computes nonlinear node-edge centralities.

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


def katz_centrality(net, bunch, cutoff=100):
    r"""Compute the Katz centrality of a hypergraph.

    Parameters
    ----------
    net : xgi.Hypergraph
        The hypergraph of interest.
    bunch : Iterable
        Nodes in `net`.
    cutoff : int
        Power at which to stop the series :math:`A + \alpha A^2 + \alpha^2 A^3 + \dots`
        Default value is 100.

    Returns
    -------
    dict
        node IDs are keys and centrality values
        are values. The centralities are 1-normalized.

    Raises
    ------
    XGIError
        If the hypergraph is empty.

    Notes
    -----
    [1] The Katz-centrality is defined as

    .. math::
        c = [(I - \alpha A^{t})^{-1} - I]{\bf 1},

    where :math:`A` is the adjacency matrix of the the (hyper)graph.
    Since :math:`A^{t} = A` for undirected graphs (our case), we have:


    .. math::
        &[I + A + \alpha A^2 + \alpha^2 A^3 + \dots](I - \alpha A^{t})

        & = [I + A + \alpha A^2 + \alpha^2 A^3 + \dots](I - \alpha A)

        & = (I + A + \alpha A^2 + \alpha^2 A^3 + \dots) - A - \alpha A^2

        & - \alpha^2 A^3 - \alpha^3 A^4 - \dots

        & = I

    And :math:`(I - \alpha A^{t})^{-1} = I + A + \alpha A^2 + \alpha^2 A^3 + \dots`
    Thus we can use the power series to compute the Katz-centrality.
    [2] The Katz-centrality of isolated nodes (no hyperedges contains them) is
    zero. The Katz-centrality of an empty hypergraph is not defined.

    References
    ----------
    See https://en.wikipedia.org/wiki/Katz_centrality#Alpha_centrality (visited
    May 20 2023) for a clear definition of Katz centrality.
    """
    c = xgi.katz_centrality(net, cutoff=cutoff)
    return {n: c[n] for n in c if n in bunch}


def local_simplicial_fraction(net, bunch, min_size=2, exclude_min_size=True):
    """The local simplicial fraction.

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
