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


@pytest.mark.parametrize(
    "generator",
    [xgi.pseudofractal_simplicial_complex, xgi.apollonian_complex],
)
def test_order_too_small(generator):
    for order in [0, 1]:
        with pytest.raises(ValueError):
            generator(order=order, n_iter=1)


def test_network_geometry_flavor():
    order, n_iter = 2, 20
    for s in [-1, 0, 1]:
        S = xgi.network_geometry_flavor(order, s, beta=1, n_iter=n_iter, seed=1)
        assert isinstance(S, xgi.SimplicialComplex)
        # one new node and one new d-simplex per iteration
        assert set(S.nodes) == set(range(order + 1 + n_iter))
        assert len(S.edges.filterby("order", order)) == n_iter + 1

    # s = -1: each (d-1)-simplex is shared by at most two d-simplices
    S = xgi.network_geometry_flavor(order, -1, beta=1, n_iter=50, seed=1)
    triangles = S.edges.filterby("order", order).members()
    face_counts = {}
    for face in xgi.subfaces(triangles, order=order - 1):
        face = frozenset(face)
        face_counts[face] = face_counts.get(face, 0) + 1
    assert max(face_counts.values()) <= 2

    # order 1 grows a tree
    S = xgi.network_geometry_flavor(1, 0, beta=1, n_iter=10, seed=1)
    assert S.num_nodes == 12
    assert len(S.edges.filterby("order", 1)) == 11

    # large beta does not underflow
    S = xgi.network_geometry_flavor(order, 0, beta=1000, n_iter=10, seed=1)
    assert S.num_nodes == order + 1 + 10


def test_network_geometry_flavor_seed():
    S1 = xgi.network_geometry_flavor(2, 1, beta=1, n_iter=30, seed=42)
    S2 = xgi.network_geometry_flavor(2, 1, beta=1, n_iter=30, seed=42)
    S3 = xgi.network_geometry_flavor(2, 1, beta=1, n_iter=30, seed=43)
    assert set(S1.edges.members()) == set(S2.edges.members())
    assert set(S1.edges.members()) != set(S3.edges.members())

    # custom energy distribution
    S = xgi.network_geometry_flavor(
        2,
        0,
        beta=1,
        n_iter=10,
        energy_distribution=lambda rng: rng.exponential(1.0),
        seed=1,
    )
    assert S.num_nodes == 13

    # energy distribution with an rng argument is reproducible with seed
    def energy(rng):
        return rng.exponential(1.0)

    S1 = xgi.network_geometry_flavor(2, 1, 1, 30, energy_distribution=energy, seed=7)
    S2 = xgi.network_geometry_flavor(2, 1, 1, 30, energy_distribution=energy, seed=7)
    assert set(S1.edges.members()) == set(S2.edges.members())

    # energy distribution without arguments also works
    calls = []

    def energy_no_arg():
        calls.append(1)
        return 1.0

    S = xgi.network_geometry_flavor(
        2, 0, beta=1, n_iter=10, energy_distribution=energy_no_arg, seed=1
    )
    assert S.num_nodes == 13
    assert len(calls) == 13  # one energy per node


def test_network_geometry_flavor_errors():
    with pytest.raises(ValueError):
        xgi.network_geometry_flavor(0, 0, beta=1, n_iter=5)
    with pytest.raises(ValueError):
        xgi.network_geometry_flavor(2, 2, beta=1, n_iter=5)
