import pytest
import xgi
from xgi.exception import XGIError

def test_is_connected():
    edgelist1 = [[1,2,3],[4],[5,6],[6,7,8]]
    edgelist2 = [[1,2,3],[3,4],[4,5,6]]
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    assert xgi.is_connected(H1) == False
    assert xgi.is_connected(H2) == True

def test_connected_components():
    edgelist1 = [[1,2,3],[4],[5,6],[6,7,8]]
    edgelist2 = [[1,2],[3,4],[4,5,6]]
    edgelist3 = [[1,2,3],[2,3,4,5],[3,4,5]]
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)
    assert sorted([len(cc) for cc in xgi.connected_components(H1)]) == [1, 3, 4]
    assert {1,2,3} in xgi.connected_components(H1)
    assert {4} in xgi.connected_components(H1)
    assert {5,6,7,8} in xgi.connected_components(H1)
    assert sorted([len(cc) for cc in xgi.connected_components(H2)]) == [2, 4]
    assert {1,2} in xgi.connected_components(H2)
    assert {3,4,5,6} in xgi.connected_components(H2)
    assert sorted([len(cc) for cc in xgi.connected_components(H3)]) == [5]
    assert {1,2,3,4,5} in xgi.connected_components(H3)

def test_number_connected_components():
    edgelist1 = [[1,2,3],[4],[5,6],[6,7,8]]
    edgelist2 = [[1,2],[3,4],[4,5,6]]
    edgelist3 = [[1,2,3],[2,3,4,5],[3,4,5]]
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)
    assert xgi.number_connected_components(H1) == 3
    assert xgi.number_connected_components(H2) == 2
    assert xgi.number_connected_components(H3) == 1

def test_node_connected_components():
    edgelist1 = [[1,2,3],[4],[5,6],[6,7,8]]
    edgelist2 = [[1,2],[3,4],[4,5,6]]
    edgelist3 = [[1,2,3],[2,3,4,5],[3,4,5]]
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)
    assert xgi.node_connected_component(H1, 1) == {1,2,3}
    assert xgi.node_connected_component(H1, 4) == {4}
    assert xgi.node_connected_component(H1, 5) == {5,6,7,8}
    assert xgi.node_connected_component(H1, 8) == {5,6,7,8}
    assert xgi.node_connected_component(H2, 1) == {1,2}
    assert xgi.node_connected_component(H2, 3) == {3,4,5,6}
    assert xgi.node_connected_component(H2, 6) == {3,4,5,6}
    assert xgi.node_connected_component(H3, 1) == {1,2,3,4,5}
    assert xgi.node_connected_component(H3, 5) == {1,2,3,4,5}
    with pytest.raises(XGIError):
        xgi.node_connected_component(H3, 6)