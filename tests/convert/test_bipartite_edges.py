import pytest

import xgi
from xgi.exception import XGIError


def test_to_bipartite_edges(edgelist2, diedgelist1):
    H = xgi.Hypergraph(edgelist2)
    el = xgi.to_bipartite_edgelist(H)
    edgelist = [(1, 0), (2, 0), (3, 1), (4, 1), (4, 2), (5, 2), (6, 2)]
    assert sorted(el) == edgelist

    H = xgi.DiHypergraph(diedgelist1)
    el = xgi.to_bipartite_edgelist(H)
    edgelist = [
        (1, 0, "in"),
        (2, 0, "in"),
        (3, 0, "in"),
        (4, 0, "out"),
        (5, 1, "in"),
        (6, 1, "in"),
        (6, 1, "out"),
        (7, 1, "out"),
        (8, 1, "out"),
    ]
    assert sorted(el) == edgelist


def test_from_bipartite_edges(edgelist2, diedgelist1):
    # undirected
    edgelist = [(1, 0), (2, 0), (3, 1), (4, 1), (4, 2), (5, 2), (6, 2)]
    H1 = xgi.from_bipartite_edgelist(edgelist)

    H2 = xgi.Hypergraph(edgelist2)
    assert H1.edges.members(dtype=dict) == H2.edges.members(dtype=dict)

    # directed
    edgelist = [
        (1, 0, "in"),
        (2, 0, "in"),
        (3, 0, "in"),
        (4, 0, "out"),
        (5, 1, "in"),
        (6, 1, "in"),
        (6, 1, "out"),
        (7, 1, "out"),
        (8, 1, "out"),
    ]

    H1 = xgi.from_bipartite_edgelist(edgelist)

    H2 = xgi.DiHypergraph(diedgelist1)
    assert H1.edges.dimembers(dtype=dict) == H2.edges.dimembers(dtype=dict)

    # test error
    edgelist = [
        (1, 0, "in", "test"),
        (2, 0, "in"),
        (3, 0, "in"),
        (4, 0, "out"),
    ]
    with pytest.raises(XGIError):
        H = xgi.from_bipartite_edgelist(edgelist)
