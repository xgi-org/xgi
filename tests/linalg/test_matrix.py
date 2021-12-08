import pytest
import xgi
import numpy as np


def test_incidence_matrix(edgelist1, edgelist3, edgelist4):
    el1 = edgelist1
    el3 = edgelist3
    el4 = edgelist4
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el3)
    H3 = xgi.Hypergraph(el4)

    I1, node_dict, edge_dict = xgi.incidence_matrix(H1, index=True)
    node_dict1 = {k: v for v, k in node_dict.items()}
    edge_dict1 = {k: v for v, k in edge_dict.items()}
    I2, node_dict, edge_dict = xgi.incidence_matrix(H2, index=True)
    node_dict2 = {k: v for v, k in node_dict.items()}
    edge_dict2 = {k: v for v, k in edge_dict.items()}
    I3, node_dict, edge_dict = xgi.incidence_matrix(H3, index=True)
    node_dict3 = {k: v for v, k in node_dict.items()}
    edge_dict3 = {k: v for v, k in edge_dict.items()}

    assert I1[node_dict1[1], edge_dict1[0]] == 1
    assert I1[node_dict1[2], edge_dict1[0]] == 1
    assert I1[node_dict1[3], edge_dict1[0]] == 1
    assert I1[node_dict1[4], edge_dict1[1]] == 1
    assert I1[node_dict1[5], edge_dict1[2]] == 1
    assert I1[node_dict1[6], edge_dict1[2]] == 1
    assert I1[node_dict1[6], edge_dict1[3]] == 1
    assert I1[node_dict1[7], edge_dict1[3]] == 1
    assert I1[node_dict1[8], edge_dict1[3]] == 1

    assert I2[node_dict2[1], edge_dict2[0]] == 1
    assert I2[node_dict2[2], edge_dict2[0]] == 1
    assert I2[node_dict2[3], edge_dict2[0]] == 1
    assert I2[node_dict2[3], edge_dict2[1]] == 1
    assert I2[node_dict2[4], edge_dict2[1]] == 1
    assert I2[node_dict2[4], edge_dict2[2]] == 1
    assert I2[node_dict2[5], edge_dict2[2]] == 1
    assert I2[node_dict2[6], edge_dict2[2]] == 1

    assert I3[node_dict3[1], edge_dict3[0]] == 1
    assert I3[node_dict3[2], edge_dict3[0]] == 1
    assert I3[node_dict3[3], edge_dict3[0]] == 1
    assert I3[node_dict3[2], edge_dict3[1]] == 1
    assert I3[node_dict3[3], edge_dict3[1]] == 1
    assert I3[node_dict3[4], edge_dict3[1]] == 1
    assert I3[node_dict3[5], edge_dict3[1]] == 1
    assert I3[node_dict3[3], edge_dict3[2]] == 1
    assert I3[node_dict3[4], edge_dict3[2]] == 1
    assert I3[node_dict3[5], edge_dict3[2]] == 1

    I4, node_dict, edge_dict = xgi.incidence_matrix(
        H1, index=True, weight=lambda node, edge, H: 3
    )
    node_dict4 = {k: v for v, k in node_dict.items()}
    edge_dict4 = {k: v for v, k in edge_dict.items()}
    assert I4[node_dict4[1], edge_dict4[0]] == 3


def test_adjacency_matrix(edgelist1, edgelist3, edgelist4):
    el1 = edgelist1
    el3 = edgelist3
    el4 = edgelist4
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el3)
    H3 = xgi.Hypergraph(el4)

    A1, node_dict = xgi.adjacency_matrix(H1, index=True)
    node_dict1 = {k: v for v, k in node_dict.items()}

    A2, node_dict = xgi.adjacency_matrix(H2, index=True)
    node_dict2 = {k: v for v, k in node_dict.items()}

    A3, node_dict = xgi.adjacency_matrix(H3, index=True)
    node_dict3 = {k: v for v, k in node_dict.items()}

    for i in range(np.size(A1, axis=0)):
        assert A1[i, i] == 0

    for i in range(np.size(A2, axis=0)):
        assert A2[i, i] == 0

    for i in range(np.size(A3, axis=0)):
        assert A3[i, i] == 0

    assert np.max(A1) == 1
    assert np.max(A2) == 1
    assert np.max(A3) == 1

    assert A1[node_dict1[1], node_dict1[2]] == 1
    assert A1[node_dict1[2], node_dict1[1]] == 1
    assert A1[node_dict1[1], node_dict1[3]] == 1
    assert A1[node_dict1[4], node_dict1[1]] == 0
    assert A1[node_dict1[4], node_dict1[6]] == 0
    assert A1[node_dict1[5], node_dict1[6]] == 1
    assert A1[node_dict1[6], node_dict1[5]] == 1
    assert A1[node_dict1[6], node_dict1[7]] == 1
    assert A1[node_dict1[7], node_dict1[8]] == 1
    assert A1[node_dict1[8], node_dict1[6]] == 1
    assert A1[node_dict1[8], node_dict1[1]] == 0


def test_clique_motif_matrix(edgelist1, edgelist3, edgelist4):
    el1 = edgelist1
    el3 = edgelist3
    el4 = edgelist4
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el3)
    H3 = xgi.Hypergraph(el4)

    W1, node_dict = xgi.clique_motif_matrix(H1, index=True)
    node_dict1 = {k: v for v, k in node_dict.items()}

    W2, node_dict = xgi.clique_motif_matrix(H2, index=True)
    node_dict2 = {k: v for v, k in node_dict.items()}

    W3, node_dict = xgi.clique_motif_matrix(H3, index=True)
    node_dict3 = {k: v for v, k in node_dict.items()}

    for i in range(np.size(W1, axis=0)):
        assert W1[i, i] == 0

    for i in range(np.size(W2, axis=0)):
        assert W2[i, i] == 0

    for i in range(np.size(W3, axis=0)):
        assert W3[i, i] == 0

    assert W3[node_dict1[1], node_dict1[2]] == 1
    assert W3[node_dict1[2], node_dict1[1]] == 1
    assert W3[node_dict1[1], node_dict1[3]] == 1
    assert W3[node_dict1[2], node_dict1[3]] == 2
    assert W3[node_dict1[4], node_dict1[5]] == 2
    assert W3[node_dict1[2], node_dict1[5]] == 1
    assert W3[node_dict1[3], node_dict1[4]] == 2
    assert W3[node_dict1[5], node_dict1[1]] == 0
