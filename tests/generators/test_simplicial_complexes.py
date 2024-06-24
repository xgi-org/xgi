import networkx as nx
import pytest

import xgi


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

    # ps
    S1 = xgi.flag_complex(G, ps=[1], seed=42)
    S2 = xgi.flag_complex(G, ps=[0.5], seed=42)
    S3 = xgi.flag_complex(G, ps=[0], seed=42)

    assert S1.edges.members() == simplices_3
    assert S2.edges.members() == simplices_2
    assert S3.edges.members() == simplices_2

    # complete graph
    G1 = nx.complete_graph(4)
    S4 = xgi.flag_complex(G1)
    S5 = xgi.flag_complex(G1, ps=[1])
    assert S4.num_nodes == S5.num_nodes
    assert S4.num_edges == S5.num_edges
    assert set(S4.edges.members()) == set(S5.edges.members())


def test_flag_complex_d2():
    G = nx.erdos_renyi_graph(15, 0.3, seed=3)

    S = xgi.flag_complex(G, max_order=2)
    S2 = xgi.flag_complex_d2(G)

    assert set(S.edges.members()) == set(S2.edges.members())


def test_random_simplicial_complex():
    # seed
    S1 = xgi.random_simplicial_complex(10, [0.1, 0.001], seed=1)
    S2 = xgi.random_simplicial_complex(10, [0.1, 0.001], seed=2)
    S3 = xgi.random_simplicial_complex(10, [0.1, 0.001], seed=2)

    assert S1._edge != S2._edge
    assert S2._edge == S3._edge

    # wrong input
    with pytest.raises(ValueError):
        S1 = xgi.random_simplicial_complex(10, [1, 1.1])
    with pytest.raises(ValueError):
        S1 = xgi.random_simplicial_complex(10, [1, -2])


def test_random_flag_complex():

    S = xgi.random_flag_complex(10, 0.4, seed=2)
    simplices = {
        frozenset({0, 4}),
        frozenset({0, 7}),
        frozenset({1, 8}),
        frozenset({2, 5}),
        frozenset({2, 9}),
        frozenset({3, 5}),
        frozenset({3, 6}),
        frozenset({3, 7}),
        frozenset({3, 8}),
        frozenset({4, 5}),
        frozenset({4, 7}),
        frozenset({4, 8}),
        frozenset({6, 7}),
        frozenset({6, 8}),
        frozenset({7, 8}),
        frozenset({0, 4, 7}),
        frozenset({3, 6, 7}),
        frozenset({3, 6, 8}),
        frozenset({3, 7, 8}),
        frozenset({4, 7, 8}),
        frozenset({6, 7, 8}),
    }

    assert set(S.edges.members()) == simplices

    # max_order
    S = xgi.random_flag_complex(10, 0.4, seed=2, max_order=3)
    assert set(S.edges.members()) == simplices.union({frozenset({3, 6, 7, 8})})

    # seed
    S1 = xgi.random_flag_complex(10, 0.1, seed=1)
    S2 = xgi.random_flag_complex(10, 0.1, seed=2)
    S3 = xgi.random_flag_complex(10, 0.1, seed=2)

    assert S1._edge != S2._edge
    assert S2._edge == S3._edge

    # wrong input
    with pytest.raises(ValueError):
        S1 = xgi.random_flag_complex(10, 1.1)
    with pytest.raises(ValueError):
        S1 = xgi.random_flag_complex(10, -2)


def test_random_flag_complex_d2():

    S = xgi.random_flag_complex_d2(10, 0.4, seed=2)
    simplices = {
        frozenset({0, 4}),
        frozenset({0, 7}),
        frozenset({1, 8}),
        frozenset({2, 5}),
        frozenset({2, 9}),
        frozenset({3, 5}),
        frozenset({3, 6}),
        frozenset({3, 7}),
        frozenset({3, 8}),
        frozenset({4, 5}),
        frozenset({4, 7}),
        frozenset({4, 8}),
        frozenset({6, 7}),
        frozenset({6, 8}),
        frozenset({7, 8}),
        frozenset({0, 4, 7}),
        frozenset({3, 6, 7}),
        frozenset({3, 6, 8}),
        frozenset({3, 7, 8}),
        frozenset({4, 7, 8}),
        frozenset({6, 7, 8}),
    }

    assert set(S.edges.members()) == simplices

    # consistency with other function
    S = xgi.random_flag_complex(10, 0.4, seed=3, max_order=2)
    S0 = xgi.random_flag_complex_d2(10, 0.4, seed=3)
    assert set(S.edges.members()) == set(S0.edges.members())

    # seed
    S1 = xgi.random_flag_complex_d2(10, 0.1, seed=1)
    S2 = xgi.random_flag_complex_d2(10, 0.1, seed=2)
    S3 = xgi.random_flag_complex_d2(10, 0.1, seed=2)

    assert S1._edge != S2._edge
    assert S2._edge == S3._edge

    # wrong input
    with pytest.raises(ValueError):
        S1 = xgi.random_flag_complex_d2(10, 1.1)
    with pytest.raises(ValueError):
        S1 = xgi.random_flag_complex_d2(10, -2)
