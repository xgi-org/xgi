import numpy as np
from scipy.sparse import csr_matrix
import itertools

__all__ = [
    "incidence_matrix",
    "adjacency_matrix",
    "clique_motif_matrix",
]


def incidence_matrix(H, sparse=True, index=False, weight=lambda node, edge, H: 1):
    """
    A function to generate a weighted incidence matrix from a Hypergraph object,
    where the rows correspond to nodes and the columns correspond to edges.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    sparse: bool, default: True
        Specifies whether the output matrix is a scipy sparse matrix or a numpy matrix
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node and edge IDs to indices
    weight: lambda function, default=lambda function outputting 1
        A function specifying the weight, given a node and edge

    Returns
    -------
    numpy.ndarray or scipy csr_matrix
        The incidence matrix
    dict
        The dictionary mapping indices to node IDs, if index is True
    dict
        The dictionary mapping indices to edge IDs, if index is True

    Examples
    --------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> I = hg.incidence_matrix(H)
    """

    edge_ids = H.edges
    node_ids = H.nodes
    num_edges = len(edge_ids)
    num_nodes = len(node_ids)

    node_dict = dict(zip(node_ids, range(num_nodes)))
    edge_dict = dict(zip(edge_ids, range(num_edges)))

    if len(node_dict) != 0:

        if index:
            rowdict = {v: k for k, v in node_dict.items()}
            coldict = {v: k for k, v in edge_dict.items()}

        if sparse:
            # Create csr sparse matrix
            rows = list()
            cols = list()
            data = list()
            for edge in H.edges:
                members = H.edges[edge]
                for node in members:
                    data.append(weight(node, edge, H))
                    rows.append(node_dict[node])
                    cols.append(edge_dict[edge])
            I = csr_matrix((data, (rows, cols)))
        else:
            # Create an np.matrix
            I = np.zeros((num_nodes, num_edges), dtype=int)
            for edge in H.edges:
                members = H.edges[edge]
                for node in members:
                    I[node_dict[node], edge_dict[edge]] = weight(node, edge, H)
        if index:
            return I, rowdict, coldict
        else:
            return I
    else:
        if index:
            return np.zeros(1), {}, {}
        else:
            return np.zeros(1)


def adjacency_matrix(H, s=1, index=False):
    """
    A function to generate an unweighted adjacency matrix from a Hypergraph object.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    s: int, default: 1
        Specifies the number of overlapping edges to be considered connected.
    index: bool, default: False
        Specifies whether to output disctionaries mapping the node and edge IDs to indices

    Returns
    -------
    if index is True:
        return A, rowdict, coldict
    else:
        return A

    Examples
    --------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> A = hg.adjacency_matrix(H)
    """

    if index:
        I, row_dict, col_dict = incidence_matrix(H, index=True)
    else:
        I = incidence_matrix(H, index=False)

    A = I.dot(I.T)
    A.setdiag(0)
    A = (A >= s) * 1

    if index:
        return A, row_dict, col_dict
    else:
        return A


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

    Examples
    --------
        >>> import hypergraph as hg
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = hg.erdos_renyi_hypergraph(n, m, p)
        >>> W = hg.clique_motif_matrix(H)
    """
    if index:
        I, row_dict, col_dict = incidence_matrix(H, index=True)
    else:
        I = incidence_matrix(H, index=False)

    W = I.dot(I.T)
    W.setdiag(0)
    W.eliminate_zeros()

    if index:
        return W, row_dict, col_dict
    else:
        return W
