import numpy as np

import xgi


def test_to_incidence_matrix(edgelist5, incidence5):
    H = xgi.Hypergraph(edgelist5)
    assert np.all(xgi.to_incidence_matrix(H) == incidence5)


def test_from_incidence_matrix(edgelist5, incidence5):
    H = xgi.from_incidence_matrix(incidence5)
    assert H.edges.members() == edgelist5


def test_fix_718():
    # Adding an edge after from_incidence_matrix must not collide with existing edge IDs
    B = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    H = xgi.from_incidence_matrix(B)
    H.add_edge([0, 3])
    assert H.edges.members(dtype=dict) == {
        0: {0, 1},
        1: {0, 2},
        2: {1, 2},
        3: {0, 3},
    }
