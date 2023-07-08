import pytest

import xgi
from xgi.exception import XGIError


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

    with pytest.warns(Warning):
        xgi.set_node_attributes(H4, {"test": "blue"}, "color")

    with pytest.warns(Warning):
        xgi.set_node_attributes(H4, {"test": {"blue": "color"}})


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
    xgi.set_edge_attributes(H2, "blue", name="color")

    for e in H2.edges:
        assert H2.edges[e]["color"] == "blue"

    H3 = xgi.Hypergraph(edgelist1)

    with pytest.warns(Warning), pytest.raises(XGIError):
        xgi.set_node_attributes(H3, attr_dict2)

    with pytest.raises(XGIError):
        xgi.set_edge_attributes(H3, 2)

    with pytest.warns(Warning):
        xgi.set_edge_attributes(H3, {"test": 2}, "weight")

    with pytest.warns(Warning):
        xgi.set_edge_attributes(H3, {"test": {2: "weight"}})


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


def test_convert_labels_to_integers(hypergraph1, hypergraph2):
    H1 = xgi.convert_labels_to_integers(hypergraph1)
    H2 = xgi.convert_labels_to_integers(hypergraph2)
    H3 = xgi.convert_labels_to_integers(hypergraph1, "old_ids")

    assert set(H1.nodes) == {0, 1, 2}
    assert set(H1.edges) == {0, 1, 2}

    assert H1.nodes[0]["label"] == "a"
    assert H1.nodes[1]["label"] == "b"
    assert H1.nodes[2]["label"] == "c"

    assert H1.edges[0]["label"] == "e1"
    assert H1.edges[1]["label"] == "e2"
    assert H1.edges[2]["label"] == "e3"

    assert H1.edges.members(0) == {0, 1}
    assert H1.edges.members(1) == {0, 1, 2}
    assert H1.edges.members(2) == {2}

    assert H1.nodes.memberships(0) == {0, 1}
    assert H1.nodes.memberships(1) == {0, 1}
    assert H1.nodes.memberships(2) == {1, 2}

    assert set(H2.nodes) == {0, 1, 2}
    assert set(H2.edges) == {0, 1, 2}

    assert H2.nodes[0]["label"] == "b"
    assert H2.nodes[1]["label"] == "c"
    assert H2.nodes[2]["label"] == 0

    assert H2.edges[0]["label"] == "e1"
    assert H2.edges[1]["label"] == "e2"
    assert H2.edges[2]["label"] == "e3"

    assert H2.edges.members(0) == {0, 2}
    assert H2.edges.members(1) == {1, 2}
    assert H2.edges.members(2) == {0, 1, 2}

    assert H2.nodes.memberships(0) == {0, 2}
    assert H2.nodes.memberships(1) == {1, 2}
    assert H2.nodes.memberships(2) == {0, 1, 2}

    assert H3.nodes[0]["old_ids"] == "a"
    assert H3.edges[0]["old_ids"] == "e1"