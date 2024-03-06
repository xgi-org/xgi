import pytest

import xgi


def test_filterby(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.filterby("order", 2).size.asdict() == {0: 3, 1: 3}
    assert H.edges.filterby("size", 4).order.asdict() == {2: 3}


def test_call_filterby(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges([1, 2]).filterby("order", 2).size.asdict() == {1: 3}


def test_filterby_with_nodestat(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert list(H.edges.filterby(H.edges.order(degree=1), 3)) == [0, 1]

    H = xgi.DiHypergraph(diedgelist2)
    assert list(H.edges.filterby(H.edges.order(degree=2), 1)) == [1]


def test_aggregates(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.edges.order.max() == 3
    assert H.edges.order.min() == 3
    assert H.edges.order.sum() == 6
    assert round(H.edges.order.mean(), 3) == 3
    assert round(H.edges.order.std(), 3) == 0
    assert round(H.edges.order.var(), 3) == 0

    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.order.max() == 3
    assert H.edges.order.min() == 2
    assert H.edges.order.sum() == 7
    assert round(H.edges.order.mean(), 3) == 2.333
    assert round(H.edges.order.std(), 3) == 0.471
    assert round(H.edges.order.var(), 3) == 0.222


def test_stats_are_views(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    es = H.edges.order
    assert es.asdict() == {0: 2, 1: 2, 2: 3}
    H.add_edge(([3, 4, 5], [6]))
    assert es.asdict() == {0: 2, 1: 2, 2: 3, 3: 3}


### di-edge specific tests


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
