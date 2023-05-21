import pytest

import xgi


def test_filterby_wrong_stat():
    H = xgi.DiHypergraph()
    with pytest.raises(AttributeError):
        H.edges.filterby("__I_DO_NOT_EXIST__", None)


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


def test_single_node(diedgelist1):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.order()[1] == 3
    assert H.edges.order[1] == 3
    with pytest.raises(KeyError):
        H.order()[-1]
    with pytest.raises(KeyError):
        H.edges.order[-1]


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


def test_stats_items(diedgelist2):
    d = {0: 2, 1: 2, 2: 3}
    H = xgi.DiHypergraph(diedgelist2)
    for e, s in H.edges.order.items():
        assert d[e] == s


def test_stats_are_views(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    es = H.edges.order
    assert es.asdict() == {0: 2, 1: 2, 2: 3}
    H.add_edge(([3, 4, 5], [6]))
    assert es.asdict() == {0: 2, 1: 2, 2: 3, 3: 3}


def test_different_views(diedgelist1):
    H = xgi.DiHypergraph(diedgelist1)
    with pytest.raises(KeyError):
        H.edges.multi(["order", H.edges([1, 2]).size]).asdict()
    with pytest.raises(KeyError):
        H.edges.multi(["order", H.edges([1, 2]).attrs("color")]).asdict()


def test_user_defined(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)

    with pytest.raises(AttributeError):
        H.user_order
    with pytest.raises(AttributeError):
        H.edges.user_order

    @xgi.diedgestat_func
    def user_order(net, bunch):
        return {n: 10 * net.order(n) for n in bunch}

    vals = {n: 10 * H.order(n) for n in H.edges}
    assert H.user_order() == vals
    assert H.edges.user_order.asdict() == vals
    assert H.edges.user_order.aslist() == [vals[n] for n in H.edges]
    assert H.edges.filterby("order", 2).user_order.asdict() == {0: 20, 1: 20}


def test_view_val(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    assert H.edges.order._val == {0: 3, 1: 3}
    assert H.edges([1]).order._val == {1: 3}

    H = xgi.DiHypergraph(diedgelist2)
    assert H.edges.order._val == {0: 2, 1: 2, 2: 3}
    assert H.edges([1, 2]).order._val == {1: 2, 2: 3}


def test_tail_size(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    H.edges.tail_size.asdict() == {0: 3, 1: 2}

    H = xgi.DiHypergraph(diedgelist2)
    H.edges.tail_size.asdict() == {0: 2, 1: 2, 2: 3}


def test_head_size(diedgelist1, diedgelist2):
    H = xgi.DiHypergraph(diedgelist1)
    H.edges.head_size.asdict() == {0: 1, 1: 3}

    H = xgi.DiHypergraph(diedgelist2)
    H.edges.head_size.asdict() == {0: 1, 1: 1, 2: 2}
