import json
import tempfile

import xgi


def test_to_hif(
    edgelist1,
    hyperwithdupsandattrs,
    simplicialcomplex1,
    diedgedict1,
    dihyperwithattrs,
):
    H = xgi.Hypergraph(edgelist1)
    _, filename = tempfile.mkstemp()
    xgi.to_hif(H, filename)
    with open(filename) as file:
        jsondata = json.loads(file.read())

    assert "nodes" not in jsondata
    assert "edges" not in jsondata
    assert "incidences" in jsondata

    incidences = [
        {"edge": 0, "node": 1},
        {"edge": 0, "node": 2},
        {"edge": 0, "node": 3},
        {"edge": 1, "node": 4},
        {"edge": 2, "node": 5},
        {"edge": 2, "node": 6},
        {"edge": 3, "node": 6},
        {"edge": 3, "node": 7},
        {"edge": 3, "node": 8},
    ]
    assert (
        sorted(jsondata["incidences"], key=lambda x: (x["edge"], x["node"]))
        == incidences
    )

    # hypergraph with attributes
    _, filename = tempfile.mkstemp()
    xgi.to_hif(hyperwithdupsandattrs, filename)

    with open(filename) as file:
        jsondata = json.loads(file.read())

    assert "nodes" in jsondata
    assert "edges" in jsondata
    assert "incidences" in jsondata

    nodes = [
        {"node": 1, "attr": {"color": "red", "name": "horse"}},
        {"node": 2, "attr": {"color": "blue", "name": "pony"}},
        {"node": 3, "attr": {"color": "yellow", "name": "zebra"}},
        {"node": 4, "attr": {"color": "red", "name": "orangutan", "age": 20}},
        {"node": 5, "attr": {"color": "blue", "name": "fish", "age": 2}},
    ]

    edges = [
        {"edge": 0, "attr": {"color": "blue"}},
        {"edge": 1, "attr": {"color": "red", "weight": 2}},
        {"edge": 2, "attr": {"color": "yellow"}},
        {"edge": 3, "attr": {"color": "purple"}},
        {"edge": 4, "attr": {"color": "purple", "name": "test"}},
    ]

    incidences = [
        {"edge": 0, "node": 1},
        {"edge": 0, "node": 2},
        {"edge": 1, "node": 1},
        {"edge": 1, "node": 2},
        {"edge": 2, "node": 1},
        {"edge": 2, "node": 2},
        {"edge": 3, "node": 3},
        {"edge": 3, "node": 4},
        {"edge": 3, "node": 5},
        {"edge": 4, "node": 3},
        {"edge": 4, "node": 4},
        {"edge": 4, "node": 5},
    ]

    assert sorted(jsondata["nodes"], key=lambda x: x["node"]) == nodes
    assert jsondata["edges"] == edges
    assert (
        sorted(jsondata["incidences"], key=lambda x: (x["edge"], x["node"]))
        == incidences
    )

    # Simplicial complexes
    _, filename = tempfile.mkstemp()
    xgi.to_hif(simplicialcomplex1, filename)

    with open(filename) as file:
        jsondata = json.loads(file.read())

    assert "nodes" not in jsondata
    assert "edges" not in jsondata
    assert "incidences" in jsondata

    incidences = [
        {"edge": "e1", "node": 0},
        {"edge": "e1", "node": "b"},
        {"edge": "e2", "node": 0},
        {"edge": "e2", "node": "c"},
        {"edge": "e3", "node": 0},
        {"edge": "e3", "node": "b"},
        {"edge": "e3", "node": "c"},
        {"edge": "e4", "node": "b"},
        {"edge": "e4", "node": "c"},
    ]

    def _mixed(ele):
        return (0, int(ele)) if isinstance(ele, int) else (1, ele)

    sorted_incidences = sorted(
        jsondata["incidences"], key=lambda x: (_mixed(x["edge"]), _mixed(x["node"]))
    )
    assert sorted_incidences == incidences

    # dihypergraphs without attributes
    H = xgi.DiHypergraph(diedgedict1)

    _, filename = tempfile.mkstemp()
    xgi.to_hif(H, filename)

    with open(filename) as file:
        jsondata = json.loads(file.read())

    assert "nodes" not in jsondata
    assert "edges" not in jsondata
    assert "incidences" in jsondata

    # dihypergraphs with attributes
    _, filename = tempfile.mkstemp()
    xgi.to_hif(dihyperwithattrs, filename)

    with open(filename) as file:
        jsondata = json.loads(file.read())

    assert "nodes" in jsondata
    assert "edges" in jsondata
    assert "incidences" in jsondata
