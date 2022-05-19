import pytest

import xgi
from xgi.exception import IDNotFound


def test_filterby_wrong_stat():
    H = xgi.Hypergraph()
    with pytest.raises(AttributeError):
        H.nodes.filterby("__I_DO_NOT_EXIST__", None)


def test_filterby(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    assert H.nodes.filterby("degree", 2).average_neighbor_degree.asdict() == {6: 1.0}
    assert H.nodes.filterby("average_neighbor_degree", 1.0).degree.asdict() == {
        1: 1,
        2: 1,
        3: 1,
        6: 2,
    }

    H = xgi.Hypergraph(edgelist8)
    assert H.nodes.filterby("degree", 3).average_neighbor_degree.asdict() == {4: 4.2}
    assert H.nodes.filterby("average_neighbor_degree", 4.2).degree.asdict() == {4: 3}


def test_filterby_modes(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    assert list(H.nodes.filterby("degree", 2)) == [6]
    assert list(H.nodes.filterby("degree", 2, "eq")) == [6]
    assert list(H.nodes.filterby("degree", 1, "neq")) == [6]
    assert list(H.nodes.filterby("degree", 2, "geq")) == [6]
    assert list(H.nodes.filterby("degree", 2, "gt")) == []
    assert list(H.nodes.filterby("degree", 0, "leq")) == []
    assert list(H.nodes.filterby("degree", 1, "lt")) == []
    assert list(H.nodes.filterby("degree", (1, 3), "between")) == list(H.nodes)

    H = xgi.Hypergraph(edgelist8)
    assert list(H.nodes.filterby("degree", 2)) == [5, 6]
    assert list(H.nodes.filterby("degree", 2, "eq")) == [5, 6]
    assert list(H.nodes.filterby("degree", 2, "neq")) == [0, 1, 2, 3, 4]
    assert list(H.nodes.filterby("degree", 5, "geq")) == [0, 1]
    assert list(H.nodes.filterby("degree", 5, "gt")) == [0]
    assert list(H.nodes.filterby("degree", 2, "leq")) == [5, 6]
    assert list(H.nodes.filterby("degree", 2, "lt")) == []
    assert list(H.nodes.filterby("degree", (2, 3), "between")) == [4, 5, 6]


def test_call_filterby(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)

    filtered = H.nodes([5, 6, 7, 8]).filterby("average_neighbor_degree", 2.0).degree
    assert filtered.asdict() == {5: 1}

    filtered = H.nodes([5, 6, 7, 8]).filterby("degree", 2).average_neighbor_degree
    assert filtered.asdict() == {6: 1.0}

    H = xgi.Hypergraph(edgelist8)
    assert list(H.nodes([1, 2, 3]).filterby("degree", 4)) == [2, 3]

    filtered = H.nodes([1, 2, 3]).filterby("average_neighbor_degree", 4.0).degree
    assert filtered.asdict() == {2: 4, 3: 4}

    filtered = H.nodes([1, 2, 3]).filterby("degree", 5).average_neighbor_degree
    assert filtered.asdict() == {1: 3.5}


def test_single_node(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert H.degree()[1] == 1
    assert H.nodes.degree[1] == 1
    with pytest.raises(KeyError):
        H.degree()[-1]
    with pytest.raises(KeyError):
        H.nodes.degree[-1]


def test_degree(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    degs = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1}
    assert H.degree() == degs
    assert H.nodes.degree.asdict() == degs
    assert H.nodes.degree.aslist() == list(degs.values())

    H = xgi.Hypergraph(edgelist8)
    degs = {0: 6, 1: 5, 2: 4, 3: 4, 4: 3, 5: 2, 6: 2}
    assert H.degree() == degs
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


def test_aggregates(edgelist1, edgelist2, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    assert H.nodes.degree.max() == 2
    assert H.nodes.degree.min() == 1
    assert H.nodes.degree.argmax() == 6
    assert H.nodes.degree.argmin() == 1
    assert round(H.nodes.degree.mean(), 3) == 1.125
    assert round(H.nodes.degree.std(), 3) == 0.331
    assert round(H.nodes.degree.var(), 3) == 0.109

    H = xgi.Hypergraph(edgelist2)
    assert H.nodes.degree.max() == 2
    assert H.nodes.degree.min() == 1
    assert H.nodes.degree.argmax() == 4
    assert H.nodes.degree.argmin() == 1
    assert round(H.nodes.degree.mean(), 3) == 1.167
    assert round(H.nodes.degree.std(), 3) == 0.373
    assert round(H.nodes.degree.var(), 3) == 0.139

    H = xgi.Hypergraph(edgelist8)
    assert H.nodes.degree.max() == 6
    assert H.nodes.degree.min() == 2
    assert H.nodes.degree.argmax() == 0
    assert H.nodes.degree.argmin() == 5
    assert round(H.nodes.degree.mean(), 3) == 3.714
    assert round(H.nodes.degree.std(), 3) == 1.385
    assert round(H.nodes.degree.var(), 3) == 1.918


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


def test_stats_are_views(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    ns = H.nodes.degree
    assert ns.asdict() == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1}
    H.add_node(10)
    assert ns.asdict() == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1, 10: 0}
    H.add_edge([1, 2, 10, 20])
    assert ns.asdict() == {1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1, 10: 1, 20: 1}
