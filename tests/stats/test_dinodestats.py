import numpy as np
import pandas as pd
import pytest

import xgi


def test_filterby(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.nodes.filterby("degree", 2).in_degree.asdict() == {1: 2, 4: 1}
    assert H.nodes.filterby("degree", 2).out_degree.asdict() == {1: 0, 4: 2}
    assert H.nodes.filterby("in_degree", 1).degree.asdict() == {0: 1, 3: 1, 4: 2}
    assert H.nodes.filterby("out_degree", 1).degree.asdict() == {2: 3, 5: 1}

    H = xgi.DiHypergraph(diedgelist1)
    assert H.nodes.filterby("degree", 1).in_degree.asdict() == {
        1: 1,
        2: 1,
        3: 1,
        4: 0,
        5: 1,
        6: 1,
        7: 0,
        8: 0,
    }
    assert H.nodes.filterby("degree", 1).out_degree.asdict() == {
        1: 0,
        2: 0,
        3: 0,
        4: 1,
        5: 0,
        6: 1,
        7: 1,
        8: 1,
    }
    assert H.nodes.filterby("in_degree", 1).degree.asdict() == {
        1: 1,
        2: 1,
        3: 1,
        5: 1,
        6: 1,
    }
    assert H.nodes.filterby("out_degree", 1).degree.asdict() == {8: 1, 4: 1, 6: 1, 7: 1}


def test_filterby_with_nodestat(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert list(H.nodes.filterby(H.nodes.degree(order=2), 1)) == [0, 4]


def test_filterby_modes(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert list(H.nodes.filterby("degree", 2)) == [1, 4]
    assert list(H.nodes.filterby("degree", 2, "eq")) == [1, 4]
    assert list(H.nodes.filterby("degree", 1, "neq")) == [1, 2, 4]
    assert list(H.nodes.filterby("degree", 3, "geq")) == [2]
    assert list(H.nodes.filterby("degree", 3, "gt")) == []
    assert list(H.nodes.filterby("degree", 0, "leq")) == []
    assert list(H.nodes.filterby("degree", 1, "lt")) == []
    assert set(H.nodes.filterby("degree", (1, 3), "between")) == set(H.nodes)


def test_aggregates(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.nodes.degree.max() == 3
    assert H.nodes.degree.min() == 1
    assert H.nodes.degree.sum() == 10
    assert round(H.nodes.degree.mean(), 3) == 1.667
    assert round(H.nodes.degree.std(), 3) == 0.745
    assert round(H.nodes.degree.var(), 3) == 0.556


def test_stats_are_views(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    ns = H.nodes.degree
    assert ns.asdict() == {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    H.add_node(10)
    assert ns.asdict() == {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1, 10: 0}


def test_after_call_with_args(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    degs = {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    assert H.nodes.degree.asdict() == degs

    # check when calling without arguments AFTER calling WITH arguments
    H.nodes.degree(order=2).asdict()
    assert H.nodes.degree.asdict() == degs


def test_moment(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    deg = H.nodes.degree
    assert round(deg.moment(), 3) == 3.333
    assert round(deg.moment(2, center=False), 3) == 3.333
    assert round(deg.moment(2, center=True), 3) == 0.556
    assert round(deg.moment(3, center=False), 3) == 7.667
    assert round(deg.moment(3, center=True), 3) == 0.259


def test_call_filterby(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)

    filtered = H.nodes([4, 5, 6]).filterby("in_degree", 1).degree
    assert filtered.asdict() == {5: 1, 6: 1}

    H = xgi.DiHypergraph(diedgelist2)
    assert set(H.nodes([1, 2, 3]).filterby("degree", 2)) == {1}


## di-node specific tests


def test_degree(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    degs = {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    assert H.degree() == degs
    assert H.degree(order=2) == {0: 1, 1: 2, 2: 2, 4: 1, 3: 0, 5: 0}
    assert H.nodes.degree.asdict() == degs
    assert H.nodes.degree.aslist() == list(degs.values())


def test_in_degree(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    degs = {0: 1, 1: 2, 2: 2, 4: 1, 3: 1, 5: 0}
    assert H.in_degree() == degs
    assert H.in_degree(order=2) == {0: 1, 1: 2, 2: 1, 4: 0, 3: 0, 5: 0}
    assert H.nodes.in_degree.asdict() == degs
    assert H.nodes.in_degree.aslist() == list(degs.values())


def test_out_degree(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    degs = {0: 0, 1: 0, 2: 1, 4: 2, 3: 0, 5: 1}
    assert H.out_degree() == degs
    assert H.out_degree(order=2) == {0: 0, 1: 0, 2: 1, 4: 1, 3: 0, 5: 0}
    assert H.nodes.out_degree.asdict() == degs
    assert H.nodes.out_degree.aslist() == list(degs.values())
