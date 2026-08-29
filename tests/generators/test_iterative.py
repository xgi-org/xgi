import pytest

import xgi
from xgi.exception import XGIError


def test_pseudofractal():

    # initial
    S0 = xgi.pseudofractal_simplicial_complex(order=2, n_iter=0)
    triangles = set(S0.edges.filterby("order", 2).members())

    assert isinstance(S0, xgi.SimplicialComplex)
    assert S0.num_nodes == 3
    assert S0.num_edges == 4
    assert triangles == {frozenset({0, 1, 2})}

    # first iteration
    S1 = xgi.pseudofractal_simplicial_complex(order=2, n_iter=1)
    triangles = set(S1.edges.filterby("order", 2).members())

    assert isinstance(S1, xgi.SimplicialComplex)
    assert S1.num_nodes == 6
    assert xgi.num_edges_order(S1, d=2) == 4
    assert triangles == {
        frozenset({1, 2, 5}),
        frozenset({0, 2, 4}),
        frozenset({0, 1, 3}),
        frozenset({0, 1, 2}),
    }

    # second iteration
    S2 = xgi.pseudofractal_simplicial_complex(order=2, n_iter=2)
    triangles = set(S2.edges.filterby("order", 2).members())

    assert isinstance(S2, xgi.SimplicialComplex)
    assert S2.num_nodes == 15
    assert xgi.num_edges_order(S2, d=2) == 13
    assert triangles == {
        frozenset({0, 4, 10}),
        frozenset({0, 2, 7}),
        frozenset({0, 1, 2}),
        frozenset({1, 5, 11}),
        frozenset({1, 2, 5}),
        frozenset({0, 2, 4}),
        frozenset({0, 3, 12}),
        frozenset({1, 3, 14}),
        frozenset({2, 4, 9}),
        frozenset({1, 2, 8}),
        frozenset({0, 1, 6}),
        frozenset({2, 5, 13}),
        frozenset({0, 1, 3}),
    }


def test_apollonian():

    # initial
    S0 = xgi.apollonian_complex(order=2, n_iter=0)
    triangles = set(S0.edges.filterby("order", 2).members())

    assert isinstance(S0, xgi.SimplicialComplex)
    assert S0.num_nodes == 3
    assert S0.num_edges == 4
    assert triangles == {frozenset({0, 1, 2})}

    # first iteration
    S1 = xgi.apollonian_complex(order=2, n_iter=1)
    triangles = set(S1.edges.filterby("order", 2).members())

    assert isinstance(S1, xgi.SimplicialComplex)
    assert S1.num_nodes == 6
    assert xgi.num_edges_order(S1, d=2) == 4
    assert triangles == {
        frozenset({1, 2, 5}),
        frozenset({0, 2, 4}),
        frozenset({0, 1, 3}),
        frozenset({0, 1, 2}),
    }

    # second iteration
    S2 = xgi.apollonian_complex(order=2, n_iter=2)
    triangles = set(S2.edges.filterby("order", 2).members())

    assert isinstance(S2, xgi.SimplicialComplex)
    assert S2.num_nodes == 12
    assert xgi.num_edges_order(S2, d=2) == 10
    assert triangles == {
        frozenset({2, 4, 6}),
        frozenset({1, 5, 8}),
        frozenset({0, 3, 9}),
        frozenset({0, 1, 2}),
        frozenset({1, 2, 5}),
        frozenset({0, 2, 4}),
        frozenset({2, 5, 10}),
        frozenset({1, 3, 11}),
        frozenset({0, 1, 3}),
        frozenset({0, 4, 7}),
    }
