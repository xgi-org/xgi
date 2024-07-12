"""Hodge theory matrices associated to hypergraphs.

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

import numpy as np

__all__ = [
    "boundary_matrix",
    "hodge_laplacian",
]


def boundary_matrix(S, order=1, orientations=None, index=False):
    """Generate the boundary matrices of an oriented simplicial complex.

    The rows correspond to the (order-1)-simplices and the columns to the
    (order)-simplices.

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
                #   it ensures that node labels which are numbers are put before
                #   strings, thus giving a list [sorted numbers, sorted strings]
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
                #   it ensures that node labels which are numbers are put before
                #   strings, thus giving a list [sorted numbers, sorted strings]
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
