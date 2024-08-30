import pickle
import tempfile

import pytest

import xgi
from xgi.exception import IDNotFound, XGIError
from xgi.utils import dual_dict


def test_constructor(edgelist5, dict5, incidence5, dataframe5):
    H_list = xgi.Hypergraph(edgelist5)
    H_dict = xgi.Hypergraph(dict5)
    H_mat = xgi.Hypergraph(incidence5)
    H_df = xgi.Hypergraph(dataframe5)
    H_hg = xgi.Hypergraph(H_list)

    assert (
        set(H_list.nodes)
        == set(H_dict.nodes)
        == set(H_mat.nodes)
        == set(H_df.nodes)
        == set(H_hg.nodes)
    )
    assert (
        set(H_list.edges)
        == set(H_dict.edges)
        == set(H_mat.edges)
        == set(H_df.edges)
        == set(H_hg.edges)
    )
    assert (
        H_list.edges.members(0)
        == H_dict.edges.members(0)
        == H_mat.edges.members(0)
        == H_df.edges.members(0)
        == H_hg.edges.members(0)
    )

    with pytest.raises(XGIError):
        xgi.Hypergraph(1)

    SC = xgi.SimplicialComplex(edgelist5)
    H_sc = xgi.Hypergraph(SC)

    assert set(H_sc.nodes) == set(SC.nodes)
    assert H_sc.edges.members() == SC.edges.members()


def test_hypergraph_attrs():
    H = xgi.Hypergraph()
    assert H._net_attr == {}
    with pytest.raises(XGIError):
        H["name"]
    H = xgi.Hypergraph(name="test")
    assert H["name"] == "test"


def test_contains(edgelist1):
    el1 = edgelist1
    H = xgi.Hypergraph(el1)
    unique_nodes = {node for edge in el1 for node in edge}
    for node in unique_nodes:
        assert node in H

    # test TypeError handling
    assert [1, 2, 3] not in H


def test_lshift(edgelist1, edgelist2, hyperwithattrs):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = hyperwithattrs
    H = H1 << H2
    nodes1 = list(H1.nodes)
    assert nodes1 == [1, 2, 3, 4, 5, 6, 8, 7]
    assert list(H.nodes) == nodes1
    assert H.num_edges == 7
    assert H.edges.members(0) == {1, 2, 3}

    H = H1 << H2 << H3
    assert set(H.nodes) == {1, 2, 3, 4, 5, 6, 7, 8}
    assert H.num_edges == 10
    assert H.nodes[1] == {"color": "red", "name": "horse"}
    assert H.edges.members(7) == {1, 2, 3}


def test_string():
    H1 = xgi.Hypergraph()
    assert str(H1) == "Unnamed Hypergraph with 0 nodes and 0 hyperedges"
    H2 = xgi.Hypergraph(name="test")
    assert str(H2) == "Hypergraph named test with 0 nodes and 0 hyperedges"


def test_len(edgelist1, edgelist2):
    el1 = edgelist1
    el2 = edgelist2
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    assert len(H1) == 8
    assert len(H2) == 6


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
    assert (D1.num_nodes, D1.num_edges) == (4, 8)
    assert (D2.num_nodes, D2.num_edges) == (3, 6)
    assert (D3.num_nodes, D3.num_edges) == (3, 5)


def test_add_nodes_from(attr1, attr2, attr3):
    H = xgi.Hypergraph()
    H.add_nodes_from(range(3), **attr1)
    assert H.nodes[0]["color"] == attr1["color"]
    assert H.nodes[1]["color"] == attr1["color"]
    assert H.nodes[2]["color"] == attr1["color"]

    H = xgi.Hypergraph()
    H.add_nodes_from(zip(range(3), [attr1, attr2, attr3]))
    assert H.nodes[0]["color"] == attr1["color"]
    assert H.nodes[1]["color"] == attr2["color"]
    assert H.nodes[2]["color"] == attr3["color"]


def test_remove_singleton_edges(edgelist1, edgelist2):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)

    H1.remove_edges_from(H1.edges.singletons())
    H2.remove_edges_from(H2.edges.singletons())

    assert list(H1.edges.singletons()) == []
    assert list(H2.edges.singletons()) == []


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


def test_memberships(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert H.nodes.memberships(1) == {0}
    assert H.nodes.memberships(2) == {0}
    assert H.nodes.memberships(3) == {0}
    assert H.nodes.memberships(4) == {1}
    assert H.nodes.memberships(6) == {2, 3}
    assert H.nodes([1, 2, 6]).memberships() == {1: {0}, 2: {0}, 6: {2, 3}}
    with pytest.raises(IDNotFound):
        H.nodes.memberships(0)


def test_add_edge():
    for edge in [[1, 2, 3], {1, 2, 3}, iter([1, 2, 3])]:
        H = xgi.Hypergraph()
        H.add_edge(edge)
        assert (1 in H) and (2 in H) and (3 in H)
        assert 0 in H.edges
        assert {1, 2, 3} in H.edges.members()
        assert {1, 2, 3} == H.edges.members(0)
        assert H.edges.members(dtype=dict) == {0: {1, 2, 3}}

    # test adding empty edges
    H = xgi.Hypergraph()
    for edge in [[], set(), iter([])]:
        H.add_edge(edge)

    assert H.edges.size.asdict() == {0: 0, 1: 0, 2: 0}

    # check that uid works correctly
    H1 = xgi.Hypergraph()
    H1.add_edge([1, 2], id=0)
    H1.add_edge([3, 4], id=2)
    H1.add_edge([5, 6])
    assert H1._edge == {0: {1, 2}, 2: {3, 4}, 3: {5, 6}}

    H2 = xgi.Hypergraph()
    H2.add_edge([1, 2])
    H2.add_edge([3, 4])
    with pytest.warns(
        UserWarning, match="uid 0 already exists, cannot add edge {5, 6}"
    ):
        H2.add_edge([5, 6], id=0)

    assert H2._edge == {0: {1, 2}, 1: {3, 4}}


def test_add_edge_with_id():
    H = xgi.Hypergraph()
    H.add_edge([1, 2, 3], id="myedge")
    assert (1 in H) and (2 in H) and (3 in H)
    assert "myedge" in H.edges
    assert {1, 2, 3} in H.edges.members()
    assert {1, 2, 3} == H.edges.members("myedge")
    assert H.edges.members(dtype=dict) == {"myedge": {1, 2, 3}}


def test_add_edge_with_attr():
    H = xgi.Hypergraph()
    H.add_edge([1, 2, 3], color="red", place="peru")
    assert (1 in H) and (2 in H) and (3 in H)
    assert 0 in H.edges
    assert {1, 2, 3} in H.edges.members()
    assert {1, 2, 3} == H.edges.members(0)
    assert H.edges.members(dtype=dict) == {0: {1, 2, 3}}
    assert H.edges[0] == {"color": "red", "place": "peru"}


def test_add_node_to_edge():
    H = xgi.Hypergraph()
    H.add_edge(["apple", "banana"], "fruits")
    H.add_node_to_edge("fruits", "pear")
    H.add_node_to_edge("veggies", "lettuce")
    assert H.edges.members(dtype=dict) == {
        "fruits": {"apple", "banana", "pear"},
        "veggies": {"lettuce"},
    }


def test_remove_node_from_edge(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    # test non-existent node
    with pytest.raises(XGIError):
        H.remove_node_from_edge(1, 1000)

    # test non-existent edge
    with pytest.raises(XGIError):
        H.remove_node_from_edge(1000, 1)

    # test node which exists, but not in the edge
    with pytest.raises(XGIError):
        H.remove_node_from_edge(1, 1)

    H.remove_node_from_edge(0, 1)
    assert 1 not in H.edges.members(0)

    with pytest.raises(XGIError):
        H.remove_node_from_edge(0, 1)

    H.remove_node_from_edge(0, 2)
    H.remove_node_from_edge(0, 3)

    assert 0 not in H.edges

    # test leaving empty edges
    H = xgi.Hypergraph(edgelist1)
    H.remove_node_from_edge(0, 1)
    H.remove_node_from_edge(0, 2)
    H.remove_node_from_edge(0, 3, remove_empty=False)
    assert 0 in H.edges
    assert H.edges.members(0) == set()


def test_add_edges_from_iterable_of_members():
    edges = [{0, 1}, {1, 2}, {2, 3, 4}]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert H.edges.members() == edges

    H1 = xgi.Hypergraph(edges)
    with pytest.raises(XGIError):
        xgi.Hypergraph(H1.edges)

    edges = {frozenset([0, 1]), frozenset([1, 2]), frozenset([2, 3, 4])}
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert H.edges.members() == [set(e) for e in edges]

    edges = [[0, 1], {1, 2}, (2, 3, 4)]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert H.edges.members() == [set(e) for e in edges]

    edges = [{"foo", "bar"}, {"bar", "baz"}, {"foo", "bar", "baz"}]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert set(H.nodes) == {"foo", "bar", "baz"}
    assert H.edges.members() == edges

    edges = [{"a", "b"}, {"b", "c"}, {"c", "d", "e"}]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert set(H.nodes) == {"a", "b", "c", "d", "e"}
    assert H.edges.members() == edges


def test_add_edges_from_format2():
    edges = [({0, 1}, 0), ({1, 2}, 1), ({2, 3, 4}, 2)]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members(dtype=dict) == {e[1]: e[0] for e in edges}

    edges = [({0, 1}, "a"), ({1, 2}, "b"), ({2, 3, 4}, "foo")]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members(dtype=dict) == {e[1]: e[0] for e in edges}

    edges = [({0, 1}, "a"), ({1, 2}, "b"), ({2, 3, 4}, 100)]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members(dtype=dict) == {e[1]: e[0] for e in edges}

    # check counter
    H.add_edge([1, 9, 2])
    assert H.edges.members(101) == {1, 9, 2}

    H1 = xgi.Hypergraph([{1, 2}, {2, 3, 4}])
    with pytest.warns(
        UserWarning, match="uid 0 already exists, cannot add edge {1, 3}."
    ):
        H1.add_edges_from([({1, 3}, 0)])
    assert H1._edge == {0: {1, 2}, 1: {2, 3, 4}}


def test_add_edges_from_format3():
    edges = [
        ({0, 1}, {"color": "red"}),
        ({1, 2}, {"age": 30}),
        ({2, 3, 4}, {"color": "blue", "age": 40}),
    ]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == list(range(len(edges)))
    assert H.edges.members() == [e[0] for e in edges]
    for idx, e in enumerate(H.edges):
        assert H.edges[e] == edges[idx][1]
    # check counter
    H.add_edge([1, 9, 2])
    assert H.edges.members(3) == {1, 9, 2}


def test_add_edges_from_format4():
    edges = [
        ({0, 1}, "one", {"color": "red"}),
        ({1, 2}, "two", {"age": 30}),
        ({2, 3, 4}, "three", {"color": "blue", "age": 40}),
    ]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members() == [e[0] for e in edges]
    for idx, e in enumerate(H.edges):
        assert H.edges[e] == edges[idx][2]
    # check counter
    H.add_edge([1, 9, 2])
    assert H.edges.members(0) == {1, 9, 2}

    H1 = xgi.Hypergraph([{1, 2}, {2, 3, 4}])
    with pytest.warns(
        UserWarning, match="uid 0 already exists, cannot add edge {0, 1}."
    ):
        H1.add_edges_from([({0, 1}, 0, {"color": "red"})])
    assert H1._edge == {0: {1, 2}, 1: {2, 3, 4}}


def test_add_edges_from_dict():
    edges = {"one": [0, 1], "two": [1, 2], 2: [2, 3, 4]}
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == ["one", "two", 2]
    assert H.edges.members() == [set(edges[e]) for e in edges]
    # check counter
    H.add_edge([1, 9, 2])
    assert H.edges.members(3) == {1, 9, 2}

    H1 = xgi.Hypergraph([{1, 2}, {2, 3, 4}])
    with pytest.warns(
        UserWarning, match="uid 0 already exists, cannot add edge {1, 3}."
    ):
        H1.add_edges_from({0: {1, 3}})
    assert H1._edge == {0: {1, 2}, 1: {2, 3, 4}}


def test_add_edges_from_attr_precedence():
    H = xgi.Hypergraph()
    edges = [
        ([0, 1], "one", {"color": "red"}),
        ([1, 2], "two", {"age": 30}),
        ([2, 3, 4], "three", {"color": "blue", "age": 40}),
    ]
    H.add_edges_from(edges, color="black")
    assert H.edges["one"] == {"color": "red"}
    assert H.edges["two"] == {"age": 30, "color": "black"}
    assert H.edges["three"] == {"age": 40, "color": "blue"}


def test_add_edges_from_wrong_format():
    edges = [0, 1, 2]
    with pytest.raises(XGIError):
        xgi.Hypergraph().add_edges_from(edges)

    edges = [
        ("foo", {"color": "red"}),
        ("bar", {"age": 30}),
        ("baz", {"color": "blue", "age": 40}),
    ]

    with pytest.raises(XGIError):
        xgi.Hypergraph().add_edges_from(edges)

    edges = [
        ("foo", "one", {"color": "red"}),
        ("bar", "two", {"age": 30}),
        ("baz", "three", {"color": "blue", "age": 40}),
    ]
    with pytest.raises(XGIError):
        xgi.Hypergraph().add_edges_from(edges)

    edges = ["a", "b", "c"]
    with pytest.raises(XGIError):
        xgi.Hypergraph().add_edges_from(edges)

    edges = ["foo", "bar", "baz"]
    with pytest.raises(XGIError):
        xgi.Hypergraph().add_edges_from(edges)

    edges = ["foo", [1, 2], [2, 3, 4]]
    with pytest.raises(XGIError):
        xgi.Hypergraph().add_edges_from(edges)


def test_copy(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    H["key"] = "value"
    copy = H.copy()
    assert list(copy.nodes) == list(H.nodes)
    assert list(copy.edges) == list(H.edges)
    assert list(copy.edges.members()) == list(H.edges.members())
    assert H._net_attr == copy._net_attr

    H.add_node(10)
    assert list(copy.nodes) != list(H.nodes)
    assert list(copy.edges) == list(H.edges)

    H.add_edge([1, 3, 5])
    assert list(copy.edges) != list(H.edges)

    H["key2"] = "value2"
    assert H._net_attr != copy._net_attr

    copy.add_node(10)
    copy.add_edge([1, 3, 5])
    copy["key2"] = "value2"
    assert list(copy.nodes) == list(H.nodes)
    assert list(copy.edges) == list(H.edges)
    assert list(copy.edges.members()) == list(H.edges.members())
    assert H._net_attr == copy._net_attr

    H1 = xgi.Hypergraph()
    H1.add_edge((1, 2), id="x")
    copy2 = H1.copy()  # does not throw error because of str id
    assert list(copy2.nodes) == list(H1.nodes)
    assert list(copy2.edges) == list(H1.edges)
    assert list(copy2.edges.members()) == list(H1.edges.members())
    assert H1._net_attr == copy2._net_attr


def test_copy_issue128():
    # see https://github.com/xgi-org/xgi/issues/128
    H = xgi.Hypergraph()
    H["key"] = "value"
    K = H.copy()
    K["key"] = "some_other_value"
    assert H["key"] == "value"


def test_double_edge_swap(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    with pytest.raises(XGIError):
        H.double_edge_swap(5, 6, 2, 3)

    H.double_edge_swap(1, 6, 0, 3)
    assert H.edges.members() == [{2, 3, 6}, {4}, {5, 6}, {1, 7, 8}]

    assert H._edge == dual_dict(H._node)

    H.double_edge_swap(3, 4, 0, 1)
    assert H.edges.members() == [{2, 4, 6}, {3}, {5, 6}, {1, 7, 8}]
    assert H._edge == dual_dict(H._node)

    with pytest.raises(IDNotFound):
        H.double_edge_swap(10, 3, 0, 1)

    with pytest.raises(IDNotFound):
        H.double_edge_swap(8, 3, 0, 1)

    H = xgi.Hypergraph(edgelist1)
    with pytest.raises(XGIError):
        H.double_edge_swap(6, 7, 2, 3)


def test_random_edge_shuffle(edgelist4):
    # trivial hypergraph
    H0 = xgi.trivial_hypergraph()
    with pytest.raises(ValueError):
        H0.random_edge_shuffle()

    # hypergraph with only two edges
    S = xgi.Hypergraph([[0, 1, 2, 3], [2, 3, 5, 6, 8]])
    H = S.copy()
    H.random_edge_shuffle()

    # the intersection of the two edges is preserved
    assert {2, 3}.issubset(H._edge[0])
    assert {2, 3}.issubset(H._edge[1])

    # edge sizes are preserved
    assert len(H._edge[0]) == len(S._edge[0])
    assert len(H._edge[1]) == len(S._edge[1])

    # verify dual of edge dict is nodes dict
    assert xgi.utilities.dual_dict(H._edge) == H._node

    # hypergraph with more than two edges
    S = xgi.Hypergraph(edgelist4)
    H = S.copy()

    # specify edges to shuffle
    H.random_edge_shuffle(e_id1=0, e_id2=1)

    # not shuffled edges are preserved
    assert H._edge[2] == S._edge[2]

    # the intersection of the two edges is preserved
    assert {2, 3}.issubset(H._edge[0])
    assert {2, 3}.issubset(H._edge[1])

    # edge sizes are preserved
    for edge_id in H._edge:
        assert len(H._edge[edge_id]) == len(S._edge[edge_id])

    # verify dual of edge dict is nodes dict
    assert xgi.utilities.dual_dict(H._edge) == H._node

    # random hypergraph
    S = xgi.random_hypergraph(50, [0.1, 0.01, 0.001], seed=1)
    H = S.copy()
    H.random_edge_shuffle()

    # number of nodes and edges are preserved
    assert H.num_nodes == S.num_nodes
    assert H.num_edges == S.num_edges

    # all edge sizes are preserved
    for edge_id in H._edge:
        assert len(H._edge[edge_id]) == len(S._edge[edge_id])

    # all node degrees are preserved
    for node_id in H._node:
        assert len(H._node[node_id]) == len(S._node[node_id])

    # verify dual of edge dict is nodes dict
    assert xgi.utilities.dual_dict(H._edge) == H._node


def test_duplicate_edges(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert list(H.edges.duplicates()) == []

    H.add_edge([1, 3, 2])  # same order as existing edge
    assert set(H.edges.duplicates()) == {4}

    H.add_edge([1, 2, 3])  # different order, same members
    assert set(H.edges.duplicates()) == {4, 5}

    H = xgi.Hypergraph([[1, 2, 3, 3], [1, 2, 3]])  # repeated nodes
    assert set(H.edges.duplicates()) == {1}

    H = xgi.Hypergraph([[1, 2, 3, 3], [3, 1, 2, 3]])  # repeated nodes
    assert set(H.edges.duplicates()) == {1}


def test_duplicate_nodes(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert set(H.nodes.duplicates()) == {2, 3, 8}

    H.add_edges_from([[1, 4], [2, 6, 7], [6, 8]])
    assert set(H.nodes.duplicates()) == set()

    # this loop makes 1 and 2 belong to the same edges
    for edgeid, members in H.edges.members(dtype=dict).items():
        if 1 in members and 2 not in members:
            H.add_node_to_edge(edgeid, 2)
        if 1 not in members and 2 in members:
            H.add_node_to_edge(edgeid, 1)
    assert set(H.nodes.duplicates()) == {2}


def test_remove_node_weak(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert 1 in H
    H.remove_node(1)
    assert 1 not in H
    with pytest.raises(IDNotFound):
        H.remove_node(10)

    # test keeping empty edges
    H = xgi.Hypergraph(edgelist1)
    H.remove_node(1)
    H.remove_node(2)
    H.remove_node(3, remove_empty=False)
    H.remove_node(4, remove_empty=False)
    assert 0 in H.edges and 1 in H.edges
    assert H.edges.size[0] == 0 and H.edges.size[1] == 0


def test_remove_node_strong(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert 1 in H
    H.remove_node(1, strong=True)
    assert 1 not in H
    assert 0 not in H.edges


def test_remove_nodes_from(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    H.remove_nodes_from([1, 2, 3])
    assert 1 not in H and 2 not in H and 3 not in H
    assert 0 not in H.edges

    with pytest.warns(Warning):
        H.remove_nodes_from([1, 2, 3])

    H = xgi.Hypergraph(edgelist1)

    H.remove_nodes_from([1, 4], strong=True)
    assert 0 not in H.edges and 1 not in H.edges

    H = xgi.Hypergraph(edgelist1)
    H.remove_nodes_from([1, 2, 3, 4], remove_empty=False)
    assert 0 in H.edges and 1 in H.edges
    assert H.edges.size[0] == 0 and H.edges.size[1] == 0


def test_issue_445(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert 1 in H
    H.remove_node(1, strong=True)
    assert 1 not in H
    assert 0 not in H.edges
    assert H._edge == xgi.dual_dict(H._node)

    H = xgi.Hypergraph([[1, 2, 3], [1, 2]])
    H.remove_node(1, strong=True)
    assert H._edge == xgi.dual_dict(H._node)


def test_clear_edges(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    H.clear_edges()
    assert len(H.edges) == 0


def test_merge_duplicate_edges(hyperwithdupsandattrs):
    H = hyperwithdupsandattrs.copy()
    H.merge_duplicate_edges()
    assert H.num_edges == 2
    assert set(H.edges) == {0, 3}
    assert H.edges[0] == {"color": "blue"}
    assert H.edges[3] == {"color": "purple"}

    H = hyperwithdupsandattrs.copy()
    H.merge_duplicate_edges(rename="tuple")
    assert set(H.edges) == {(0, 1, 2), (3, 4)}
    assert H.edges.members((0, 1, 2)) == {1, 2}
    assert H.edges.members((3, 4)) == {3, 4, 5}

    H = hyperwithdupsandattrs.copy()
    H.merge_duplicate_edges(rename="new")
    assert set(H.edges) == {5, 6}
    assert H.edges.members(5) == {1, 2}
    assert H.edges.members(6) == {3, 4, 5}

    H = hyperwithdupsandattrs.copy()
    with pytest.warns(
        UserWarning,
        match="You will not be able to color/draw by merged attributes with xgi.draw()",
    ):
        H.merge_duplicate_edges(merge_rule="union", multiplicity="mult")
    assert H.edges[0] == {
        "color": {"blue", "red", "yellow"},
        "weight": {2, None},
        "mult": 3,
    }
    assert H.edges[3] == {"color": {"purple"}, "name": {"test", None}, "mult": 2}

    H = hyperwithdupsandattrs.copy()
    H.merge_duplicate_edges(merge_rule="intersection", multiplicity="multiplicity")
    assert H.edges[0] == {"color": None, "weight": None, "multiplicity": 3}
    assert H.edges[3] == {"color": "purple", "name": None, "multiplicity": 2}
    assert H.edges.attrs("multiplicity").asdict() == {0: 3, 3: 2}


def test_issue_198(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    H.clear_edges()
    assert len(H.edges) == 0

    # this used to fail
    H.add_edge({1, 2, 3})


def test_pickle(edgelist1):
    _, filename = tempfile.mkstemp()
    H1 = xgi.Hypergraph(edgelist1)

    with open(filename, "wb") as file:
        pickle.dump(H1, file)
    with open(filename, "rb") as file:
        H2 = pickle.load(file)

    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges
    assert [H1.edges.members(id) for id in H1.edges] == [
        H2.edges.members(id) for id in H2.edges
    ]


def test_freeze(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    H.freeze()
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

    assert H.is_frozen


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
    H1.set_node_attributes(attr_dict1)

    for n in H1.nodes:
        assert H1.nodes[n]["name"] == attr_dict1[n]["name"]

    H2 = xgi.Hypergraph(edgelist1)
    H2.set_node_attributes(attr_dict2, name="name")

    for n in H2.nodes:
        assert H2.nodes[n]["name"] == attr_dict2[n]

    H3 = xgi.Hypergraph(edgelist1)
    H3.set_node_attributes(2, name="weight")

    for n in H3.nodes:
        assert H3.nodes[n]["weight"] == 2

    H4 = xgi.Hypergraph(edgelist1)

    with pytest.raises(XGIError):
        H4.set_node_attributes(attr_dict2)

    with pytest.raises(XGIError):
        H4.set_node_attributes(2)

    with pytest.warns(Warning):
        H4.set_node_attributes({"test": "blue"}, "color")

    with pytest.warns(Warning):
        H4.set_node_attributes({"test": {"blue": "color"}})


def test_set_edge_attributes(edgelist1):
    H1 = xgi.Hypergraph(edgelist1)
    attr_dict1 = {
        0: {"weight": 1},
        1: {"weight": 2},
        2: {"weight": 3.0},
        3: {"weight": -1},
    }

    attr_dict2 = {0: 1, 1: 2, 2: 3, 3: -1}
    H1.set_edge_attributes(attr_dict1)

    for e in H1.edges:
        assert H1.edges[e]["weight"] == attr_dict1[e]["weight"]

    H2 = xgi.Hypergraph(edgelist1)
    H2.set_edge_attributes("blue", name="color")

    for e in H2.edges:
        assert H2.edges[e]["color"] == "blue"

    H3 = xgi.Hypergraph(edgelist1)

    with pytest.warns(Warning), pytest.raises(XGIError):
        H3.set_node_attributes(attr_dict2)

    with pytest.raises(XGIError):
        H3.set_edge_attributes(2)

    with pytest.warns(Warning):
        H3.set_edge_attributes({"test": 2}, "weight")

    with pytest.warns(Warning):
        H3.set_edge_attributes({"test": {2: "weight"}})


def test_480(edgelist1):
    H1 = xgi.Hypergraph(edgelist1)
    attr_dict1 = {
        0: 1,
        1: 2,
        2: 3,
        3: -1,
    }
    H1.set_edge_attributes(attr_dict1, "weight")
    assert H1.edges.attrs("weight").asdict() == attr_dict1


def test_cleanup():
    H = xgi.Hypergraph()
    H.add_edges_from([["a", "b", "c"], ["a", "b", "c"], ["e", "f"]])
    H.add_nodes_from(["d", "g"])

    assert set(H.nodes) == {"a", "b", "c", "d", "e", "f", "g"}

    # test removing isolates
    cleanH = H.cleanup(connected=False, multiedges=True, relabel=False, in_place=False)
    assert set(cleanH.nodes) == {"a", "b", "c", "e", "f"}
    assert set(cleanH.edges) == {0, 1, 2}
    edges = cleanH.edges.members()
    assert {"a", "b", "c"} in edges
    assert {"e", "f"} in edges

    # test removing multiedges
    cleanH = H.cleanup(connected=False, isolates=False, relabel=False, in_place=False)
    assert set(cleanH.nodes) == {"a", "b", "c", "e", "f"}
    assert set(cleanH.edges) == {0, 2}
    edges = cleanH.edges.members()
    assert {"a", "b", "c"} in edges
    assert {"e", "f"} in edges

    # test getting giant component
    cleanH = H.cleanup(relabel=False, in_place=False)
    assert set(cleanH.nodes) == {"a", "b", "c"}
    assert cleanH.num_edges == 1

    # test relabel
    cleanH = H.cleanup(connected=False, in_place=False)
    assert set(cleanH.nodes) == {0, 1, 2, 3, 4}
    assert cleanH.num_edges == 2
    edges = cleanH.edges.members()
    assert {0, 1, 2} in edges
    assert {3, 4} in edges

    assert id(cleanH) != id(H)
    ### In-place versions

    # test removing isolates
    cleanH = H.copy()
    cleanH.cleanup(connected=False, multiedges=True, relabel=False)
    assert set(cleanH.nodes) == {"a", "b", "c", "e", "f"}
    assert set(cleanH.edges) == {0, 1, 2}
    edges = cleanH.edges.members()
    assert {"a", "b", "c"} in edges
    assert {"e", "f"} in edges

    # test removing multiedges
    cleanH = H.copy()
    cleanH.cleanup(connected=False, isolates=False, relabel=False)
    assert set(cleanH.nodes) == {"a", "b", "c", "e", "f"}
    assert set(cleanH.edges) == {0, 2}
    edges = cleanH.edges.members()
    assert {"a", "b", "c"} in edges
    assert {"e", "f"} in edges

    # test getting giant component
    cleanH = H.copy()
    cleanH.cleanup(relabel=False)
    assert set(cleanH.nodes) == {"a", "b", "c"}
    assert cleanH.num_edges == 1

    # test relabel
    cleanH = H.copy()
    cleanH["name"] = "test"
    cleanH.cleanup(connected=False)
    assert set(cleanH.nodes) == {0, 1, 2, 3, 4}
    assert cleanH.num_edges == 2
    edges = cleanH.edges.members()
    assert {0, 1, 2} in edges
    assert {3, 4} in edges
    assert cleanH["name"] == "test"

    assert cleanH._edge == xgi.dual_dict(cleanH._node)
