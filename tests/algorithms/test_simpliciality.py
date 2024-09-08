import xgi
import numpy as np


def test_edit_simpliciality(
    sc1_with_singletons,
    h_missing_one_singleton,
    h_missing_one_link,
    h_links_and_triangles2,
    h1,
):
    # simplicial complex
    es = xgi.edit_simpliciality(sc1_with_singletons)
    assert es == 1.0

    es = xgi.edit_simpliciality(sc1_with_singletons, min_size=1)
    assert es == 1.0

    es = xgi.edit_simpliciality(sc1_with_singletons, min_size=1, exclude_min_size=False)
    assert es == 1.0

    # h1
    es = xgi.edit_simpliciality(h_missing_one_singleton)
    assert es == 1.0

    es = xgi.edit_simpliciality(h_missing_one_singleton, min_size=1)
    assert np.allclose(es, 6 / 7)

    es = xgi.edit_simpliciality(
        h_missing_one_singleton, min_size=1, exclude_min_size=False
    )
    assert np.allclose(es, 6 / 7)

    # h2
    es = xgi.edit_simpliciality(h_missing_one_link)
    assert np.allclose(es, 3 / 4)

    es = xgi.edit_simpliciality(h_missing_one_link, min_size=1)
    assert np.allclose(es, 6 / 7)

    # links and triangles 2
    es = xgi.edit_simpliciality(h_links_and_triangles2)
    assert np.allclose(es, 3 / 4)

    es = xgi.edit_simpliciality(h_links_and_triangles2, min_size=1)
    assert np.allclose(es, 1 / 2)

    es = xgi.edit_simpliciality(h_links_and_triangles2, exclude_min_size=False)
    assert np.allclose(es, 3 / 4)

    # test h1
    es = xgi.edit_simpliciality(h1)
    s = 4
    m = 4 + 10
    assert np.allclose(es, s / (m + s))

    es = xgi.edit_simpliciality(h1, min_size=1)
    s = 4
    m = 4 + 10 + 7
    assert np.allclose(es, s / (m + s))

    es = xgi.edit_simpliciality(h1, exclude_min_size=False)
    s = 4
    m = 4 + 10
    assert np.allclose(es, s / (m + s))


def test_face_edit_simpliciality(
    sc1_with_singletons,
    h_missing_one_singleton,
    h_missing_one_link,
    h_links_and_triangles2,
):
    # simplicial complex
    fes = xgi.face_edit_simpliciality(sc1_with_singletons)
    assert fes == 1.0

    fes = xgi.face_edit_simpliciality(sc1_with_singletons, min_size=1)
    assert fes == 1.0

    fes = xgi.face_edit_simpliciality(
        sc1_with_singletons, min_size=1, exclude_min_size=False
    )
    assert fes == 1.0

    # h1
    fes = xgi.face_edit_simpliciality(h_missing_one_singleton)
    assert fes == 1.0

    fes = xgi.face_edit_simpliciality(h_missing_one_singleton, min_size=1)
    assert np.allclose(fes, 5 / 6)

    fes = xgi.face_edit_simpliciality(
        h_missing_one_singleton, min_size=1, exclude_min_size=False
    )
    assert np.allclose(fes, 5 / 6)

    # h2
    fes = xgi.face_edit_simpliciality(h_missing_one_link)
    assert np.allclose(fes, 2 / 3)

    fes = xgi.face_edit_simpliciality(h_missing_one_link, min_size=1)
    assert np.allclose(fes, 5 / 6)

    # links and triangles 2
    fes = xgi.face_edit_simpliciality(h_links_and_triangles2)
    assert np.allclose(fes, 2 / 3)

    fes = xgi.face_edit_simpliciality(h_links_and_triangles2, min_size=1)
    assert np.allclose(fes, 2 / 9)

    fes = xgi.face_edit_simpliciality(h_links_and_triangles2, exclude_min_size=False)
    assert np.allclose(fes, 7 / 9)


def test_simplicial_fraction(
    sc1_with_singletons, h_missing_one_singleton, h_missing_one_link
):
    # simplicial complex
    sf = xgi.simplicial_fraction(sc1_with_singletons)
    assert sf == 1.0

    sf = xgi.simplicial_fraction(sc1_with_singletons, min_size=1)
    assert sf == 1.0

    sf = xgi.simplicial_fraction(
        sc1_with_singletons, min_size=1, exclude_min_size=False
    )
    assert sf == 1.0

    # h1
    sf = xgi.simplicial_fraction(h_missing_one_singleton)
    assert sf == 1.0

    sf = xgi.simplicial_fraction(h_missing_one_singleton, min_size=1)
    assert sf == 1 / 4

    sf = xgi.simplicial_fraction(
        h_missing_one_singleton, min_size=1, exclude_min_size=False
    )
    assert sf == 0.5

    # h2
    sf = xgi.simplicial_fraction(h_missing_one_link)
    assert sf == 0

    sf = xgi.simplicial_fraction(h_missing_one_link, min_size=1)
    assert sf == 2 / 3


def test_is_simplex(sc1_with_singletons, h_missing_one_singleton):
    t = xgi.Trie()
    edges = sc1_with_singletons.edges.members()
    t.build_trie(edges)

    is_simplex = xgi.algorithms.simpliciality._is_simplex

    assert is_simplex(t, {1, 2, 3}, min_size=2)
    assert is_simplex(t, {1, 2, 3}, min_size=1)
    assert is_simplex(t, {1, 2}, min_size=1)

    t = xgi.Trie()
    edges = h_missing_one_singleton.edges.members()
    t.build_trie(edges)

    assert is_simplex(t, {1, 2, 3})
    assert not is_simplex(t, {1, 2, 3}, min_size=1)
    assert not is_simplex(t, {2, 3}, min_size=1)
    assert is_simplex(t, {1, 2}, min_size=1)


def test_count_simplices(sc1_with_singletons, h_missing_one_singleton):
    count_simplices = xgi.algorithms.simpliciality._count_simplices

    ns = count_simplices(sc1_with_singletons)
    assert ns == 1

    ns = count_simplices(sc1_with_singletons, min_size=1)
    assert ns == 4

    ns = count_simplices(sc1_with_singletons, min_size=1, exclude_min_size=False)
    assert ns == 7

    ns = count_simplices(h_missing_one_singleton, min_size=1)
    assert ns == 1


def test_potential_simplices(sc1_with_singletons, h_missing_one_link):
    potential_simplices = xgi.algorithms.simpliciality._potential_simplices

    ps = potential_simplices(sc1_with_singletons)
    assert ps == 1

    ps = potential_simplices(sc1_with_singletons, min_size=1)
    assert ps == 4

    ps = potential_simplices(sc1_with_singletons, min_size=1, exclude_min_size=False)
    assert ps == 7

    ps = potential_simplices(h_missing_one_link, min_size=1)
    assert ps == 3


def test_powerset():
    powerset = xgi.algorithms.simpliciality._powerset
    a = {1, 2, 3}

    # test default behavior
    subsets = {frozenset(s) for s in powerset(a, min_size=1)}
    assert subsets == {
        frozenset({1}),
        frozenset({2}),
        frozenset({3}),
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({2, 3}),
        frozenset({1, 2, 3}),
    }

    subsets = {frozenset(s) for s in powerset(a, min_size=2)}
    assert subsets == {
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({2, 3}),
        frozenset({1, 2, 3}),
    }

    subsets = {frozenset(s) for s in powerset(a, max_size=2)}
    assert subsets == {
        frozenset({1}),
        frozenset({2}),
        frozenset({3}),
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({2, 3}),
    }


def test_count_subfaces(h_missing_one_link):
    count_subfaces = xgi.algorithms.simpliciality._count_subfaces
    t = xgi.Trie()
    t.build_trie(h_missing_one_link.edges.members())
    assert count_subfaces(t, {1}, min_size=2) == 0
    assert count_subfaces(t, {2, 3}, min_size=2) == 0
    assert count_subfaces(t, {2, 3}) == 2
    assert count_subfaces(t, {1, 2, 3}) == 5
    assert count_subfaces(t, {1, 2, 3}, min_size=2) == 2


def test_max_number_of_subfaces():
    max_number_of_subfaces = xgi.algorithms.simpliciality._max_number_of_subfaces
    assert max_number_of_subfaces(1, 3) == 6
    assert max_number_of_subfaces(2, 3) == 3
    assert max_number_of_subfaces(1, 4) == 14
    assert max_number_of_subfaces(2, 4) == 10
