import pytest

import xgi
from xgi.exception import IDNotFound, XGIError


def test_constructor(edgelist5, dict5, incidence5, dataframe5):
    H_list = xgi.Hypergraph(edgelist5)
    H_dict = xgi.Hypergraph(dict5)
    H_mat = xgi.Hypergraph(incidence5)
    H_df = xgi.Hypergraph(dataframe5)
    H_hg = xgi.Hypergraph(H_list)

    assert (
        list(H_list.nodes)
        == list(H_dict.nodes)
        == list(H_mat.nodes)
        == list(H_df.nodes)
        == list(H_hg.nodes)
    )
    assert (
        list(H_list.edges)
        == list(H_dict.edges)
        == list(H_mat.edges)
        == list(H_df.edges)
        == list(H_hg.edges)
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


def test_hypergraph_attrs():
    H = xgi.Hypergraph()
    assert H._hypergraph == {}
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


def test_members(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert H.nodes.memberships(1) == {0}
    assert H.nodes.memberships(2) == {0}
    assert H.nodes.memberships(3) == {0}
    assert H.nodes.memberships(4) == {1}
    assert H.nodes.memberships(6) == {2, 3}
    with pytest.raises(IDNotFound):
        H.nodes.memberships(0)
    with pytest.raises(TypeError):
        H.nodes.memberships(slice(1, 4))


def test_add_edge():
    for edge in [[1, 2, 3], {1, 2, 3}, iter([1, 2, 3])]:
        H = xgi.Hypergraph()
        H.add_edge(edge)
        assert (1 in H) and (2 in H) and (3 in H)
        assert 0 in H.edges
        assert {1, 2, 3} in H.edges.members()
        assert {1, 2, 3} == H.edges.members(0)
        assert H.edges.members(dtype=dict) == {0: {1, 2, 3}}

    H = xgi.Hypergraph()
    for edge in [[], set(), iter([])]:
        with pytest.raises(XGIError):
            H.add_edge(edge)


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


def test_add_edges_from_iterable_of_members():
    edges = [[0, 1], [1, 2], [2, 3, 4]]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges.members()) == [set(e) for e in edges]

    H1 = xgi.Hypergraph(edges)
    with pytest.raises(XGIError):
        xgi.Hypergraph(H1.edges)

    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges.members()) == [set(e) for e in edges]

    edges = {frozenset([0, 1]), frozenset([1, 2]), frozenset([2, 3, 4])}
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges.members()) == [set(e) for e in edges]

    edges = [[0, 1], frozenset([1, 2]), (2, 3, 4)]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges.members()) == [set(e) for e in edges]

    edges = [["foo", "bar"], ["bar", "baz"], ["foo", "bar", "baz"]]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.nodes) == ["foo", "bar", "baz"]
    assert list(H.edges.members()) == [set(e) for e in edges]

    edges = [["a", "b"], ["b", "c"], ["c", "d", "e"]]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.nodes) == ["a", "b", "c", "d", "e"]
    assert list(H.edges.members()) == [set(e) for e in edges]


def test_add_edges_from_format1():
    edges = [([0, 1], 0), ([1, 2], 1), ([2, 3, 4], 2)]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members(dtype=dict) == {e[1]: set(e[0]) for e in edges}

    edges = [([0, 1], "a"), ([1, 2], "b"), ([2, 3, 4], "foo")]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members(dtype=dict) == {e[1]: set(e[0]) for e in edges}

    edges = [([0, 1], "a"), ([1, 2], "b"), ([2, 3, 4], 100)]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members(dtype=dict) == {e[1]: set(e[0]) for e in edges}


def test_add_edges_from_format2():
    edges = [
        ([0, 1], {"color": "red"}),
        ([1, 2], {"age": 30}),
        ([2, 3, 4], {"color": "blue", "age": 40}),
    ]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == list(range(len(edges)))
    assert H.edges.members() == [set(e[0]) for e in edges]
    for idx, e in enumerate(H.edges):
        assert H.edges[e] == edges[idx][1]


def test_add_edges_from_format3():
    edges = [
        ([0, 1], "one", {"color": "red"}),
        ([1, 2], "two", {"age": 30}),
        ([2, 3, 4], "three", {"color": "blue", "age": 40}),
    ]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members() == [set(e[0]) for e in edges]
    for idx, e in enumerate(H.edges):
        assert H.edges[e] == edges[idx][2]


def test_add_edges_from_dict():
    edges = {"one": [0, 1], "two": [1, 2], "three": [2, 3, 4]}
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    assert list(H.edges) == ["one", "two", "three"]
    assert H.edges.members() == [set(edges[e]) for e in edges]


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
    assert H._hypergraph == copy._hypergraph

    H.add_node(10)
    assert list(copy.nodes) != list(H.nodes)
    assert list(copy.edges) == list(H.edges)

    H.add_edge([1, 3, 5])
    assert list(copy.edges) != list(H.edges)

    H["key2"] = "value2"
    assert H._hypergraph != copy._hypergraph

    copy.add_node(10)
    copy.add_edge([1, 3, 5])
    copy["key2"] = "value2"
    assert list(copy.nodes) == list(H.nodes)
    assert list(copy.edges) == list(H.edges)
    assert list(copy.edges.members()) == list(H.edges.members())
    assert H._hypergraph == copy._hypergraph


def test_copy_issue128():
    # see https://github.com/ComplexGroupInteractions/xgi/issues/128
    H = xgi.Hypergraph()
    H["key"] = "value"
    K = H.copy()
    K["key"] = "some_other_value"
    assert H["key"] == "value"


def test_double_edge_swap(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    with pytest.raises(XGIError):
        H.double_edge_swap(5, 6, 2, 3, is_loopy=False)

    H.double_edge_swap(1, 6, 0, 3)
    assert H.edges.members() == [[6, 2, 3], [4], [5, 6], [1, 7, 8]]

    H.double_edge_swap(3, 4, 0, 1)
    assert H.edges.members() == [[6, 2, 4], [3], [5, 6], [1, 7, 8]]

    with pytest.raises(IDNotFound):
        H.double_edge_swap(10, 3, 0, 1)

    with pytest.raises(XGIError):
        H.double_edge_swap(8, 3, 0, 1)

    # loopy swap
    H.double_edge_swap(4, 6, 0, 2)
    assert H.edges.members() == [[6, 2, 6], [3], [5, 4], [1, 7, 8]]


def test_duplicate_edges(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert list(H.edges.duplicates()) == []

    H.add_edge([1, 3, 2])  # same order as existing edge
    assert list(H.edges.duplicates()) == [0, 4]

    H.add_edge([1, 2, 3])  # different order, same members
    assert list(H.edges.duplicates()) == [0, 4, 5]

    H = xgi.Hypergraph([[1, 2, 3, 3], [1, 2, 3]])  # repeated nodes
    assert list(H.edges.duplicates()) == []

    H = xgi.Hypergraph([[1, 2, 3, 3], [3, 1, 2, 3]])  # repeated nodes
    assert list(H.edges.duplicates()) == [0, 1]


def test_duplicate_nodes(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert list(H.nodes.duplicates()) == [1, 2, 3, 7, 8]

    H.add_edges_from([[1, 4], [2, 6, 7], [6, 8]])
    assert list(H.nodes.duplicates()) == []

    # this loop makes 1 and 2 belong to the same edges
    for edgeid, members in H.edges.members(dtype=dict).items():
        if 1 in members and 2 not in members:
            H.add_node_to_edge(edgeid, 2)
        if 1 not in members and 2 in members:
            H.add_node_to_edge(edgeid, 1)
    assert list(H.nodes.duplicates()) == [1, 2]
