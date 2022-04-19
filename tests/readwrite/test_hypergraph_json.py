import tempfile

import xgi

json_string = """
{
    "hypergraph-data": {
      "name": "test",
      "author": "Nicholas Landry"
    },
    "node-data": {
      "1": {
        "color": "blue"
      },
      "2": {
        "color": "yellow"
      },
      "3": {
        "color": "cyan"
      },
      "4": {
        "color": "green"
      }
    },
    "edge-data": {
      "edge1": {
        "weight": 2
      },
      "edge2": {
        "weight": 4
      },
      "edge3": {
        "weight": -1
      }
    },
    "edge-dict": {
      "edge1": [
        "1",
        "2"
      ],
      "edge2": [
        "2",
        "3",
        "4"
      ],
      "edge3": [
        "1",
        "4"
      ]
    }
  }
"""


def test_read_hypergraph_json():
    _, filename = tempfile.mkstemp()
    with open(filename, "w") as file:
        file.write(json_string)

    H1 = xgi.read_hypergraph_json(filename, nodetype=int)
    H2 = xgi.read_hypergraph_json(filename)

    assert list(H1.nodes) == [1, 2, 3, 4]
    assert list(H1.edges) == ["edge1", "edge2", "edge3"]

    assert list(H2.nodes) == ["1", "2", "3", "4"]
    assert H1["name"] == "test"
    assert H1["author"] == "Nicholas Landry"
    assert [H1.edges.members(id) for id in H1.edges] == [[1, 2], [2, 3, 4], [1, 4]]
    assert [H2.edges.members(id) for id in H2.edges] == [
        ["1", "2"],
        ["2", "3", "4"],
        ["1", "4"],
    ]

    assert H1.nodes[1]["color"] == "blue"
    assert H1.edges["edge2"]["weight"] == 4


def test_write_hypergraph_json(edgelist1):
    _, filename = tempfile.mkstemp()
    H1 = xgi.Hypergraph(edgelist1)

    H1["name"] = "test"
    H1["author"] = "Nicholas Landry"

    node_attr_dict = {
        1: {"name": "Leonie"},
        2: {"name": "Ilya"},
        3: {"name": "Alice"},
        4: {"name": "Giovanni"},
    }
    xgi.set_node_attributes(H1, node_attr_dict)

    edge_attr_dict = {
        0: {"weight": 1},
        1: {"weight": 2},
        2: {"weight": 3},
        3: {"weight": -1},
    }
    xgi.set_edge_attributes(H1, edge_attr_dict)

    xgi.write_hypergraph_json(H1, filename)

    H2 = xgi.read_hypergraph_json(filename, nodetype=int, edgetype=int)

    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges
    assert [H1.edges.members(id) for id in H1.edges] == [
        H2.edges.members(id) for id in H2.edges
    ]
    assert H2.nodes[2] == {"name": "Ilya"}
    assert H2.edges[1] == {"weight": 2}
    assert H2["name"] == "test"
