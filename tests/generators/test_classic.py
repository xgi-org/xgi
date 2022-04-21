import networkx as nx
import pytest
import xgi


def test_empty_hypergraph():
    H = xgi.empty_hypergraph()
    assert (H.num_nodes, H.num_edges) == (0, 0)


def test_star_clique():

    with pytest.raises(ValueError):
        H = xgi.star_clique(-1, 7, 3)
    with pytest.raises(ValueError):
        H = xgi.star_clique(6, -1, 3)
    with pytest.raises(ValueError):
        H = xgi.star_clique(6, 7, -1)
    with pytest.raises(ValueError):
        H = xgi.star_clique(6, 7, 7)

    H = xgi.star_clique(6, 7, 3)
    assert H.num_nodes == 13
    assert H.num_edges == 97
    assert H.max_edge_order() == 3


def test_flag_complex():
    edges = [[0, 1], [1, 2], [2, 0], [0, 3]]
    G = nx.Graph(edges)

    S = xgi.flag_complex(G)

    simplices = [
        frozenset({0, 1, 2}),
        frozenset({0, 1}),
        frozenset({0, 2}),
        frozenset({1, 2}),
        frozenset({0, 3}),
    ]

    assert S.edges.members() == simplices
