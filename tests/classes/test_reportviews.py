import numpy as np

import pytest

import xgi
from xgi.exception import XGIError

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
    assert H2.degree(1, order=1) == 0
    assert H2.degree(4, order=1) == 1
    assert H2.degree(5, order=1) == 0

    assert H2.degree(1, order=2) == 0
    assert H2.degree(4, order=2) == 0
    assert H2.degree(6, order=2) == 1

    assert H1.degree(3, order=2) == 0
    assert H1.degree(3, order=3) == 2
    assert H1.degree(3, order=4) == 1
    assert H1.degree(5, order=3) == 1

    # test weights
    attr_dict1 = {0: {"weight": -2}, 1: {"weight": 4.0}, 2: {"weight": 0.3}}
    xgi.set_edge_attributes(H1, attr_dict1)

    assert H1.degree(weight="weight")[H1.nodes] == {1: -2, 2: 2, 3: 2.3, 4: 4.3, 5: 4.3}
    assert H1.degree(weight="weight", order=3)[H1.nodes] == {
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