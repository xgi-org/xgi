import xgi


def test_empty_hypergraph():
    H = xgi.empty_hypergraph()
    assert (H.num_nodes, H.num_edges) == (0, 0)
