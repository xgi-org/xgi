"""Laplacian matrices associated to hypergraphs.

Note that the order of the rows and columns of the
matrices in this module correspond to the order in
which nodes/edges are added to the hypergraph or
simplicial complex. If the node and edge IDs are
able to be sorted, the following is an example to sort
by the node and edge IDs.

>>> import xgi
>>> import pandas as pd
>>> H = xgi.Hypergraph([[1, 2, 3, 7], [4], [5, 6, 7]])
>>> I, nodedict, edgedict = xgi.incidence_matrix(H, sparse=False, index=True)
>>> # Sorting the resulting numpy array:
>>> sortedI = I.copy()
>>> sortedI = sortedI[sorted(nodedict, key=nodedict.get), :]
>>> sortedI = sortedI[:, sorted(edgedict, key=edgedict.get)]
>>> sortedI
array([[1, 0, 0],
       [1, 0, 0],
       [1, 0, 0],
       [0, 1, 0],
       [0, 0, 1],
       [0, 0, 1],
       [1, 0, 1]])
>>> # Indexing a Pandas dataframe by the node/edge IDs
>>> df = pd.DataFrame(I, index=nodedict.values(), columns=edgedict.values())

If the nodes are already sorted, this order can be preserved by adding the nodes
to the hypergraph prior to adding edges. For example,

>>> import xgi
>>> H = xgi.Hypergraph()
>>> H.add_nodes_from(range(1, 8))
>>> H.add_edges_from([[1, 2, 3, 7], [4], [5, 6, 7]])
>>> xgi.incidence_matrix(H, sparse=False)
array([[1, 0, 0],
       [1, 0, 0],
       [1, 0, 0],
       [0, 1, 0],
       [0, 0, 1],
       [0, 0, 1],
       [1, 0, 1]])

"""

from warnings import warn

import numpy as np
from scipy.sparse import csr_array, diags

from ..exception import XGIError
from .hypergraph_matrix import adjacency_matrix, clique_motif_matrix, degree_matrix

__all__ = [
    "laplacian",
    "multiorder_laplacian",
    "normalized_hypergraph_laplacian",
]


def laplacian(H, order=1, sparse=False, rescale_per_node=False, index=False):
    """Laplacian matrix of order d, see [1].

    Parameters
    ----------
    HG : Hypergraph
        Hypergraph
    order : int
        Order of interactions to consider. If order=1 (default),
        returns the usual graph Laplacian.
    sparse: bool, default: False
        Specifies whether the output matrix is a scipy sparse matrix or a numpy matrix.
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node and edge IDs to
        indices.

    Returns
    -------
    L_d : numpy array
        Array of dim (N, N)
    if index is True:
        return rowdict

    See also
    --------
    multiorder_laplacian

    References
    ----------
    .. [1] Lucas, M., Cencetti, G., & Battiston, F. (2020).
        Multiorder Laplacian for synchronization in higher-order networks.
        Physical Review Research, 2(3), 033410.

    """
    A, row_dict = adjacency_matrix(
        H, order=order, sparse=sparse, weighted=True, index=True
    )

    if A.shape == (0, 0):
        L = csr_array((0, 0)) if sparse else np.empty((0, 0))
        return (L, {}) if index else L

    if sparse:
        K = csr_array(diags(degree_matrix(H, order=order)))
    else:
        K = np.diag(degree_matrix(H, order=order))

    L = order * K - A  # ravel needed to convert sparse matrix

    if rescale_per_node:
        L = L / order

    return (L, row_dict) if index else L


def multiorder_laplacian(
    H, orders, weights, sparse=False, rescale_per_node=False, index=False
):
    """Multiorder Laplacian matrix, see [1].

    Parameters
    ----------
    HG : Hypergraph
        Hypergraph
    orders : list of int
        Orders of interactions to consider.
    weights: list of float
        Weights associated to each order, i.e coupling strengths gamma_i in [1].
    sparse: bool, default: False
        Specifies whether the output matrix is a scipy sparse matrix or a numpy matrix
    rescale_per_node: bool, (default=False)
        Whether to rescale each Laplacian of order d by d (per node).
    index: bool, default: False
        Specifies whether to output dictionaries mapping the node and edge IDs to
        indices.

    Returns
    -------
    L_multi : numpy array
        Array of dim (N, N)
    if index is True:
        return rowdict

    See also
    --------
    laplacian

    References
    ----------
    .. [1] Lucas, M., Cencetti, G., & Battiston, F. (2020).
        Multiorder Laplacian for synchronization in higher-order networks.
        Physical Review Research, 2(3), 033410.

    """
    if len(orders) != len(weights):
        raise ValueError("orders and weights must have the same length.")

    Ls = [
        laplacian(H, order=d, sparse=sparse, rescale_per_node=rescale_per_node)
        for d in orders
    ]
    Ks = [degree_matrix(H, order=d) for d in orders]

    if sparse:
        L_multi = csr_array((H.num_nodes, H.num_nodes))
    else:
        L_multi = np.zeros((H.num_nodes, H.num_nodes))

    for L, K, w, d in zip(Ls, Ks, weights, orders):
        if np.all(K == 0):
            # avoid getting nans from dividing by 0
            # manually setting contribution to 0 as it should be
            warn(
                f"No edges of order {d}. Contribution of "
                "that order is zero. Its weight is effectively zero."
            )
        else:
            L_multi += L * w / np.mean(K)

    rowdict = {i: v for i, v in enumerate(H.nodes)}

    return (L_multi, rowdict) if index else L_multi


def normalized_hypergraph_laplacian(H, sparse=True, index=False):
    """Compute the normalized Laplacian.

    Parameters
    ----------
    H : Hypergraph
        Hypergraph
    sparse : bool, optional
        whether or not the laplacian is sparse, by default True
    index : bool, optional
        whether to return a dictionary mapping IDs to rows, by default False

    Returns
    -------
    array
        csr_array if sparse and if not, a numpy ndarray
    dict
        a dictionary mapping node IDs to rows and columns
        if index is True.


    Raises
    ------
    XGIError
        If there are isolated nodes.

    References
    ----------
    "Learning with Hypergraphs: Clustering, Classification, and Embedding"
    by Dengyong Zhou, Jiayuan Huang, Bernhard Schölkopf
    Advances in Neural Information Processing Systems (2006)

    """
    if H.nodes.isolates():
        raise XGIError(
            "Every node must be a member of an edge to avoid divide by zero error!"
        )

    D = degree_matrix(H)
    A, rowdict = clique_motif_matrix(H, sparse=sparse, index=True)

    if sparse:
        Dinvsqrt = csr_array(diags(np.power(D, -0.5)))
        eye = csr_array((H.num_nodes, H.num_nodes))
        eye.setdiag(1)
    else:
        Dinvsqrt = np.diag(np.power(D, -0.5))
        eye = np.eye(H.num_nodes)

    L = 0.5 * (eye - Dinvsqrt @ A @ Dinvsqrt)
    return (L, rowdict) if index else L
