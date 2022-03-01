import xgi
import pytest

from xgi.exception import XGIError


def test_chung_lu_hypergraph():
    k1 = {1: 1, 2: 2, 3: 3, 4: 4}
    k2 = {1: 2, 2: 2, 3: 3, 4: 3}
    H = xgi.chung_lu_hypergraph(k1, k2)
    assert H.num_nodes == 4

    with pytest.warns(Warning):
        k1 = {1: 1, 2: 2}
        k2 = {1: 2, 1: 2}
        H = xgi.chung_lu_hypergraph(k1, k2)
