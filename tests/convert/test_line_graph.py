from networkx import Graph

import xgi


def test_to_line_graph(edgelist1, hypergraph1):
    H = xgi.Hypergraph(edgelist1)
    L = xgi.to_line_graph(H)

    assert isinstance(L, Graph)
    assert set(L.nodes) == {0, 1, 2, 3}
    assert [set(e) for e in L.edges] == [{2, 3}]

    L = xgi.to_line_graph(hypergraph1)
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == [{"e1", "e2"}, {"e2", "e3"}]

    L = xgi.to_line_graph(hypergraph1, s=2)
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == [{"e1", "e2"}]

    L = xgi.to_line_graph(hypergraph1, s=3)
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == []

    H = xgi.Hypergraph()
    L = xgi.to_line_graph(H)

    assert L.number_of_nodes() == 0
    assert L.number_of_edges() == 0

    H.add_nodes_from([0, 1, 2])
    L = xgi.to_line_graph(H)

    assert L.number_of_nodes() == 0
    assert L.number_of_edges() == 0
