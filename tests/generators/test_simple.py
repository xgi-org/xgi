import pytest

import xgi
from xgi.exception import XGIError


def test_star_clique():
    with pytest.raises(ValueError):
        H = xgi.star_clique(-1, 7, 3)
    with pytest.raises(ValueError):
        H = xgi.star_clique(6, -1, 3)
    with pytest.raises(ValueError):
        H = xgi.star_clique(6, 7, -1)
    with pytest.raises(ValueError):
        H = xgi.star_clique(6, 7, 7)

    H = xgi.star_clique(6, 7, 3)
    assert H.num_nodes == 13
    assert H.num_edges == 97
    assert xgi.max_edge_order(H) == 3


def test_sunflower():
    with pytest.raises(XGIError):
        H = xgi.sunflower(3, 4, 2)

    H = xgi.sunflower(3, 1, 5)

    assert H.nodes.memberships(0) == {0, 1, 2}
    assert set(H.nodes) == set(range(13))
    assert H.num_edges == 3
    for n in range(1, H.num_nodes):
        assert len(H.nodes.memberships(n)) == 1

    H = xgi.sunflower(4, 3, 6)
    for i in range(3):
        H.nodes.memberships(i) == {0, 1, 2, 3}

    assert H.num_nodes == 15

    for i in range(3, 15):
        assert len(H.nodes.memberships(i)) == 1
