"""Matrices associated to hypergraphs."""
from warnings import warn

import numpy as np
from scipy.sparse import csr_matrix, diags

__all__ = [
    "incidence_matrix",
    "adjacency_matrix",
    "intersection_profile",
    "degree_matrix",
    "laplacian",
    "multiorder_laplacian",
    "clique_motif_matrix",
]


def incidence_matrix(
    H, order=None, sparse=True, index=False, weight=lambda node, edge, H: 1
):
    """
    A function to generate a weighted incidence matrix from a Hypergraph object,
    where the rows correspond to nodes and the columns correspond to edges.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    order: int, optional
        Order of interactions to use. If None (default), all orders are used. If int,
        must be >= 1.
    sparse: bool, default: True
        Specifies whether the output matrix is a scipy sparse matrix or a numpy matrix
    index: bool, default: False
        Specifies whether to output dictionaries mapping the node and edge IDs to indices
    weight: lambda function, default=lambda function outputting 1
        A function specifying the weight, given a node and edge

    Returns
    -------
    I: numpy.ndarray or scipy csr_matrix
        The incidence matrix, has dimension (n_nodes, n_edges)
    rowdict: dict
        The dictionary mapping indices to node IDs, if index is True
    coldict: dict
        The dictionary mapping indices to edge IDs, if index is True

    """
    node_ids = H.nodes
    edge_ids = H.edges

    if order is not None:
        edge_ids = H.edges.filterby("order", order)
    if not edge_ids or not node_ids:
        return (np.array([]), {}, {}) if index else np.array([])

    num_edges = len(edge_ids)
    num_nodes = len(node_ids)

    node_dict = dict(zip(node_ids, range(num_nodes)))
    edge_dict = dict(zip(edge_ids, range(num_edges)))

    if index:
        rowdict = {v: k for k, v in node_dict.items()}
        coldict = {v: k for k, v in edge_dict.items()}

    if sparse:
        # Create csr sparse matrix
        rows = []
        cols = []
        data = []
        for node in node_ids:
            memberships = H.nodes.memberships(node)
            # keep only those with right order
            memberships = [i for i in memberships if i in edge_ids]
            if len(memberships) > 0:
                for edge in memberships:
                    data.append(weight(node, edge, H))
                    rows.append(node_dict[node])
                    cols.append(edge_dict[edge])
            else:  # include disconnected nodes
                for edge in edge_ids:
                    data.append(0)
                    rows.append(node_dict[node])
                    cols.append(edge_dict[edge])
        I = csr_matrix((data, (rows, cols)))
    else:
        # Create an np.matrix
        I = np.zeros((num_nodes, num_edges), dtype=int)
        for edge in edge_ids:
            members = H.edges.members(edge)
            for node in members:
                I[node_dict[node], edge_dict[edge]] = weight(node, edge, H)
    if index:
        return I, rowdict, coldict
    else:
        return I


def adjacency_matrix(H, order=None, s=1, weighted=False, index=False):
    """
    A function to generate an adjacency matrix (N,N) from a Hypergraph object.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    order: int, optional
        Order of interactions to use. If None (default), all orders are used. If int,
        must be >= 1.
    s: int, default: 1
        Specifies the number of overlapping edges to be considered connected.
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node IDs to indices

    Returns
    -------
    if index is True:
        return A, rowdict
    else:
        return A

    """
    I, rowdict, coldict = incidence_matrix(H, index=True, order=order)

    if I.shape == (0,):
        if not rowdict:
            A = np.array([])
        if not coldict:
            A = np.zeros((H.num_nodes, H.num_nodes))
        return (A, {}) if index else A

    A = I.dot(I.T)
    A = A - diags(A.diagonal())

    if not weighted:
        A = (A >= s) * 1
    else:
        A.data[np.where(A.data < s)] = 0

    if index:
        return A, rowdict
    else:
        return A


def intersection_profile(H, order=None, index=False):
    """
    A function to generate an intersection profile from a Hypergraph object.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    order: int, optional
        Order of interactions to use. If None (default), all orders are used. If int,
        must be >= 1.
    index: bool, default: False
        Specifies whether to output dictionaries mapping the edge IDs to indices

    Returns
    -------
    if index is True:
        return P, rowdict, coldict
    else:
        return P

    """

    if index:
        I, _, coldict = incidence_matrix(H, order=order, index=True)
    else:
        I = incidence_matrix(H, order=order, index=False)

    P = I.T.dot(I)

    if index:
        return P, coldict
    else:
        return P


def degree_matrix(H, order=None, index=False):
    """Returns the degree of each node as an array

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    order: int, optional
        Order of interactions to use. If None (default), all orders are used. If int,
        must be >= 1.
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node and edge IDs to indices

    Returns
    -------
    if index is True:
        return K, rowdict
    else:
        return K

    """
    I, rowdict, _ = incidence_matrix(H, order=order, index=True)

    if I.shape == (0,):
        K = np.zeros(H.num_nodes)
    else:
        K = np.ravel(np.sum(I, axis=1))  # flatten

    return (K, rowdict) if index else K


def laplacian(H, order=1, rescale_per_node=False, index=False):
    """Laplacian matrix of order d, see [1].

    Parameters
    ----------
    HG : Hypergraph
        Hypergraph
    order : int
        Order of interactions to consider. If order=1 (default),
        returns the usual graph Laplacian
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node and edge IDs to indices

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
    A, row_dict = adjacency_matrix(H, order=order, weighted=True, index=True)
    if A.shape == (0,):
        return (np.array([]), {}) if index else np.array([])

    K = degree_matrix(H, order=order, index=False)

    L = order * np.diag(K) - A  # ravel needed to convert sparse matrix
    L = np.asarray(L)

    if rescale_per_node:
        L = L / order

    if index:
        return L, row_dict
    else:
        return L


def multiorder_laplacian(H, orders, weights, rescale_per_node=False, index=False):
    """Multiorder Laplacian matrix, see [1].

    Parameters
    ----------
    HG : Hypergraph
        Hypergraph
    orders : list of int
        Orders of interactions to consider.
    weights: list of float
        Weights associated to each order, i.e coupling strengths gamma_i in [1].
    rescale_per_node: bool, (default=False)
        Whether to rescale each Laplacian of order d by d (per node).
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node and edge IDs to indices

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

    Ls = [laplacian(H, order=i, rescale_per_node=rescale_per_node) for i in orders]
    Ks = [degree_matrix(H, order=i) for i in orders]

    L_multi = np.zeros((H.num_nodes, H.num_nodes))
    for L, K, w, d in zip(Ls, Ks, weights, orders):
        if np.all(K == 0):
            # avoid getting nans from dividing by 0
            # manually setting contribution to 0 as it should be
            warn(
                f"No edges of order {d}. Contribution of that order is zero. Its weight is effectively zero."
            )
        else:
            L_multi += L * w / np.mean(K)

    if index:
        _, rowdict, _ = incidence_matrix(H, index=True)
        return L_multi, rowdict
    else:
        return L_multi


def clique_motif_matrix(H, index=False):
    """
    A function to generate a weighted clique motif matrix
    from a Hypergraph object.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    index: bool, default: False
        Specifies whether to output dictionaries
        mapping the node and edge IDs to indices

    Returns
    -------
    if index is True:
        return W, rowdict, coldict
    else:
        return W

    References
    ----------
    "Higher-order organization of complex networks"
    by Austin Benson, David Gleich, and Jure Leskovic
    https://doi.org/10.1126/science.aad9029

    """
    if index:
        I, rowdict, _ = incidence_matrix(H, index=True)
    else:
        I = incidence_matrix(H, index=False)

    if I.shape == (0,):
        return (np.array([]), rowdict) if index else np.array([])

    W = I.dot(I.T)
    W.setdiag(0)
    W.eliminate_zeros()

    if index:
        return W, rowdict
    else:
        return W
