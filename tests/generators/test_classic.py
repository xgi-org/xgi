import pytest
import xgi


def test_empty_hypergraph():
    H = xgi.empty_hypergraph()
    assert H.shape == (0, 0)

def test_star_clique(): 

    with pytest.raises(ValueError):
        H = xgi.erdos_renyi_hypergraph(-1, 7, 3)
    with pytest.raises(ValueError):
        H = xgi.erdos_renyi_hypergraph(6, -1, 3)
    with pytest.raises(ValueError):
        H = xgi.erdos_renyi_hypergraph(6, 7, -1)
    with pytest.raises(ValueError):
        H = xgi.erdos_renyi_hypergraph(6, 7, 7)

    H = xgi.erdos_renyi_hypergraph(6, 7, 3)
    assert H.number_of_nodes() == 13
