import xgi

def test_empty_hypergraph():
    H = xgi.empty_hypergraph()
    assert H.shape == (0, 0)
