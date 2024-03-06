import numpy as np
import pandas as pd
import pytest

import xgi


def test_degree(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    degs = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1}
    assert H.degree() == degs
    assert H.degree(order=2) == {1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1}
    assert H.nodes.degree.asdict() == degs
    assert H.nodes.degree.aslist() == list(degs.values())

    H = xgi.Hypergraph(edgelist8)
    degs = {0: 6, 1: 5, 2: 4, 3: 4, 4: 3, 5: 2, 6: 2}
    assert H.degree() == degs
    assert H.degree(order=2) == {0: 3, 1: 2, 2: 3, 3: 3, 4: 2, 5: 2, 6: 0}
    assert H.nodes.degree.asdict() == degs
    assert H.nodes.degree.aslist() == list(degs.values())


def test_average_neighbor_degree(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    vals = {1: 1.0, 2: 1.0, 3: 1.0, 4: 0, 5: 2.0, 6: 1.0, 7: 1.5, 8: 1.5}
    assert H.average_neighbor_degree() == vals
    assert H.nodes.average_neighbor_degree().asdict() == vals
    assert H.nodes.average_neighbor_degree().aslist() == list(vals.values())

    H = xgi.Hypergraph(edgelist8)
    vals = {0: 3.6, 1: 3.5, 2: 4.0, 3: 4.0, 4: 4.2, 5: 4.0, 6: 5.5}
    assert H.average_neighbor_degree() == vals
    assert H.nodes.average_neighbor_degree().asdict() == vals
    assert H.nodes.average_neighbor_degree().aslist() == list(vals.values())


def test_clustering_coefficient():
    # no nodes
    H = xgi.Hypergraph()

    assert H.clustering_coefficient() == dict()
    assert H.nodes.clustering_coefficient().aslist() == []
    assert H.nodes.clustering_coefficient().asdict() == dict()

    # no edges
    H.add_nodes_from(range(3))
    assert H.nodes.clustering_coefficient().aslist() == [0, 0, 0]
    assert H.nodes.clustering_coefficient().asdict() == {0: 0, 1: 0, 2: 0}

    # edges
    edges = [[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]]
    H = xgi.Hypergraph(edges)
    assert np.allclose(
        H.nodes.clustering_coefficient.aslist(), np.array([1, 2 / 3, 2 / 3, 1, 1])
    )


def test_local_clustering_coefficient():
    # no nodes
    H = xgi.Hypergraph()

    assert H.local_clustering_coefficient() == dict()
    assert H.nodes.local_clustering_coefficient().aslist() == []
    assert H.nodes.local_clustering_coefficient().asdict() == dict()

    # no edges
    H.add_nodes_from(range(3))
    assert H.nodes.local_clustering_coefficient().aslist() == [0, 0, 0]
    assert H.nodes.local_clustering_coefficient().asdict() == {0: 0, 1: 0, 2: 0}

    # edges
    edges = [[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]]
    H = xgi.Hypergraph(edges)
    assert np.allclose(
        H.nodes.local_clustering_coefficient.aslist(), np.array([0, 0, 0.25, 0, 0])
    )


def test_two_node_clustering_coefficient():
    # no nodes
    H = xgi.Hypergraph()

    assert H.two_node_clustering_coefficient() == dict()
    assert H.nodes.two_node_clustering_coefficient().aslist() == []
    assert H.nodes.two_node_clustering_coefficient().asdict() == dict()

    # no edges
    H.add_nodes_from(range(3))
    assert H.nodes.two_node_clustering_coefficient().aslist() == [0, 0, 0]
    assert H.nodes.two_node_clustering_coefficient().asdict() == {0: 0, 1: 0, 2: 0}

    # edges
    edges = [[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]]
    H = xgi.Hypergraph(edges)
    assert np.allclose(
        H.nodes.two_node_clustering_coefficient(kind="union").aslist(),
        np.array(
            [
                0.41666666666666663,
                0.45833333333333326,
                0.5833333333333333,
                0.6666666666666666,
                0.6666666666666666,
            ]
        ),
    )


def test_attrs(hyperwithattrs, attr1, attr2, attr3, attr4, attr5):
    H = hyperwithattrs
    attrs = {
        1: attr1,
        2: attr2,
        3: attr3,
        4: attr4,
        5: attr5,
    }
    assert H.nodes.attrs.asdict() == attrs
    assert H.nodes.attrs.aslist() == list(attrs.values())
    assert H.nodes.attrs("color").asdict() == {n: H._node_attr[n]["color"] for n in H}

    filtered = H.nodes.filterby_attr("color", "blue").attrs
    assert filtered.asdict() == {2: attr2, 5: attr5}

    filtered = H.nodes([1, 2, 3]).filterby_attr("color", "blue").attrs
    assert filtered.asdict() == {2: attr2}

    filtered = H.nodes([1, 2, 3]).filterby("degree", 3).attrs
    assert filtered.asdict() == {3: attr3}

    with pytest.raises(ValueError):
        H.nodes.attrs(-1).asdict()
