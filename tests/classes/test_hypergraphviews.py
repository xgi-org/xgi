import xgi
import pytest
from xgi.exception import XGIError


def test_generic_hypergraph_view(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    new_H = xgi.classes.hypergraphviews.generic_hypergraph_view(H)

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

    assert xgi.is_frozen(new_H)
    assert not xgi.is_frozen(H)

    assert list(H.nodes) == list(new_H.nodes)
    assert list(H.edges) == list(new_H.edges)


def test_subhypergraph_view(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    new_H = xgi.classes.hypergraphviews.subhypergraph_view(H)

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

    assert xgi.is_frozen(new_H)
    assert not xgi.is_frozen(H)

    assert list(H.nodes) == list(new_H.nodes)
    assert list(H.edges) == list(new_H.edges)
    print("hi")
    new_H = xgi.classes.hypergraphviews.subhypergraph_view(
        H, filtered_nodes=[1, 2, 3, 4, 5]
    )
    assert list(new_H.nodes) == [1, 2, 3, 4, 5]
    assert list(new_H.edges) == [0, 1]

    new_H = xgi.classes.hypergraphviews.subhypergraph_view(H, filtered_edges=[1, 2])
    assert list(new_H.nodes) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert list(new_H.edges) == [1, 2]
    assert new_H.isolates(ignore_singletons=False) == {1, 2, 3, 7, 8}

    new_H = xgi.classes.hypergraphviews.subhypergraph_view(
        H, filtered_nodes=[1, 2, 3, 4, 5], filtered_edges=[1, 2]
    )
    assert list(new_H.nodes) == [1, 2, 3, 4, 5]
    assert list(new_H.edges) == [1]
    assert new_H.isolates(ignore_singletons=False) == {1, 2, 3, 5}
