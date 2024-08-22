import json
import tempfile

import xgi


def test_to_hif(edgelist1, hyperwithattrs):
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
    xgi.to_hif(hyperwithattrs, filename)

