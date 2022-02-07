import pytest
import xgi
from xgi.exception import XGIError


def test_constructor(edgelist5, dict5, incidence5, dataframe5):
    H_list = xgi.Hypergraph(edgelist5)
    H_dict = xgi.Hypergraph(dict5)
    H_mat = xgi.Hypergraph(incidence5)
    H_df = xgi.Hypergraph(dataframe5)

    assert H_list.shape == H_dict.shape == H_mat.shape == H_df.shape
    assert (
        list(H_list.nodes)
        == list(H_dict.nodes)
        == list(H_mat.nodes)
        == list(H_df.nodes)
    )
    assert (
        list(H_list.edges)
        == list(H_dict.edges)
        == list(H_mat.edges)
        == list(H_df.edges)
    )
    assert (
        list(H_list.edges.members(0))
        == list(H_dict.edges.members(0))
        == list(H_mat.edges.members(0))
        == list(H_df.edges.members(0))
    )


def test_name():
    H = xgi.Hypergraph()
    assert H.name == ""
    H.name = "test"
    assert H.name == "test"
    H = xgi.Hypergraph(name="test")
    assert H.name == "test"


def test_contains(edgelist1):
    el1 = edgelist1
    H = xgi.Hypergraph(el1)
    unique_nodes = {node for edge in el1 for node in edge}
    for node in unique_nodes:
        assert node in H

    assert 0 not in H


def test_len(edgelist1, edgelist2):
    el1 = edgelist1
    el2 = edgelist2
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    assert len(H1) == 8
    assert len(H2) == 6


def test_shape(edgelist1, edgelist2):
    el1 = edgelist1
    el2 = edgelist2
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    assert H1.shape == (8, 4)
    assert H2.shape == (6, 3)


def test_neighbors(edgelist1, edgelist2):
    el1 = edgelist1
    el2 = edgelist2
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    assert H1.neighbors(1) == {2, 3}
    assert H1.neighbors(4) == set()
    assert H1.neighbors(6) == {5, 7, 8}
    assert H2.neighbors(4) == {3, 5, 6}
    assert H2.neighbors(1) == {2}


def test_dual(edgelist1, edgelist2, edgelist4):
    el1 = edgelist1
    el2 = edgelist2
    el4 = edgelist4
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    H3 = xgi.Hypergraph(el4)

    D1 = H1.dual()
    D2 = H2.dual()
    D3 = H3.dual()
    assert D1.shape == (4, 8)
    assert D2.shape == (3, 6)
    assert D3.shape == (3, 5)


def test_max_edge_order(edgelist1, edgelist4, edgelist5):
    H0 = xgi.empty_hypergraph()
    H1 = xgi.empty_hypergraph()
    H1.add_nodes_from(range(5))
    H2 = xgi.Hypergraph(edgelist1)
    H3 = xgi.Hypergraph(edgelist4)
    H4 = xgi.Hypergraph(edgelist5)

    assert H0.max_edge_order() == None
    assert H1.max_edge_order() == 0
    assert H2.max_edge_order() == 2
    assert H3.max_edge_order() == 3
    assert H4.max_edge_order() == 3


def test_is_possible_order(edgelist1):
    H1 = xgi.Hypergraph(edgelist1)

    assert H1.is_possible_order(-1) == False
    assert H1.is_possible_order(0) == False
    assert H1.is_possible_order(1) == True
    assert H1.is_possible_order(2) == True
    assert H1.is_possible_order(3) == False


def test_singleton_edges(edgelist1, edgelist2):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)

    assert H1.singleton_edges() == {1: [4]}
    assert H2.singleton_edges() == {}


def test_remove_singleton_edges(edgelist1, edgelist2):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)

    H1.remove_singleton_edges()
    H2.remove_singleton_edges()

    assert H1.singleton_edges() == {}
    assert H2.singleton_edges() == {}


def test_is_uniform(edgelist1, edgelist6, edgelist7):
    H0 = xgi.Hypergraph(edgelist1)
    H1 = xgi.Hypergraph(edgelist6)
    H2 = xgi.Hypergraph(edgelist7)
    H3 = xgi.empty_hypergraph()

    assert H0.is_uniform() == False
    assert H1.is_uniform() == 2
    assert H2.is_uniform() == 2
    assert H3.is_uniform() == False


def test_isolates(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert H.isolates(ignore_singletons=False) == set()
    assert H.isolates() == {4}
    H.remove_isolates()
    assert 4 not in H


def test_add_node_attr(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert "new_node" not in H
    H.add_node("new_node", color="red")
    assert "new_node" in H
    assert "color" in H.nodes["new_node"]
    assert H.nodes["new_node"]["color"] == "red"


def test_hypergraph_attr(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    with pytest.raises(XGIError):
        H["color"]
    H["color"] = "red"
    assert H["color"] == "red"


def test_members(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert H.nodes.members(1) == H.nodes.memberships(1) == [0]
    assert H.nodes.members(2) == H.nodes.memberships(2) == [0]
    assert H.nodes.members(3) == H.nodes.memberships(3) == [0]
    assert H.nodes.members(4) == H.nodes.memberships(4) == [1]
    assert H.nodes.members(6) == H.nodes.memberships(6) == [2, 3]
