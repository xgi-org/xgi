import pytest
import xgi
from xgi.exception import XGIError


def test_constructor(edgelist5, dict5, incidence5, dataframe5):
    S_list = xgi.SimplicialComplex(edgelist5)
    S_df = xgi.SimplicialComplex(dataframe5)

    with pytest.raises(XGIError):
        S_dict = xgi.SimplicialComplex(dict5)
    with pytest.raises(XGIError):
        S_mat = xgi.SimplicialComplex(incidence5)

    assert list(S_list.nodes) == list(S_df.nodes)
    assert list(S_list.edges) == list(S_df.edges)
    assert list(S_list.edges.members(0)) == list(S_df.edges.members(0))


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


def test_add_edge():
    S = xgi.SimplicialComplex()
    with pytest.raises(XGIError):
        S.add_edge([1, 2, 3])


def test_add_simplices_from(edgelist5):
    S1 = xgi.SimplicialComplex()
    S1.add_simplices_from(edgelist5, max_order=None)

    S2 = xgi.SimplicialComplex()
    S2.add_simplices_from(edgelist5, max_order=2)

    assert S1.nodes == S2.nodes

    assert S1.max_edge_order() == 3
    assert S2.max_edge_order() == 2

    assert set(S1.edges(order=1).members()) == set(S2.edges(order=1).members())
    assert set(S1.edges(order=2).members()) == set(S2.edges(order=2).members())


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
