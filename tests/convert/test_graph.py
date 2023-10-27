import xgi


def test_to_graph(edgelist2, edgelist5):
    H1 = xgi.Hypergraph(edgelist2)
    H2 = xgi.Hypergraph(edgelist5)

    G1 = xgi.to_graph(H1)
    assert set(G1.nodes) == {1, 2, 3, 4, 5, 6}
    assert set(G1.edges) == {(1, 2), (3, 4), (4, 5), (4, 6), (5, 6)}

    G2 = xgi.to_graph(H2)
    assert set(G2.nodes) == {0, 1, 2, 3, 4, 5, 6, 7, 8}
    assert {frozenset(e) for e in G2.edges} == {
        frozenset({0, 1}),
        frozenset({0, 2}),
        frozenset({0, 3}),
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({2, 3}),
        frozenset({5, 6}),
        frozenset({6, 7}),
        frozenset({6, 8}),
        frozenset({7, 8}),
    }
