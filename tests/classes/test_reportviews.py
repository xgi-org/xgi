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
