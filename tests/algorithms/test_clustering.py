import numpy as np
import pytest

import xgi
from xgi.exception import XGIError


def test_local_clustering_coefficient(edgelist8):
    H = xgi.random_hypergraph(3, [1])

    cc = xgi.local_clustering_coefficient(H)
    true_cc = {0: 1.0, 1: 1.0, 2: 1.0}
    assert cc == true_cc

    H = xgi.random_hypergraph(3, [1, 1])
    cc = xgi.local_clustering_coefficient(H)
    true_cc = {0: 1.0, 1: 1.0, 2: 1.0}
    assert cc == true_cc

    H = xgi.random_hypergraph(3, [0, 1])
    cc = xgi.local_clustering_coefficient(H)
    true_cc = {0: 0.0, 1: 0.0, 2: 0.0}
    assert cc == true_cc

    H = xgi.Hypergraph()
    cc = xgi.local_clustering_coefficient(H)
    assert cc == {}

    H = xgi.Hypergraph()
    H.add_nodes_from(range(3))
    cc = xgi.local_clustering_coefficient(H)
    assert set(cc) == {0, 1, 2}
    for i in cc:
        assert np.isnan(cc[i])

    H = xgi.Hypergraph(edgelist8)
    cc = xgi.local_clustering_coefficient(H)
    true_cc = {
        0: 0.6777777777777778,
        1: 0.575,
        2: 0.3333333333333333,
        3: 0.3333333333333333,
        4: 0.6666666666666666,
        5: 0.0,
        6: 0.0,
    }
    assert cc == true_cc


def test_clustering_coefficient(edgelist1):
    H = xgi.random_hypergraph(3, [1])

    cc = xgi.clustering_coefficient(H)
    true_cc = {0: 1.0, 1: 1.0, 2: 1.0}
    assert cc == true_cc

    H = xgi.random_hypergraph(3, [1, 1])
    cc = xgi.clustering_coefficient(H)
    true_cc = {0: 1.0, 1: 1.0, 2: 1.0}
    assert cc == true_cc

    H = xgi.random_hypergraph(3, [0, 1])
    cc = xgi.clustering_coefficient(H)
    true_cc = {0: 1.0, 1: 1.0, 2: 1.0}
    assert cc == true_cc

    H = xgi.Hypergraph()
    cc = xgi.clustering_coefficient(H)
    assert cc == {}

    H = xgi.Hypergraph()
    H.add_nodes_from(range(3))
    cc = xgi.clustering_coefficient(H)
    assert set(cc) == {0, 1, 2}
    for i in cc:
        assert np.isnan(cc[i])

    H = xgi.Hypergraph(edgelist1)
    cc = xgi.clustering_coefficient(H)
    true_cc = {1: 1.0, 2: 1.0, 3: 1.0, 4: np.nan, 5: np.nan, 6: 1 / 3, 8: 1.0, 7: 1.0}
    assert np.isnan(cc[4])
    assert np.isnan(cc[5])
    assert {i: cc[i] for i in cc if i not in [4, 5]} == {
        i: true_cc[i] for i in true_cc if i not in [4, 5]
    }


def test_two_node_clustering_coefficient(edgelist1, edgelist8):
    H = xgi.random_hypergraph(3, [1])

    cc = xgi.two_node_clustering_coefficient(H)
    true_cc = {0: 1 / 3, 1: 1 / 3, 2: 1 / 3}
    assert cc == true_cc

    # check default keyword
    cc1 = xgi.two_node_clustering_coefficient(H, kind="union")
    assert cc == cc1

    H = xgi.random_hypergraph(3, [1, 1])
    cc = xgi.two_node_clustering_coefficient(H)
    true_cc = {0: 0.5, 1: 0.5, 2: 0.5}
    assert cc == true_cc

    H = xgi.Hypergraph(edgelist1)
    cc1 = xgi.two_node_clustering_coefficient(H, kind="union")
    cc2 = xgi.two_node_clustering_coefficient(H, kind="min")
    cc3 = xgi.two_node_clustering_coefficient(H, kind="max")

    true_cc1 = {1: 1.0, 2: 1.0, 3: 1.0, 4: np.nan, 5: 0.5, 6: 0.5, 8: 0.75, 7: 0.75}
    true_cc2 = {1: 1.0, 2: 1.0, 3: 1.0, 4: np.nan, 5: 1.0, 6: 1.0, 8: 1.0, 7: 1.0}
    true_cc3 = {1: 1.0, 2: 1.0, 3: 1.0, 4: np.nan, 5: 0.5, 6: 0.5, 8: 0.75, 7: 0.75}

    assert {i: cc1[i] for i in cc1 if i != 4} == {
        i: true_cc1[i] for i in true_cc1 if i != 4
    }
    assert np.isnan(cc1[4])

    assert {i: cc2[i] for i in cc2 if i != 4} == {
        i: true_cc2[i] for i in true_cc2 if i != 4
    }
    assert np.isnan(cc2[4])

    assert {i: cc3[i] for i in cc3 if i != 4} == {
        i: true_cc3[i] for i in true_cc3 if i != 4
    }
    assert np.isnan(cc3[4])

    with pytest.raises(XGIError):
        xgi.two_node_clustering_coefficient(H, kind="test")

    H = xgi.Hypergraph(edgelist8)
    H.add_node(10)
    cc = xgi.two_node_clustering_coefficient(H, kind="min")
    true_cc = {
        0: 0.6533333333333333,
        1: 0.4888888888888888,
        2: 0.5833333333333333,
        3: 0.5833333333333333,
        4: 0.5666666666666667,
        5: 0.5,
        6: 0.5,
        10: np.nan,
    }
    assert {i: cc[i] for i in cc if i != 10} == {
        i: true_cc[i] for i in true_cc if i != 10
    }
    assert np.isnan(cc[10])
