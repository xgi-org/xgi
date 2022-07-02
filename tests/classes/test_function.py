import pytest

import xgi
from xgi.exception import IDNotFound, XGIError


def test_max_edge_order(edgelist1, edgelist4, edgelist5):
    H0 = xgi.empty_hypergraph()
    H1 = xgi.empty_hypergraph()
    H1.add_nodes_from(range(5))
    H2 = xgi.Hypergraph(edgelist1)
    H3 = xgi.Hypergraph(edgelist4)
    H4 = xgi.Hypergraph(edgelist5)

    assert xgi.max_edge_order(H0) == None
    assert xgi.max_edge_order(H1) == 0
    assert xgi.max_edge_order(H2) == 2
    assert xgi.max_edge_order(H3) == 3
    assert xgi.max_edge_order(H4) == 3


def test_is_possible_order(edgelist1):
    H1 = xgi.Hypergraph(edgelist1)

    assert xgi.is_possible_order(H1, -1) == False
    assert xgi.is_possible_order(H1, 0) == False
    assert xgi.is_possible_order(H1, 1) == True
    assert xgi.is_possible_order(H1, 2) == True
    assert xgi.is_possible_order(H1, 3) == False


def test_is_uniform(edgelist1, edgelist6, edgelist7):
    H0 = xgi.Hypergraph(edgelist1)
    H1 = xgi.Hypergraph(edgelist6)
    H2 = xgi.Hypergraph(edgelist7)
    H3 = xgi.empty_hypergraph()

    assert xgi.is_uniform(H0) == False
    assert xgi.is_uniform(H1) == 2
    assert xgi.is_uniform(H2) == 2
    assert xgi.is_uniform(H3) == False


def test_edge_neighborhood(edgelist3):
    H = xgi.Hypergraph(edgelist3)
    assert H.nodes.neighbors(3) == {1, 2, 4}
    assert xgi.edge_neighborhood(H, 3) == [[1, 2], [4]]
    assert xgi.edge_neighborhood(H, 3, include_self=True) == [[1, 2, 3], [3, 4]]
    with pytest.raises(IDNotFound):
        xgi.edge_neighborhood(H, 7)


def test_degree_counts(edgelist1, edgelist2, edgelist3):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)

    assert xgi.degree_counts(H1) == [0, 7, 1]
    assert xgi.degree_counts(H2) == [0, 5, 1]
    assert xgi.degree_counts(H3) == [0, 4, 2]


def test_degree_histogram(edgelist1, edgelist2, edgelist3):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)

    assert xgi.degree_histogram(H1) == ([1, 2], [7, 1])
    assert xgi.degree_histogram(H2) == ([1, 2], [5, 1])
    assert xgi.degree_histogram(H3) == ([1, 2], [4, 2])


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

    assert (E1.num_nodes, E1.num_edges) == (8, 0)
    for node in E1.nodes:
        assert len(E1.nodes.memberships(node)) == 0
    assert E1._hypergraph == {}

    assert (E2.num_nodes, E2.num_edges) == (8, 0)
    for node in E2.nodes:
        assert len(E1.nodes.memberships(node)) == 0
    assert E2["name"] == "test"
    assert E2["timestamp"] == "Nov. 20"
    with pytest.raises(XGIError):
        author = E2["author"]
    for n in E2.nodes:
        assert E2.nodes[n]["name"] == attr_dict[n]["name"]


def test_set_node_attributes(edgelist1):
    attr_dict1 = {
        1: {"name": "Leonie"},
        2: {"name": "Ilya"},
        3: {"name": "Alice"},
        4: {"name": "Giovanni"},
        5: {"name": "Heather"},
        6: {"name": "Juan"},
        7: {"name": "Nicole"},
        8: {"name": "Sinan"},
    }

    attr_dict2 = {
        1: "Leonie",
        2: "Ilya",
        3: "Alice",
        4: "Giovanni",
        5: "Heather",
        6: "Juan",
        7: "Nicole",
        8: "Sinan",
    }

    H1 = xgi.Hypergraph(edgelist1)
    xgi.set_node_attributes(H1, attr_dict1)

    for n in H1.nodes:
        assert H1.nodes[n]["name"] == attr_dict1[n]["name"]

    H2 = xgi.Hypergraph(edgelist1)
    xgi.set_node_attributes(H2, attr_dict2, name="name")

    for n in H2.nodes:
        assert H2.nodes[n]["name"] == attr_dict2[n]

    H3 = xgi.Hypergraph(edgelist1)
    xgi.set_node_attributes(H3, 2, name="weight")

    for n in H3.nodes:
        assert H3.nodes[n]["weight"] == 2

    H4 = xgi.Hypergraph(edgelist1)

    with pytest.raises(XGIError):
        xgi.set_node_attributes(H4, attr_dict2)

    with pytest.raises(XGIError):
        xgi.set_node_attributes(H4, 2)


def test_get_node_attributes(edgelist1):
    H1 = xgi.Hypergraph(edgelist1)
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
    xgi.set_node_attributes(H1, attr_dict)

    assert xgi.get_node_attributes(H1) == attr_dict

    assert xgi.get_node_attributes(H1, "name") == {
        id: data["name"] for id, data in attr_dict.items()
    }
    assert xgi.get_node_attributes(H1, "weight") == dict()


def test_set_edge_attributes(edgelist1):
    H1 = xgi.Hypergraph(edgelist1)
    attr_dict1 = {
        0: {"weight": 1},
        1: {"weight": 2},
        2: {"weight": 3.0},
        3: {"weight": -1},
    }

    attr_dict2 = {0: 1, 1: 2, 2: 3, 3: -1}
    xgi.set_edge_attributes(H1, attr_dict1)

    for e in H1.edges:
        assert H1.edges[e]["weight"] == attr_dict1[e]["weight"]

    H2 = xgi.Hypergraph(edgelist1)
    xgi.set_node_attributes(H2, "blue", name="color")

    for n in H2.nodes:
        assert H2.nodes[n]["color"] == "blue"

    H3 = xgi.Hypergraph(edgelist1)

    with pytest.raises(XGIError):
        xgi.set_node_attributes(H3, attr_dict2)

    with pytest.raises(XGIError):
        xgi.set_edge_attributes(H3, 2)


def test_get_edge_attributes(edgelist1):
    H1 = xgi.Hypergraph(edgelist1)
    attr_dict = {
        0: {"weight": 1},
        1: {"weight": 2},
        2: {"weight": 3},
        3: {"weight": -1},
    }

    xgi.set_edge_attributes(H1, attr_dict)

    assert xgi.get_edge_attributes(H1) == attr_dict

    assert xgi.get_edge_attributes(H1, "weight") == {
        id: data["weight"] for id, data in attr_dict.items()
    }
    assert xgi.get_node_attributes(H1, "name") == dict()


def test_is_empty():
    H1 = xgi.Hypergraph()
    H2 = xgi.Hypergraph()
    H2.add_nodes_from([0, 1, 2])
    H3 = xgi.Hypergraph([[0, 1], [1, 2, 3]])
    assert xgi.is_empty(H1)
    assert xgi.is_empty(H2)
    assert not xgi.is_empty(H3)
