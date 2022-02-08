import xgi
import pytest

from xgi.exception import XGIError


def test_erdos_renyi_hypergraph():
    with pytest.raises(ValueError):
        H = xgi.erdos_renyi_hypergraph(10, 20, -0.1)
    with pytest.raises(ValueError):
        H = xgi.erdos_renyi_hypergraph(10, 20, 2.0)

    H = xgi.erdos_renyi_hypergraph(10, 20, 0.0)
    assert H.number_of_nodes() == 10
    assert H.number_of_edges() == 0

    H = xgi.erdos_renyi_hypergraph(10, 20, 1.0)
    assert H.number_of_nodes() == 10
    assert H.number_of_edges() == 20

    H = xgi.erdos_renyi_hypergraph(10, 20, 0.1)
    assert H.number_of_nodes() == 10


def test_chung_lu_hypergraph():
    k1 = {1: 1, 2: 2, 3: 3, 4: 4}
    k2 = {1: 2, 2: 2, 3: 3, 4: 3}
    H = xgi.chung_lu_hypergraph(k1, k2)
    assert H.number_of_nodes() == 4

    with pytest.warns(Warning):
        k1 = {1: 1, 2: 2}
        k2 = {1: 2, 1: 2}
        H = xgi.chung_lu_hypergraph(k1, k2)
