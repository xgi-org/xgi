import numpy as np

__all__ = [
    "incidence_matrix",
    "adjacency_matrix",
    "clique_motif_matrix",
]

def incidence_matrix(H, sparse=True, index=False, weight = lambda node, edge, H : 1):
    
    if sparse:
        from scipy.sparse import coo_matrix

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
            I = coo_matrix((data, (rows, cols)))
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


def adjacency_matrix(H, sparse=True, index=False):
    if index:
        I, row_dict, col_dict = incidence_matrix(H, sparse=sparse, index=True)
    else:
        I = incidence_matrix(H, sparse=sparse, index=False)

    A = I.dot(I.T)
    if sparse:
        A.setdiag(0)
        A.eliminate_zeros()
    else:
        np.fill_diagonal(A, 0)
    
    if index:
        return A, row_dict, col_dict
    else:
        return A

def clique_motif_matrix(H, sparse=True, index=False):
    if index:
        I, row_dict, col_dict = incidence_matrix(H, sparse=sparse, index=True)
    else:
        I = incidence_matrix(H, sparse=sparse, index=False)

    W = I.dot(I.T)
    if sparse:
        W.setdiag(0)
        W.eliminate_zeros()
    else:
        np.fill_diagonal(W, 0)
    
    if index:
        return W, row_dict, col_dict
    else:
        return W