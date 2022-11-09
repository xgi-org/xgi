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

    assert set(S_list.nodes) == set(S_df.nodes)
    assert set(S_list.edges) == set(S_df.edges)
    assert set(S_list.edges.members(0)) == set(S_df.edges.members(0))

    with pytest.raises(XGIError):
        xgi.SimplicialComplex(1)


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

    assert xgi.max_edge_order(S1) == 3
    assert xgi.max_edge_order(S2) == 2

    s1o1, s1o2 = S1.edges.filterby("order", 1), S1.edges.filterby("order", 2)
    s2o1, s2o2 = S2.edges.filterby("order", 1), S2.edges.filterby("order", 2)
    assert set(s1o1.members()) == set(s2o1.members())
    assert set(s1o2.members()) == set(s2o2.members())

    S3 = xgi.SimplicialComplex()
    simplex = ((1,2,3), {"color": "red"})
    S3.add_simplices_from([simplex], max_order=2)

    assert S3.edges.members(dtype=dict) == {0: frozenset({1, 2, 3}),
                                            1: frozenset({1, 2}),
                                            2: frozenset({1, 3}),
                                            3: frozenset({2, 3})}

    assert S3.edges[0] == {'color': 'red'} 
    assert S3.edges[1] == {}
    assert S3.edges[2] == {}
    assert S3.edges[3] == {}                       

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
