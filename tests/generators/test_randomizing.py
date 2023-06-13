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
    for order in [1, 2, 3]: # number of edges is preserved
        assert xgi.num_edges_order(H, order) == xgi.num_edges_order(S, order)
    for order in [2, 3]: # orders not shuffled unchanged
        assert H.edges.filterby("order", order).members(dtype=dict) == S.edges.filterby("order", order).members(dtype=dict)
    # order shuffled changed 
    assert H.edges.filterby("order", 1).members(dtype=dict) != S.edges.filterby("order", 1).members(dtype=dict)

    # p < 1
    H = xgi.shuffle_hyperedges(S, order=1, p=0.5)
    assert not isinstance(H, xgi.SimplicialComplex)
    assert isinstance(H, xgi.Hypergraph)
    assert H.num_nodes == S.num_nodes
    for order in [1, 2, 3]: # number of edges is preserved
        assert xgi.num_edges_order(H, order) == xgi.num_edges_order(S, order)
    for order in [2, 3]: # orders not shuffled unchanged
        assert H.edges.filterby("order", order).members(dtype=dict) == S.edges.filterby("order", order).members(dtype=dict)
    # order shuffled changed 
    assert H.edges.filterby("order", 1).members(dtype=dict) != S.edges.filterby("order", 1).members(dtype=dict)

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
    for order in [1, 2, 3]: # number of edges is preserved
        assert xgi.num_edges_order(H, order) == xgi.num_edges_order(S, order)
    for order in [1, 3]: # orders not shuffled unchanged
        assert H.edges.filterby("order", order).members(dtype=dict) == S.edges.filterby("order", order).members(dtype=dict)
    # order shuffled changed 
    assert H.edges.filterby("order", 2).members(dtype=dict) != S.edges.filterby("order", 1).members(dtype=dict)

    # errors raised
    with pytest.raises(ValueError):
        H = xgi.shuffle_hyperedges(S, order=1, p=1.1)
    with pytest.raises(ValueError):
        H = xgi.shuffle_hyperedges(S, order=1, p=-0.5)
    with pytest.raises(ValueError):
        H = xgi.shuffle_hyperedges(S, order=10, p=1)
