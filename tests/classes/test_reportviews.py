import numpy as np
import pytest

import xgi
from xgi.exception import XGIError


def test_edge_order(edgelist3):
    H = xgi.Hypergraph(edgelist3)

    with pytest.raises(TypeError):
        H.edges()

    assert len(H.edges(order=1)) == 1
    assert len(H.edges(order=3)) == 0

    ord2 = H.edges(order=2)
    assert len(ord2) == 2
    assert (0 in ord2) and (2 in ord2)

    H.add_edge([3, 7, 8, 9, 10])

    assert len(H.edges(order=4)) == 1
    assert 3 in H.edges(order=4)

    H.add_node_to_edge(0, 7)

    assert 0 not in H.edges(order=2)
    assert len(H.edges(order=2)) == 1
    assert 2 in H.edges(order=2)


def test_node_degree(edgelist3):
    H = xgi.Hypergraph(edgelist3)

    with pytest.raises(TypeError):
        H.edges()

    assert len(H.nodes(degree=1)) == 4
    assert len(H.nodes(degree=3)) == 0
    deg2 = H.nodes(degree=2)
    assert len(deg2) == 2
    assert (3 in deg2) and (4 in deg2)

    H.add_edge([3, 7])

    assert len(H.nodes(degree=2)) == 1
    assert len(H.nodes(degree=3)) == 1
    assert 3 in H.nodes(degree=3)
    assert 7 in H.nodes(degree=1)

    H.add_node_to_edge(0, 7)
    assert 7 in H.nodes(degree=2)


def test_id_degree_view(edgelist1, edgelist4):
    H1 = xgi.Hypergraph(edgelist4)
    H2 = xgi.Hypergraph(edgelist1)
    # test basic functionality
    assert H1.degree(1) == 1
    assert H1.degree(2) == 2
    assert H1.degree(3) == 3
    with pytest.raises(XGIError):
        H1.degree(0)

    assert H1.edge_size()[H1.edges] == {0: 3, 1: 4, 2: 3}
    assert H2.edge_size()[H2.edges] == {0: 3, 1: 1, 2: 2, 3: 3}

    # check len
    assert len(H1.degree([1, 2])) == 2
    assert len(H1.degree()) == 5

    # check string
    assert str(H1.degree()) == "[1, 2, 3, 4, 5]"

    # check representation
    assert repr(H1.degree()) == "DegreeView({1: 1, 2: 2, 3: 3, 4: 2, 5: 2})"

    # check __iter__
    assert {id: deg for id, deg in H1.degree()} == {1: 1, 2: 2, 3: 3, 4: 2, 5: 2}

    # check dtype parameter
    assert H1.degree(dtype="list")[H1.nodes] == [1, 2, 3, 2, 2]
    assert (H1.degree(dtype="nparray")[H1.nodes] == np.array([1, 2, 3, 2, 2])).all()

    # test order
    assert H2.degree(1, order=0) == 0
    assert H2.degree(4, order=0) == 1
    assert H2.degree(5, order=0) == 0

    assert H2.degree(1, order=1) == 0
    assert H2.degree(4, order=1) == 0
    assert H2.degree(6, order=1) == 1

    assert H1.degree(3, order=1) == 0
    assert H1.degree(3, order=2) == 2
    assert H1.degree(3, order=3) == 1
    assert H1.degree(5, order=2) == 1

    # test weights
    attr_dict1 = {0: {"weight": -2}, 1: {"weight": 4.0}, 2: {"weight": 0.3}}
    xgi.set_edge_attributes(H1, attr_dict1)

    assert H1.degree(weight="weight")[H1.nodes] == {1: -2, 2: 2, 3: 2.3, 4: 4.3, 5: 4.3}
    assert H1.degree(weight="weight", order=2)[H1.nodes] == {
        1: -2,
        2: -2,
        3: -1.7,
        4: 0.3,
        5: 0.3,
    }


def test_edge_members(edgelist3):
    H = xgi.Hypergraph(edgelist3)
    assert H.edges.members(0) == [1, 2, 3]
    assert H.edges.members() == [[1, 2, 3], [3, 4], [4, 5, 6]]
    assert H.edges.members(dtype=dict) == {0: [1, 2, 3], 1: [3, 4], 2: [4, 5, 6]}


def test_bunch_view(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    bunch_view = H.edges.from_view(H.edges, bunch=[1, 2])
    assert len(bunch_view) == 2
    assert (1 in bunch_view) and (2 in bunch_view)
    assert 0 not in bunch_view
    assert bunch_view.members(dtype=dict) == {1: [4], 2: [5, 6]}
