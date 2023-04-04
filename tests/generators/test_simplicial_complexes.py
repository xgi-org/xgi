import networkx as nx

import xgi
from xgi.exception import XGIError


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
