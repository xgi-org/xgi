import pytest

import xgi
from xgi.exception import XGIError


def test_subhypergraph(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    new_H = xgi.core.globalviews.subhypergraph(H)

    with pytest.raises(XGIError):
        new_H.add_node(10)

    with pytest.raises(XGIError):
        new_H.add_nodes_from([8, 9, 10])

    with pytest.raises(XGIError):
        new_H.add_node_to_edge(0, 10)

    with pytest.raises(XGIError):
        new_H.add_edge([1, 5, 7])

    with pytest.raises(XGIError):
        new_H.add_edges_from([[1, 7], [7]])

    with pytest.raises(XGIError):
        new_H.remove_node(1)

    with pytest.raises(XGIError):
        new_H.remove_nodes_from([1, 2, 3])

    with pytest.raises(XGIError):
        new_H.remove_edge(1)

    with pytest.raises(XGIError):
        new_H.remove_edges_from([0, 1])

    with pytest.raises(XGIError):
        new_H.remove_node_from_edge(0, 1)

    assert new_H.is_frozen
    assert not H.is_frozen

    assert set(H.nodes) == set(new_H.nodes)
    assert set(H.edges) == set(new_H.edges)

    new_H = xgi.core.globalviews.subhypergraph(H, nodes=[1, 2, 3, 4, 5])
    assert set(new_H.nodes) == {1, 2, 3, 4, 5}
    assert set(new_H.edges) == {0, 1}

    new_H = xgi.core.globalviews.subhypergraph(H, edges=[1, 2])
    assert set(new_H.nodes) == {1, 2, 3, 4, 5, 6, 7, 8}
    assert set(new_H.edges) == {1, 2}
    assert set(new_H.nodes.isolates(ignore_singletons=False)) == {1, 2, 3, 7, 8}

    new_H = xgi.core.globalviews.subhypergraph(H, nodes=[1, 2, 3, 4, 5], edges=[1, 2])
    assert set(new_H.nodes) == {1, 2, 3, 4, 5}
    assert set(new_H.edges) == {1}
    assert set(new_H.nodes.isolates(ignore_singletons=False)) == {1, 2, 3, 5}

    new_H = xgi.core.globalviews.subhypergraph(H, nodes=[4], edges=[0, 1, 2])
    assert set(new_H.nodes) == {4}
    assert set(new_H.edges) == {1}

    new_H = xgi.core.globalviews.subhypergraph(H, nodes=[3, 4, 5, 6], edges=[2])
    assert set(new_H.nodes) == {3, 4, 5, 6}
    assert set(new_H.edges) == {2}
    assert set(new_H.nodes.isolates(ignore_singletons=False)) == {3, 4}

    # test keep isolates
    new_H = xgi.core.globalviews.subhypergraph(
        H, nodes=[3, 4, 5, 6], edges=[2], keep_isolates=False
    )
    assert set(new_H.nodes) == {5, 6}
    assert set(new_H.edges) == {2}
    assert set(new_H.nodes.isolates(ignore_singletons=False)) == set()
