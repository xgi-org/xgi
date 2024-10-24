# This module tests the following:

# Numerical node and edge statistics: The degree and edge size
# are the stats on which to test all of the stat functionality.
# Tests include
#    * Functions for casting to different types (tohist, tonumpy, etc.)
#    * Statistics of stats (max, min, etc.)
#    * Filterby

# Node and edge attributes: Conversion functions (tohist, tonumpy, etc.), stats of stats (max, min, etc.), and filterby

# Tests specific to different metrics are implemented in the other files.

### General functionality

import numpy as np
import pandas as pd
import pytest

import xgi


def test_hypergraph_filterby_wrong_stat():
    H = xgi.Hypergraph()
    with pytest.raises(AttributeError):
        H.nodes.filterby("__I_DO_NOT_EXIST__", None)

    with pytest.raises(AttributeError):
        H.edges.filterby("__I_DO_NOT_EXIST__", None)


def test_sc_filterby_wrong_stat():
    H = xgi.SimplicialComplex()
    with pytest.raises(AttributeError):
        H.nodes.filterby("__I_DO_NOT_EXIST__", None)

    with pytest.raises(AttributeError):
        H.edges.filterby("__I_DO_NOT_EXIST__", None)


def test_dihypergraph_filterby_wrong_stat():
    H = xgi.DiHypergraph()
    with pytest.raises(AttributeError):
        H.nodes.filterby("__I_DO_NOT_EXIST__", None)

    with pytest.raises(AttributeError):
        H.edges.filterby("__I_DO_NOT_EXIST__", None)


def test_hypergraph_stats_items(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    deg = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1}
    for n, d in H.nodes.degree.items():
        assert deg[n] == d

    o = {0: 2, 1: 0, 2: 1, 3: 2}
    for e, s in H.edges.order.items():
        assert o[e] == s


def test_dihypergraph_stats_items(diedgelist2):
    d = {0: 2, 1: 2, 2: 3}
    H = xgi.DiHypergraph(diedgelist2)
    for e, s in H.edges.order.items():
        assert d[e] == s


def test_hypergraph_view_val(edgelist1, edgelist2):
    H = xgi.Hypergraph(edgelist1)
    d = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1}
    assert H.nodes.degree._val == d
    assert H.nodes([1, 2, 3]).degree._val == {1: 1, 2: 1, 3: 1}
    assert H.edges.order._val == {0: 2, 1: 0, 2: 1, 3: 2}
    assert H.edges([1, 2]).order._val == {1: 0, 2: 1}

    H = xgi.Hypergraph(edgelist2)
    assert H.nodes.degree._val == {1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1}
    assert H.nodes([4, 5, 6]).degree._val == {4: 2, 5: 1, 6: 1}
    assert H.edges.order._val == {0: 1, 1: 1, 2: 2}
    assert H.edges([1, 2]).order._val == {1: 1, 2: 2}


def test_dihypergraph_view_val(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.edges.order._val == {0: 3, 1: 3}
    assert H.edges([1]).order._val == {1: 3}

    H = xgi.DiHypergraph(diedgelist2)
    assert H.nodes.degree._val == {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    assert H.nodes([1, 2]).degree._val == {1: 2, 2: 3}

    assert H.edges.order._val == {0: 2, 1: 2, 2: 3}
    assert H.edges([1, 2]).order._val == {1: 2, 2: 3}


def test_hypergraph_stats_are_views(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    ns = H.nodes.degree
    d = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1}
    assert ns.asdict() == d
    H.add_node(10)
    d = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1, 10: 0}
    assert ns.asdict() == d
    H.add_edge([1, 2, 10, 20])
    d = {1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1, 10: 1, 20: 1}
    assert ns.asdict() == d

    H = xgi.Hypergraph(edgelist1)
    es = H.edges.order
    assert es.asdict() == {0: 2, 1: 0, 2: 1, 3: 2}
    H.add_edge([3, 4, 5])
    assert es.asdict() == {0: 2, 1: 0, 2: 1, 3: 2, 4: 2}


def test_dihypergraph_stats_are_views(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    es = H.edges.order
    assert es.asdict() == {0: 2, 1: 2, 2: 3}
    H.add_edge(([3, 4, 5], [6]))
    assert es.asdict() == {0: 2, 1: 2, 2: 3, 3: 3}

    H = xgi.DiHypergraph(diedgelist2)
    ns = H.nodes.degree
    d = {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    assert ns.asdict() == d
    H.add_node(10)
    d = {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1, 10: 0}
    assert ns.asdict() == d


def test_hypergraph_user_defined(edgelist1):

    # Hypergraphs
    H = xgi.Hypergraph(edgelist1)

    with pytest.raises(AttributeError):
        H.user_degree
    with pytest.raises(AttributeError):
        H.nodes.user_degree

    @xgi.nodestat_func
    def user_degree(net, bunch):
        return {n: 10 * net.degree(n) for n in bunch}

    vals = {n: 10 * H.degree(n) for n in H}
    assert H.user_degree() == vals
    assert H.nodes.user_degree.asdict() == vals
    assert H.nodes.user_degree.aslist() == [vals[n] for n in H]
    assert (
        list(H.nodes.filterby("user_degree", 20))
        == list(H.nodes.filterby("degree", 2))
        == [6]
    )
    assert H.nodes.filterby("degree", 2).user_degree.asdict() == {6: 20}

    with pytest.raises(AttributeError):
        H.user_order
    with pytest.raises(AttributeError):
        H.edges.user_order

    @xgi.edgestat_func
    def user_order(net, bunch):
        return {e: 10 * net.order(e) for e in bunch}

    vals = {e: 10 * H.order(e) for e in H.edges}
    assert H.user_order() == vals
    assert H.edges.user_order.asdict() == vals
    assert H.edges.user_order.aslist() == [vals[n] for n in H.edges]
    assert (
        list(H.edges.filterby("user_order", 20))
        == list(H.edges.filterby("order", 2))
        == [0, 3]
    )
    assert H.edges.filterby("order", 2).user_order.asdict() == {0: 20, 3: 20}


def test_dihypergraph_user_defined(diedgelist2):
    # DiHypergraphs
    H = xgi.DiHypergraph(diedgelist2)

    with pytest.raises(AttributeError):
        H.user_didegree
    with pytest.raises(AttributeError):
        H.nodes.user_didegree

    @xgi.dinodestat_func
    def user_didegree(net, bunch):
        return {n: 10 * net.degree(n) for n in bunch}

    vals = {n: 10 * H.degree(n) for n in H.nodes}
    assert H.user_didegree() == vals
    assert H.nodes.user_didegree.asdict() == vals
    assert H.nodes.user_didegree.aslist() == [vals[n] for n in H.nodes]
    assert H.nodes.filterby("degree", 2).user_didegree.asdict() == {1: 20, 4: 20}

    with pytest.raises(AttributeError):
        H.user_diorder
    with pytest.raises(AttributeError):
        H.edges.user_diorder

    @xgi.diedgestat_func
    def user_diorder(net, bunch):
        return {e: 10 * net.order(e) for e in bunch}

    vals = {e: 10 * H.order(e) for e in H.edges}
    assert H.user_diorder() == vals
    assert H.edges.user_diorder.asdict() == vals
    assert H.edges.user_diorder.aslist() == [vals[n] for n in H.edges]
    assert H.edges.filterby("order", 2).user_diorder.asdict() == {0: 20, 1: 20}


def test_hypergraph_different_views(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    with pytest.raises(KeyError):
        H.nodes.multi([H.nodes.degree, H.nodes([1, 2]).degree]).asdict()
    with pytest.raises(KeyError):
        H.nodes.multi([H.nodes.attrs("color"), H.nodes([1, 2]).attrs("color")]).asdict()

    with pytest.raises(KeyError):
        H.edges.multi(["order", H.edges([1, 2]).size]).asdict()
    with pytest.raises(KeyError):
        H.edges.multi(["order", H.edges([1, 2]).attrs("color")]).asdict()


def test_dihypergraph_different_views(diedgelist1):
    H = xgi.DiHypergraph(diedgelist1)
    with pytest.raises(KeyError):
        H.nodes.multi([H.nodes.degree, H.nodes([1, 2]).degree]).asdict()
    with pytest.raises(KeyError):
        H.nodes.multi([H.nodes.attrs("color"), H.nodes([1, 2]).attrs("color")]).asdict()

    with pytest.raises(KeyError):
        H.edges.multi(["order", H.edges([1, 2]).size]).asdict()
    with pytest.raises(KeyError):
        H.edges.multi(["order", H.edges([1, 2]).attrs("color")]).asdict()


def test_hypergraph_stats_items(edgelist1):
    d = {0: 2, 1: 0, 2: 1, 3: 2}
    H = xgi.Hypergraph(edgelist1)
    for e, s in H.edges.order.items():
        assert d[e] == s


def test_dihypergraph_stats_items(diedgelist2):
    deg = {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    H = xgi.DiHypergraph(diedgelist2)
    for n, d in H.nodes.degree.items():
        assert deg[n] == d


### Numerical statistics


def test_hypergraph_filterby(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    d = {6: 1.0}
    assert H.nodes.filterby("degree", 2).average_neighbor_degree.asdict() == d
    d = {1: 1, 2: 1, 3: 1, 6: 2}
    assert H.nodes.filterby("average_neighbor_degree", 1.0).degree.asdict() == d
    d = {0: 3, 3: 3}
    assert H.edges.filterby("order", 2).size.asdict() == d
    d = {2: 1}
    assert H.edges.filterby("size", 2).order.asdict() == d

    H = xgi.Hypergraph(edgelist8)
    assert H.nodes.filterby("degree", 3).average_neighbor_degree.asdict() == {4: 4.2}
    assert H.nodes.filterby("average_neighbor_degree", 4.2).degree.asdict() == {4: 3}
    assert H.edges.filterby("order", 2).size.asdict() == {1: 3, 2: 3, 4: 3, 5: 3, 6: 3}
    assert H.edges.filterby("size", 2).order.asdict() == {0: 1, 8: 1, 7: 1}


def test_dihypergraph_filterby(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert H.nodes.filterby("degree", 2).in_degree.asdict() == {1: 0, 4: 2}
    assert H.nodes.filterby("degree", 2).out_degree.asdict() == {1: 2, 4: 1}
    assert H.nodes.filterby("in_degree", 1).degree.asdict() == {2: 3, 5: 1}
    assert H.nodes.filterby("out_degree", 1).degree.asdict() == {0: 1, 3: 1, 4: 2}

    assert H.edges.filterby("order", 2).size.asdict() == {0: 3, 1: 3}
    assert H.edges.filterby("size", 4).order.asdict() == {2: 3}

    H = xgi.DiHypergraph(diedgelist1)
    d = {1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1, 8: 1, 7: 1}
    assert H.nodes.filterby("degree", 1).in_degree.asdict() == d
    d = {1: 1, 2: 1, 3: 1, 4: 0, 5: 1, 6: 1, 8: 0, 7: 0}
    assert H.nodes.filterby("degree", 1).out_degree.asdict() == d
    d = {4: 1, 6: 1, 8: 1, 7: 1}
    assert H.nodes.filterby("in_degree", 1).degree.asdict() == d
    d = {1: 1, 2: 1, 3: 1, 5: 1, 6: 1}
    assert H.nodes.filterby("out_degree", 1).degree.asdict() == d


def test_filterby_modes(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    assert list(H.nodes.filterby("degree", 2)) == [6]
    assert list(H.nodes.filterby("degree", 2, "eq")) == [6]
    assert list(H.nodes.filterby("degree", 1, "neq")) == [6]
    assert list(H.nodes.filterby("degree", 2, "geq")) == [6]
    assert list(H.nodes.filterby("degree", 2, "gt")) == []
    assert list(H.nodes.filterby("degree", 0, "leq")) == []
    assert list(H.nodes.filterby("degree", 1, "lt")) == []
    assert set(H.nodes.filterby("degree", (1, 3), "between")) == set(H.nodes)

    H = xgi.Hypergraph(edgelist8)
    assert set(H.nodes.filterby("degree", 2)) == {5, 6}
    assert set(H.nodes.filterby("degree", 2, "eq")) == {5, 6}
    assert set(H.nodes.filterby("degree", 2, "neq")) == {0, 1, 2, 3, 4}
    assert set(H.nodes.filterby("degree", 5, "geq")) == {0, 1}
    assert set(H.nodes.filterby("degree", 5, "gt")) == {0}
    assert set(H.nodes.filterby("degree", 2, "leq")) == {5, 6}
    assert set(H.nodes.filterby("degree", 2, "lt")) == set()
    assert set(H.nodes.filterby("degree", (2, 3), "between")) == {4, 5, 6}


def test_dihypergraph_filterby_modes(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    assert list(H.nodes.filterby("degree", 2)) == [1, 4]
    assert list(H.nodes.filterby("degree", 2, "eq")) == [1, 4]
    assert list(H.nodes.filterby("degree", 1, "neq")) == [1, 2, 4]
    assert list(H.nodes.filterby("degree", 3, "geq")) == [2]
    assert list(H.nodes.filterby("degree", 3, "gt")) == []
    assert list(H.nodes.filterby("degree", 0, "leq")) == []
    assert list(H.nodes.filterby("degree", 1, "lt")) == []
    assert set(H.nodes.filterby("degree", (1, 3), "between")) == set(H.nodes)


def test_hypergraph_call_filterby(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)

    filtered = H.nodes([5, 6, 7, 8]).filterby("average_neighbor_degree", 2.0).degree
    assert filtered.asdict() == {5: 1}

    filtered = H.nodes([5, 6, 7, 8]).filterby("degree", 2).average_neighbor_degree
    assert filtered.asdict() == {6: 1.0}

    filtered = H.edges([1, 2, 3]).filterby("order", 2).size
    assert filtered.asdict() == {3: 3}

    H = xgi.Hypergraph(edgelist8)
    assert set(H.nodes([1, 2, 3]).filterby("degree", 4)) == {2, 3}

    filtered = H.nodes([1, 2, 3]).filterby("average_neighbor_degree", 4.0).degree
    assert filtered.asdict() == {2: 4, 3: 4}

    filtered = H.nodes([1, 2, 3]).filterby("degree", 5).average_neighbor_degree
    assert filtered.asdict() == {1: 3.5}

    filtered = H.edges([5, 6]).filterby("order", 2).size
    assert filtered.asdict() == {5: 3, 6: 3}


def test_dihypergraph_call_filterby(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)

    filtered = H.nodes([4, 5, 6]).filterby("in_degree", 1).degree
    assert filtered.asdict() == {4: 1, 6: 1}

    H = xgi.DiHypergraph(diedgelist2)
    assert set(H.nodes([1, 2, 3]).filterby("degree", 2)) == {1}
    assert H.edges([1, 2]).filterby("order", 2).size.asdict() == {1: 3}


def test_hypergraph_after_call_with_args(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    degs = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1}
    assert H.nodes.degree.asdict() == degs

    # check when calling without arguments AFTER calling WITH arguments
    H.nodes.degree(order=2).asdict()
    assert H.nodes.degree.asdict() == degs


def test_dihypergraph_after_call_with_args(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    degs = {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    assert H.nodes.degree.asdict() == degs

    # check when calling without arguments AFTER calling WITH arguments
    H.nodes.degree(order=2).asdict()
    assert H.nodes.degree.asdict() == degs


def test_hypergraph_filterby_with_nodestat(edgelist4, edgelist8):
    H = xgi.Hypergraph(edgelist4)
    assert list(H.nodes.filterby(H.nodes.degree(order=2), 2)) == [3]

    H = xgi.Hypergraph(edgelist8)
    assert list(H.nodes.filterby(H.nodes.degree(order=2), 2)) == [1, 4, 5]


def test_dihypergraph_filterby_with_nodestat(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert list(H.edges.filterby(H.edges.order(degree=1), 3)) == [0, 1]

    H = xgi.DiHypergraph(diedgelist2)
    assert list(H.edges.filterby(H.edges.order(degree=2), 1)) == [1]
    assert list(H.nodes.filterby(H.nodes.degree(order=2), 1)) == [0, 4]


def test_filterby_edgestat_with_nodestat(edgelist4, edgelist8):
    H = xgi.Hypergraph(edgelist4)
    assert list(H.edges.filterby(H.edges.order(degree=2), 2)) == [1]

    H = xgi.Hypergraph(edgelist8)
    assert list(H.edges.filterby(H.edges.order(degree=4), 1)) == [2, 3]


def test_hypergraph_aggregates(edgelist1, edgelist2, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    assert H.nodes.degree.max() == 2
    assert H.nodes.degree.min() == 1
    assert H.nodes.degree.argmax() == 6
    assert H.nodes.degree.argmin() == 1
    assert H.nodes.degree.argsort() == list(H.nodes.filterby("degree", 1)) + list(
        H.nodes.filterby("degree", 2)
    )
    assert H.nodes.degree.argsort(reverse=True) == list(
        H.nodes.filterby("degree", 2)
    ) + list(H.nodes.filterby("degree", 1))
    assert H.nodes.degree.sum() == 9
    assert round(H.nodes.degree.mean(), 3) == 1.125
    assert round(H.nodes.degree.std(), 3) == 0.331
    assert round(H.nodes.degree.var(), 3) == 0.109
    assert np.allclose(H.nodes.degree.unique(), np.array([1, 2]))

    assert H.edges.order.max() == 2
    assert H.edges.order.min() == 0
    assert H.edges.order.sum() == 5
    assert round(H.edges.order.mean(), 3) == 1.25
    assert round(H.edges.order.std(), 3) == 0.829
    assert round(H.edges.order.var(), 3) == 0.688
    assert np.allclose(H.edges.order.unique(), np.array([0, 1, 2]))

    H = xgi.Hypergraph(edgelist2)
    assert H.nodes.degree.max() == 2
    assert H.nodes.degree.min() == 1
    assert H.nodes.degree.argmax() == 4
    assert H.nodes.degree.argmin() == 1
    assert H.nodes.degree.argsort() == list(H.nodes.filterby("degree", 1)) + list(
        H.nodes.filterby("degree", 2)
    )
    assert H.nodes.degree.sum() == 7
    assert round(H.nodes.degree.mean(), 3) == 1.167
    assert round(H.nodes.degree.std(), 3) == 0.373
    assert round(H.nodes.degree.var(), 3) == 0.139
    assert np.allclose(H.nodes.degree.unique(), np.array([1, 2]))

    assert H.edges.order.max() == 2
    assert H.edges.order.min() == 1
    assert H.edges.order.sum() == 4
    assert round(H.edges.order.mean(), 3) == 1.333
    assert round(H.edges.order.std(), 3) == 0.471
    assert round(H.edges.order.var(), 3) == 0.222
    assert np.allclose(H.edges.order.unique(), np.array([1, 2]))
    assert len(H.edges.order.unique(return_counts=True)) == 2
    assert np.allclose(H.edges.order.unique(return_counts=True)[1], np.array([2, 1]))

    H = xgi.Hypergraph(edgelist8)
    assert H.nodes.degree.max() == 6
    assert H.nodes.degree.min() == 2
    assert H.nodes.degree.argmax() == 0
    assert H.nodes.degree.argmin() == 5
    assert H.nodes.degree.argsort() == list(H.nodes.filterby("degree", 2)) + list(
        H.nodes.filterby("degree", 3)
    ) + list(H.nodes.filterby("degree", 4)) + list(
        H.nodes.filterby("degree", 5)
    ) + list(
        H.nodes.filterby("degree", 6)
    )
    assert H.nodes.degree.sum() == 26
    assert round(H.nodes.degree.mean(), 3) == 3.714
    assert round(H.nodes.degree.std(), 3) == 1.385
    assert round(H.nodes.degree.var(), 3) == 1.918

    assert H.edges.order.max() == 4
    assert H.edges.order.min() == 1
    assert H.edges.order.sum() == 17
    assert round(H.edges.order.mean(), 3) == 1.889
    assert round(H.edges.order.std(), 3) == 0.875
    assert round(H.edges.order.var(), 3) == 0.765


def test_dihypergraph_aggregates(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.edges.order.max() == 3
    assert H.edges.order.min() == 3
    assert H.edges.order.sum() == 6
    assert round(H.edges.order.mean(), 3) == 3
    assert round(H.edges.order.std(), 3) == 0
    assert round(H.edges.order.var(), 3) == 0

    H = xgi.DiHypergraph(diedgelist2)
    assert H.nodes.degree.max() == 3
    assert H.nodes.degree.min() == 1
    assert H.nodes.degree.sum() == 10
    assert round(H.nodes.degree.mean(), 3) == 1.667
    assert round(H.nodes.degree.std(), 3) == 0.745
    assert round(H.nodes.degree.var(), 3) == 0.556

    assert H.edges.order.max() == 3
    assert H.edges.order.min() == 2
    assert H.edges.order.sum() == 7
    assert round(H.edges.order.mean(), 3) == 2.333
    assert round(H.edges.order.std(), 3) == 0.471
    assert round(H.edges.order.var(), 3) == 0.222


def test_hypergraph_moment(edgelist1, edgelist6):
    H = xgi.Hypergraph(edgelist1)
    deg = H.nodes.degree
    assert round(deg.moment(), 3) == 1.375
    assert round(deg.moment(2, center=False), 3) == 1.375
    assert round(deg.moment(2, center=True), 3) == 0.109
    assert round(deg.moment(3, center=False), 3) == 1.875
    assert round(deg.moment(3, center=True), 3) == 0.082

    H = xgi.Hypergraph(edgelist6)
    deg = H.edges.size
    assert round(deg.moment(), 3) == 9.0
    assert round(deg.moment(2, center=False), 3) == 9.0
    assert round(deg.moment(2, center=True), 3) == 0.0
    assert round(deg.moment(3, center=False), 3) == 27.0
    assert round(deg.moment(3, center=True), 3) == 0.0


def test_dihypergraph_moment(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    deg = H.nodes.degree
    assert round(deg.moment(), 3) == 3.333
    assert round(deg.moment(2, center=False), 3) == 3.333
    assert round(deg.moment(2, center=True), 3) == 0.556
    assert round(deg.moment(3, center=False), 3) == 7.667
    assert round(deg.moment(3, center=True), 3) == 0.259


def test_hypergraph_single_id(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert H.degree()[1] == 1
    assert H.nodes.degree[1] == 1
    with pytest.raises(KeyError):
        H.degree()[-1]
    with pytest.raises(KeyError):
        H.nodes.degree[-1]

    assert H.order()[1] == 0
    assert H.edges.order[1] == 0
    with pytest.raises(KeyError):
        H.order()[-1]
    with pytest.raises(KeyError):
        H.edges.order[-1]


def test_dihypergraph_single_id(diedgelist1):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.degree()[1] == 1
    assert H.nodes.degree[1] == 1
    with pytest.raises(KeyError):
        H.degree()[-1]
    with pytest.raises(KeyError):
        H.nodes.degree[-1]

    assert H.order()[1] == 3
    assert H.edges.order[1] == 3
    with pytest.raises(KeyError):
        H.order()[-1]
    with pytest.raises(KeyError):
        H.edges.order[-1]


def test_issue_468():
    H = xgi.sunflower(3, 1, 20)
    df = pd.DataFrame([[20.0, 3]], columns=["bin_center", "value"])
    assert H.edges.size.ashist().equals(df)


### Attribute statistics


def test_hypergraph_attrs(hyperwithattrs, attr1, attr2, attr3, attr4, attr5):
    H = hyperwithattrs
    attrs = {
        1: attr1,
        2: attr2,
        3: attr3,
        4: attr4,
        5: attr5,
    }
    assert H.nodes.attrs.asdict() == attrs
    assert H.nodes.attrs.aslist() == list(attrs.values())
    assert H.nodes.attrs("color").asdict() == {n: H._node_attr[n]["color"] for n in H}

    filtered = H.nodes.filterby_attr("color", "blue").attrs
    assert filtered.asdict() == {2: attr2, 5: attr5}

    filtered = H.nodes([1, 2, 3]).filterby_attr("color", "blue").attrs
    assert filtered.asdict() == {2: attr2}

    filtered = H.nodes([1, 2, 3]).filterby("degree", 3).attrs
    assert filtered.asdict() == {3: attr3}

    with pytest.raises(ValueError):
        H.nodes.attrs(-1).asdict()


# test pre-defined functions
def test_dihypergraph_attrs(dihyperwithattrs):
    c = dihyperwithattrs.nodes.attrs("color")
    assert c.asdict() == {
        0: "brown",
        1: "red",
        2: "blue",
        3: "yellow",
        4: "red",
        5: "blue",
    }
    c = dihyperwithattrs.nodes.attrs("age", missing=100)
    assert c.asdict() == {0: 100, 1: 100, 2: 100, 3: 100, 4: 20, 5: 2}
    c = dihyperwithattrs.nodes.attrs()
    assert c.asdict() == {
        0: {"color": "brown", "name": "camel"},
        1: {"color": "red", "name": "horse"},
        2: {"color": "blue", "name": "pony"},
        3: {"color": "yellow", "name": "zebra"},
        4: {"color": "red", "name": "orangutan", "age": 20},
        5: {"color": "blue", "name": "fish", "age": 2},
    }
    with pytest.raises(ValueError):
        dihyperwithattrs.nodes.attrs(attr=100).asdict()


def test_filterby_attr(hyperwithattrs):
    H = hyperwithattrs

    filtered = H.nodes.filterby_attr("age", 20, "eq")
    assert set(filtered) == {4}

    filtered = H.nodes.filterby_attr("age", 2, "neq")
    assert set(filtered) == {4}

    filtered = H.nodes.filterby_attr("age", 20, "lt")
    assert set(filtered) == {5}

    filtered = H.nodes.filterby_attr("age", 2, "gt")
    assert set(filtered) == {4}

    filtered = H.nodes.filterby_attr("age", 20, "leq")
    assert set(filtered) == {4, 5}

    filtered = H.nodes.filterby_attr("age", 2, "geq")
    assert set(filtered) == {4, 5}

    filtered = H.nodes.filterby_attr("age", [1, 3], "between")
    assert set(filtered) == {5}

    filtered = H.nodes.filterby_attr("age", [2, 20], "between")
    assert set(filtered) == {4, 5}

    filtered = H.nodes.filterby_attr("age", 2, "leq", 1)
    assert set(filtered) == {1, 2, 3, 5}

    filtered = H.nodes.filterby_attr("age", 2, "leq", 10)
    assert set(filtered) == {5}


def test_missing_attrs(hyperwithattrs):
    H = hyperwithattrs
    H.add_node(10)
    assert H.nodes.attrs("color").asdict() == {
        1: "red",
        2: "blue",
        3: "yellow",
        4: "red",
        5: "blue",
        10: None,
    }
    assert H.nodes.attrs("color", missing="missingval").asdict() == {
        1: "red",
        2: "blue",
        3: "yellow",
        4: "red",
        5: "blue",
        10: "missingval",
    }


### Test multiple stats


def test_multi_stats_order(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    d = {
        1: {"degree": 1, "average_neighbor_degree": 1.0},
        2: {"degree": 1, "average_neighbor_degree": 1.0},
        3: {"degree": 1, "average_neighbor_degree": 1.0},
        4: {"degree": 1, "average_neighbor_degree": 0},
        5: {"degree": 1, "average_neighbor_degree": 2.0},
        6: {"degree": 2, "average_neighbor_degree": 1.0},
        7: {"degree": 1, "average_neighbor_degree": 1.5},
        8: {"degree": 1, "average_neighbor_degree": 1.5},
    }
    assert H.nodes.multi(["degree", "average_neighbor_degree"]).asdict() == d
    d = {
        1: {"average_neighbor_degree": 1.0, "degree": 1},
        2: {"average_neighbor_degree": 1.0, "degree": 1},
        3: {"average_neighbor_degree": 1.0, "degree": 1},
        4: {"average_neighbor_degree": 0, "degree": 1},
        5: {"average_neighbor_degree": 2.0, "degree": 1},
        6: {"average_neighbor_degree": 1.0, "degree": 2},
        7: {"average_neighbor_degree": 1.5, "degree": 1},
        8: {"average_neighbor_degree": 1.5, "degree": 1},
    }
    assert H.nodes.multi(["average_neighbor_degree", "degree"]).asdict() == d

    H = xgi.Hypergraph(edgelist8)
    d = {
        0: {"degree": 6, "average_neighbor_degree": 3.6},
        1: {"degree": 5, "average_neighbor_degree": 3.5},
        2: {"degree": 4, "average_neighbor_degree": 4.0},
        3: {"degree": 4, "average_neighbor_degree": 4.0},
        4: {"degree": 3, "average_neighbor_degree": 4.2},
        5: {"degree": 2, "average_neighbor_degree": 4.0},
        6: {"degree": 2, "average_neighbor_degree": 5.5},
    }
    assert H.nodes.multi(["degree", "average_neighbor_degree"]).asdict() == d
    d = {
        0: {"average_neighbor_degree": 3.6, "degree": 6},
        1: {"average_neighbor_degree": 3.5, "degree": 5},
        2: {"average_neighbor_degree": 4.0, "degree": 4},
        3: {"average_neighbor_degree": 4.0, "degree": 4},
        4: {"average_neighbor_degree": 4.2, "degree": 3},
        5: {"average_neighbor_degree": 4.0, "degree": 2},
        6: {"average_neighbor_degree": 5.5, "degree": 2},
    }
    assert H.nodes.multi(["average_neighbor_degree", "degree"]).asdict() == d


def test_multi_stats_with_parameters(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    multi = H.nodes.multi(["degree", H.nodes.degree(order=2)])
    d = {
        1: {"degree": 1, "degree(order=2)": 1},
        2: {"degree": 1, "degree(order=2)": 1},
        3: {"degree": 1, "degree(order=2)": 1},
        4: {"degree": 1, "degree(order=2)": 0},
        5: {"degree": 1, "degree(order=2)": 0},
        6: {"degree": 2, "degree(order=2)": 1},
        7: {"degree": 1, "degree(order=2)": 1},
        8: {"degree": 1, "degree(order=2)": 1},
    }
    assert multi.asdict() == d


def test_multi_stats_dict_transpose(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    multi = H.nodes.multi(
        ["average_neighbor_degree", "degree", H.nodes.degree(order=2)]
    )

    d = {
        1: {"average_neighbor_degree": 1.0, "degree": 1, "degree(order=2)": 1},
        2: {"average_neighbor_degree": 1.0, "degree": 1, "degree(order=2)": 1},
        3: {"average_neighbor_degree": 1.0, "degree": 1, "degree(order=2)": 1},
        4: {"average_neighbor_degree": 0, "degree": 1, "degree(order=2)": 0},
        5: {"average_neighbor_degree": 2.0, "degree": 1, "degree(order=2)": 0},
        6: {"average_neighbor_degree": 1.0, "degree": 2, "degree(order=2)": 1},
        7: {"average_neighbor_degree": 1.5, "degree": 1, "degree(order=2)": 1},
        8: {"average_neighbor_degree": 1.5, "degree": 1, "degree(order=2)": 1},
    }
    assert multi.asdict() == d

    d = {
        "average_neighbor_degree": {
            1: 1.0,
            2: 1.0,
            3: 1.0,
            4: 0,
            5: 2.0,
            6: 1.0,
            7: 1.5,
            8: 1.5,
        },
        "degree": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1},
        "degree(order=2)": {1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1},
    }
    assert multi.asdict(transpose=True) == d

    H = xgi.Hypergraph(edgelist8)
    multi = H.nodes.multi(
        ["average_neighbor_degree", "degree", H.nodes.degree(order=2)]
    )

    d = {
        0: {"average_neighbor_degree": 3.6, "degree": 6, "degree(order=2)": 3},
        1: {"average_neighbor_degree": 3.5, "degree": 5, "degree(order=2)": 2},
        2: {"average_neighbor_degree": 4.0, "degree": 4, "degree(order=2)": 3},
        3: {"average_neighbor_degree": 4.0, "degree": 4, "degree(order=2)": 3},
        4: {"average_neighbor_degree": 4.2, "degree": 3, "degree(order=2)": 2},
        5: {"average_neighbor_degree": 4.0, "degree": 2, "degree(order=2)": 2},
        6: {"average_neighbor_degree": 5.5, "degree": 2, "degree(order=2)": 0},
    }
    assert multi.asdict() == d

    d = {
        "average_neighbor_degree": {
            0: 3.6,
            1: 3.5,
            2: 4.0,
            3: 4.0,
            4: 4.2,
            5: 4.0,
            6: 5.5,
        },
        "degree": {0: 6, 1: 5, 2: 4, 3: 4, 4: 3, 5: 2, 6: 2},
        "degree(order=2)": {0: 3, 1: 2, 2: 3, 3: 3, 4: 2, 5: 2, 6: 0},
    }
    assert multi.asdict(transpose=True) == d


def test_multi_stats_dict_list(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    multi = H.nodes.multi(["average_neighbor_degree", "degree"])

    d = {
        1: [1.0, 1],
        2: [1.0, 1],
        3: [1.0, 1],
        4: [0, 1],
        5: [2.0, 1],
        6: [1.0, 2],
        7: [1.5, 1],
        8: [1.5, 1],
    }
    assert multi.asdict(list) == d

    H = xgi.Hypergraph(edgelist8)
    multi = H.nodes.multi(["average_neighbor_degree", "degree"])

    d = {
        0: [3.6, 6],
        1: [3.5, 5],
        2: [4.0, 4],
        3: [4.0, 4],
        4: [4.2, 3],
        5: [4.0, 2],
        6: [5.5, 2],
    }
    assert multi.asdict(list) == d


def test_multi_stats_list_dict(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    multi = H.nodes.multi(["average_neighbor_degree", "degree"])

    l = [
        {"average_neighbor_degree": 1.0, "degree": 1},
        {"average_neighbor_degree": 1.0, "degree": 1},
        {"average_neighbor_degree": 1.0, "degree": 1},
        {"average_neighbor_degree": 0, "degree": 1},
        {"average_neighbor_degree": 2.0, "degree": 1},
        {"average_neighbor_degree": 1.0, "degree": 2},
        {"average_neighbor_degree": 1.5, "degree": 1},
        {"average_neighbor_degree": 1.5, "degree": 1},
    ]
    assert multi.aslist(dict) == l

    H = xgi.Hypergraph(edgelist8)
    multi = H.nodes.multi(["average_neighbor_degree", "degree"])

    l = [
        {"average_neighbor_degree": 3.6, "degree": 6},
        {"average_neighbor_degree": 3.5, "degree": 5},
        {"average_neighbor_degree": 4.0, "degree": 4},
        {"average_neighbor_degree": 4.0, "degree": 4},
        {"average_neighbor_degree": 4.2, "degree": 3},
        {"average_neighbor_degree": 4.0, "degree": 2},
        {"average_neighbor_degree": 5.5, "degree": 2},
    ]
    assert multi.aslist(dict) == l


def test_multi_stats_list_transpose(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    multi = H.nodes.multi(
        ["average_neighbor_degree", "degree", H.nodes.degree(order=2)]
    )

    l = [
        [1.0, 1, 1],
        [1.0, 1, 1],
        [1.0, 1, 1],
        [0, 1, 0],
        [2.0, 1, 0],
        [1.0, 2, 1],
        [1.5, 1, 1],
        [1.5, 1, 1],
    ]
    assert multi.aslist() == l

    l = [
        [1.0, 1.0, 1.0, 0, 2.0, 1.0, 1.5, 1.5],
        [1, 1, 1, 1, 1, 2, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1],
    ]
    assert multi.aslist(transpose=True) == l

    H = xgi.Hypergraph(edgelist8)
    multi = H.nodes.multi(
        ["average_neighbor_degree", "degree", H.nodes.degree(order=2)]
    )

    l = [
        [3.6, 6, 3],
        [3.5, 5, 2],
        [4.0, 4, 3],
        [4.0, 4, 3],
        [4.2, 3, 2],
        [4.0, 2, 2],
        [5.5, 2, 0],
    ]
    assert multi.aslist() == l

    l = [
        [3.6, 3.5, 4.0, 4.0, 4.2, 4.0, 5.5],
        [6, 5, 4, 4, 3, 2, 2],
        [3, 2, 3, 3, 2, 2, 0],
    ]
    assert multi.aslist(transpose=True) == l


def test_multi_stats_aspandas(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    multi = H.nodes.multi(
        ["average_neighbor_degree", "degree", H.nodes.degree(order=2)]
    )
    df = pd.DataFrame(multi.asdict(transpose=True))
    pd.testing.assert_frame_equal(df, multi.aspandas(), check_like=True)

    H = xgi.Hypergraph(edgelist8)
    multi = H.nodes.multi(
        ["average_neighbor_degree", "degree", H.nodes.degree(order=2)]
    )
    df = pd.DataFrame(multi.asdict(transpose=True))
    pd.testing.assert_frame_equal(df, multi.aspandas())


def test_multi_with_attrs(hyperwithattrs):
    H = hyperwithattrs
    multi = H.nodes.multi([H.nodes.attrs("color")])

    d = {
        1: {"attrs(color)": "red"},
        2: {"attrs(color)": "blue"},
        3: {"attrs(color)": "yellow"},
        4: {"attrs(color)": "red"},
        5: {"attrs(color)": "blue"},
    }
    assert multi.asdict() == d

    d = {"attrs(color)": {1: "red", 2: "blue", 3: "yellow", 4: "red", 5: "blue"}}
    assert multi.asdict(transpose=True) == d

    multi = H.nodes.multi([H.nodes.degree, H.nodes.attrs("color")])

    d = {
        1: {"degree": 1, "attrs(color)": "red"},
        2: {"degree": 2, "attrs(color)": "blue"},
        3: {"degree": 3, "attrs(color)": "yellow"},
        4: {"degree": 2, "attrs(color)": "red"},
        5: {"degree": 2, "attrs(color)": "blue"},
    }
    assert multi.asdict() == d

    d = {
        1: [1, "red"],
        2: [2, "blue"],
        3: [3, "yellow"],
        4: [2, "red"],
        5: [2, "blue"],
    }
    assert multi.asdict(list) == d


def test_aggregate_stats_types(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert isinstance(H.nodes.degree.max(), int)
    assert isinstance(H.nodes.degree.min(), int)
    assert isinstance(H.nodes.degree.median(), float)
    assert isinstance(H.nodes.degree.mean(), float)
    assert isinstance(H.nodes.degree.sum(), int)
    assert isinstance(H.nodes.degree.std(), float)
    assert isinstance(H.nodes.degree.var(), float)
    assert isinstance(H.nodes.degree.moment(), float)
