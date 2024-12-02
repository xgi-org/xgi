import pytest

import xgi


def test_to_hif_dict(
    edgelist1,
    hyperwithdupsandattrs,
    simplicialcomplex1,
    diedgedict1,
    dihyperwithattrs,
):
    H = xgi.Hypergraph(edgelist1)
    d = xgi.to_hif_dict(H)

    assert "nodes" not in d
    assert "edges" not in d
    assert "incidences" in d
    assert "network-type" in d
    assert d["network-type"] == "undirected"

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
    assert sorted(d["incidences"], key=lambda x: (x["edge"], x["node"])) == incidences

    # hypergraph with attributes
    hyperwithdupsandattrs["name"] = "test"
    d = xgi.to_hif_dict(hyperwithdupsandattrs)

    assert "nodes" in d
    assert "edges" in d
    assert "incidences" in d
    assert "network-type" in d
    assert d["network-type"] == "undirected"
    assert "metadata" in d
    assert d["metadata"] == {"name": "test"}

    nodes = [
        {"node": 1, "attrs": {"color": "red", "name": "horse"}},
        {"node": 2, "attrs": {"color": "blue", "name": "pony"}},
        {"node": 3, "attrs": {"color": "yellow", "name": "zebra"}},
        {"node": 4, "attrs": {"color": "red", "name": "orangutan", "age": 20}},
        {"node": 5, "attrs": {"color": "blue", "name": "fish", "age": 2}},
    ]

    edges = [
        {"edge": 0, "attrs": {"color": "blue"}},
        {"edge": 1, "attrs": {"color": "red", "weight": 2}},
        {"edge": 2, "attrs": {"color": "yellow"}},
        {"edge": 3, "attrs": {"color": "purple"}},
        {"edge": 4, "attrs": {"color": "purple", "name": "test"}},
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

    assert sorted(d["nodes"], key=lambda x: x["node"]) == nodes
    assert d["edges"] == edges
    assert sorted(d["incidences"], key=lambda x: (x["edge"], x["node"])) == incidences

    # Simplicial complexes
    d = xgi.to_hif_dict(simplicialcomplex1)

    assert "nodes" not in d
    assert "edges" not in d
    assert "incidences" in d
    assert "network-type" in d
    assert d["network-type"] == "asc"

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
        d["incidences"], key=lambda x: (_mixed(x["edge"]), _mixed(x["node"]))
    )
    assert sorted_incidences == incidences

    # dihypergraphs without attributes
    H = xgi.DiHypergraph(diedgedict1)

    d = xgi.to_hif_dict(H)

    assert "nodes" not in d
    assert "edges" not in d
    assert "incidences" in d

    # dihypergraphs with attributes
    d = xgi.to_hif_dict(dihyperwithattrs)

    assert "nodes" in d
    assert "edges" in d
    assert "incidences" in d


def test_from_hif_dict(
    hyperwithdupsandattrs,
    simplicialcomplex1,
    dihyperwithattrs,
):
    d = xgi.to_hif_dict(hyperwithdupsandattrs)

    # test basic import
    H = xgi.from_hif_dict(d)

    assert isinstance(H, xgi.Hypergraph)
    assert (H.num_nodes, H.num_edges) == (5, 5)
    assert set(H.nodes) == {1, 2, 3, 4, 5}
    assert H.nodes[1] == {"color": "red", "name": "horse"}
    assert H.nodes[2] == {"color": "blue", "name": "pony"}
    assert H.nodes[3] == {"color": "yellow", "name": "zebra"}
    assert H.nodes[4] == {"color": "red", "name": "orangutan", "age": 20}
    assert H.nodes[5] == {"color": "blue", "name": "fish", "age": 2}

    assert set(H.edges) == {0, 1, 2, 3, 4}
    assert H.edges[0] == {"color": "blue"}
    assert H.edges[1] == {"color": "red", "weight": 2}
    assert H.edges[2] == {"color": "yellow"}
    assert H.edges[3] == {"color": "purple"}
    assert H.edges[4] == {"color": "purple", "name": "test"}

    edgedict = {0: {1, 2}, 1: {1, 2}, 2: {1, 2}, 3: {3, 4, 5}, 4: {3, 4, 5}}
    assert H.edges.members(dtype=dict) == edgedict

    # cast nodes and edges
    H = xgi.from_hif_dict(d, nodetype=str, edgetype=float)
    assert set(H.nodes) == {"1", "2", "3", "4", "5"}
    assert set(H.edges) == {0.0, 1.0, 2.0, 3.0, 4.0}

    assert H.nodes["1"] == {"color": "red", "name": "horse"}
    assert H.edges[0.0] == {"color": "blue"}

    edgedict = {
        0: {"1", "2"},
        1: {"1", "2"},
        2: {"1", "2"},
        3: {"3", "4", "5"},
        4: {"3", "4", "5"},
    }
    assert H.edges.members(dtype=dict) == edgedict

    ds = xgi.to_hif_dict(simplicialcomplex1)

    S = xgi.from_hif_dict(ds)
    assert isinstance(S, xgi.SimplicialComplex)
    assert (S.num_nodes, S.num_edges) == (3, 4)

    assert set(S.nodes) == {0, "b", "c"}
    assert set(S.edges) == {"e1", "e2", "e3", "e4"}

    # dihypergraphs
    d = xgi.to_hif_dict(dihyperwithattrs)

    DH = xgi.from_hif_dict(d)
    assert (DH.num_nodes, DH.num_edges) == (6, 3)
    assert isinstance(DH, xgi.DiHypergraph)
    assert set(DH.nodes) == {0, 1, 2, 3, 4, 5}
    assert set(DH.edges) == {0, 1, 2}

    edgedict = {0: ({0, 1}, {2}), 1: ({1, 2}, {4}), 2: ({2, 3, 4}, {4, 5})}
    assert DH.edges.dimembers(dtype=dict) == edgedict

    # test error checking
    with pytest.raises(TypeError):
        S = xgi.from_hif_dict(ds, edgetype=int)

    # metadata
    hyperwithdupsandattrs["name"] = "test"
    d = xgi.to_hif_dict(hyperwithdupsandattrs)
    H = xgi.from_hif_dict(d)

    assert H["name"] == "test"

    # test isolates and empty edges
    H = xgi.Hypergraph()
    H.add_nodes_from(range(5))
    H.add_edges_from([[1, 2, 3], []])

    d = xgi.to_hif_dict(H)

    H = xgi.from_hif_dict(d)
    assert H.edges.size.aslist() == [3, 0]
    assert set(H.nodes.isolates()) == {0, 4}

    H = xgi.DiHypergraph()
    H.add_nodes_from(range(5))
    H.add_edges_from([([1, 2, 3], [2, 4]), [[], []]])

    d = xgi.to_hif_dict(H)

    H = xgi.from_hif_dict(d)

    assert H.edges.size.aslist() == [4, 0]
    assert set(H.nodes.isolates()) == {0}
