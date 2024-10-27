import networkx as nx
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
    true_cc = {0: 0.333, 1: 0.333, 2: 0.333}
    for n in cc:
        assert round(cc[n], 3) == true_cc[n]

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
    assert cc == {0: 0, 1: 0, 2: 0}

    H = xgi.Hypergraph(edgelist8)
    cc = xgi.local_clustering_coefficient(H)
    true_cc = {
        0: 0.47111111111111115,
        1: 0.44833333333333336,
        2: 0.625,
        3: 0.625,
        4: 0.5833333333333334,
        5: 1.0,
        6: 1.0,
    }
    for n in cc:
        assert round(cc[n], 3) == round(true_cc[n], 3)

    G = nx.erdos_renyi_graph(50, 0.1, seed=0)
    H = xgi.Hypergraph()
    H.add_nodes_from(G.nodes)
    H.add_edges_from(G.edges)
    cc = nx.clustering(G)
    lcc = xgi.local_clustering_coefficient(H)
    assert cc == lcc


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
    assert {0: 0, 1: 0, 2: 0}

    H = xgi.Hypergraph(edgelist1)
    cc = xgi.clustering_coefficient(H)
    true_cc = {1: 1.0, 2: 1.0, 3: 1.0, 4: 0, 5: 0, 6: 1 / 3, 8: 1.0, 7: 1.0}
    assert cc == true_cc


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

    true_cc1 = {1: 1.0, 2: 1.0, 3: 1.0, 4: 0, 5: 0.5, 6: 0.5, 8: 0.75, 7: 0.75}
    true_cc2 = {1: 1.0, 2: 1.0, 3: 1.0, 4: 0, 5: 1.0, 6: 1.0, 8: 1.0, 7: 1.0}
    true_cc3 = {1: 1.0, 2: 1.0, 3: 1.0, 4: 0, 5: 0.5, 6: 0.5, 8: 0.75, 7: 0.75}

    assert cc1 == true_cc1
    assert cc2 == true_cc2
    assert cc3 == true_cc3

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
        10: 0,
    }
    assert cc == true_cc
