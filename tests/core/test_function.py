import xgi


def test_convert_labels_to_integers(hypergraph1, hypergraph2):
    H1 = xgi.convert_labels_to_integers(hypergraph1)
    H2 = xgi.convert_labels_to_integers(hypergraph2)
    H3 = xgi.convert_labels_to_integers(hypergraph1, "old_ids")

    assert set(H1.nodes) == {0, 1, 2}
    assert set(H1.edges) == {0, 1, 2}

    assert H1.nodes[0]["label"] == "a"
    assert H1.nodes[1]["label"] == "b"
    assert H1.nodes[2]["label"] == "c"

    assert H1.edges[0]["label"] == "e1"
    assert H1.edges[1]["label"] == "e2"
    assert H1.edges[2]["label"] == "e3"

    assert H1.edges.members(0) == {0, 1}
    assert H1.edges.members(1) == {0, 1, 2}
    assert H1.edges.members(2) == {2}

    assert H1.nodes.memberships(0) == {0, 1}
    assert H1.nodes.memberships(1) == {0, 1}
    assert H1.nodes.memberships(2) == {1, 2}

    assert set(H2.nodes) == {0, 1, 2}
    assert set(H2.edges) == {0, 1, 2}

    assert H2.nodes[0]["label"] == "b"
    assert H2.nodes[1]["label"] == "c"
    assert H2.nodes[2]["label"] == 0

    assert H2.edges[0]["label"] == "e1"
    assert H2.edges[1]["label"] == "e2"
    assert H2.edges[2]["label"] == "e3"

    assert H2.edges.members(0) == {0, 2}
    assert H2.edges.members(1) == {1, 2}
    assert H2.edges.members(2) == {0, 1, 2}

    assert H2.nodes.memberships(0) == {0, 2}
    assert H2.nodes.memberships(1) == {1, 2}
    assert H2.nodes.memberships(2) == {0, 1, 2}

    assert H3.nodes[0]["old_ids"] == "a"
    assert H3.edges[0]["old_ids"] == "e1"
