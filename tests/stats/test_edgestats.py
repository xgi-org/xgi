import xgi

### edge stat specific tests


def test_size(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    sizes = {0: 3, 1: 1, 2: 2, 3: 3}
    assert H.size() == sizes
    assert H.size(degree=2) == {0: 0, 1: 0, 2: 1, 3: 1}
    assert H.edges.size.asdict() == sizes

    H = xgi.Hypergraph(edgelist8)
    sizes = {0: 2, 1: 3, 2: 3, 3: 5, 4: 3, 5: 3, 6: 3, 7: 2, 8: 2}
    assert H.size() == sizes
    assert H.size(degree=2) == {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 1, 8: 1}
    assert H.edges.size.asdict() == sizes


def test_order(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    orders = {0: 2, 1: 0, 2: 1, 3: 2}
    assert H.order() == orders
    assert H.order(degree=2) == {0: -1, 1: -1, 2: 0, 3: 0}
    assert H.edges.order().asdict() == orders

    H = xgi.Hypergraph(edgelist8)
    orders = {0: 1, 1: 2, 2: 2, 3: 4, 4: 2, 5: 2, 6: 2, 7: 1, 8: 1}
    assert H.order() == orders
    assert H.order(degree=2) == {
        0: -1,
        1: -1,
        2: -1,
        3: -1,
        4: 0,
        5: 0,
        6: -1,
        7: 0,
        8: 0,
    }
    assert H.edges.order().asdict() == orders
