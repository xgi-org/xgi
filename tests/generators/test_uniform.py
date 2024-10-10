import numpy as np
import pytest
from scipy.special import comb

import xgi
from xgi.exception import XGIError


def test_uniform_configuration_model_hypergraph():
    m = 3
    k = {1: 1, 2: 2, 3: 3, 4: 3}
    H = xgi.uniform_hypergraph_configuration_model(k, m, seed=3)
    assert H.num_nodes == 4
    assert dict(H.degree()) == k
    assert H.num_edges == 3

    with pytest.warns(Warning):
        m = 3
        k = {1: 1, 2: 6}
        H = xgi.uniform_hypergraph_configuration_model(k, m)
    assert H.nodes.degree.asnumpy().sum() % m == 0


def test_uniform_HSBM():
    # sum of sizes != n
    with pytest.raises(XGIError):
        m = 2
        n = 10
        sizes = [4, 5]
        p = np.array([[0.5, 0.1], [0.1, 0.5]])
        xgi.uniform_HSBM(n, m, p, sizes)

    # non-square p
    with pytest.raises(XGIError):
        m = 2
        n = 10
        sizes = [4, 6]
        p = np.array([[0.5, 0.1], [0.1, 0.5], [0, 1]])
        xgi.uniform_HSBM(n, m, p, sizes)

    # length of sizes and length of p don't match
    with pytest.raises(XGIError):
        m = 2
        n = 10
        sizes = [4, 5, 1]
        p = np.array([[0.5, 0.1], [0.1, 0.5]])
        xgi.uniform_HSBM(n, m, p, sizes)

    # dim of p is not m
    # non-square p
    with pytest.raises(XGIError):
        m = 3
        n = 10
        sizes = [4, 6]
        p = np.array([[0.5, 0.1], [0.1, 0.5]])
        xgi.uniform_HSBM(n, m, p, sizes)

    # test p < 0
    with pytest.raises(XGIError):
        m = 2
        n = 10
        sizes = [4, 6]
        p = np.array([[0.5, -0.1], [0.1, 0.5]])
        xgi.uniform_HSBM(n, m, p, sizes)

    # test p > 1
    with pytest.raises(XGIError):
        m = 2
        n = 10
        sizes = [4, 6]
        p = np.array([[0.5, 1.1], [0.1, 0.5]])
        xgi.uniform_HSBM(n, m, p, sizes)

    m = 2
    n = 10
    sizes = [4, 6]
    p = np.array([[0.5, 0.1], [0.1, 0.5]])
    H1 = xgi.uniform_HSBM(n, m, p, sizes, seed=0)

    assert H1.num_nodes == 10
    assert xgi.unique_edge_sizes(H1) == [2]

    # test that the seed works
    H2 = xgi.uniform_HSBM(n, m, p, sizes, seed=0)

    assert H1.edges.members(dtype=dict) == H2.edges.members(dtype=dict)


def test_uniform_HPPM():
    # rho < 0
    with pytest.raises(XGIError):
        m = 2
        n = 10
        rho = -0.1
        k = 2
        epsilon = 0.5
        xgi.uniform_HPPM(n, m, k, epsilon, rho)

    # rho > 1
    with pytest.raises(XGIError):
        m = 2
        n = 10
        rho = 1.1
        k = 2
        epsilon = 0.5
        xgi.uniform_HPPM(n, m, k, epsilon, rho)

    # k < 0
    with pytest.raises(XGIError):
        m = 2
        n = 10
        rho = 0.5
        k = -2
        epsilon = 0.5
        xgi.uniform_HPPM(n, m, k, epsilon, rho)

    # epsilon < 0
    with pytest.raises(XGIError):
        m = 2
        n = 10
        rho = 0.5
        k = 2
        epsilon = -0.1
        xgi.uniform_HPPM(n, m, k, epsilon)

    # epsilon < 0
    with pytest.raises(XGIError):
        m = 2
        n = 10
        rho = 0.5
        k = 2
        epsilon = 1.1
        xgi.uniform_HPPM(n, m, k, epsilon)

    m = 2
    n = 10
    rho = 0.5
    k = 2
    epsilon = 0.8
    H1 = xgi.uniform_HPPM(n, m, k, epsilon, seed=0)

    assert H1.num_nodes == 10
    assert xgi.unique_edge_sizes(H1) == [2]

    # test that the seed works
    H2 = xgi.uniform_HPPM(n, m, k, epsilon, rho, seed=0)

    assert H1.edges.members(dtype=dict) == H2.edges.members(dtype=dict)


def test_uniform_erdos_renyi_hypergraph():
    m = 2
    n = 10
    p = 1
    H1 = xgi.uniform_erdos_renyi_hypergraph(n, m, p, seed=0)
    ne1 = H1.num_edges
    H1.merge_duplicate_edges(rename="tuple")
    ne2 = H1.num_edges
    assert ne1 == ne2
    assert ne1 == comb(n, m)

    assert H1.num_nodes == 10
    assert xgi.unique_edge_sizes(H1) == [2]

    H2 = xgi.uniform_erdos_renyi_hypergraph(n, m, p, seed=0, multiedges=True)
    print(H2.edges)
    ne1 = H2.num_edges
    H2.merge_duplicate_edges()
    ne2 = H2.num_edges
    assert ne1 != ne2
    assert ne1 == n**m - n  # remove loopy edges

    # test that the seed works
    p = 0.1
    H1 = xgi.uniform_erdos_renyi_hypergraph(n, m, p, seed=0)
    H2 = xgi.uniform_erdos_renyi_hypergraph(n, m, p, seed=0)

    assert H1.edges.members(dtype=dict) == H2.edges.members(dtype=dict)

    # test p < 0
    with pytest.raises(XGIError):
        m = 2
        n = 10
        p = -0.1
        xgi.uniform_erdos_renyi_hypergraph(n, m, p, p_type="prob")

    # test p > 1
    with pytest.raises(XGIError):
        m = 2
        n = 10
        p = 1.1
        xgi.uniform_erdos_renyi_hypergraph(n, m, p, p_type="prob")

    # test wrong p_type arg
    with pytest.raises(XGIError):
        m = 2
        n = 10
        k = 2
        xgi.uniform_erdos_renyi_hypergraph(n, m, k, p_type="test")
