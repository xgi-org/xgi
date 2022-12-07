import pytest
from warnings import warn

import xgi
from xgi.exception import XGIError


def test_constructor(edgelist5, dict5, incidence5, dataframe5):
    S_list = xgi.SimplicialComplex(edgelist5)
    S_df = xgi.SimplicialComplex(dataframe5)
    S_sc = xgi.SimplicialComplex(S_list)

    with pytest.raises(XGIError):
        S_dict = xgi.SimplicialComplex(dict5)
    with pytest.raises(XGIError):
        S_mat = xgi.SimplicialComplex(incidence5)

    assert set(S_list.nodes) == set(S_df.nodes) == set(S_sc.nodes)
    assert set(S_list.edges) == set(S_df.edges) == set(S_sc.edges)
    assert set(S_list.edges.members(0)) == set(S_df.edges.members(0)) == set(S_sc.edges.members(0))

    with pytest.raises(XGIError):
        xgi.SimplicialComplex(1)

def test_string():
    S1 = xgi.SimplicialComplex()
    assert str(S1) == "Unnamed SimplicialComplex with 0 nodes and 0 simplices"
    S2 = xgi.SimplicialComplex(name="test")
    assert str(S2) == "SimplicialComplex named 'test' with 0 nodes and 0 simplices"


def test_add_simplex():
    S = xgi.SimplicialComplex()
    S.add_simplex([1, 2, 3])

    edge_dict = {
        0: frozenset({1, 2, 3}),
        1: frozenset({1, 2}),
        2: frozenset({1, 3}),
        3: frozenset({2, 3}),
    }

    assert S.num_nodes == 3
    assert S._edge == edge_dict

    S.add_simplex([2, 1])
    assert S._edge == edge_dict

    # check uid
    S2 = xgi.SimplicialComplex()
    S2.add_simplex([1, 2])
    S2.add_simplex([3, 4])
    S2.add_simplex([5, 6], id=1)
    assert S2._edge == {0: frozenset({1, 2}), 1: frozenset({3, 4})}


def test_add_edge():
    S = xgi.SimplicialComplex()
    with pytest.warns(UserWarning):
        S.add_simplex([1, 2, 3])
        warn("add_edge is deprecated in SimplicialComplex. Use add_simplex instead", UserWarning)
    S1 = xgi.SimplicialComplex()
    S1.add_simplex([1, 2, 3])
    assert S._edge == S1._edge

def test_add_simplices_from_iterable_of_members():
    edges = [{0, 1}, {1, 2}, {1, 2, 4}]
    simplices1 = [frozenset({0, 1}),
                 frozenset({1, 2}),
                 frozenset({1, 2, 4}),
                 frozenset({1, 4}),
                 frozenset({2, 4})]
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert S.edges.members() == simplices1

    S1 = xgi.SimplicialComplex(edges)
    with pytest.raises(XGIError):
        xgi.SimplicialComplex(S1.edges)

    edges = {frozenset([0, 1]), frozenset([1, 2]), frozenset([1, 2, 4])}
    simplices2 = [frozenset({0, 1}),
                 frozenset({1, 2, 4}),
                 frozenset({1, 2}),
                 frozenset({1, 4}),
                 frozenset({2, 4})]
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert S.edges.members() == simplices2

    edges = [[0, 1], {1, 2}, (1, 2, 4)]
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert S.edges.members() == simplices1

    edges = [{"foo", "bar"}, {"bar", "baz"}, {"foo", "bar", "baz"}]
    simplices3 = [frozenset({'bar', 'foo'}),
                 frozenset({'bar', 'baz'}),
                 frozenset({'bar', 'baz', 'foo'}),
                 frozenset({'baz', 'foo'})]
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert set(S.nodes) == {"foo", "bar", "baz"}
    assert S.edges.members() == simplices3

    edges = [{"a", "b"}, {"b", "c"}, {"c", "d", "e"}]
    simplices4 = [frozenset({'a', 'b'}),
                 frozenset({'b', 'c'}),
                 frozenset({'c', 'd', 'e'}),
                 frozenset({'c', 'e'}),
                 frozenset({'c', 'd'}),
                 frozenset({'d', 'e'})]

    S = xgi.SimplicialComplex()
    S.add_simplices_from(edges)
    assert set(S.nodes) == {"a", "b", "c", "d", "e"}
    assert set(S.edges.members()) == set(simplices4)

def test_add_simplices_from_format2():
    edges = [({0, 1}, 0), ({1, 2}, 1), ({1, 2, 4}, 2)]
    simplices1 = [frozenset({0, 1}),
                 frozenset({1, 2}),
                 frozenset({1, 2, 4}),
                 frozenset({1, 4}),
                 frozenset({2, 4})]
    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == list(range(6))
    assert H.edges.members(dtype=dict) == simplices1

    edges = [({0, 1}, "a"), ({1, 2}, "b"), ({1, 2, 4}, "foo")]
    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == list(range(6))
    assert H.edges.members(dtype=dict) == {e[1]: e[0] for e in edges}

    edges = [({0, 1}, "a"), ({1, 2}, "b"), ({2, 3, 4}, 100)]
    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == [e[1] for e in edges]
    assert H.edges.members(dtype=dict) == {e[1]: e[0] for e in simplices1}

    # check counter
    H.add_edge([1, 9, 2])
    assert H.edges.members(101) == {1, 9, 2}

    H1 = xgi.SimplicialComplex([{1, 2}, {2, 3, 4}])
    with pytest.warns(UserWarning, match="uid 0 already exists, cannot add edge {1, 3}."):
        H1.add_edges_from([({1, 3}, 0)])
    assert H1._edge == {0: {1, 2}, 1: {2, 3, 4}}


def test_add_simplices_from_format3():
    edges = [
        ({0, 1}, {"color": "red"}),
        ({1, 2}, {"age": 30}),
        ({1, 2, 4}, {"color": "blue", "age": 40}),
    ]
    simplices1 = [frozenset({0, 1}),
                 frozenset({1, 2}),
                 frozenset({1, 2, 4}),
                 frozenset({1, 4}),
                 frozenset({2, 4})]
    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == list(range(5))
    assert H.edges.members() == simplices1
    assert H.edges[0] == edges[0][1]
    assert H.edges[1] == edges[1][1]
    assert H.edges[2] == edges[2][1]
    assert H.edges[3] == dict()
    assert H.edges[4] == dict()
    # check counter
    H.add_simplex([1, 9, 2])
    assert H.edges.members(5) == {1, 9, 2}

def test_add_simplices_from_format4():
    edges = [
        ({0, 1}, "one", {"color": "red"}),
        ({1, 2}, "two", {"age": 30}),
        ({1, 2, 4}, "three", {"color": "blue", "age": 40}),
    ]
    simplices1 = [frozenset({0, 1}),
                 frozenset({1, 2}),
                 frozenset({1, 2, 4}),
                 frozenset({1, 4}),
                 frozenset({2, 4})]

    H = xgi.SimplicialComplex()
    H.add_simplices_from(edges)
    assert list(H.edges) == ['one', 'two', 'three', 0, 1]
    assert H.edges.members() == simplices1
    assert H.edges["one"] == edges[0][2]
    assert H.edges["two"] == edges[1][2]
    assert H.edges["three"] == edges[2][2]
    assert H.edges[0] == dict()
    assert H.edges[1] == dict()
    # check counter
    H.add_simplex([1, 9, 2])
    assert H.edges.members(2) == {1, 9, 2}

    H1 = xgi.SimplicialComplex([{1, 2}, {2, 3, 4}])
    with pytest.warns(UserWarning, match="uid 0 already exists, cannot add simplex {0, 1}."):
        H1.add_simplices_from([({0, 1}, 0, {"color": "red"})])
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

    assert S3.edges.members(dtype=dict) == {
        0: frozenset({1, 2, 3}),
        1: frozenset({1, 2}),
        2: frozenset({1, 3}),
        3: frozenset({2, 3}),
    }

    assert S3.edges[0] == {"color": "red"}
    assert S3.edges[1] == {}
    assert S3.edges[2] == {}
    assert S3.edges[3] == {}

    # check counter
    S4 = xgi.SimplicialComplex([{1, 2}, {2, 3}])
    S4.add_simplices_from([({1, 3}, 0)])
    assert S4._edge == {0: frozenset({1, 2}), 1: frozenset({2, 3})}

    S5 = xgi.SimplicialComplex([{1, 2}, {2, 3}])
    S5.add_simplices_from([({0, 1}, 0, {"color": "red"})])
    assert S5._edge == {0: frozenset({1, 2}), 1: frozenset({2, 3})}

    S6 = xgi.SimplicialComplex([{1, 2}, {2, 3}])
    S6.add_simplices_from({0: {1, 3}})
    assert S6._edge == {0: frozenset({1, 2}), 1: frozenset({2, 3})}

    S7 = xgi.SimplicialComplex()
    S7.add_simplices_from([({0, 1, 2}, 0, {})])
    assert S7._edge == {0: frozenset({0, 1, 2}), 1: frozenset({0, 1}), 2: frozenset({0, 2}), 3: frozenset({1, 2})}


def test_remove_simplex_id(edgelist6):
    S = xgi.SimplicialComplex()
    S.add_simplices_from(edgelist6)

    # remove simplex and others it belongs to
    S.remove_simplex_id(6)  # simplex {2, 3}
    edge_dict = {
        0: frozenset({0, 1, 2}),
        1: frozenset({0, 1}),
        2: frozenset({0, 2}),
        3: frozenset({1, 2}),
        5: frozenset({1, 3}),
        8: frozenset({2, 4}),
        9: frozenset({3, 4}),
    }
    assert S._edge == edge_dict
