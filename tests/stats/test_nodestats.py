import numpy as np
import pytest

import xgi

### node stat specific tests


def test_degree(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    degs = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1}
    assert H.degree() == degs
    assert H.degree(order=2) == {1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1}
    assert H.nodes.degree.asdict() == degs

    H = xgi.Hypergraph(edgelist8)
    degs = {0: 6, 1: 5, 2: 4, 3: 4, 4: 3, 5: 2, 6: 2}
    assert H.degree() == degs
    assert H.degree(order=2) == {0: 3, 1: 2, 2: 3, 3: 3, 4: 2, 5: 2, 6: 0}
    assert H.nodes.degree.asdict() == degs


def test_average_neighbor_degree(edgelist1, edgelist8):
    H = xgi.Hypergraph(edgelist1)
    vals = {1: 1.0, 2: 1.0, 3: 1.0, 4: 0, 5: 2.0, 6: 1.0, 7: 1.5, 8: 1.5}
    assert H.average_neighbor_degree() == vals
    assert H.nodes.average_neighbor_degree().asdict() == vals

    H = xgi.Hypergraph(edgelist8)
    vals = {0: 3.6, 1: 3.5, 2: 4.0, 3: 4.0, 4: 4.2, 5: 4.0, 6: 5.5}
    assert H.average_neighbor_degree() == vals
    assert H.nodes.average_neighbor_degree().asdict() == vals


def test_clustering_coefficient():
    # no nodes
    H = xgi.Hypergraph()

    assert H.clustering_coefficient() == dict()
    assert H.nodes.clustering_coefficient().asdict() == dict()

    # no edges
    H.add_nodes_from(range(3))
    assert H.nodes.clustering_coefficient().asdict() == {0: 0, 1: 0, 2: 0}

    # edges
    edges = [[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]]
    H = xgi.Hypergraph(edges)
    val = H.nodes.clustering_coefficient.asdict()
    true_val = {1: 1, 2: 2 / 3, 3: 2 / 3, 4: 1, 5: 1}
    assert val == true_val


def test_local_clustering_coefficient():
    # no nodes
    H = xgi.Hypergraph()

    assert H.local_clustering_coefficient() == dict()
    assert H.nodes.local_clustering_coefficient().asdict() == dict()

    # no edges
    H.add_nodes_from(range(3))
    assert H.nodes.local_clustering_coefficient().asdict() == {0: 0, 1: 0, 2: 0}

    # edges
    edges = [[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]]
    H = xgi.Hypergraph(edges)
    val = H.nodes.local_clustering_coefficient.asdict()
    true_val = {1: 0, 2: 0, 3: 0.25, 4: 0, 5: 0}
    assert val == true_val


def test_two_node_clustering_coefficient():
    # no nodes
    H = xgi.Hypergraph()

    assert H.two_node_clustering_coefficient() == dict()
    assert H.nodes.two_node_clustering_coefficient().asdict() == dict()

    # no edges
    H.add_nodes_from(range(3))
    assert H.nodes.two_node_clustering_coefficient().asdict() == {0: 0, 1: 0, 2: 0}

    # edges
    edges = [[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]]
    H = xgi.Hypergraph(edges)
    val = H.nodes.two_node_clustering_coefficient(kind="union").asdict()
    true_val = {
        1: 0.41666666666666663,
        2: 0.45833333333333326,
        3: 0.5833333333333333,
        4: 0.6666666666666666,
        5: 0.6666666666666666,
    }
    assert val == true_val


def test_attrs(hyperwithattrs, attr1, attr2, attr3, attr4, attr5):
    H = hyperwithattrs
    attrs = {
        1: attr1,
        2: attr2,
        3: attr3,
        4: attr4,
        5: attr5,
    }
    assert H.nodes.attrs.asdict() == attrs
    assert H.nodes.attrs("color").asdict() == {n: H._node_attr[n]["color"] for n in H}

    filtered = H.nodes.filterby_attr("color", "blue").attrs
    assert filtered.asdict() == {2: attr2, 5: attr5}

    filtered = H.nodes([1, 2, 3]).filterby_attr("color", "blue").attrs
    assert filtered.asdict() == {2: attr2}

    filtered = H.nodes([1, 2, 3]).filterby("degree", 3).attrs
    assert filtered.asdict() == {3: attr3}

    with pytest.raises(ValueError):
        H.nodes.attrs(-1).asdict()


def test_local_edit_simpliciality(
    sc1_with_singletons,
    h_links_and_triangles2,
):
    # no nodes
    H = xgi.Hypergraph()

    assert H.local_edit_simpliciality() == dict()
    assert H.nodes.local_edit_simpliciality().asdict() == dict()

    val = sc1_with_singletons.nodes.local_edit_simpliciality.asdict()
    true_val = {
        1: 1.0,
        2: 1.0,
        3: 1.0,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_edit_simpliciality.asdict()
    true_val = {
        1: 2 / 3,
        2: 2 / 3,
        3: 2 / 3,
        4: 2 / 3,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_edit_simpliciality(min_size=1).asdict()
    true_val = {
        1: 1 / 3,
        2: 1 / 3,
        3: 1 / 3,
        4: 1 / 3,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_edit_simpliciality(
        min_size=1, exclude_min_size=False
    ).asdict()
    true_val = {
        1: 1 / 3,
        2: 1 / 3,
        3: 1 / 3,
        4: 1 / 3,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)


def test_local_face_edit_simpliciality(
    sc1_with_singletons,
    h_links_and_triangles2,
):
    # no nodes
    H = xgi.Hypergraph()

    assert H.local_face_edit_simpliciality() == dict()
    assert H.nodes.local_face_edit_simpliciality().asdict() == dict()

    val = sc1_with_singletons.nodes.local_face_edit_simpliciality.asdict()
    true_val = {
        1: 1.0,
        2: 1.0,
        3: 1.0,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_face_edit_simpliciality.asdict()
    true_val = {
        1: 2 / 3,
        2: 2 / 3,
        3: 2 / 3,
        4: 2 / 3,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_face_edit_simpliciality(
        min_size=1
    ).asdict()
    true_val = {
        1: 0.2222222222222222,
        2: 0.2222222222222222,
        3: 0.2222222222222222,
        4: 0.2222222222222222,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_face_edit_simpliciality(
        min_size=1, exclude_min_size=False
    ).asdict()
    true_val = {
        1: 0.2222222222222222,
        2: 0.2222222222222222,
        3: 0.2222222222222222,
        4: 0.2222222222222222,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)


def test_local_simplicial_fraction(
    sc1_with_singletons,
    h_links_and_triangles2,
):
    # no nodes
    H = xgi.Hypergraph()

    assert H.local_simplicial_fraction() == dict()
    assert H.nodes.local_simplicial_fraction().asdict() == dict()

    val = sc1_with_singletons.nodes.local_simplicial_fraction.asdict()
    true_val = {
        1: 1.0,
        2: 1.0,
        3: 1.0,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_simplicial_fraction.asdict()
    true_val = {
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.0,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_simplicial_fraction(min_size=1).asdict()
    true_val = {
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.0,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)

    val = h_links_and_triangles2.nodes.local_simplicial_fraction(
        min_size=1, exclude_min_size=False
    ).asdict()
    true_val = {
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.0,
    }
    for n in true_val:
        assert np.allclose(val[n], true_val[n])
    assert sorted(val) == sorted(true_val)
