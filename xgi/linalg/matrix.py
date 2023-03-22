"""Matrices associated to hypergraphs.

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

__all__ = [
    "incidence_matrix",
    "adjacency_matrix",
    "intersection_profile",
    "degree_matrix",
    "laplacian",
    "multiorder_laplacian",
    "clique_motif_matrix",
    "boundary_matrix",
    "hodge_laplacian",
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
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node IDs to indices

    Returns
    -------
    if index is True:
        return A, rowdict
    else:
        return A

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
        A.setdiag(0)
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
    I, _, coldict = incidence_matrix(H, order=order, sparse=sparse, index=True)
    P = I.T.dot(I)
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
        Specifies whether to output disctionaries mapping the node and edge IDs to indices

    Returns
    -------
    if index is True:
        return K, rowdict
    else:
        return K

    """
    I, rowdict, _ = incidence_matrix(H, order=order, index=True)

    if I.shape == (0, 0):
        K = np.zeros(H.num_nodes)
    else:
        K = np.ravel(np.sum(I, axis=1))  # flatten

    return (K, rowdict) if index else K


def laplacian(H, order=1, sparse=False, rescale_per_node=False, index=False):
    """Laplacian matrix of order d, see [1].

    Parameters
    ----------
    HG : Hypergraph
        Hypergraph
    order : int
        Order of interactions to consider. If order=1 (default),
        returns the usual graph Laplacian
    sparse: bool, default: False
        Specifies whether the output matrix is a scipy sparse matrix or a numpy matrix
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
        Specifies whether to output dictionaries mapping the node and edge IDs to indices

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
                f"No edges of order {d}. Contribution of that order is zero. Its weight is effectively zero."
            )
        else:
            L_multi += L * w / np.mean(K)

    rowdict = {i: v for i, v in enumerate(H.nodes)}

    return (L_multi, rowdict) if index else L_multi


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


def boundary_matrix(S, order=1, orientations=None, index=False):
    """
    A function to generate the boundary matrices of an oriented simplicial complex.
    The rows correspond to the (order-1)-simplices and the columns to the (order)-simplices.

    Parameters
    ----------
    S: simplicial complex object
        The simplicial complex of interest
    order: int, default: 1
        Specifies the order of the boundary
        matrix to compute
    orientations: dict, default: None
        Dictionary mapping non-singleton simplices
        IDs to their boolean orientation
    index: bool, default: False
        Specifies whether to output dictionaries
        mapping the simplices IDs to indices

    Returns
    -------
    B: numpy.ndarray
        The boundary matrix of the chosen order, has dimension
        (n_simplices of given order - 1, n_simplices of given order)
    rowdict: dict
        The dictionary mapping indices to
        (order-1)-simplices IDs, if index is True
    coldict: dict
        The dictionary mapping indices to
        (order)-simplices IDs, if index is True

    References
    ----------
    "Discrete Calculus"
    by Leo J. Grady and Jonathan R. Polimeni
    https://doi.org/10.1007/978-1-84996-290-2

    """

    # Extract the simplices involved
    if order == 1:
        simplices_d_ids = S.nodes
    else:
        simplices_d_ids = S.edges.filterby("order", order - 1)

    if order == 0:
        simplices_u_ids = S.nodes
    else:
        simplices_u_ids = S.edges.filterby("order", order)
    nd = len(simplices_d_ids)
    nu = len(simplices_u_ids)

    simplices_d_dict = dict(zip(simplices_d_ids, range(nd)))
    simplices_u_dict = dict(zip(simplices_u_ids, range(nu)))

    if index:
        rowdict = {v: k for k, v in simplices_d_dict.items()}
        coldict = {v: k for k, v in simplices_u_dict.items()}

    if orientations is None:
        orientations = {idd: 0 for idd in S.edges.filterby("order", 1, mode="geq")}

    B = np.zeros((nd, nu))
    if not (nu == 0 or nd == 0):
        if order == 1:
            for u_simplex_id in simplices_u_ids:
                u_simplex = list(S.edges.members(u_simplex_id))
                u_simplex.sort(
                    key=lambda e: (isinstance(e, str), e)
                )  # Sort the simplex's vertices to get a reference orientation
                # The key is needed to sort a mixed list of numbers and strings:
                #   it ensures that node labels which are numbers are put before strings,
                #   thus giving a list [sorted numbers, sorted strings]
                matrix_id = simplices_u_dict[u_simplex_id]
                head_idx = u_simplex[1]
                tail_idx = u_simplex[0]
                B[simplices_d_dict[head_idx], matrix_id] = (-1) ** orientations[
                    u_simplex_id
                ]
                B[simplices_d_dict[tail_idx], matrix_id] = -(
                    (-1) ** orientations[u_simplex_id]
                )
        else:
            for u_simplex_id in simplices_u_ids:
                u_simplex = list(S.edges.members(u_simplex_id))
                u_simplex.sort(
                    key=lambda e: (isinstance(e, str), e)
                )  # Sort the simplex's vertices to get a reference orientation
                # The key is needed to sort a mixed list of numbers and strings:
                #   it ensures that node labels which are numbers are put before strings,
                #   thus giving a list [sorted numbers, sorted strings]
                matrix_id = simplices_u_dict[u_simplex_id]
                u_simplex_subfaces = S._subfaces(u_simplex, all=False)
                subfaces_induced_orientation = [
                    (orientations[u_simplex_id] + order - i) % 2
                    for i in range(order + 1)
                ]
                for count, subf in enumerate(u_simplex_subfaces):
                    subface_ID = list(S.edges)[S.edges.members().index(frozenset(subf))]
                    B[simplices_d_dict[subface_ID], matrix_id] = (-1) ** (
                        subfaces_induced_orientation[count] + orientations[subface_ID]
                    )
    return (B, rowdict, coldict) if index else B


def hodge_laplacian(S, order=1, orientations=None, index=False):

    """
    A function to compute the Hodge Laplacians of an oriented
    simplicial complex.

    Parameters
    ----------
    S: simplicial complex object
        The simplicial complex of interest
    order: int, default: 1
        Specifies the order of the Hodge
        Laplacian matrix to be computed
    orientations: dict, default: None
        Dictionary mapping non-singleton simplices
        IDs to their boolean orientation
    index: bool, default: False
        Specifies whether to output dictionaries
        mapping the simplices IDs to indices

    Returns
    -------
    L_o: numpy.ndarray
        The Hodge Laplacian matrix of the chosen order, has dimension
        (n_simplices of given order, n_simplices of given order)
    matdict: dict
        The dictionary mapping indices to
        (order)-simplices IDs, if index is True

    """
    if index:
        B_o, __, matdict = boundary_matrix(S, order, orientations, True)
    else:
        B_o = boundary_matrix(S, order, orientations, False)
    D_om1 = np.transpose(B_o)

    B_op1 = boundary_matrix(S, order + 1, orientations, False)
    D_o = np.transpose(B_op1)

    L_o = D_om1 @ B_o + B_op1 @ D_o

    return (L_o, matdict) if index else L_o
