import pytest
import xgi
from xgi.exception import XGIError


def test_degree_histogram(edgelist1, edgelist2, edgelist3):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)

    assert xgi.degree_histogram(H1) == [0, 7, 1]
    assert xgi.degree_histogram(H2) == [0, 5, 1]
    assert xgi.degree_histogram(H3) == [0, 4, 2]


def test_unique_edge_sizes(edgelist1, edgelist2, edgelist4, edgelist5):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist4)
    H4 = xgi.Hypergraph(edgelist5)

    assert xgi.unique_edge_sizes(H1) == [1, 2, 3]
    assert xgi.unique_edge_sizes(H2) == [2, 3]
    assert xgi.unique_edge_sizes(H3) == [3, 4]
    assert xgi.unique_edge_sizes(H4) == [1, 2, 3, 4]


def test_freeze(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    xgi.freeze(H)
    with pytest.raises(XGIError):
        H.add_node(10)

    with pytest.raises(XGIError):
        H.add_nodes_from([8, 9, 10])

    with pytest.raises(XGIError):
        H.add_node_to_edge(0, 10)

    with pytest.raises(XGIError):
        H.add_edge([1, 5, 7])

    with pytest.raises(XGIError):
        H.add_edges_from([[1, 7], [7]])

    with pytest.raises(XGIError):
        H.remove_node(1)

    with pytest.raises(XGIError):
        H.remove_nodes_from([1, 2, 3])

    with pytest.raises(XGIError):
        H.remove_edge(1)

    with pytest.raises(XGIError):
        H.remove_edges_from([0, 1])

    with pytest.raises(XGIError):
        H.remove_node_from_edge(0, 1)

    assert xgi.is_frozen(H)


def test_create_empty_copy(edgelist1):
    H = xgi.Hypergraph(edgelist1, name="test", timestamp="Nov. 20")
    attr_dict = {
        1: {"name": "Leonie"},
        2: {"name": "Ilya"},
        3: {"name": "Alice"},
        4: {"name": "Giovanni"},
        5: {"name": "Heather"},
        6: {"name": "Juan"},
        7: {"name": "Nicole"},
        8: {"name": "Sinan"},
    }
    xgi.set_node_attributes(H, attr_dict)

    E1 = xgi.create_empty_copy(H, with_data=False)
    E2 = xgi.create_empty_copy(H)

    assert E1.shape == (8, 0)
    for node in E1.nodes:
        assert len(E1.nodes.membership(node)) == 0
    assert E1.name == ""
    assert E1._hypergraph == {}

    assert E2.shape == (8, 0)
    for node in E2.nodes:
        assert len(E1.nodes.membership(node)) == 0
    assert E2._hypergraph == {"name": "test", "timestamp": "Nov. 20"}
    for n in H.nodes:
        assert H.nodes[n]["name"] == attr_dict[n]["name"]


def test_is_empty():
    H1 = xgi.Hypergraph()
    H2 = xgi.Hypergraph()
    H2.add_nodes_from([0, 1, 2])
    H3 = xgi.Hypergraph([[0, 1], [1, 2, 3]])
    assert xgi.is_empty(H1)
    assert xgi.is_empty(H2)
    assert not xgi.is_empty(H3)
