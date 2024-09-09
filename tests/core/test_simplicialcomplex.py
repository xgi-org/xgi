from warnings import warn

import pytest

import xgi
from xgi.exception import XGIError


def test_constructor(edgelist5, dict5, incidence5, dataframe5):
    S_list = xgi.SimplicialComplex(edgelist5)
    S_df = xgi.SimplicialComplex(dataframe5)
    S_sc = xgi.SimplicialComplex(S_list)
    S_dict = xgi.SimplicialComplex(dict5)

    with pytest.raises(XGIError):
        _ = xgi.SimplicialComplex(incidence5)

    assert set(S_list.nodes) == set(S_df.nodes) == set(S_sc.nodes) == set(S_dict.nodes)
    assert set(S_list.edges) == set(S_df.edges) == set(S_sc.edges) == set(S_dict.edges)
    assert (
        set(S_list.edges.members(0))
        == set(S_df.edges.members(0))
        == set(S_sc.edges.members(0))
        == set(S_dict.edges.members(0))
    )

    with pytest.raises(XGIError):
        xgi.SimplicialComplex(1)

    H = xgi.Hypergraph(edgelist5)
    S_h = xgi.SimplicialComplex(H)

    assert set(S_h.nodes) == set(H.nodes) == set(S_list.nodes)
    assert S_h.edges.members() == S_list.edges.members()
    assert H.edges.members() <= S_h.edges.members()  # check it's a subset


def test_string():
    S1 = xgi.SimplicialComplex()
    assert str(S1) == "Unnamed SimplicialComplex with 0 nodes and 0 simplices"
    S2 = xgi.SimplicialComplex(name="test")
    assert str(S2) == "SimplicialComplex named 'test' with 0 nodes and 0 simplices"


def test_add_simplex():
    S = xgi.SimplicialComplex()
    S.add_simplex([1, 2, 3])

    edges = [
        frozenset({1, 2, 3}),
        frozenset({2, 3}),
        frozenset({1, 2}),
        frozenset({1, 3}),
    ]

    assert S.num_nodes == 3
    assert list(S.edges) == list(range(4))
    assert set(S.edges.members()) == set(edges)

    S.add_simplex([2, 1])
    assert set(S.edges.members()) == set(edges)

    # check uid
    S2 = xgi.SimplicialComplex()
    S2.add_simplex([1, 2])
    S2.add_simplex([3, 4])
    with pytest.warns(UserWarning, match="uid 1 already exists, cannot add simplex"):
        S2.add_simplex([5, 6], id=1)
    assert S2._edge == {0: frozenset({1, 2}), 1: frozenset({3, 4})}


def test_add_edge():
    S = xgi.SimplicialComplex()
    with pytest.warns(UserWarning):
        S.add_simplex([1, 2, 3])
        warn(
            "add_edge is deprecated in SimplicialComplex. Use add_simplex instead",
            UserWarning,
        )
    S1 = xgi.SimplicialComplex()
    S1.add_simplex([1, 2, 3])
    assert S._edge == S1._edge


def test_add_simplices_from_iterable_of_members():
    edges = [{0, 1}, {1, 2}, {1, 2, 4}]
    simplices1 = [
        frozenset({0, 1}),
        frozenset({1, 2}),
        frozenset({1, 2, 4}),
        frozenset({1, 4}),
        frozenset({2, 4}),
    ]
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert set(S.edges.members()) == set(simplices1)

    S1 = xgi.SimplicialComplex(edges)
    with pytest.raises(XGIError):
        xgi.SimplicialComplex(S1.edges)

    edges = {frozenset([0, 1]), frozenset([1, 2]), frozenset([1, 2, 4])}

    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert set(S.edges.members()) == set(simplices1)

    edges = [[0, 1], {1, 2}, (1, 2, 4)]
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert set(S.edges.members()) == set(simplices1)

    edges = [{"foo", "bar"}, {"bar", "baz"}, {"foo", "bar", "baz"}]
    simplices3 = [
        frozenset({"bar", "foo"}),
        frozenset({"bar", "baz"}),
        frozenset({"bar", "baz", "foo"}),
        frozenset({"baz", "foo"}),
    ]
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert set(S.nodes) == {"foo", "bar", "baz"}
    assert S.edges.members() == simplices3

    edges = [{"a", "b"}, {"b", "c"}, {"c", "d", "e"}]
    simplices4 = [
        frozenset({"a", "b"}),
        frozenset({"b", "c"}),
        frozenset({"c", "d", "e"}),
        frozenset({"c", "e"}),
        frozenset({"c", "d"}),
        frozenset({"d", "e"}),
    ]

    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert set(S.nodes) == {"a", "b", "c", "d", "e"}
    assert set(S.edges.members()) == set(simplices4)


def test_add_simplices_from_format2():
    edges = [({0, 1}, 0), ({1, 2}, 1), ({1, 2, 4}, 2)]
    simplices1 = {
        0: frozenset({0, 1}),
        1: frozenset({1, 2}),
        2: frozenset({1, 2, 4}),
        3: frozenset({2, 4}),
        4: frozenset({1, 4}),
    }
    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == list(range(5))
    assert H._edge == simplices1

    edges = [({0, 1}, "a"), ({1, 2}, "b"), ({1, 2, 4}, "foo")]
    simplices = {
        "a": frozenset({0, 1}),
        "b": frozenset({1, 2}),
        "foo": frozenset({1, 2, 4}),
        0: frozenset({2, 4}),
        1: frozenset({1, 4}),
    }
    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == ["a", "b", "foo", 0, 1]
    assert H._edge == simplices

    edges = [({0, 1}, "a"), ({1, 2}, "b"), ({2, 3, 4}, 100)]
    simplices = [
        frozenset({0, 1}),
        frozenset({1, 2}),
        frozenset({2, 3, 4}),
        frozenset({2, 3}),
        frozenset({2, 4}),
        frozenset({3, 4}),
    ]
    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == ["a", "b", 100, 101, 102, 103]
    assert set(H.edges.members()) == set(simplices)

    # check counter
    H.add_simplex([1, 9, 2])
    assert next(H._edge_uid) == 107

    H1 = xgi.SimplicialComplex([{1, 2}, {2, 3, 4}])
    with pytest.warns(
        UserWarning, match="uid 0 already exists, cannot add simplex {1, 3}."
    ):
        H1.add_simplices_from([({1, 3}, 0)])
    simplices = [
        frozenset({1, 2}),
        frozenset({2, 3, 4}),
        frozenset({2, 3}),
        frozenset({2, 4}),
        frozenset({3, 4}),
    ]
    assert set(H1.edges.members()) == set(simplices)


def test_add_simplices_from_format3():
    edges = [
        ({0, 1}, {"color": "red"}),
        ({1, 2}, {"age": 30}),
        ({1, 2, 4}, {"color": "blue", "age": 40}),
    ]
    simplices1 = {
        0: frozenset({0, 1}),
        1: frozenset({1, 2}),
        2: frozenset({1, 2, 4}),
        3: frozenset({2, 4}),
        4: frozenset({1, 4}),
    }
    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == list(range(5))
    assert H._edge == simplices1
    assert H.edges[0] == edges[0][1]
    assert H.edges[1] == edges[1][1]
    assert H.edges[2] == edges[2][1]
    assert H.edges[3] == dict()
    assert H.edges[4] == dict()
    # check counter
    H.add_simplex([1, 9, 2])
    assert next(H._edge_uid) == 8


def test_add_simplices_from_format4():
    edges = [
        ({0, 1}, "one", {"color": "red"}),
        ({1, 2}, "two", {"age": 30}),
        ({1, 2, 4}, "three", {"color": "blue", "age": 40}),
    ]
    simplices1 = {
        "one": frozenset({0, 1}),
        "two": frozenset({1, 2}),
        "three": frozenset({1, 2, 4}),
        0: frozenset({2, 4}),
        1: frozenset({1, 4}),
    }

    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == ["one", "two", "three", 0, 1]
    assert H._edge == simplices1
    assert H.edges["one"] == edges[0][2]
    assert H.edges["two"] == edges[1][2]
    assert H.edges["three"] == edges[2][2]
    assert H.edges[0] == dict()
    assert H.edges[1] == dict()
    # check counter
    H.add_simplex([1, 9, 2])
    assert next(H._edge_uid) == 5

    H1 = xgi.SimplicialComplex([{1, 2}, {2, 3, 4}])
    with pytest.warns(
        UserWarning, match="uid 0 already exists, cannot add simplex {0, 1}."
    ):
        H1.add_simplices_from([({0, 1}, 0, {"color": "red"})])
    assert next(H1._edge_uid) == 5


def test_add_edges_from_dict():
    edges = {"one": [0, 1], "two": [1, 2], 2: [1, 2, 4]}
    simplices1 = {
        "one": frozenset({0, 1}),
        "two": frozenset({1, 2}),
        2: frozenset({1, 2, 4}),
        3: frozenset({2, 4}),
        4: frozenset({1, 4}),
    }

    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == ["one", "two", 2, 3, 4]
    assert H._edge == simplices1
    # check counter
    H.add_simplex([1, 9, 2])
    assert H.edges.members(5) == {1, 9, 2}

    H1 = xgi.SimplicialComplex([{1, 2}, {2, 3, 4}])
    with pytest.warns(
        UserWarning, match="uid 0 already exists, cannot add simplex {1, 3}"
    ):
        H1.add_simplices_from({0: {1, 3}})
    assert next(H1._edge_uid) == 5


def test_add_simplices_from(edgelist5):
    S1 = xgi.SimplicialComplex()
    S1.add_simplices_from(edgelist5, max_order=None)

    S2 = xgi.SimplicialComplex()
    S2.add_simplices_from(edgelist5, max_order=2)

    assert S1.nodes == S2.nodes

    assert xgi.max_edge_order(S1) == 3
    assert xgi.max_edge_order(S2) == 2

    s1o1, s1o2 = S1.edges.filterby("order", 1), S1.edges.filterby("order", 2)
    s2o1, s2o2 = S2.edges.filterby("order", 1), S2.edges.filterby("order", 2)
    assert set(s1o1.members()) == set(s2o1.members())
    assert set(s1o2.members()) == set(s2o2.members())

    S3 = xgi.SimplicialComplex()
    simplex = ((1, 2, 3), {"color": "red"})
    S3.add_simplices_from([simplex], max_order=2)

    simplices = [
        frozenset({1, 2, 3}),
        frozenset({2, 3}),
        frozenset({1, 2}),
        frozenset({1, 3}),
    ]

    assert set(S3.edges.members()) == set(simplices)

    assert S3.edges[0] == {"color": "red"}
    assert S3.edges[1] == {}
    assert S3.edges[2] == {}
    assert S3.edges[3] == {}

    # check counter
    S4 = xgi.SimplicialComplex([{1, 2}, {2, 3}])
    with pytest.warns(UserWarning, match="uid 0 already exists, cannot add simplex"):
        S4.add_simplices_from([({1, 3}, 0)])
    assert S4._edge == {0: frozenset({1, 2}), 1: frozenset({2, 3})}

    S5 = xgi.SimplicialComplex([{1, 2}, {2, 3}])
    with pytest.warns(UserWarning, match="uid 0 already exists, cannot add simplex"):
        S5.add_simplices_from([({0, 1}, 0, {"color": "red"})])
    assert S5._edge == {0: frozenset({1, 2}), 1: frozenset({2, 3})}

    S6 = xgi.SimplicialComplex([{1, 2}, {2, 3}])
    with pytest.warns(UserWarning, match="uid 0 already exists, cannot add simplex"):
        S6.add_simplices_from({0: {1, 3}})
    assert S6._edge == {0: frozenset({1, 2}), 1: frozenset({2, 3})}

    S7 = xgi.SimplicialComplex()
    S7.add_simplices_from([({0, 1, 2}, 0, {})])
    assert S7._edge == {
        0: frozenset({0, 1, 2}),
        1: frozenset({0, 1}),
        2: frozenset({0, 2}),
        3: frozenset({1, 2}),
    }


def test_add_simplices_from_wrong_format():
    edges = [0, 1, 2]
    with pytest.raises(XGIError):
        xgi.SimplicialComplex().add_simplices_from(edges)

    edges = [
        ("foo", {"color": "red"}),
        ("bar", {"age": 30}),
        ("baz", {"color": "blue", "age": 40}),
    ]

    with pytest.raises(XGIError):
        xgi.SimplicialComplex().add_simplices_from(edges)

    edges = [
        ("foo", "one", {"color": "red"}),
        ("bar", "two", {"age": 30}),
        ("baz", "three", {"color": "blue", "age": 40}),
    ]
    with pytest.raises(XGIError):
        xgi.SimplicialComplex().add_simplices_from(edges)

    edges = ["a", "b", "c"]
    with pytest.raises(XGIError):
        xgi.SimplicialComplex().add_simplices_from(edges)

    edges = ["foo", "bar", "baz"]
    with pytest.raises(XGIError):
        xgi.SimplicialComplex().add_simplices_from(edges)

    edges = ["foo", [1, 2], [2, 3, 4]]
    with pytest.raises(XGIError):
        xgi.SimplicialComplex().add_simplices_from(edges)


def test_copy(edgelist1):
    H = xgi.SimplicialComplex(edgelist1)
    H["key"] = "value"
    copy = H.copy()
    assert list(copy.nodes) == list(H.nodes)
    assert list(copy.edges) == list(H.edges)
    assert list(copy.edges.members()) == list(H.edges.members())
    assert H._net_attr == copy._net_attr

    H.add_node(10)
    assert list(copy.nodes) != list(H.nodes)
    assert list(copy.edges) == list(H.edges)

    H.add_simplex([1, 3, 5])
    assert list(copy.edges) != list(H.edges)

    H["key2"] = "value2"
    assert H._net_attr != copy._net_attr

    copy.add_node(10)
    copy.add_simplex([1, 3, 5])
    copy["key2"] = "value2"
    assert list(copy.nodes) == list(H.nodes)
    assert list(copy.edges) == list(H.edges)
    assert list(copy.edges.members()) == list(H.edges.members())
    assert H._net_attr == copy._net_attr

    H1 = xgi.SimplicialComplex()
    H1.add_simplex((1, 2), id="x")
    copy2 = H1.copy()  # does not throw error because of str id
    assert list(copy2.nodes) == list(H1.nodes)
    assert list(copy2.edges) == list(H1.edges)
    assert list(copy2.edges.members()) == list(H1.edges.members())
    assert H1._net_attr == copy2._net_attr


def test_duplicate_edges(edgelist1):
    H = xgi.SimplicialComplex(edgelist1)
    assert set(H.edges.duplicates()) == set()

    H.add_simplex([1, 3, 2])  # same order as existing edge
    assert set(H.edges.duplicates()) == set()

    H.add_simplex([1, 2, 3])  # different order, same members
    assert set(H.edges.duplicates()) == set()

    H = xgi.SimplicialComplex([[1, 2, 3, 3], [1, 2, 3]])  # repeated nodes
    assert set(H.edges.duplicates()) == set()

    H = xgi.SimplicialComplex([[1, 2, 3, 3], [3, 1, 2, 3]])  # repeated nodes
    assert set(H.edges.duplicates()) == set()


def test_duplicate_nodes(edgelist1):
    H = xgi.SimplicialComplex(edgelist1)
    assert set(H.nodes.duplicates()) == set()

    H.add_simplices_from([[1, 4], [2, 6, 7], [6, 8]])
    assert set(H.nodes.duplicates()) == set()


def test_remove_simplex_id(edgelist6):
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edgelist6)

    # remove simplex and others it belongs to
    id = list(S._edge.values()).index(frozenset({2, 3}))
    S.remove_simplex_id(id)  # simplex {2, 3}
    edges = [
        frozenset({0, 1, 2}),
        frozenset({0, 1}),
        frozenset({2, 4}),
        frozenset({1, 2}),
        frozenset({3, 4}),
        frozenset({0, 2}),
        frozenset({1, 3}),
    ]
    assert set(S.edges.members()) == set(edges)


def test_remove_simplex_ids_from(edgelist6, edgelist4):
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edgelist6)

    # remove simplex and others it belongs to
    id1 = list(S._edge.values()).index(frozenset({2, 3}))
    id2 = list(S._edge.values()).index(frozenset({0, 1, 2}))
    S.remove_simplex_ids_from([id1, id2])
    edges = [
        frozenset({0, 1}),
        frozenset({2, 4}),
        frozenset({1, 2}),
        frozenset({3, 4}),
        frozenset({0, 2}),
        frozenset({1, 3}),
    ]
    assert set(S.edges.members()) == set(edges)

    # test issue 580
    S1 = xgi.SimplicialComplex(edgelist4)
    id_all = list(S1.edges)
    S1.remove_simplex_ids_from(id_all)
    assert S1.num_edges == 0


def test_freeze(edgelist1):
    SC = xgi.SimplicialComplex(edgelist1)
    SC.freeze()
    with pytest.raises(XGIError):
        SC.add_node(10)

    with pytest.raises(XGIError):
        SC.add_nodes_from([8, 9, 10])

    with pytest.raises(XGIError):
        SC.add_simplex([1, 5, 7])

    with pytest.raises(XGIError):
        SC.add_simplices_from([[1, 7], [7]])

    with pytest.raises(XGIError):
        SC.remove_node(1)

    with pytest.raises(XGIError):
        SC.remove_nodes_from([1, 2, 3])

    with pytest.raises(XGIError):
        SC.remove_simplex_id(1)

    with pytest.raises(XGIError):
        SC.remove_simplex_ids_from([0, 1])

    assert SC.is_frozen


def test_cleanup():
    SC = xgi.SimplicialComplex()
    SC.add_simplices_from([["a", "b", "c"], ["e", "f"]])
    SC.add_nodes_from(["d", "g"])

    assert set(SC.nodes) == {"a", "b", "c", "d", "e", "f", "g"}

    # test removing isolates
    cleanSC = SC.cleanup(connected=False, relabel=False, in_place=False)
    assert set(cleanSC.nodes) == {"a", "b", "c", "e", "f"}
    assert set(cleanSC.edges) == {0, 1, 2, 3, 4}
    simplices = cleanSC.edges.members()
    assert frozenset({"a", "b", "c"}) in simplices
    assert frozenset({"e", "f"}) in simplices
    assert frozenset({"a", "b"}) in simplices
    assert frozenset({"a", "c"}) in simplices
    assert frozenset({"b", "c"}) in simplices

    # test getting giant component
    cleanSC = SC.cleanup(isolates=True, relabel=False, in_place=False)
    assert set(cleanSC.nodes) == {"a", "b", "c"}
    assert cleanSC.num_edges == 4

    # test relabel
    cleanSC = SC.cleanup(isolates=True, connected=False, in_place=False)
    assert set(cleanSC.nodes) == {0, 1, 2, 3, 4, 5, 6}
    assert cleanSC.num_edges == 5
    simplices = cleanSC.edges.members()
    assert frozenset({0, 1, 2}) in simplices
    assert frozenset({3, 4}) in simplices
    assert frozenset({0, 1}) in simplices
    assert frozenset({0, 2}) in simplices
    assert frozenset({1, 2}) in simplices

    ### In-place versions

    # test removing isolates
    cleanSC = SC.copy()
    cleanSC.cleanup(connected=False, relabel=False)
    assert set(cleanSC.nodes) == {"a", "b", "c", "e", "f"}
    assert set(cleanSC.edges) == {0, 1, 2, 3, 4}
    simplices = cleanSC.edges.members()
    assert frozenset({"a", "b", "c"}) in simplices
    assert frozenset({"e", "f"}) in simplices
    assert frozenset({"a", "b"}) in simplices
    assert frozenset({"a", "c"}) in simplices
    assert frozenset({"b", "c"}) in simplices

    # test getting giant component
    cleanSC = SC.copy()
    cleanSC.cleanup(isolates=False, relabel=False)
    assert set(cleanSC.nodes) == {"a", "b", "c"}
    assert cleanSC.num_edges == 4

    # test relabel
    cleanSC = SC.copy()
    cleanSC["name"] = "test"
    cleanSC.cleanup(connected=False)
    assert cleanSC["name"] == "test"
    assert set(cleanSC.nodes) == {0, 1, 2, 3, 4}
    assert cleanSC.num_edges == 5
    simplices = cleanSC.edges.members()
    assert frozenset({0, 1, 2}) in simplices
    assert frozenset({3, 4}) in simplices
    assert frozenset({0, 1}) in simplices
    assert frozenset({0, 2}) in simplices
    assert frozenset({1, 2}) in simplices


def test_remove_node(edgelist1):
    S = xgi.SimplicialComplex(edgelist1)
    assert 1 in S
    S.remove_node(1)
    assert 1 not in S
    assert 0 not in S.edges


def test_issue_445(edgelist1):
    S = xgi.SimplicialComplex(edgelist1)
    assert 1 in S
    S.remove_node(1)
    assert 1 not in S
    assert 0 not in S.edges
    assert S._edge == xgi.dual_dict(S._node)
