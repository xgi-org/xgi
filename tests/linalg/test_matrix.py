import numpy as np
import pytest
from scipy.sparse import csr_array
from scipy.sparse.linalg import norm as spnorm

import xgi


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

    I4, node_dict, edge_dict = xgi.incidence_matrix(H1, index=True, sparse=False)
    node_dict4 = {k: v for v, k in node_dict.items()}
    edge_dict4 = {k: v for v, k in edge_dict.items()}

    assert I4[node_dict4[1], edge_dict4[0]] == 1
    assert I4[node_dict4[2], edge_dict4[0]] == 1
    assert I4[node_dict4[3], edge_dict4[0]] == 1
    assert I4[node_dict4[4], edge_dict4[1]] == 1
    assert I4[node_dict4[5], edge_dict4[2]] == 1
    assert I4[node_dict4[6], edge_dict4[2]] == 1
    assert I4[node_dict4[6], edge_dict4[3]] == 1
    assert I4[node_dict4[7], edge_dict4[3]] == 1
    assert I4[node_dict4[8], edge_dict4[3]] == 1

    I5, node_dict, edge_dict = xgi.incidence_matrix(
        H1, index=True, weight=lambda node, edge, H: 3
    )
    node_dict5 = {k: v for v, k in node_dict.items()}
    edge_dict5 = {k: v for v, k in edge_dict.items()}
    assert I5[node_dict5[1], edge_dict5[0]] == 3
    unique_entries = np.unique(np.ravel(I5.todense())).tolist()
    assert unique_entries == [0, 3]

    I6, node_dict, edge_dict = xgi.incidence_matrix(H1, index=True, order=2)
    node_dict6 = {k: v for v, k in node_dict.items()}
    edge_dict6 = {k: v for v, k in edge_dict.items()}

    assert I6[node_dict6[1], edge_dict6[0]] == 1
    assert I6[node_dict6[2], edge_dict6[0]] == 1
    assert I6[node_dict6[3], edge_dict6[0]] == 1
    assert I6[node_dict6[6], edge_dict6[3]] == 1
    assert I6[node_dict6[7], edge_dict6[3]] == 1
    assert I6[node_dict6[8], edge_dict6[3]] == 1

    data = xgi.incidence_matrix(H1)
    assert type(data) == csr_array

    H7 = xgi.empty_hypergraph()
    H7.add_nodes_from(range(8))  # disconnected node 0
    H7.add_edges_from(el1)

    I7_sparse = xgi.incidence_matrix(H7, order=None, sparse=True)
    I7 = xgi.incidence_matrix(H7, order=None, sparse=False)
    assert np.all(I7_sparse == I7)

    I7_sparse_1 = xgi.incidence_matrix(H7, order=1, sparse=True)
    I7_1 = xgi.incidence_matrix(H7, order=1, sparse=False)
    assert np.all(I7_sparse_1 == I7_1)

    I7_sparse_2 = xgi.incidence_matrix(H7, order=2, sparse=True)
    I7_2 = xgi.incidence_matrix(H7, order=2, sparse=False)
    assert np.all(I7_sparse_2 == I7_2)


def test_degree_matrix(edgelist1):
    el1 = edgelist1
    H1 = xgi.Hypergraph(el1)

    K, node_dict = xgi.degree_matrix(H1, order=None, index=True)
    node_dict = {k: v for v, k in node_dict.items()}
    assert K.shape == (8,)

    assert K[node_dict[1]] == 1
    assert K[node_dict[2]] == 1
    assert K[node_dict[3]] == 1
    assert K[node_dict[4]] == 1
    assert K[node_dict[5]] == 1
    assert K[node_dict[6]] == 2
    assert K[node_dict[7]] == 1
    assert K[node_dict[8]] == 1

    K1, node_dict1 = xgi.degree_matrix(H1, order=1, index=True)
    node_dict1 = {k: v for v, k in node_dict1.items()}
    assert K1.shape == (8,)

    assert K1[node_dict[1]] == 0
    assert K1[node_dict[2]] == 0
    assert K1[node_dict[3]] == 0
    assert K1[node_dict[4]] == 0
    assert K1[node_dict[5]] == 1
    assert K1[node_dict[6]] == 1
    assert K1[node_dict[7]] == 0
    assert K1[node_dict[8]] == 0

    K3, node_dict3 = xgi.degree_matrix(H1, order=3, index=True)
    node_dict3 = {k: v for v, k in node_dict3.items()}
    assert K3.shape == (8,)
    for i in range(8):
        assert K3[i] == 0


def test_adjacency_matrix(edgelist1, edgelist4):
    el1 = edgelist1
    el2 = edgelist4
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)

    A1, node_dict = xgi.adjacency_matrix(H1, index=True)
    node_dict1 = {k: v for v, k in node_dict.items()}

    A2, node_dict = xgi.adjacency_matrix(H2, index=True, s=2)
    node_dict2 = {k: v for v, k in node_dict.items()}

    data = xgi.adjacency_matrix(H2)
    assert type(data) == csr_array

    for i in range(np.size(A1, axis=0)):
        assert A1[i, i] == 0

    for i in range(np.size(A2, axis=0)):
        assert A2[i, i] == 0

    assert np.max(A1) == 1
    assert np.max(A2) == 1

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

    assert A2[node_dict2[1], node_dict2[2]] == 0
    assert A2[node_dict2[2], node_dict2[1]] == 0
    assert A2[node_dict2[1], node_dict2[3]] == 0
    assert A2[node_dict2[2], node_dict2[3]] == 1
    assert A2[node_dict2[3], node_dict2[4]] == 1
    assert A2[node_dict2[4], node_dict2[5]] == 1
    assert A2[node_dict2[3], node_dict2[5]] == 1
    assert A2[node_dict2[2], node_dict2[5]] == 0
    assert A2[node_dict2[1], node_dict2[5]] == 0

    A3, node_dict3 = xgi.adjacency_matrix(H1, index=True, order=1)
    node_dict3 = {k: v for v, k in node_dict3.items()}

    for i in range(np.size(A3, axis=0)):
        assert A3[i, i] == 0

    assert spnorm(A3.T - A3) < 1e-6

    assert A3[node_dict3[5], node_dict3[6]] == 1
    assert A3[node_dict3[1], node_dict3[2]] == 0
    assert A3[node_dict3[1], node_dict3[3]] == 0
    assert A3[node_dict3[1], node_dict3[4]] == 0
    assert A3[node_dict3[1], node_dict3[5]] == 0
    assert A3[node_dict3[1], node_dict3[6]] == 0
    assert A3[node_dict3[2], node_dict3[3]] == 0
    assert A3[node_dict3[2], node_dict3[4]] == 0
    assert A3[node_dict3[2], node_dict3[5]] == 0
    assert A3[node_dict3[2], node_dict3[6]] == 0
    assert A3[node_dict3[3], node_dict3[4]] == 0
    assert A3[node_dict3[3], node_dict3[5]] == 0
    assert A3[node_dict3[3], node_dict3[6]] == 0
    assert A3[node_dict3[4], node_dict3[5]] == 0
    assert A3[node_dict3[4], node_dict3[6]] == 0

    A4, node_dict4 = xgi.adjacency_matrix(H1, index=True, order=2)
    node_dict4 = {k: v for v, k in node_dict4.items()}

    for i in range(np.size(A4, axis=0)):
        assert A4[i, i] == 0

    assert spnorm(A4.T - A4) < 1e-6

    assert A4[node_dict4[6], node_dict4[7]] == 1
    assert A4[node_dict4[6], node_dict4[8]] == 1
    assert A4[node_dict4[7], node_dict4[8]] == 1
    assert A4[node_dict4[1], node_dict4[2]] == 1
    assert A4[node_dict4[1], node_dict4[3]] == 1
    assert A4[node_dict4[1], node_dict4[4]] == 0
    assert A4[node_dict4[1], node_dict4[5]] == 0
    assert A4[node_dict4[1], node_dict4[6]] == 0
    assert A4[node_dict4[2], node_dict4[3]] == 1
    assert A4[node_dict4[2], node_dict4[4]] == 0
    assert A4[node_dict4[2], node_dict4[5]] == 0
    assert A4[node_dict4[2], node_dict4[6]] == 0
    assert A4[node_dict4[3], node_dict4[4]] == 0
    assert A4[node_dict4[3], node_dict4[5]] == 0
    assert A4[node_dict4[3], node_dict4[6]] == 0
    assert A4[node_dict4[4], node_dict4[5]] == 0
    assert A4[node_dict4[4], node_dict4[6]] == 0

    A5 = xgi.adjacency_matrix(H1, sparse=False)
    A5_sp = xgi.adjacency_matrix(H1, sparse=True)
    assert isinstance(A5, np.ndarray)
    assert np.all(A5 == A5_sp.todense())

    A6 = xgi.adjacency_matrix(H1, order=1, sparse=False)
    A6_sp = xgi.adjacency_matrix(H1, order=1, sparse=True)
    assert np.all(A6 == A6_sp.todense())

    A7 = xgi.adjacency_matrix(H1, order=2, sparse=False)
    A7_sp = xgi.adjacency_matrix(H1, order=2, sparse=True)
    assert np.all(A7 == A7_sp.todense())


def test_laplacian(edgelist2, edgelist6):
    el1 = edgelist6
    H1 = xgi.Hypergraph(el1)
    el2 = edgelist2
    H2 = xgi.Hypergraph(el2)

    L1, node_dict1 = xgi.laplacian(H1, order=2, index=True)
    node_dict1 = {k: v for v, k in node_dict1.items()}

    assert isinstance(L1, np.ndarray)

    assert L1[node_dict1[0], node_dict1[0]] == 2
    assert L1[node_dict1[1], node_dict1[1]] == 4
    assert L1[node_dict1[2], node_dict1[2]] == 6
    assert L1[node_dict1[3], node_dict1[3]] == 4
    assert L1[node_dict1[4], node_dict1[4]] == 2
    assert np.all((L1.T == L1))
    assert L1[node_dict1[0], node_dict1[1]] == -1
    assert L1[node_dict1[0], node_dict1[2]] == -1
    assert L1[node_dict1[0], node_dict1[3]] == 0
    assert L1[node_dict1[0], node_dict1[4]] == 0
    assert L1[node_dict1[1], node_dict1[2]] == -2
    assert L1[node_dict1[1], node_dict1[3]] == -1
    assert L1[node_dict1[1], node_dict1[4]] == 0
    assert L1[node_dict1[2], node_dict1[3]] == -2
    assert L1[node_dict1[2], node_dict1[4]] == -1
    assert L1[node_dict1[3], node_dict1[4]] == -1

    L2, node_dict2 = xgi.laplacian(H1, order=2, index=True, rescale_per_node=True)
    node_dict2 = {k: v for v, k in node_dict2.items()}

    assert L2[node_dict2[0], node_dict2[0]] == 1
    assert L2[node_dict2[1], node_dict2[1]] == 2
    assert L2[node_dict2[2], node_dict2[2]] == 3
    assert L2[node_dict2[3], node_dict2[3]] == 2
    assert L2[node_dict2[4], node_dict2[4]] == 1
    assert np.all((L2.T == L2))
    assert L2[node_dict2[0], node_dict2[1]] == -0.5
    assert L2[node_dict2[0], node_dict2[2]] == -0.5
    assert L2[node_dict2[0], node_dict2[3]] == 0
    assert L2[node_dict2[0], node_dict2[4]] == 0
    assert L2[node_dict2[1], node_dict2[2]] == -1
    assert L2[node_dict2[1], node_dict2[3]] == -0.5
    assert L2[node_dict2[1], node_dict2[4]] == 0
    assert L2[node_dict2[2], node_dict2[3]] == -1
    assert L2[node_dict2[2], node_dict2[4]] == -0.5
    assert L2[node_dict2[3], node_dict2[4]] == -0.5

    L3, node_dict3 = xgi.laplacian(H2, order=1, index=True)
    node_dict3 = {k: v for v, k in node_dict3.items()}

    assert np.all((L3.T == L3))
    assert L3[node_dict3[1], node_dict3[1]] == 1
    assert L3[node_dict3[2], node_dict3[2]] == 1
    assert L3[node_dict3[3], node_dict3[3]] == 1
    assert L3[node_dict3[4], node_dict3[4]] == 1
    assert L3[node_dict3[5], node_dict3[5]] == 0
    assert L3[node_dict3[6], node_dict3[6]] == 0

    assert L3[node_dict3[1], node_dict3[2]] == -1
    assert L3[node_dict3[1], node_dict3[3]] == 0
    assert L3[node_dict3[1], node_dict3[4]] == 0
    assert L3[node_dict3[2], node_dict3[3]] == 0
    assert L3[node_dict3[2], node_dict3[4]] == 0
    assert L3[node_dict3[3], node_dict3[4]] == -1

    L4 = xgi.laplacian(H1, order=2, sparse=True)
    assert isinstance(L4, csr_array)
    assert np.all(L1 == L4.todense())

    L5 = xgi.laplacian(H1, sparse=False)
    L5_sp = xgi.laplacian(H1, sparse=True)
    assert isinstance(L5, np.ndarray)
    assert np.all(L5 == L5_sp.todense())

    L6 = xgi.laplacian(H1, order=1, sparse=False)
    L6_sp = xgi.laplacian(H1, order=1, sparse=True)
    assert np.all(L6 == L6_sp.todense())

    L7 = xgi.laplacian(H1, order=2, sparse=False)
    L7_sp = xgi.laplacian(H1, order=2, sparse=True)
    assert np.all(L7 == L7_sp.todense())


def test_multiorder_laplacian(edgelist2, edgelist6):
    el1 = edgelist6
    H1 = xgi.Hypergraph(el1)
    el2 = edgelist2
    H2 = xgi.Hypergraph(el2)
    with pytest.warns(Warning):
        L1, node_dict1 = xgi.multiorder_laplacian(
            H1, orders=[1, 2], weights=[1, 1], index=True
        )

    # different order and weight lengths
    with pytest.raises(ValueError):
        L1, node_dict1 = xgi.multiorder_laplacian(
            H2, orders=[1, 2], weights=[1, 1, 1], index=True
        )
    node_dict1 = {k: v for v, k in node_dict1.items()}
    assert L1.shape == (5, 5)
    assert np.all((L1.T == L1))

    assert L1[node_dict1[0], node_dict1[3]] == 0
    assert L1[node_dict1[0], node_dict1[4]] == 0
    assert L1[node_dict1[1], node_dict1[4]] == 0

    L2, node_dict2 = xgi.multiorder_laplacian(
        H2, orders=[1, 2], weights=[1, 1], index=True, rescale_per_node=False
    )
    node_dict2 = {k: v for v, k in node_dict2.items()}
    assert L2.shape == (6, 6)
    assert np.all((L2.T == L2))

    assert L2[node_dict2[1], node_dict2[3]] == 0
    assert L2[node_dict2[1], node_dict2[4]] == 0
    assert L2[node_dict2[1], node_dict2[5]] == 0
    assert L2[node_dict2[1], node_dict2[6]] == 0
    assert L2[node_dict2[2], node_dict2[3]] == 0
    assert L2[node_dict2[2], node_dict2[4]] == 0
    assert L2[node_dict2[2], node_dict2[5]] == 0
    assert L2[node_dict2[2], node_dict2[6]] == 0
    assert L2[node_dict2[3], node_dict2[5]] == 0
    assert L2[node_dict2[3], node_dict2[6]] == 0

    L2 = xgi.multiorder_laplacian(H2, orders=[1, 2], weights=[1, 1])
    assert isinstance(L2, np.ndarray)
    assert np.shape(L2) == (6, 6)

    L3 = xgi.multiorder_laplacian(H2, orders=[1, 2], weights=[1, 1], sparse=True)
    assert isinstance(L3, csr_array)
    assert np.all(L2 == L3.todense())


def test_intersection_profile(edgelist2):
    el1 = edgelist2
    H1 = xgi.Hypergraph(el1)

    P, edge_dict = xgi.intersection_profile(H1, index=True)
    edge_dict = {k: v for v, k in edge_dict.items()}

    assert P[edge_dict[0], edge_dict[0]] == 2
    assert P[edge_dict[1], edge_dict[1]] == 2
    assert P[edge_dict[2], edge_dict[2]] == 3
    assert P[edge_dict[0], edge_dict[1]] == 0
    assert P[edge_dict[0], edge_dict[2]] == 0
    assert P[edge_dict[1], edge_dict[2]] == 1

    P1, edge_dict1 = xgi.intersection_profile(H1, order=1, index=True)
    edge_dict1 = {k: v for v, k in edge_dict1.items()}

    assert P1[edge_dict1[0], edge_dict1[0]] == 2
    assert P1[edge_dict1[1], edge_dict1[1]] == 2
    assert P1[edge_dict1[0], edge_dict1[1]] == 0

    P2, edge_dict2 = xgi.intersection_profile(H1, order=2, index=True)
    edge_dict2 = {k: v for v, k in edge_dict2.items()}

    assert P2[edge_dict2[2], edge_dict2[2]] == 3

    P2 = xgi.intersection_profile(H1, order=2)
    assert np.shape(P2) == (1, 1)
    assert P2[0, 0] == 3


def test_clique_motif_matrix(edgelist4):
    H1 = xgi.Hypergraph(edgelist4)

    W1, node_dict = xgi.clique_motif_matrix(H1, index=True)
    node_dict1 = {k: v for v, k in node_dict.items()}

    data = xgi.clique_motif_matrix(H1)
    assert type(data) == csr_array

    for i in range(np.size(W1, axis=0)):
        assert W1[i, i] == 0

    assert W1[node_dict1[1], node_dict1[2]] == 1
    assert W1[node_dict1[2], node_dict1[1]] == 1
    assert W1[node_dict1[1], node_dict1[3]] == 1
    assert W1[node_dict1[2], node_dict1[3]] == 2
    assert W1[node_dict1[4], node_dict1[5]] == 2
    assert W1[node_dict1[2], node_dict1[5]] == 1
    assert W1[node_dict1[3], node_dict1[4]] == 2
    assert W1[node_dict1[5], node_dict1[1]] == 0

    W2 = xgi.clique_motif_matrix(H1, sparse=False)
    assert isinstance(W2, np.ndarray)
    assert np.all(W1.todense() == W2)


def test_boundary_matrix(edgelist4):
    S1 = xgi.SimplicialComplex(edgelist4)
    orientations = {idd: 0 for idd in list(S1.edges.filterby("order", 1, mode="geq"))}
    B0, _, nodedict1 = xgi.boundary_matrix(
        S1, order=0, orientations=orientations, index=True
    )
    B1, nodedict2, edgedict1 = xgi.boundary_matrix(
        S1, order=1, orientations=orientations, index=True
    )
    B2, edgedict2, facedict1 = xgi.boundary_matrix(
        S1, order=2, orientations=orientations, index=True
    )
    B3, facedict2, tetdict1 = xgi.boundary_matrix(
        S1, order=3, orientations=orientations, index=True
    )
    B4, tetdict2, _ = xgi.boundary_matrix(
        S1, order=4, orientations=orientations, index=True
    )

    n0 = len(S1.nodes)
    n1 = len(S1.edges.filterby("order", 1))
    n2 = len(S1.edges.filterby("order", 2))
    n3 = len(S1.edges.filterby("order", 3))

    assert np.shape(B0) == (0, n0)
    assert np.shape(B1) == (n0, n1)
    assert np.shape(B2) == (n1, n2)
    assert np.shape(B3) == (n2, n3)
    assert np.shape(B4) == (n3, 0)

    assert nodedict1 == nodedict2
    assert edgedict1 == edgedict2
    assert facedict1 == facedict2
    assert tetdict1 == tetdict2

    nodedict1 = {k: v for v, k in nodedict1.items()}
    edgedict1 = {k: v for v, k in edgedict1.items()}
    facedict1 = {k: v for v, k in facedict1.items()}
    tetdict1 = {k: v for v, k in tetdict1.items()}

    members_to_id = {simplex: v for v, simplex in S1.edges.members(dtype=dict).items()}

    i123 = facedict1[members_to_id[frozenset([1, 2, 3])]]
    i2345 = tetdict1[members_to_id[frozenset([2, 3, 4, 5])]]
    i345 = facedict1[members_to_id[frozenset([3, 4, 5])]]
    i245 = facedict1[members_to_id[frozenset([2, 4, 5])]]
    i12 = edgedict1[members_to_id[frozenset([1, 2])]]
    i24 = edgedict1[members_to_id[frozenset([2, 4])]]
    i34 = edgedict1[members_to_id[frozenset([3, 4])]]
    i235 = facedict1[members_to_id[frozenset([2, 3, 5])]]
    i23 = edgedict1[members_to_id[frozenset([2, 3])]]
    i45 = edgedict1[members_to_id[frozenset([4, 5])]]
    i234 = facedict1[members_to_id[frozenset([2, 3, 4])]]
    i25 = edgedict1[members_to_id[frozenset([2, 5])]]
    i13 = edgedict1[members_to_id[frozenset([1, 3])]]
    i35 = edgedict1[members_to_id[frozenset([3, 5])]]

    assert B1[nodedict1[1], i12] == -1
    assert B1[nodedict1[2], i12] == 1
    assert B1[nodedict1[2], i24] == -1
    assert B1[nodedict1[4], i24] == 1
    assert B1[nodedict1[3], i34] == -1
    assert B1[nodedict1[4], i34] == 1
    assert B1[nodedict1[2], i23] == -1
    assert B1[nodedict1[3], i23] == 1
    assert B1[nodedict1[4], i45] == -1
    assert B1[nodedict1[5], i45] == 1
    assert B1[nodedict1[2], i25] == -1
    assert B1[nodedict1[5], i25] == 1
    assert B1[nodedict1[1], i13] == -1
    assert B1[nodedict1[3], i13] == 1
    assert B1[nodedict1[3], i35] == -1
    assert B1[nodedict1[5], i35] == 1

    assert B2[i12, i123] == 1
    assert B2[i23, i123] == 1
    assert B2[i13, i123] == -1
    assert B2[i34, i345] == 1
    assert B2[i45, i345] == 1
    assert B2[i35, i345] == -1
    assert B2[i24, i245] == 1
    assert B2[i45, i245] == 1
    assert B2[i25, i245] == -1
    assert B2[i23, i235] == 1
    assert B2[i35, i235] == 1
    assert B2[i25, i235] == -1
    assert B2[i23, i234] == 1
    assert B2[i34, i234] == 1
    assert B2[i24, i234] == -1

    assert B3[i345, i2345] == 1
    assert B3[i245, i2345] == -1
    assert B3[i235, i2345] == 1
    assert B3[i234, i2345] == -1

    assert np.linalg.norm(B1 @ B2) == 0
    assert np.linalg.norm(B2 @ B3) == 0

    # Change the orientation of a face
    orientations[members_to_id[frozenset([3, 4, 5])]] = 1

    B1 = xgi.boundary_matrix(S1, order=1, orientations=orientations, index=False)
    B2 = xgi.boundary_matrix(S1, order=2, orientations=orientations, index=False)
    B3 = xgi.boundary_matrix(S1, order=3, orientations=orientations, index=False)

    assert B1[nodedict1[1], i12] == -1
    assert B1[nodedict1[2], i12] == 1
    assert B1[nodedict1[2], i24] == -1
    assert B1[nodedict1[4], i24] == 1
    assert B1[nodedict1[3], i34] == -1
    assert B1[nodedict1[4], i34] == 1
    assert B1[nodedict1[2], i23] == -1
    assert B1[nodedict1[3], i23] == 1
    assert B1[nodedict1[4], i45] == -1
    assert B1[nodedict1[5], i45] == 1
    assert B1[nodedict1[2], i25] == -1
    assert B1[nodedict1[5], i25] == 1
    assert B1[nodedict1[1], i13] == -1
    assert B1[nodedict1[3], i13] == 1
    assert B1[nodedict1[3], i35] == -1
    assert B1[nodedict1[5], i35] == 1

    assert B2[i12, i123] == 1
    assert B2[i23, i123] == 1
    assert B2[i13, i123] == -1
    assert B2[i34, i345] == -1
    assert B2[i45, i345] == -1
    assert B2[i35, i345] == 1
    assert B2[i24, i245] == 1
    assert B2[i45, i245] == 1
    assert B2[i25, i245] == -1
    assert B2[i23, i235] == 1
    assert B2[i35, i235] == 1
    assert B2[i25, i235] == -1
    assert B2[i23, i234] == 1
    assert B2[i34, i234] == 1
    assert B2[i24, i234] == -1

    assert B3[i345, i2345] == -1
    assert B3[i245, i2345] == -1
    assert B3[i235, i2345] == 1
    assert B3[i234, i2345] == -1

    assert np.linalg.norm(B1 @ B2) == 0
    assert np.linalg.norm(B2 @ B3) == 0


def test_normalized_hypergraph_laplacian():
    el = [[1, 2, 3], [4], [5, 6], [6, 7, 8]]
    H = xgi.Hypergraph(el)
    L1 = xgi.normalized_hypergraph_laplacian(H)

    assert isinstance(L1, csr_array)
    assert L1.shape == (8, 8)

    L2 = xgi.normalized_hypergraph_laplacian(H, sparse=False)

    assert isinstance(L2, np.ndarray)
    assert np.all(L1.toarray() == L2)
    assert np.all(np.diag(L2) == 0.5)

    L3, d = xgi.normalized_hypergraph_laplacian(H, index=True)

    assert d == {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}
    true_L = np.array(
        [
            [0.5, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-0.5, 0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-0.5, -0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.5, -0.35355339, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, -0.35355339, 0.5, -0.35355339, -0.35355339],
            [0.0, 0.0, 0.0, 0.0, 0.0, -0.35355339, 0.5, -0.5],
            [0.0, 0.0, 0.0, 0.0, 0.0, -0.35355339, -0.5, 0.5],
        ]
    )
    assert np.allclose(true_L, L2)


def test_empty_order(edgelist6):
    H = xgi.Hypergraph(edgelist6)
    I, _, _ = xgi.incidence_matrix(H, order=1, sparse=False, index=True)
    A, _ = xgi.adjacency_matrix(H, order=1, sparse=False, index=True)
    L, _ = xgi.laplacian(H, order=1, sparse=False, index=True)
    assert I.shape == (0, 0)
    assert A.shape == (5, 5)
    assert L.shape == (5, 5)

    # sparse
    I_sp, _, _ = xgi.incidence_matrix(H, order=1, sparse=True, index=True)
    A_sp, _ = xgi.adjacency_matrix(H, order=1, sparse=True, index=True)
    L_sp, _ = xgi.laplacian(H, order=1, sparse=True, index=True)
    assert I_sp.shape == (0, 0)
    assert A_sp.shape == (5, 5)
    assert L_sp.shape == (5, 5)


def test_empty():
    H = xgi.Hypergraph([])
    assert xgi.incidence_matrix(H).shape == (0, 0)
    assert xgi.adjacency_matrix(H).shape == (0, 0)
    assert xgi.laplacian(H).shape == (0, 0)
    assert xgi.clique_motif_matrix(H).shape == (0, 0)

    # with indices
    data = xgi.incidence_matrix(H, index=True)
    assert len(data) == 3
    assert data[0].shape == (0, 0)
    assert type(data[1]) == dict and type(data[2]) == dict

    data = xgi.adjacency_matrix(H, index=True)
    assert len(data) == 2
    assert data[0].shape == (0, 0)
    assert type(data[1]) == dict

    data = xgi.laplacian(H, index=True)
    assert len(data) == 2
    assert data[0].shape == (0, 0)
    assert type(data[1]) == dict

    data = xgi.normalized_hypergraph_laplacian(H, index=True)
    assert len(data) == 2
    assert data[0].shape == (0, 0)
    assert type(data[1]) == dict

    data = xgi.clique_motif_matrix(H, index=True)
    assert len(data) == 2
    assert data[0].shape == (0, 0)
    assert type(data[1]) == dict

    # sparse
    assert xgi.incidence_matrix(H, sparse=True).shape == (0, 0)
    assert xgi.incidence_matrix(H, sparse=False).shape == (0, 0)

    assert xgi.adjacency_matrix(H, sparse=True).shape == (0, 0)
    assert xgi.adjacency_matrix(H, sparse=False).shape == (0, 0)

    assert xgi.laplacian(H, sparse=True).shape == (0, 0)
    assert xgi.laplacian(H, sparse=False).shape == (0, 0)

    assert xgi.normalized_hypergraph_laplacian(H, sparse=True).shape == (0, 0)
    assert xgi.normalized_hypergraph_laplacian(H, sparse=False).shape == (0, 0)

    assert xgi.boundary_matrix(H).shape == (0, 0)

    assert xgi.hodge_laplacian(H).shape == (0, 0)
