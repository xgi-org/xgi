import xgi


def test_empty_hypergraph():
    H = xgi.empty_hypergraph()
    assert (H.number_of_nodes(), H.number_of_edges()) == (0, 0)
