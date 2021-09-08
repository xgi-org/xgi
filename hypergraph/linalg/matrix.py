import numpy as np

def incidence_matrix(H, sparse=True, index=False):
    
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
                    data.append(1)
                    rows.append(node_dict[node])
                    cols.append(edge_dict[edge])
            I = coo_matrix((data, (rows, cols)))
        else:
            # Create an np.matrix
            I = np.zeros((num_nodes, num_edges), dtype=int)
            for edge in H.edges:
                members = H.edges[edge]
                for node in members:
                    I[node_dict[node], edge_dict[edge]] = 1
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
    if index == True:
        I, row_dict, col_dict = incidence_matrix(H, sparse=sparse, index=True)
        A = I*I.T
        return A, row_dict, col_dict
    else:
        I = incidence_matrix(H, sparse=sparse, index=False)
        A = I*(I.T)
        return A