import networkx as nx
import pytest

import xgi
from xgi.exception import IDNotFound, XGIError


def test_iddict(edgelist1):
    H = xgi.Hypergraph()
    with pytest.raises(IDNotFound):
        H.nodes[0]
    with pytest.raises(IDNotFound):
        H.edges[0]

    H = xgi.Hypergraph(edgelist1)
    with pytest.raises(IDNotFound):
        H.nodes[0]
    with pytest.raises(IDNotFound):
        H.edges[4]

    assert H.edges[0] == dict()

    with pytest.raises(XGIError):
        H._edge[None] = {1, 2, 3}

    with pytest.raises(IDNotFound):
        del H._node["test"]

    with pytest.raises(TypeError):
        H._node[[0, 1, 2]] = [0, 1]


def test_neighbors():
    H = xgi.Hypergraph()
    with pytest.raises(IDNotFound):
        H.nodes.neighbors(0)
    with pytest.raises(IDNotFound):
        H.remove_node(0)
    with pytest.raises(IDNotFound):
        H.remove_edge(0)


def test_dual_dict(dict5):
    dual = xgi.dual_dict(dict5)
    assert dual[0] == {0}
    assert dual[1] == {0}
    assert dual[2] == {0}
    assert dual[3] == {0}
    assert dual[4] == {1}
    assert dual[5] == {2}
    assert dual[6] == {2, 3}
    assert dual[7] == {3}
    assert dual[8] == {3}


def test_powerset():
    edge = [1, 2, 3, 4]

    PS = xgi.powerset(edge)
    PS1 = xgi.powerset(edge, include_empty=True)
    PS2 = xgi.powerset(edge, include_empty=True, include_full=True)

    out = [
        (1,),
        (2,),
        (3,),
        (4,),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
        (1, 2, 3),
        (1, 2, 4),
        (1, 3, 4),
        (2, 3, 4),
    ]

    assert list(PS) == out
    assert list(PS1) == [()] + out
    assert list(PS2) == [()] + out + [tuple(edge)]


def test_find_triangles():
    G = nx.erdos_renyi_graph(20, 0.2, seed=0)
    triangles = xgi.find_triangles(G)

    cliques = [
        {8, 9, 17},
        {8, 9, 19},
        {9, 16, 19},
        {8, 13, 17},
        {6, 17, 18},
        {2, 6, 12},
        {7, 8, 13},
        {2, 6, 18},
    ]

    num_tri = sum(nx.triangles(G).values()) / 3

    assert triangles == cliques
    assert num_tri == len(cliques)
