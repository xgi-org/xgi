import xgi

### di-edge stat specific tests


def test_order(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.order.asdict() == {0: 2, 1: 2, 2: 3}
    assert H.edges.order(degree=1).asdict() == {0: 0, 1: -1, 2: 1}


def test_size(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.size.asdict() == {0: 3, 1: 3, 2: 4}
    assert H.edges.size(degree=1).asdict() == {0: 1, 1: 0, 2: 2}


def test_tail_order(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.edges.tail_order.asdict() == {0: 2, 1: 1}

    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.tail_order.asdict() == {0: 1, 1: 1, 2: 2}
    assert H.edges.tail_order(degree=1).asdict() == {0: 0, 1: -1, 2: 0}


def test_tail_size(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.edges.tail_size.asdict() == {0: 3, 1: 2}

    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.tail_size.asdict() == {0: 2, 1: 2, 2: 3}
    assert H.edges.tail_size(degree=1).asdict() == {0: 1, 1: 0, 2: 1}


def test_head_order(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.edges.head_order.asdict() == {0: 0, 1: 2}

    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.head_order.asdict() == {0: 0, 1: 0, 2: 1}
    assert H.edges.head_order(degree=1).asdict() == {0: -1, 1: -1, 2: 0}


def test_head_size(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.edges.head_size.asdict() == {0: 1, 1: 3}

    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.head_size.asdict() == {0: 1, 1: 1, 2: 2}
    assert H.edges.head_size(degree=1).asdict() == {0: 0, 1: 0, 2: 1}
