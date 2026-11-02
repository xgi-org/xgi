import pytest

import xgi


def test_ring_lattice():
    H = xgi.ring_lattice(5, 2, 2, 0)
    assert H.num_nodes == 5
    assert H.num_edges == 5
    assert xgi.unique_edge_sizes(H) == [2]

    H = xgi.ring_lattice(5, 3, 4, 1)
    edges = H.edges.members()
    for i in range(H.num_edges - 1):
        assert len(set(edges[i]).intersection(set(edges[i + 1]))) == 2  # d-l
    assert xgi.unique_edge_sizes(H) == [3]

    # k < 2 test
    with pytest.warns(Warning):
        H = xgi.ring_lattice(5, 2, 1, 0)
    assert H.num_nodes == 5
    assert H.num_edges == 0

    # k % 2 != 0 test
    with pytest.warns(Warning):
        xgi.ring_lattice(5, 2, 3, 0)

    # k < 0 test
    with pytest.raises(ValueError):
        xgi.ring_lattice(5, 2, -1, 0)


def test_ring_lattice_with_positions():
    from math import cos, pi, sin

    # default: no pos stored
    H = xgi.ring_lattice(5, 2, 2, 0)
    assert H.nodes.attrs("pos").asdict() == {i: None for i in range(5)}

    # with_positions=True: each node has a unit-circle coordinate
    H = xgi.ring_lattice(8, 3, 2, 0, with_positions=True)
    pos = H.nodes.attrs("pos").asdict()
    assert set(pos.keys()) == set(range(8))
    for i, p in pos.items():
        expected = (cos(2 * pi * i / 8), sin(2 * pi * i / 8))
        assert p == pytest.approx(expected)
