import pytest

import xgi
from xgi.exception import XGIError


def test_is_connected(edgelist1, edgelist3):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist3)
    assert xgi.is_connected(H1) is False
    assert xgi.is_connected(H2) is True


def test_connected_components(edgelist1, edgelist2, edgelist4):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist4)
    cc1 = list(xgi.connected_components(H1))
    cc2 = list(xgi.connected_components(H2))
    cc3 = list(xgi.connected_components(H3))
    assert sorted([len(cc) for cc in cc1]) == [1, 3, 4]
    assert {1, 2, 3} in cc1
    assert {4} in cc1
    assert {5, 6, 7, 8} in cc1
    assert sorted([len(cc) for cc in cc2]) == [2, 4]
    assert {1, 2} in cc2
    assert {3, 4, 5, 6} in cc2
    assert sorted([len(cc) for cc in cc3]) == [5]
    assert {1, 2, 3, 4, 5} in cc3


def test_number_connected_components(edgelist1, edgelist2, edgelist4):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist4)
    assert xgi.number_connected_components(H1) == 3
    assert xgi.number_connected_components(H2) == 2
    assert xgi.number_connected_components(H3) == 1


def test_largest_connected_component(edgelist1, edgelist2):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)

    lcc_1 = xgi.largest_connected_component(H1)
    lcc_2 = xgi.largest_connected_component(H2)

    assert lcc_1 == {5, 6, 7, 8}
    assert lcc_2 == {3, 4, 5, 6}


def test_node_connected_components(edgelist1, edgelist2, edgelist4):
    el1 = edgelist1
    el2 = edgelist2
    el4 = edgelist4
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    H3 = xgi.Hypergraph(el4)
    assert xgi.node_connected_component(H1, 1) == {1, 2, 3}
    assert xgi.node_connected_component(H1, 4) == {4}
    assert xgi.node_connected_component(H1, 5) == {5, 6, 7, 8}
    assert xgi.node_connected_component(H1, 8) == {5, 6, 7, 8}
    assert xgi.node_connected_component(H2, 1) == {1, 2}
    assert xgi.node_connected_component(H2, 3) == {3, 4, 5, 6}
    assert xgi.node_connected_component(H2, 6) == {3, 4, 5, 6}
    assert xgi.node_connected_component(H3, 1) == {1, 2, 3, 4, 5}
    assert xgi.node_connected_component(H3, 5) == {1, 2, 3, 4, 5}
    with pytest.raises(XGIError):
        xgi.node_connected_component(H3, 6)


def test_largest_connected_hypergraph(edgelist1, edgelist2):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)

    H1_lcc = xgi.largest_connected_hypergraph(H1)
    assert xgi.is_connected(H1_lcc)
    assert sorted(H1_lcc.nodes) == [5, 6, 7, 8]

    xgi.largest_connected_hypergraph(H2, in_place=True)
    assert xgi.is_connected(H2)
    assert sorted(H2.nodes) == [3, 4, 5, 6]
