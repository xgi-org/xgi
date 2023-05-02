from math import comb

import pytest

import xgi


def test_empty_hypergraph():
    H = xgi.empty_hypergraph()
    assert (H.num_nodes, H.num_edges) == (0, 0)


def test_empty_simplicial_complex():
    SC = xgi.empty_simplicial_complex()
    assert (SC.num_nodes, SC.num_edges) == (0, 0)


def test_trivial_hypergraph():
    H = xgi.trivial_hypergraph()
    assert (H.num_nodes, H.num_edges) == (1, 0)

    H = xgi.trivial_hypergraph(n=1)
    assert (H.num_nodes, H.num_edges) == (1, 0)

    H = xgi.trivial_hypergraph(n=2)
    assert (H.num_nodes, H.num_edges) == (2, 0)


def test_complete_hypergraph():

    N = 4

    # single order
    H1 = xgi.complete_hypergraph(N=N, order=1)
    H2 = xgi.complete_hypergraph(N=N, order=2)
    H3 = xgi.complete_hypergraph(N=N, order=3)
    H03 = xgi.complete_hypergraph(N=N, order=3, include_singletons=True)

    assert H3._edge == H03._edge

    assert H1.edges.members() == [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}]
    assert H2.edges.members() == [{0, 1, 2}, {0, 1, 3}, {0, 2, 3}, {1, 2, 3}]
    assert H3.edges.members() == [{0, 1, 2, 3}]

    assert xgi.unique_edge_sizes(H1) == [2]
    assert xgi.unique_edge_sizes(H2) == [3]
    assert xgi.unique_edge_sizes(H3) == [4]

    assert H1.num_edges == comb(N, 2)
    assert H2.num_edges == comb(N, 3)
    assert H3.num_edges == comb(N, 4)

    # max_order
    H1 = xgi.complete_hypergraph(N=N, max_order=1)
    H2 = xgi.complete_hypergraph(N=N, max_order=2)
    H3 = xgi.complete_hypergraph(N=N, max_order=3)
    H03 = xgi.complete_hypergraph(N=N, max_order=3, include_singletons=True)

    assert xgi.unique_edge_sizes(H1) == [2]
    assert xgi.unique_edge_sizes(H2) == [2, 3]
    assert xgi.unique_edge_sizes(H3) == [2, 3, 4]
    assert xgi.unique_edge_sizes(H03) == [1, 2, 3, 4]

    assert H1.num_edges == comb(N, 2)
    assert H2.num_edges == comb(N, 2) + comb(N, 3)
    assert H3.num_edges == comb(N, 2) + comb(N, 3) + comb(N, 4)
    assert H03.num_edges == comb(N, 2) + comb(N, 3) + comb(N, 4) + N

    # errors
    with pytest.raises(ValueError):
        H1 = xgi.complete_hypergraph(N=N, order=1, max_order=2)

    with pytest.raises(ValueError):
        H1 = xgi.complete_hypergraph(N=N, order=None, max_order=None)
