import pytest

import xgi
from xgi.exception import XGIError


def test_to_hypergraph_dict():
    H = xgi.Hypergraph()
    H.add_edges_from(
        [
            (["1", "2"], "edge1", {"weight": 2}),
            (["2", "3", "4"], "edge2", {"weight": 4}),
            (["1", "4"], "edge3", {"weight": -1}),
        ]
    )
    H.set_node_attributes(
        {
            "1": {"color": "blue"},
            "2": {"color": "yellow"},
            "3": {"color": "cyan"},
            "4": {"color": "green"},
        }
    )
    H["name"] = "test"
    H["author"] = "Nicholas Landry"

    d = xgi.to_hypergraph_dict(H)

    hd = {
        "type": "hypergraph",
        "hypergraph-data": {"name": "test", "author": "Nicholas Landry"},
        "node-data": {
            "1": {"color": "blue"},
            "2": {"color": "yellow"},
            "3": {"color": "cyan"},
            "4": {"color": "green"},
        },
        "edge-data": {
            "edge1": {"weight": 2},
            "edge2": {"weight": 4},
            "edge3": {"weight": -1},
        },
        "edge-dict": {
            "edge1": ["1", "2"],
            "edge2": ["2", "3", "4"],
            "edge3": ["1", "4"],
        },
    }

    assert hd == d

    # test that nodes that get cast to the same id
    # raises an error.
    H = xgi.Hypergraph()
    H.add_nodes_from(["2", 2])
    with pytest.raises(XGIError):
        xgi.to_hypergraph_dict(H)

    # test that edges that get cast to the same id
    # raises an error.
    H = xgi.Hypergraph()
    H.add_edges_from({"2": [1, 2, 3], 2: [3, 4]})
    with pytest.raises(XGIError):
        xgi.to_hypergraph_dict(H)


def test_from_hypergraph_dict(edgelist1):
    hd = {
        "type": "hypergraph",
        "hypergraph-data": {"name": "test", "author": "Nicholas Landry"},
        "node-data": {
            "1": {"color": "blue"},
            "2": {"color": "yellow"},
            "3": {"color": "cyan"},
            "4": {"color": "green"},
        },
        "edge-data": {
            "edge1": {"weight": 2},
            "edge2": {"weight": 4},
            "edge3": {"weight": -1},
        },
        "edge-dict": {
            "edge1": ["1", "2"],
            "edge2": ["2", "3", "4"],
            "edge3": ["1", "4"],
        },
    }
    Hd = xgi.from_hypergraph_dict(hd)

    H = xgi.Hypergraph()
    H.add_edges_from(
        [
            (["1", "2"], "edge1", {"weight": 2}),
            (["2", "3", "4"], "edge2", {"weight": 4}),
            (["1", "4"], "edge3", {"weight": -1}),
        ]
    )
    H.set_node_attributes(
        {
            "1": {"color": "blue"},
            "2": {"color": "yellow"},
            "3": {"color": "cyan"},
            "4": {"color": "green"},
        }
    )
    H["name"] = "test"
    H["author"] = "Nicholas Landry"

    assert H.nodes == Hd.nodes
    assert H.edges == Hd.edges
    for e in H.edges:
        assert H.edges.members(e) == Hd.edges.members(e)
        assert H.edges[e] == Hd.edges[e]

    for n in H.nodes:
        assert H.nodes[n] == Hd.nodes[n]

    assert H._net_attr == Hd._net_attr

    # test bad dicts
    hd = {
        "type": "hypergraph",
        "node-data": {
            "1": {"color": "blue"},
        },
        "edge-data": {
            "edge1": {"weight": 2},
        },
        "edge-dict": {
            "edge1": ["1", "5"],
        },
    }
    with pytest.raises(XGIError):
        xgi.from_hypergraph_dict(hd)

    hd = {
        "type": "hypergraph",
        "node-data": {
            "1": {"color": "blue"},
            "5": {},
        },
        "edge-data": {},
        "edge-dict": {
            "edge1": ["1", "5"],
        },
    }
    with pytest.raises(XGIError):
        xgi.from_hypergraph_dict(hd)
