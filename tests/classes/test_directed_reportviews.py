import numpy as np
import pytest

import xgi
from xgi.exception import IDNotFound, XGIError


def test_edge_order(diedgelist1):
    H = xgi.DiHypergraph(diedgelist1)

    with pytest.raises(TypeError):
        H.edges()

    assert len(H.edges.filterby("order", 3)) == 2
    assert len(H.edges.filterby("order", 2)) == 0

    ord2 = H.edges.filterby("order", 3)
    assert len(ord2) == 2
    assert (0 in ord2) and (1 in ord2)

    H.add_edge(([3, 7, 8, 9, 10], [11, 12]))

    assert len(H.edges.filterby("order", 6)) == 1
    assert 2 in H.edges.filterby("order", 6)


def test_node_degree(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)

    with pytest.raises(TypeError):
        H.edges()

    assert H.degree() == {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    assert H.degree(1) == 2
    assert H.degree(2) == 3
    with pytest.raises(KeyError):
        H.degree(-1)

    assert len(H.nodes.filterby("degree", 1)) == 3
    assert len(H.nodes.filterby("degree", 3)) == 1
    deg2 = H.nodes.filterby("degree", 2)
    assert len(deg2) == 2
    assert (1 in deg2) and (4 in deg2)

    H.add_edge(([3, 7], [9, 10]))

    assert len(H.nodes.filterby("degree", 2)) == 3
    assert len(H.nodes.filterby("degree", 3)) == 1
    assert 3 in H.nodes.filterby("degree", 2)
    assert 7 in H.nodes.filterby("degree", 1)


def test_size_degree(diedgelist1, diedgelist2):
    H1 = xgi.DiHypergraph(diedgelist1)
    H2 = xgi.DiHypergraph(diedgelist2)
    assert H1.edges.size.asdict() == {0: 3, 1: 4, 2: 3}
    assert H2.edges.size.asdict() == {0: 3, 1: 1, 2: 2, 3: 3}
    assert H1.edges.order.asdict() == {0: 2, 1: 3, 2: 2}
    assert H2.edges.order.asdict() == {0: 2, 1: 0, 2: 1, 3: 2}


def test_degree(edgelist1, edgelist4):
    H1 = xgi.Hypergraph(edgelist4)
    H2 = xgi.Hypergraph(edgelist1)
    # test basic functionality
    assert H1.degree(1) == 1
    assert H1.degree(2) == 2
    assert H1.degree(3) == 3
    with pytest.raises(KeyError):
        H1.degree(0)

    # check len
    assert len(H1.degree()) == 5

    # test order
    assert H2.nodes.degree(order=0).asdict() == {
        1: 0,
        2: 0,
        3: 0,
        4: 1,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
    }
    assert H2.nodes.degree(order=1).asdict() == {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 1,
        6: 1,
        7: 0,
        8: 0,
    }
    assert H2.nodes.degree(order=2).asdict() == {
        1: 1,
        2: 1,
        3: 1,
        4: 0,
        5: 0,
        6: 1,
        7: 1,
        8: 1,
    }

    # test weights
    attr_dict1 = {0: {"weight": -2}, 1: {"weight": 4.0}, 2: {"weight": 0.3}}
    xgi.set_edge_attributes(H1, attr_dict1)

    assert H1.nodes.degree(weight="weight").asdict() == {
        1: -2,
        2: 2,
        3: 2.3,
        4: 4.3,
        5: 4.3,
    }
    assert H1.nodes.degree(weight="weight", order=2).asdict() == {
        1: -2,
        2: -2,
        3: -1.7,
        4: 0.3,
        5: 0.3,
    }


def test_edge_members(edgelist3):
    H = xgi.Hypergraph(edgelist3)
    assert H.edges.members(0) == {1, 2, 3}
    assert H.edges.members() == [{1, 2, 3}, {3, 4}, {4, 5, 6}]
    assert H.edges.members(dtype=dict) == {0: {1, 2, 3}, 1: {3, 4}, 2: {4, 5, 6}}
    with pytest.raises(XGIError):
        H.edges.members(dtype=np.array)

    with pytest.raises(TypeError):
        H.edges.members(slice(1, 4, 1))

    with pytest.raises(TypeError):
        H.edges.members([1, 2])

    with pytest.raises(IDNotFound):
        H.edges.members("test")


def test_view_len(edgelist2):
    H = xgi.Hypergraph(edgelist2)
    nodes = H.nodes
    assert len(nodes) == len(H._node)
    H.add_node(10)
    assert len(nodes) == len(H._node)
    H.add_nodes_from(range(10, 20))
    assert len(nodes) == len(H._node)


def test_bunch_view(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    bunch_view = H.edges.from_view(H.edges, bunch=[1, 2])
    assert len(bunch_view) == 2
    assert (1 in bunch_view) and (2 in bunch_view)
    assert 0 not in bunch_view
    assert bunch_view.members(dtype=dict) == {1: {4}, 2: {5, 6}}
    with pytest.raises(IDNotFound):
        bunch_view.members(0)


def test_call_wrong_bunch():
    H = xgi.Hypergraph()
    with pytest.raises(IDNotFound):
        H.nodes([0])

    H.add_node(0)
    assert len(H.nodes([0]))
    with pytest.raises(TypeError):
        H.nodes(0)


def test_call(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert len(H.nodes([])) == 0
    assert H.nodes(list(H.nodes)) == H.nodes
    assert H.nodes(H.nodes) == H.nodes


def test_isolates(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert list(H.nodes.isolates(ignore_singletons=True)) == [4]
    assert list(H.nodes.isolates()) == []
    H.remove_nodes_from(H.nodes.isolates(ignore_singletons=True))
    assert 4 not in H

    H.add_nodes_from([10, 11, 12])
    assert 10 in H and 11 in H and 12 in H
    H.remove_nodes_from(H.nodes.isolates())
    assert 10 not in H and 11 not in H and 12 not in H


def test_singletons(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert list(H.edges.singletons()) == [1]
    H.remove_edge(1)
    assert 1 not in H.edges
    assert list(H.edges.singletons()) == []


def test_lookup(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert list(H.edges.lookup([1, 2, 3])) == [0]
    assert list(H.edges.lookup({1, 2, 3})) == [0]
    assert list(H.edges.lookup({4})) == [1]
    assert list(H.edges.lookup([4, 5])) == []
    assert list(H.edges.lookup([3])) == []
    assert list(H.edges.lookup([4])) == [1]
    assert list(H.edges.lookup([1, 2])) == []

    H = xgi.Hypergraph([["a", "b", "c"], ["a", "b", "e"], ["c", "d", "e"]])
    assert set(H.nodes.lookup([0, 1])) == {"a", "b"}


def test_bool(edgelist1):
    H = xgi.Hypergraph([])
    assert bool(H.edges) is False
    H = xgi.Hypergraph(edgelist1)
    assert bool(H.edges) is True


def test_set_operations(hyperwithattrs):
    H = hyperwithattrs

    nodes1 = H.nodes.filterby_attr("color", "blue")
    nodes2 = H.nodes.filterby("degree", 2, "geq")
    assert set(nodes2 - nodes1) == {3, 4}
    assert set(nodes1 - nodes2) == set()
    assert set(nodes1 & nodes2) == {2, 5}
    assert set(nodes1 | nodes2) == {2, 3, 4, 5}
    assert set(nodes1 ^ nodes2) == {3, 4}

    edges1 = H.edges
    edges2 = H.edges.filterby("size", 3, "leq")
    assert set(edges2 - edges1) == set()
    assert set(edges1 - edges2) == {1}
    assert set(edges1 & edges2) == {0, 2}
    assert set(edges1 | edges2) == {0, 1, 2}
    assert set(edges1 ^ edges2) == {1}


def test_maximal(edgelist5, edgelist8):
    S1 = xgi.SimplicialComplex(edgelist5)
    S2 = xgi.SimplicialComplex(edgelist8)

    m1 = S1.edges.maximal()
    m2 = S2.edges.maximal()

    simp1 = S1.edges(m1).members()
    simp2 = S2.edges(m2).members()

    assert len(m1) == 4
    assert {0, 1, 2, 3} in simp1
    assert {4} in simp1
    assert {5, 6} in simp1
    assert {6, 7, 8} in simp1

    assert len(m2) == 5
    assert {0, 1, 2, 3, 4} in simp2
    assert {2, 4, 5} in simp2
    assert {1, 3, 5} in simp2
    assert {1, 6} in simp2
    assert {0, 6} in simp2

    H = xgi.Hypergraph([{1, 2, 3}, {1, 2}, {2, 3}, {2}, {2}, {3, 4}, {1, 2, 3}])

    m = H.edges.maximal()
    assert set(m) == {0, 5, 6}

    H.add_node(10)
    m = H.edges.maximal()
    assert set(m) == {0, 5, 6}

    # try strict=True
    m = H.edges.maximal(strict=True)
    assert set(m) == {5}
