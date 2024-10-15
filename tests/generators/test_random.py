import random

import numpy as np
import pytest
from scipy.special import comb

import xgi


def test_chung_lu_hypergraph():
    k1 = {1: 1, 2: 2, 3: 3, 4: 4}
    k2 = {1: 2, 2: 2, 3: 3, 4: 3}
    H = xgi.chung_lu_hypergraph(k1, k2)
    assert H.num_nodes == 4

    # seed
    H1 = xgi.chung_lu_hypergraph(k1, k2, seed=1)
    H2 = xgi.chung_lu_hypergraph(k1, k2, seed=2)
    H3 = xgi.chung_lu_hypergraph(k1, k2, seed=2)
    assert H1._edge != H2._edge
    assert H2._edge == H3._edge

    with pytest.warns(Warning):
        _ = xgi.chung_lu_hypergraph({1: 1, 2: 2}, {1: 2, 2: 2})


def test_dcsbm_hypergraph():
    n = 50
    k1 = {i: random.randint(1, n) for i in range(n)}
    k2 = {i: sorted(k1.values())[i] for i in range(n)}
    g1 = {i: random.choice([0, 1]) for i in range(n)}
    g2 = {i: random.choice([0, 1]) for i in range(n)}
    omega = np.array([[n // 2, 10], [10, n // 2]])

    H = xgi.dcsbm_hypergraph(k1, k2, g1, g2, omega)

    assert H.num_nodes == 50

    # seed
    H1 = xgi.dcsbm_hypergraph(k1, k2, g1, g2, omega, seed=1)
    H2 = xgi.dcsbm_hypergraph(k1, k2, g1, g2, omega, seed=2)
    H3 = xgi.dcsbm_hypergraph(k1, k2, g1, g2, omega, seed=2)
    assert H1._edge != H2._edge
    assert H2._edge == H3._edge


def test_random_hypergraph():
    # seed
    H1 = xgi.random_hypergraph(10, [0.1, 0.01], seed=1)
    H2 = xgi.random_hypergraph(10, [0.1, 0.01], seed=2)
    H3 = xgi.random_hypergraph(10, [0.1, 0.01], seed=2)

    assert H1._edge != H2._edge
    assert H2._edge == H3._edge

    assert H1.num_nodes == 10
    assert xgi.unique_edge_sizes(H1) == [2, 3]

    # wrong inputs
    # p > 1
    with pytest.raises(ValueError):
        H1 = xgi.random_hypergraph(10, [1, 1.1])
    # p < 0
    with pytest.raises(ValueError):
        H1 = xgi.random_hypergraph(10, [1, -2])
    # p list and order number
    with pytest.raises(ValueError):
        H1 = xgi.random_hypergraph(10, [0.1, 0.1], order=3)
    # different lengths
    with pytest.raises(ValueError):
        H1 = xgi.random_hypergraph(10, [0.1, 0.1], order=[3])

    # uniform
    H4 = xgi.random_hypergraph(10, 0.1, order=2, seed=1)
    assert H4.num_nodes == 10
    assert xgi.unique_edge_sizes(H4) == [3]

    H5 = xgi.random_hypergraph(10, [0.1, 0.1], order=[1, 3], seed=1)
    assert H5.num_nodes == 10
    assert xgi.unique_edge_sizes(H5) == [2, 4]


def test_fast_random_hypergraph():
    # seed
    H1 = xgi.fast_random_hypergraph(10, [0.1, 0.01], seed=1)
    H2 = xgi.fast_random_hypergraph(10, [0.1, 0.01], seed=2)
    H3 = xgi.fast_random_hypergraph(10, [0.1, 0.01], seed=2)

    assert H1._edge != H2._edge
    assert H2._edge == H3._edge

    assert H1.num_nodes == 10
    assert xgi.unique_edge_sizes(H1) == [2, 3]

    # wrong inputs
    # p > 1
    with pytest.raises(ValueError):
        H1 = xgi.fast_random_hypergraph(10, [1, 1.1])
    # p < 0
    with pytest.raises(ValueError):
        H1 = xgi.fast_random_hypergraph(10, [1, -2])
    # p list and order number
    with pytest.raises(ValueError):
        H1 = xgi.fast_random_hypergraph(10, [0.1, 0.1], order=3)
    # different lengths
    with pytest.raises(ValueError):
        H1 = xgi.fast_random_hypergraph(10, [0.1, 0.1], order=[3])

    # uniform
    H4 = xgi.fast_random_hypergraph(10, 0.1, order=2, seed=1)
    assert H4.num_nodes == 10
    assert xgi.unique_edge_sizes(H4) == [3]

    H5 = xgi.fast_random_hypergraph(10, [0.1, 0.1], order=[1, 3], seed=1)
    assert H5.num_nodes == 10
    assert xgi.unique_edge_sizes(H5) == [2, 4]

    H5 = xgi.fast_random_hypergraph(10, [1, 1])
    assert H5.num_edges == comb(10, 2) + comb(10, 3)

    with pytest.raises(ValueError):
        xgi.fast_random_hypergraph(10, 0.1)

    with pytest.raises(ValueError):
        xgi.fast_random_hypergraph(10, 0.1, order=[1, 2])

    with pytest.raises(ValueError):
        xgi.fast_random_hypergraph(10, [1.1, 1])

    with pytest.raises(ValueError):
        xgi.fast_random_hypergraph(10, [-0.1, 1])
