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

    assert H1.edges.size.asdict() == {0: 4, 1: 4}
    assert H2.edges.size.asdict() == {0: 3, 1: 3, 2: 4}
    assert H1.edges.order.asdict() == {0: 3, 1: 3}
    assert H2.edges.order.asdict() == {0: 2, 1: 2, 2: 3}


def test_degree(diedgelist1, diedgelist2):
    H1 = xgi.DiHypergraph(diedgelist1)
    H2 = xgi.DiHypergraph(diedgelist2)
    # test basic functionality
    assert H1.degree(1) == 1
    assert H1.degree(2) == 1
    assert H1.degree(3) == 1
    with pytest.raises(KeyError):
        H1.degree(0)

    # check len
    assert len(H1.degree()) == 8

    # test order
    assert H2.nodes.degree(order=1).asdict() == {0: 0, 1: 0, 2: 0, 4: 0, 3: 0, 5: 0}
    assert H2.nodes.degree(order=2).asdict() == {0: 1, 1: 2, 2: 2, 4: 1, 3: 0, 5: 0}
    assert H2.nodes.degree(order=3).asdict() == {0: 0, 1: 0, 2: 1, 4: 1, 3: 1, 5: 1}

    # test weights
    attr_dict1 = {0: {"weight": -2}, 1: {"weight": 4.0}, 2: {"weight": 0.3}}
    H2.set_edge_attributes(attr_dict1)

    assert H2.nodes.degree(weight="weight").asdict() == {
        0: -2,
        1: 2.0,
        2: 2.3,
        4: 4.3,
        3: 0.3,
        5: 0.3,
    }
    assert H2.nodes.degree(weight="weight", order=2).asdict() == {
        0: -2,
        1: 2.0,
        2: 2.0,
        4: 4.0,
        3: 0,
        5: 0,
    }


def test_edge_members(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.members(0) == {0, 1, 2}
    assert H.edges.members() == [{0, 1, 2}, {1, 2, 4}, {2, 3, 4, 5}]
    assert H.edges.members(dtype=dict) == {0: {0, 1, 2}, 1: {1, 2, 4}, 2: {2, 3, 4, 5}}
    with pytest.raises(XGIError):
        H.edges.members(dtype=np.array)

    with pytest.raises(TypeError):
        H.edges.members([1, 2])

    with pytest.raises(IDNotFound):
        H.edges.members("test")


def test_edge_dimembers(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.dimembers(0) == ({0, 1}, {2})
    assert H.edges.dimembers() == [({0, 1}, {2}), ({1, 2}, {4}), ({2, 3, 4}, {4, 5})]
    assert H.edges.dimembers(dtype=dict) == {
        0: ({0, 1}, {2}),
        1: ({1, 2}, {4}),
        2: ({2, 3, 4}, {4, 5}),
    }
    with pytest.raises(XGIError):
        H.edges.dimembers(dtype=np.array)

    with pytest.raises(TypeError):
        H.edges.dimembers([1, 2])

    with pytest.raises(IDNotFound):
        H.edges.dimembers("test")


def test_edge_tail(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)

    assert H.edges.tail(0) == {0, 1}
    assert H.edges.tail() == [{0, 1}, {1, 2}, {2, 3, 4}]
    assert H.edges.tail(dtype=dict) == {0: {0, 1}, 1: {1, 2}, 2: {2, 3, 4}}

    with pytest.raises(XGIError):
        H.edges.tail(dtype=np.array)

    with pytest.raises(TypeError):
        H.edges.tail([1, 2])

    with pytest.raises(IDNotFound):
        H.edges.tail("test")


def test_edge_head(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)

    assert H.edges.head(0) == {2}
    assert H.edges.head() == [{2}, {4}, {4, 5}]
    assert H.edges.head(dtype=dict) == {0: {2}, 1: {4}, 2: {4, 5}}
    with pytest.raises(XGIError):
        H.edges.head(dtype=np.array)

    with pytest.raises(TypeError):
        H.edges.head([1, 2])

    with pytest.raises(IDNotFound):
        H.edges.head("test")


def test_view_len(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    nodes = H.nodes
    assert len(nodes) == len(H._node_in)
    H.add_node(10)
    assert len(nodes) == len(H._node_in)
    H.add_nodes_from(range(10, 20))
    assert len(nodes) == len(H._node_in)


def test_bunch_view(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    bunch_view = H.edges.from_view(H.edges, bunch=[2, 1])
    assert len(bunch_view) == 2
    assert (1 in bunch_view) and (2 in bunch_view)
    assert 0 not in bunch_view
    assert bunch_view.members(dtype=dict) == {1: {1, 2, 4}, 2: {2, 3, 4, 5}}
    with pytest.raises(IDNotFound):
        bunch_view.members(0)
    # test ID order
    assert list(bunch_view) == [1, 2]


def test_call_wrong_bunch():
    H = xgi.DiHypergraph()
    with pytest.raises(IDNotFound):
        H.nodes([0])

    H.add_node(0)
    assert len(H.nodes([0]))
    with pytest.raises(TypeError):
        H.nodes(0)


def test_call(diedgelist1):
    H = xgi.DiHypergraph(diedgelist1)
    assert len(H.nodes([])) == 0
    assert H.nodes(list(H.nodes)) == H.nodes
    assert H.nodes(H.nodes) == H.nodes


def test_bool(diedgelist1):
    H = xgi.DiHypergraph([])
    assert bool(H.edges) is False
    H = xgi.DiHypergraph(diedgelist1)
    assert bool(H.edges) is True


def test_isolates():
    DH = xgi.DiHypergraph()
    DH.add_nodes_from([0, 1, 2, 3])
    assert set(DH.nodes.isolates()) == {0, 1, 2, 3}
    DH.add_edge([{0}, {1, 2}])
    assert set(DH.nodes.isolates()) == {3}


def test_diview_custom_filterby(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)

    f = lambda val, arg: val % arg == 0
    assert set(H.edges.filterby("tail_size", 2, mode=f)) == {0, 1}


def test_diview_custom_filterby_attr(dihyperwithattrs):
    f = lambda val, arg: arg in val
    assert set(dihyperwithattrs.nodes.filterby_attr("color", "l", mode=f)) == {2, 3, 5}
