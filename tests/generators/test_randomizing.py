import pytest

import xgi


def test_shuffle_hyperedges():
    # trivial hypergraph
    H0 = xgi.trivial_hypergraph()
    with pytest.raises(ValueError):
        H = xgi.shuffle_hyperedges(H0, order=1, p=1)

    # random simplicial complex
    S = xgi.random_simplicial_complex(50, [0.1, 0.01, 0.001], seed=1)
    H = xgi.shuffle_hyperedges(S, order=1, p=1)

    assert not isinstance(H, xgi.SimplicialComplex)
    assert isinstance(H, xgi.Hypergraph)
    assert H.num_nodes == S.num_nodes
    for order in [1, 2, 3]:  # number of edges is preserved
        assert xgi.num_edges_order(H, order) == xgi.num_edges_order(S, order)
    for order in [2, 3]:  # orders not shuffled unchanged
        assert H.edges.filterby("order", order).members(dtype=dict) == S.edges.filterby(
            "order", order
        ).members(dtype=dict)
    # order shuffled changed
    assert H.edges.filterby("order", 1).members(dtype=dict) != S.edges.filterby(
        "order", 1
    ).members(dtype=dict)

    # p < 1
    H = xgi.shuffle_hyperedges(S, order=1, p=0.5)
    assert not isinstance(H, xgi.SimplicialComplex)
    assert isinstance(H, xgi.Hypergraph)
    assert H.num_nodes == S.num_nodes
    for order in [1, 2, 3]:  # number of edges is preserved
        assert xgi.num_edges_order(H, order) == xgi.num_edges_order(S, order)
    for order in [2, 3]:  # orders not shuffled unchanged
        assert H.edges.filterby("order", order).members(dtype=dict) == S.edges.filterby(
            "order", order
        ).members(dtype=dict)
    # order shuffled changed
    assert H.edges.filterby("order", 1).members(dtype=dict) != S.edges.filterby(
        "order", 1
    ).members(dtype=dict)

    # p=0, unchanged
    H = xgi.shuffle_hyperedges(S, order=1, p=0)
    assert not isinstance(H, xgi.SimplicialComplex)
    assert isinstance(H, xgi.Hypergraph)
    assert H.num_nodes == S.num_nodes
    assert H._edge == S._edge

    # order 2
    H = xgi.shuffle_hyperedges(S, order=2, p=1)

    assert not isinstance(H, xgi.SimplicialComplex)
    assert isinstance(H, xgi.Hypergraph)
    assert H.num_nodes == S.num_nodes
    for order in [1, 2, 3]:  # number of edges is preserved
        assert xgi.num_edges_order(H, order) == xgi.num_edges_order(S, order)
    for order in [1, 3]:  # orders not shuffled unchanged
        assert H.edges.filterby("order", order).members(dtype=dict) == S.edges.filterby(
            "order", order
        ).members(dtype=dict)
    # order shuffled changed
    assert H.edges.filterby("order", 2).members(dtype=dict) != S.edges.filterby(
        "order", 1
    ).members(dtype=dict)

    # errors raised
    with pytest.raises(ValueError):
        H = xgi.shuffle_hyperedges(S, order=1, p=1.1)
    with pytest.raises(ValueError):
        H = xgi.shuffle_hyperedges(S, order=1, p=-0.5)
    with pytest.raises(ValueError):
        H = xgi.shuffle_hyperedges(S, order=10, p=1)


def test_node_swap(edgelist8):

    H0 = xgi.Hypergraph(edgelist8)
    edges_orig = dict(H0._edge)

    H = xgi.node_swap(H0, 2, 5)  # all orders
    edges_new = {
        0: {0, 1},
        1: {0, 1, 5},
        2: {0, 5, 3},
        3: {0, 1, 5, 3, 4},
        4: {5, 4, 2},
        5: {1, 3, 2},
        6: {0, 3, 4},
        7: {1, 6},
        8: {0, 6},
    }
    assert H._edge == edges_new

    # original is not modified
    assert H0._edge == edges_orig

    # edges containing neither swapped node are unchanged
    assert H._edge[0] == H0._edge[0]  # {0, 1}
    assert H._edge[6] == H0._edge[6]  # {0, 3, 4}
    assert H._edge[7] == H0._edge[7]  # {1, 6}

    # edge containing both swapped nodes is unchanged (swap is self-inverse on that edge)
    assert H._edge[4] == H0._edge[4]  # {2, 4, 5}: 2<->5 leaves the set identical

    # selected order
    H = xgi.node_swap(H0, 2, 5, order=2)
    edges_new = {
        0: {0, 1},
        1: {0, 1, 5},
        2: {0, 5, 3},
        3: {0, 1, 2, 3, 4},
        4: {5, 4, 2},
        5: {1, 3, 2},
        6: {0, 3, 4},
        7: {1, 6},
        8: {0, 6},
    }
    assert H._edge == edges_new

    # node attributes are preserved after swap
    H0_attrs = xgi.Hypergraph(edgelist8)
    H0_attrs.nodes[2]["color"] = "red"
    H0_attrs.nodes[5]["color"] = "blue"
    H_attrs = xgi.node_swap(H0_attrs, 2, 5)
    assert H_attrs.nodes[2]["color"] == "red"
    assert H_attrs.nodes[5]["color"] == "blue"

    # symmetry: swapping A,B then B,A returns the original edges
    H_twice = xgi.node_swap(xgi.node_swap(H0, 2, 5), 2, 5)
    assert H_twice._edge == edges_orig

    # errors raised
    with pytest.raises(ValueError):
        H = xgi.node_swap(H0, 7, 5)  # 7 not in H
    with pytest.raises(ValueError):
        H = xgi.node_swap(H0, 2, 5, order=1)  # 2 not in pairwise
    with pytest.raises(ValueError):
        H = xgi.node_swap(H0, 7, 5, order=10)
