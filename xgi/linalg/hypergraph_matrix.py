"""General matrices associated to hypergraphs.

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

from warnings import catch_warnings, warn

import numpy as np
from scipy.sparse import csr_array

__all__ = [
    "incidence_matrix",
    "adjacency_matrix",
    "intersection_profile",
    "degree_matrix",
    "clique_motif_matrix",
]


def incidence_matrix(
    H, order=None, sparse=True, index=False, weight=lambda node, edge, H: 1
):
    """A function to generate a weighted incidence matrix from a Hypergraph object,
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
        Specifies whether to output dictionaries mapping the node and edge IDs to
        indices.
    weight: lambda function, default=lambda function outputting 1
        A function specifying the weight, given a node and edge

    Returns
    -------
    I: numpy.ndarray or scipy csr_array
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
        if sparse:
            I = csr_array((0, 0), dtype=int)
        else:
            I = np.empty((0, 0), dtype=int)
        return (I, {}, {}) if index else I

    num_edges = len(edge_ids)
    num_nodes = len(node_ids)

    node_dict = dict(zip(node_ids, range(num_nodes)))
    edge_dict = dict(zip(edge_ids, range(num_edges)))

    if index:
        rowdict = {v: k for k, v in node_dict.items()}
        coldict = {v: k for k, v in edge_dict.items()}

    # Compute the non-zero values, row and column indices for the given order
    rows = []
    cols = []
    data = []
    for edge in edge_ids:
        members = H._edge[edge]
        for node in members:
            rows.append(node_dict[node])
            cols.append(edge_dict[edge])
            data.append(weight(node, edge, H))

    # Create the incidence matrix as a CSR matrix
    if sparse:
        I = csr_array((data, (rows, cols)), shape=(num_nodes, num_edges), dtype=int)
    else:
        I = np.zeros((num_nodes, num_edges), dtype=int)
        I[rows, cols] = data

    return (I, rowdict, coldict) if index else I


def adjacency_matrix(H, order=None, sparse=True, s=1, weighted=False, index=False):
    """
    A function to generate an adjacency matrix (N,N) from a Hypergraph object.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    order: int, optional
        Order of interactions to use. If None (default), all orders are used. If int,
        must be >= 1.
    sparse: bool, default: True
        Specifies whether the output matrix is a scipy sparse matrix or a numpy matrix
    s: int, default: 1
        Specifies the number of overlapping edges to be considered connected.
    weighted: bool
        If True, entry (i, j) [and (j, i)] is the number of edges that connect i and j.
        If False, entry (i, j) [and (j, i] is 1 if i and j share at least one edge
        and 0 otherwise. By default, False.
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node IDs to indices

    Returns
    -------
    if index is True:
        return A, rowdict
    else:
        return A

    Warns
    -----
    warn
        If there are isolated nodes and the matrix is sparse.

    """
    I, rowdict, coldict = incidence_matrix(H, order=order, sparse=sparse, index=True)

    if I.shape == (0, 0):
        if not rowdict:
            A = csr_array((0, 0)) if sparse else np.empty((0, 0))
        if not coldict:
            shape = (H.num_nodes, H.num_nodes)
            A = csr_array(shape, dtype=int) if sparse else np.zeros(shape, dtype=int)
        return (A, {}) if index else A

    A = I.dot(I.T)

    if sparse:
        with catch_warnings(record=True) as w:
            A.setdiag(0)
        if w:
            warn(
                "Forming the adjacency matrix can "
                "be expensive when there are isolated nodes!"
            )
    else:
        np.fill_diagonal(A, 0)

    if not weighted:
        A = (A >= s) * 1
    else:
        A = (A >= s) * A

    if sparse:
        A.eliminate_zeros()

    return (A, rowdict) if index else A


def intersection_profile(H, order=None, sparse=True, index=False):
    """
    A function to generate an intersection profile from a Hypergraph object.

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
        Specifies whether to output dictionaries mapping the edge IDs to indices

    Returns
    -------
    if index is True:
        return P, rowdict, coldict
    else:
        return P

    """
    eye, _, coldict = incidence_matrix(H, order=order, sparse=sparse, index=True)
    P = eye.T.dot(eye)
    return (P, coldict) if index else P


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
        Specifies whether to output disctionaries mapping the node and edge IDs to
        indices.

    Returns
    -------
    if index is True:
        return K, rowdict
    else:
        return K

    """
    eye, rowdict, _ = incidence_matrix(H, order=order, index=True)

    if eye.shape == (0, 0):
        K = np.zeros(H.num_nodes)
    else:
        K = np.ravel(np.sum(eye, axis=1))  # flatten

    return (K, rowdict) if index else K


def clique_motif_matrix(H, sparse=True, index=False):
    """
    A function to generate a weighted clique motif matrix
    from a Hypergraph object.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    sparse: bool, default: True
        Specifies whether the output matrix is a scipy sparse matrix or a numpy matrix
    index: bool, default: False
        Specifies whether to output dictionaries
        mapping the node and edge IDs to indices

    Returns
    -------
    if index is True:
        return W, rowdict
    else:
        return W

    References
    ----------
    "Higher-order organization of complex networks"
    by Austin Benson, David Gleich, and Jure Leskovic
    https://doi.org/10.1126/science.aad9029

    """
    W, rowdict = adjacency_matrix(H, sparse=sparse, weighted=True, index=True)

    return (W, rowdict) if index else W
