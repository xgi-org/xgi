from networkx import DiGraph

import xgi


def test_to_encapsulation_dag(edgelist1, edgelist8, hypergraph1, hypergraph2):

    H = xgi.Hypergraph(edgelist1)
    for subset_types in ["all", "immediate", "empirical"]:
        L = xgi.to_encapsulation_dag(H, subset_types=subset_types)
        assert isinstance(L, DiGraph)
        assert set(L.nodes) == set(list(range(4)))
        assert len(L.edges) == 0

    H = xgi.Hypergraph(edgelist8)
    L = xgi.to_encapsulation_dag(H, subset_types="immediate")
    assert isinstance(L, DiGraph)
    assert set(L.nodes) == set(list(range(9)))
    assert len(L.edges) == 1
    assert len(L[3]) == 0
    assert len(list(L.predecessors(0))) == 1
    assert len(list(L.successors(1))) == 1

    L = xgi.to_encapsulation_dag(H, subset_types="empirical")
    assert isinstance(L, DiGraph)
    assert set(L.nodes) == set(list(range(9)))
    assert len(L.edges) == 4
    assert len(L[3]) == 3
    assert len(list(L.predecessors(0))) == 1
    assert len(list(L.successors(1))) == 1

    H = xgi.Hypergraph(edgelist8)
    L = xgi.to_encapsulation_dag(H)

    assert isinstance(L, DiGraph)
    assert set(L.nodes) == set(list(range(9)))
    assert len(L.edges) == 5
    assert len(L[3]) == 4
    assert len(list(L.predecessors(0))) == 2

    L = xgi.to_encapsulation_dag(H, subset_types="immediate")
    assert isinstance(L, DiGraph)
    assert set(L.nodes) == set(list(range(9)))
    assert len(L.edges) == 1
    assert len(L[3]) == 0
    assert len(list(L.predecessors(0))) == 1
    assert len(list(L.successors(1))) == 1

    L = xgi.to_encapsulation_dag(H, subset_types="empirical")
    assert isinstance(L, DiGraph)
    assert set(L.nodes) == set(list(range(9)))
    assert len(L.edges) == 4
    assert len(L[3]) == 3
    assert len(list(L.predecessors(0))) == 1
    assert len(list(L.successors(1))) == 1

    L = xgi.to_encapsulation_dag(hypergraph1)
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [e for e in L.edges] == [("e2", "e1"), ("e2", "e3")]

    L = xgi.to_encapsulation_dag(hypergraph2)
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [e for e in L.edges] == [("e3", "e1"), ("e3", "e2")]

    H = xgi.Hypergraph()
    L = xgi.to_encapsulation_dag(H)

    assert L.number_of_nodes() == 0
    assert L.number_of_edges() == 0

    H.add_nodes_from([0, 1, 2])
    L = xgi.to_encapsulation_dag(H)

    assert L.number_of_nodes() == 0
    assert L.number_of_edges() == 0
