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

    # id temp already exists
    H = xgi.node_swap(H0, 2, 5, id_temp=1)
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

    # errors raised
    with pytest.raises(ValueError):
        H = xgi.node_swap(H0, 7, 5)  # 7 not in H
    with pytest.raises(ValueError):
        H = xgi.node_swap(H0, 2, 5, order=1)  # 2 not in pairwise
    with pytest.raises(ValueError):
        H = xgi.node_swap(H0, 7, 5, order=10)


def test_random_edge_shuffle():
    # trivial hypergraph
    H0 = xgi.trivial_hypergraph()
    with pytest.raises(ValueError):
        H = xgi.random_edge_shuffle(H0)

    # hypergraph with only two edges
    S = xgi.Hypergraph([[0, 1, 2, 3], [2, 3, 5, 6, 8]])
    H = S.copy()
    xgi.random_edge_shuffle(H)

    # the intersection of the two edges is preserved
    assert {2, 3}.issubset(H._edge[0])
    assert {2, 3}.issubset(H._edge[1])

    # edge sizes are preserved
    assert len(H._edge[0]) == len(S._edge[0])
    assert len(H._edge[1]) == len(S._edge[1])

    # hypergraph with more than two edges
    S = xgi.Hypergraph([[0, 1, 2, 3], [2, 3, 5, 6, 8], [1, 2, 3, 4, 5]])
    H = S.copy()

    # specify edges to shuffle
    xgi.random_edge_shuffle(H, e_id1=0, e_id2=2)

    # not shuffled edges are preserved
    assert H._edge[1] == S._edge[1]

    # the intersection of the two edges is preserved
    assert {1, 2, 3}.issubset(H._edge[0])
    assert {1, 2, 3}.issubset(H._edge[2])

    # edge sizes are preserved
    for edge_id in H._edge:
        assert len(H._edge[edge_id]) == len(S._edge[edge_id])

    # random hypergraph
    S = xgi.random_hypergraph(50, [0.1, 0.01, 0.001], seed=1)
    H = S.copy()
    xgi.random_edge_shuffle(H)

    # number of nodes and edges are preserved
    assert H.num_nodes == S.num_nodes
    assert H.num_edges == S.num_edges

    # all edge sizes are preserved
    for edge_id in H._edge:
        assert len(H._edge[edge_id]) == len(S._edge[edge_id])

    # all node degrees are preserved
    for node_id in H._node:
        assert len(H._node[node_id]) == len(S._node[node_id])


def test_run_markov_chain():
    # random hypergraph
    S = xgi.random_hypergraph(50, [0.1, 0.01, 0.001], seed=1)
    metrics = xgi.run_markov_chain(S, 100, 10, xgi.num_edges_order)

    # correct number of metrics
    assert len(metrics) == 10

    # last metric in list is the same as the current metric
    assert metrics[-1] == xgi.num_edges_order(S)
