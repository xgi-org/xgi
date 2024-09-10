import pytest

import xgi
from xgi.exception import XGIError


def test_k_skeleton(edgelist1, edgelist2):
    S = xgi.SimplicialComplex(edgelist1)
    S1 = xgi.k_skeleton(S, 1, in_place=False)
    edges_skeleton = [
        frozenset({4}),
        frozenset({5, 6}),
        frozenset({1, 2}),
        frozenset({8, 7}),
        frozenset({2, 3}),
        frozenset({6, 7}),
        frozenset({8, 6}),
        frozenset({1, 3}),
    ]
    assert set(S1.edges.members()) == set(edges_skeleton)

    with pytest.raises(XGIError):
        xgi.k_skeleton(S, 5, in_place=True)

    S2 = xgi.SimplicialComplex(edgelist2)
    xgi.k_skeleton(S2, 0, in_place=True)
    assert S2.num_edges == 0
