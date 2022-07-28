import pandas as pd
import pytest

import xgi
from xgi.exception import IDNotFound


def test_filterby_wrong_stat():
    H = xgi.Hypergraph()
    with pytest.raises(AttributeError):
        H.edges.filterby("__I_DO_NOT_EXIST__", None)


def test_filterby(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    assert H.edges.filterby("order", 2).size.asdict() == {0: 3, 3: 3}
    assert H.edges.filterby("size", 2).order.asdict() == {2: 1}

    H = xgi.Hypergraph(edgelist8)
    assert H.edges.filterby("order", 2).size.asdict() == {1: 3, 2: 3, 4: 3, 5: 3, 6: 3}
    assert H.edges.filterby("size", 2).order.asdict() == {0: 1, 8: 1, 7: 1}


def test_call_filterby(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    assert H.edges([1, 2, 3]).filterby("order", 2).size.asdict() == {3: 3}

    H = xgi.Hypergraph(edgelist8)
    assert H.edges([5, 6]).filterby("order", 2).size.asdict() == {5: 3, 6: 3}


def test_filterby_with_nodestat(edgelist4, edgelist8):
    H = xgi.Hypergraph(edgelist4)
    assert list(H.edges.filterby(H.edges.order(degree=2), 2)) == [1]

    H = xgi.Hypergraph(edgelist8)
    assert list(H.edges.filterby(H.edges.order(degree=4), 1)) == [2, 3]


def test_single_node(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert H.order()[1] == 0
    assert H.edges.order[1] == 0
    with pytest.raises(KeyError):
        H.order()[-1]
    with pytest.raises(KeyError):
        H.edges.order[-1]


def test_aggregates(edgelist1, edgelist2, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    assert H.edges.order.max() == 2
    assert H.edges.order.min() == 0
    assert round(H.edges.order.mean(), 3) == 1.25
    assert round(H.edges.order.std(), 3) == 0.829
    assert round(H.edges.order.var(), 3) == 0.688

    H = xgi.Hypergraph(edgelist2)
    assert H.edges.order.max() == 2
    assert H.edges.order.min() == 1
    assert round(H.edges.order.mean(), 3) == 1.333
    assert round(H.edges.order.std(), 3) == 0.471
    assert round(H.edges.order.var(), 3) == 0.222

    H = xgi.Hypergraph(edgelist8)
    assert H.edges.order.max() == 4
    assert H.edges.order.min() == 1
    assert round(H.edges.order.mean(), 3) == 1.889
    assert round(H.edges.order.std(), 3) == 0.875
    assert round(H.edges.order.var(), 3) == 0.765


def test_stats_are_views(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    es = H.edges.order
    assert es.asdict() == {0: 2, 1: 0, 2: 1, 3: 2}
    H.add_edge([3, 4, 5])
    assert es.asdict() == {0: 2, 1: 0, 2: 1, 3: 2, 4: 2}


def test_different_views(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    with pytest.raises(KeyError):
        H.edges.multi(["order", H.edges([1, 2]).size]).asdict()
    with pytest.raises(KeyError):
        H.edges.multi(["order", H.edges([1, 2]).attrs("color")]).asdict()


def test_user_defined(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    with pytest.raises(AttributeError):
        H.user_order
    with pytest.raises(AttributeError):
        H.edges.user_order

    @xgi.edgestat_func
    def user_order(net, bunch):
        return {n: 10 * net.order(n) for n in bunch}

    vals = {n: 10 * H.order(n) for n in H.edges}
    assert H.user_order() == vals
    assert H.edges.user_order.asdict() == vals
    assert H.edges.user_order.aslist() == [vals[n] for n in H.edges]
    assert (
        list(H.edges.filterby("user_order", 20))
        == list(H.edges.filterby("order", 2))
        == [0, 3]
    )
    assert H.edges.filterby("order", 2).user_order.asdict() == {0: 20, 3: 20}


def test_view_val(edgelist1, edgelist2):
    H = xgi.Hypergraph(edgelist1)
    assert H.edges.order._val == {0: 2, 1: 0, 2: 1, 3: 2}
    assert H.edges([1, 2]).order._val == {1: 0, 2: 1}

    H = xgi.Hypergraph(edgelist2)
    assert H.edges.order._val == {0: 1, 1: 1, 2: 2}
    assert H.edges([1, 2]).order._val == {1: 1, 2: 2}
