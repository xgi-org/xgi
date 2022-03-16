import pytest

import xgi


def test_chung_lu_hypergraph():
    k1 = {1: 1, 2: 2, 3: 3, 4: 4}
    k2 = {1: 2, 2: 2, 3: 3, 4: 3}
    H = xgi.chung_lu_hypergraph(k1, k2)
    assert H.num_nodes == 4

    with pytest.warns(Warning):
        k1 = {1: 1, 2: 2}
        k2 = {1: 2, 1: 2}
        H = xgi.chung_lu_hypergraph(k1, k2)

def test_random_seed():
    H1 = xgi.random_hypergraph(10, [0.1, 0.001], seed=1)
    H2 = xgi.random_hypergraph(10, [0.1, 0.001], seed=2)
    H3 = xgi.random_hypergraph(10, [0.1, 0.001], seed=2)

    assert H1._edge != H2._edge
    assert H2._edge == H3._edge
