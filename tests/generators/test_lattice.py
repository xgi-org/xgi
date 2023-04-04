import pytest

import xgi
from xgi.exception import XGIError


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
    with pytest.raises(XGIError):
        xgi.ring_lattice(5, 2, -1, 0)
