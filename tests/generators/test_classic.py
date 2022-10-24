import networkx as nx
import pytest

import xgi
from xgi.exception import XGIError


def test_empty_hypergraph():
    H = xgi.empty_hypergraph()
    assert (H.num_nodes, H.num_edges) == (0, 0)


def test_empty_hypergraph():
    SC = xgi.empty_simplicial_complex()
    assert (SC.num_nodes, SC.num_edges) == (0, 0)


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
    assert xgi.max_edge_order(H) == 3


def test_flag_complex():
    edges = [[0, 1], [1, 2], [2, 0], [0, 3]]
    G = nx.Graph(edges)

    S = xgi.flag_complex(G)

    simplices_2 = [
        frozenset({0, 1}),
        frozenset({0, 2}),
        frozenset({0, 3}),
        frozenset({1, 2}),
    ]

    simplices_3 = simplices_2 + [frozenset({0, 1, 2})]

    assert S.edges.members() == simplices_3

    S1 = xgi.flag_complex(G, ps=[1], seed=42)
    S2 = xgi.flag_complex(G, ps=[0.5], seed=42)
    S3 = xgi.flag_complex(G, ps=[0], seed=42)

    assert S1.edges.members() == simplices_3
    assert S2.edges.members() == simplices_2
    assert S3.edges.members() == simplices_2


def test_ring_lattice():
    H = xgi.ring_lattice(5, 2, 2, 0)
    assert H.num_nodes == 5
    assert H.num_edges == 5
    assert xgi.unique_edge_sizes(H) == [2]

    H = xgi.ring_lattice(5, 3, 4, 1)
    edges = H.edges.members()
    for i in range(H.num_edges - 1):
        assert len(set(edges[i]).intersection(set(edges[i + 1]))) == 2  # d-l
    assert xgi.unique_edge_sizes(H) == [3]

    # k < 2 test
    with pytest.warns(Warning):
        H = xgi.ring_lattice(5, 2, 1, 0)
    assert H.num_nodes == 5
    assert H.num_edges == 0

    # k % 2 != 0 test
    with pytest.warns(Warning):
        xgi.ring_lattice(5, 2, 3, 0)

    # k < 0 test
    with pytest.raises(XGIError):
        xgi.ring_lattice(5, 2, -1, 0)


def test_sunflower():
    with pytest.raises(XGIError):
        H = xgi.sunflower(3, 4, 2)

    H = xgi.sunflower(3, 1, 5)

    assert H.nodes.memberships(0) == {0, 1, 2}
    assert set(H.nodes) == set(range(13))
    assert H.num_edges == 3
    for n in range(1, H.num_nodes):
        assert len(H.nodes.memberships(n)) == 1

    H = xgi.sunflower(4, 3, 6)
    for i in range(3):
        H.nodes.memberships(i) == {0, 1, 2, 3}

    assert H.num_nodes == 15

    for i in range(3, 15):
        assert len(H.nodes.memberships(i)) == 1

