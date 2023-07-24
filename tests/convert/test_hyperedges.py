import xgi


def test_from_hyperedge_list(edgelist1):
    H = xgi.from_hyperedge_list(edgelist1)
    assert list(H._edge.values()) == [set(e) for e in edgelist1]


def test_to_hyperedge_list(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert xgi.to_hyperedge_list(H) == [set(e) for e in edgelist1]


def test_from_hyperedge_dict(dict5):
    H = xgi.from_hyperedge_dict(dict5)
    assert H._edge == dict5


def test_to_hyperedge_dict(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert xgi.to_hyperedge_dict(H) == {i: set(d) for i, d in enumerate(edgelist1)}
