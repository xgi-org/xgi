import pytest

import xgi
from xgi.exception import XGIError


def test_edge_members(edgelist3):
    H = xgi.Hypergraph(edgelist3)
    assert H.edges.members() == [[1, 2, 3], [3, 4], [4, 5, 6]]
    assert H.edges.members(dtype=dict) == {0: [1, 2, 3], 1: [3, 4], 2: [4, 5, 6]}
