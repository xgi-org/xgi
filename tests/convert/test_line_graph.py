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


def test_557():
    H = xgi.Hypergraph(
        {
            0: [
                (6.019592999999995, 47.2350647),
                (6.019592999999853, 47.2350647),
                (6.01959299999999, 47.2350647),
                (6.019592999999993, 47.2350647),
                (6.0195929999999755, 47.2350647),
            ],
            1: [
                (6.019592999999995, 47.2350647),
                (6.019592999999853, 47.2350647),
                (6.01959299999999, 47.2350647),
                (6.019592999999993, 47.2350647),
                (6.0195929999999755, 47.2350647),
            ],
        }
    )
    L = xgi.to_line_graph(H)

    assert L.number_of_nodes() == 2
    assert L.number_of_edges() == 1


def test_abs_weighted_line_graph(edgelist1, hypergraph1, hypergraph2):
    H = xgi.Hypergraph(edgelist1)
    L = xgi.to_line_graph(H)

    L = xgi.to_line_graph(H, weights="absolute")
    assert isinstance(L, Graph)
    assert all(["weight" in dat for u, v, dat in L.edges(data=True)])
    assert set(L.nodes) == {0, 1, 2, 3}
    assert [set(e) for e in L.edges] == [{2, 3}]
    assert L.edges[(2, 3)]["weight"] == 1

    L = xgi.to_line_graph(hypergraph1, weights="absolute")
    assert isinstance(L, Graph)
    assert all(["weight" in dat for u, v, dat in L.edges(data=True)])
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == [{"e1", "e2"}, {"e2", "e3"}]
    assert L.edges[("e1", "e2")]["weight"] == 2
    assert L.edges[("e2", "e3")]["weight"] == 1
    assert sum([dat["weight"] for _, _, dat in L.edges(data=True)]) == 3

    L = xgi.to_line_graph(hypergraph1, s=2, weights="absolute")
    assert isinstance(L, Graph)
    assert all(["weight" in dat for u, v, dat in L.edges(data=True)])
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == [{"e1", "e2"}]
    assert L.edges[("e1", "e2")]["weight"] == 2
    assert sum([dat["weight"] for _, _, dat in L.edges(data=True)]) == 2

    L = xgi.to_line_graph(hypergraph2, weights="absolute")
    assert isinstance(L, Graph)
    assert all(["weight" in dat for u, v, dat in L.edges(data=True)])
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == [{"e1", "e2"}, {"e1", "e3"}, {"e2", "e3"}]
    assert L.edges[("e1", "e2")]["weight"] == 1
    assert L.edges[("e2", "e3")]["weight"] == 2
    assert L.edges[("e1", "e3")]["weight"] == 2
    assert sum([dat["weight"] for _, _, dat in L.edges(data=True)]) == 5

    L = xgi.to_line_graph(hypergraph2, s=2, weights="absolute")
    assert isinstance(L, Graph)
    assert all(["weight" in dat for u, v, dat in L.edges(data=True)])
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == [{"e1", "e3"}, {"e2", "e3"}]
    assert L.edges[("e2", "e3")]["weight"] == 2
    assert L.edges[("e1", "e3")]["weight"] == 2
    assert sum([dat["weight"] for _, _, dat in L.edges(data=True)]) == 4


def test_normed_weighted_line_graph(edgelist1, hypergraph1, edgelist2, hypergraph2):
    H = xgi.Hypergraph(edgelist1)
    L = xgi.to_line_graph(H)

    L = xgi.to_line_graph(H, weights="normalized")
    assert isinstance(L, Graph)
    assert all(["weight" in dat for u, v, dat in L.edges(data=True)])
    assert set(L.nodes) == {0, 1, 2, 3}
    assert [set(e) for e in L.edges] == [{2, 3}]
    assert L.edges[(2, 3)]["weight"] == 0.5

    L = xgi.to_line_graph(hypergraph1, weights="normalized")
    assert isinstance(L, Graph)
    assert all(["weight" in dat for u, v, dat in L.edges(data=True)])
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == [{"e1", "e2"}, {"e2", "e3"}]
    assert L.edges[("e1", "e2")]["weight"] == 1.0
    assert L.edges[("e2", "e3")]["weight"] == 1.0
    assert sum([dat["weight"] for _, _, dat in L.edges(data=True)]) == 2.0

    L = xgi.to_line_graph(hypergraph2, weights="normalized")
    assert isinstance(L, Graph)
    assert all(["weight" in dat for u, v, dat in L.edges(data=True)])
    assert set(L.nodes) == {"e1", "e2", "e3"}
    assert [set(e) for e in L.edges] == [{"e1", "e2"}, {"e1", "e3"}, {"e2", "e3"}]
    assert L.edges[("e1", "e2")]["weight"] == 0.5
    assert L.edges[("e2", "e3")]["weight"] == 1.0
    assert L.edges[("e1", "e3")]["weight"] == 1.0
    assert sum([dat["weight"] for _, _, dat in L.edges(data=True)]) == 2.5
