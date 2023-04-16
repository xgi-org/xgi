import xgi


def test_empty_hypergraph():
    H = xgi.empty_hypergraph()
    assert (H.num_nodes, H.num_edges) == (0, 0)


def test_empty_hypergraph():
    SC = xgi.empty_simplicial_complex()
    assert (SC.num_nodes, SC.num_edges) == (0, 0)


def test_trivial_hypergraph():
    H = xgi.trivial_hypergraph()
    assert (H.num_nodes, H.num_edges) == (1, 0)

    H = xgi.trivial_hypergraph(n=1)
    assert (H.num_nodes, H.num_edges) == (1, 0)

    H = xgi.trivial_hypergraph(n=2)
    assert (H.num_nodes, H.num_edges) == (2, 0)
