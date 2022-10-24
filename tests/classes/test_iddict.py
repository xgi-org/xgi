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
