import pytest
import xgi
from xgi.exception import XGIError


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
