import xgi
from xgi.exception import XGIError
import pytest


def test_uniform_configuration_model_hypergraph():
    m = 3
    k = {1: 1, 2: 2, 3: 3, 4: 3}
    H = xgi.uniform_hypergraph_configuration_model(k, m)
    assert H.number_of_nodes() == 4
    assert dict(H.degree) == k
    assert H.number_of_edges() == 3

    with pytest.warns(Warning):
        m = 3
        k = {1: 1, 2: 6}
        H = xgi.uniform_hypergraph_configuration_model(k, m)
    assert sum(dict(H.degree).values()) % m == 0
