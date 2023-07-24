import pytest

import xgi
from xgi.exception import XGIError


def test_to_bipartite_graph(edgelist1, edgelist3, edgelist4):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist3)
    H3 = xgi.Hypergraph(edgelist4)

    true_bi_el1 = [
        [1, 0],
        [2, 0],
        [3, 0],
        [4, 1],
        [5, 2],
        [6, 2],
        [6, 3],
        [7, 3],
        [8, 3],
    ]
    true_bi_el2 = [[1, 0], [2, 0], [3, 0], [3, 1], [4, 1], [4, 2], [5, 2], [6, 2]]
    true_bi_el3 = [
        [1, 0],
        [2, 0],
        [3, 0],
        [2, 1],
        [3, 1],
        [4, 1],
        [5, 1],
        [3, 2],
        [4, 2],
        [5, 2],
    ]

    G1, node_dict, edge_dict = xgi.to_bipartite_graph(H1, index=True)
    bi_el1 = [[node_dict[u], edge_dict[v]] for u, v in G1.edges]
    assert sorted(bi_el1) == sorted(true_bi_el1)
    assert G1.edges() == xgi.to_bipartite_graph(H1, index=False).edges()

    G2, node_dict, edge_dict = xgi.to_bipartite_graph(H2, index=True)
    bi_el2 = [[node_dict[u], edge_dict[v]] for u, v in G2.edges]
    assert sorted(bi_el2) == sorted(true_bi_el2)
    assert G2.edges() == xgi.to_bipartite_graph(H2, index=False).edges()

    G3, node_dict, edge_dict = xgi.to_bipartite_graph(H3, index=True)
    bi_el3 = [[node_dict[u], edge_dict[v]] for u, v in G3.edges]
    assert sorted(bi_el3) == sorted(true_bi_el3)
    assert G3.edges() == xgi.to_bipartite_graph(H3, index=False).edges()


def test_from_bipartite_graph(
    bipartite_graph1, bipartite_graph2, bipartite_graph3, bipartite_graph4
):
    H = xgi.from_bipartite_graph(bipartite_graph1)

    assert set(H.nodes) == {1, 2, 3, 4}
    assert set(H.edges) == {"a", "b", "c"}
    assert H.edges.members("a") == {1, 4}
    assert H.edges.members("b") == {1, 2}
    assert H.edges.members("c") == {2, 3}

    H = xgi.from_bipartite_graph(bipartite_graph1, dual=True)

    assert set(H.nodes) == {"a", "b", "c"}
    assert set(H.edges) == {1, 2, 3, 4}
    assert H.edges.members(1) == {"a", "b"}
    assert H.edges.members(2) == {"b", "c"}
    assert H.edges.members(3) == {"c"}
    assert H.edges.members(4) == {"a"}

    # incorrect bipartite label
    with pytest.raises(XGIError):
        H = xgi.from_bipartite_graph(bipartite_graph2, dual=True)

    # no bipartite label
    with pytest.raises(XGIError):
        H = xgi.from_bipartite_graph(bipartite_graph3, dual=True)

    # not bipartite
    with pytest.raises(XGIError):
        H = xgi.from_bipartite_graph(bipartite_graph4, dual=True)
