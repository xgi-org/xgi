import pytest

import xgi
from xgi.exception import IDNotFound


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


def test_neighbors():
    H = xgi.Hypergraph()
    with pytest.raises(IDNotFound):
        H.neighbors(0)
    with pytest.raises(IDNotFound):
        H.remove_node(0)
    with pytest.raises(IDNotFound):
        H.remove_edge(0)
