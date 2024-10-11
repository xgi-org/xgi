from itertools import chain, combinations

import numpy as np
from scipy.special import binom

from ..core import Hypergraph
from ..utils import Trie

__all__ = [
    "edit_simpliciality",
    "simplicial_edit_distance",
    "face_edit_simpliciality",
    "mean_face_edit_distance",
    "simplicial_fraction",
]


def edit_simpliciality(H, min_size=2, exclude_min_size=True):
    r"""Computes the edit simpliciality.

    The fraction of sub-edges contained when compared to a simplicial complex.

    Parameters
    ----------
    H : xgi.Hypergraph
        The hypergraph of interest
    min_size: int, optional
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces. For more details, see
        the Notes below. By default, 2.
    exclude_min_size : bool, optional
        Whether to exclude minimal simplices when counting simplices.
        For more detailed information, see the Notes below. By default, True.

    Returns
    -------
    float
        The edit simpliciality

    See Also
    --------
    simplicial_edit_distance

    Notes
    -----
    1. The formal definition of a simplicial complex can be unnecessarily
    strict when used to represent perfect inclusion structures.
    By definition, a simplex always contains singletons
    (edges comprising a single node) and the empty set.
    Several datasets will not include such interactions by construction.
    To circumvent this issue, we use a relaxed definition of
    downward closure that excludes edges of a certain size or smaller
    wherever it makes sense. By default, we set the minimum size
    to be 2 since some datasets do not contain singletons.

    2. Hyperedges we call “minimal faces” may significantly skew the
    simpliciality of a dataset. The minimal faces of a hypergraph :math:`H`
    are the edges of the minimal size, i.e., :math:`|e| = \min(K)`, where :math:`K`
    is the set of sizes that we consider based on note 1.
    (In a traditional simplicial complex, the minimal faces are singletons).
    With the size restrictions in place, the minimal faces of a hypergraph
    are always simplices because, by definition, there are no smaller edges
    for these edges to include. When measuring the simpliciality of a dataset,
    it is most meaningful to focus on the faces for which inclusion is possible,
    and so, by default, we exclude these minimal faces when counting potential
    simplices.

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    return 1 - simplicial_edit_distance(
        H, min_size=min_size, exclude_min_size=exclude_min_size
    )


def simplicial_edit_distance(H, min_size=2, exclude_min_size=True, normalize=True):
    r"""Computes the simplicial edit distance.

    The number (or fraction) of sub-edges needed to be added
    to a hypergraph to make it a simplicial complex.

    Parameters
    ----------
    H : xgi.Hypergraph
        The hypergraph of interest
    min_size: int, optional
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces. For more details, see
        the Notes below. By default, 2.
    exclude_min_size : bool, optional
        Whether to exclude minimal simplices when counting simplices.
        For more detailed information, see the Notes below. By default, True.

    normalize : bool, optional
        Whether to normalize by the total number of edges

    Returns
    -------
    float
        The edit simpliciality

    See Also
    --------
    edit_simpliciality

    Notes
    -----
    1. The formal definition of a simplicial complex can be unnecessarily
    strict when used to represent perfect inclusion structures.
    By definition, a simplex always contains singletons
    (edges comprising a single node) and the empty set.
    Several datasets will not include such interactions by construction.
    To circumvent this issue, we use a relaxed definition of
    downward closure that excludes edges of a certain size or smaller
    wherever it makes sense. By default, we set the minimum size
    to be 2 since some datasets do not contain singletons.

    2. Hyperedges we call “minimal faces” may significantly skew the
    simpliciality of a dataset. The minimal faces of a hypergraph :math:`H`
    are the edges of the minimal size, i.e., :math:`|e| = \min(K)`, where :math:`K`
    is the set of sizes that we consider based on note 1.
    (In a traditional simplicial complex, the minimal faces are singletons).
    With the size restrictions in place, the minimal faces of a hypergraph
    are always simplices because, by definition, there are no smaller edges
    for these edges to include. When measuring the simpliciality of a dataset,
    it is most meaningful to focus on the faces for which inclusion is possible,
    and so, by default, we exclude these minimal faces when counting potential
    simplices.

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    edges = H.edges.filterby("size", min_size, "geq").members()

    t = Trie()
    t.build_trie(edges)

    maxH = Hypergraph(
        H.edges.maximal()
        .filterby("size", min_size + exclude_min_size, "geq")
        .members(dtype=dict)
    )
    if not maxH.edges:
        return np.nan

    id_to_num = dict(zip(maxH.edges, range(maxH.num_edges)))

    ms = 0
    for id1, e in maxH.edges.members(dtype=dict).items():
        redundant_missing_faces = set()
        for id2 in maxH.edges.neighbors(id1):
            if id_to_num[id2] < id_to_num[id1]:
                c = maxH._edge[id2].intersection(e)
                if len(c) >= min_size:
                    redundant_missing_faces.update(_missing_subfaces(t, c, min_size))

                    # we don't have to worry about the intersection being a max face
                    # because a) there are no multiedges and b) these are all maximal
                    # faces so no inclusions.
                    if not t.search(c):
                        redundant_missing_faces.add(frozenset(c))

        mf = _count_missing_subfaces(t, e, min_size)
        rmf = len(redundant_missing_faces)
        ms += mf - rmf

    if normalize:
        s = len(edges)
        mf = maxH.num_edges
        if s - mf + ms > 0:
            return ms / (s - mf + ms)
        else:
            return np.nan
    else:
        return ms


def face_edit_simpliciality(H, min_size=2, exclude_min_size=True):
    r"""Computes the face edit simpliciality.

    The average fraction of sub-edges contained in a hyperedge
    relative to a simplex.

    Parameters
    ----------
    H : xgi.Hypergraph
        The hypergraph of interest
    min_size: int, optional
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces. For more details, see
        the Notes below. By default, 2.
    exclude_min_size : bool, optional
        Whether to exclude minimal simplices when counting simplices.
        For more detailed information, see the Notes below. By default, True.

    Returns
    -------
    float
        The face edit simpliciality

    See Also
    --------
    mean_face_edit_distance

    Notes
    -----
    1. The formal definition of a simplicial complex can be unnecessarily
    strict when used to represent perfect inclusion structures.
    By definition, a simplex always contains singletons
    (edges comprising a single node) and the empty set.
    Several datasets will not include such interactions by construction.
    To circumvent this issue, we use a relaxed definition of
    downward closure that excludes edges of a certain size or smaller
    wherever it makes sense. By default, we set the minimum size
    to be 2 since some datasets do not contain singletons.

    2. Hyperedges we call “minimal faces” may significantly skew the
    simpliciality of a dataset. The minimal faces of a hypergraph :math:`H`
    are the edges of the minimal size, i.e., :math:`|e| = \min(K)`, where :math:`K`
    is the set of sizes that we consider based on note 1.
    (In a traditional simplicial complex, the minimal faces are singletons).
    With the size restrictions in place, the minimal faces of a hypergraph
    are always simplices because, by definition, there are no smaller edges
    for these edges to include. When measuring the simpliciality of a dataset,
    it is most meaningful to focus on the faces for which inclusion is possible,
    and so, by default, we exclude these minimal faces when counting potential
    simplices.

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    return 1 - mean_face_edit_distance(
        H, min_size=min_size, exclude_min_size=exclude_min_size
    )


def mean_face_edit_distance(H, min_size=2, exclude_min_size=True, normalize=True):
    r"""Computes the mean face edit distance

    The average number (or fraction) of sub-edges needed to be added to make
    a hyperedge a simplex.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    min_size: int, optional
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces. For more details, see
        the Notes below. By default, 2.
    exclude_min_size : bool, optional
        Whether to exclude minimal simplices when counting simplices.
        For more detailed information, see the Notes below. By default, True.
    normalize : bool, optional
        Whether to normalize the face edit distance, by default True

    Returns
    -------
    float
        The mean face edit distance

    See Also
    --------
    face_edit_simpliciality

    Notes
    -----
    1. The formal definition of a simplicial complex can be unnecessarily
    strict when used to represent perfect inclusion structures.
    By definition, a simplex always contains singletons
    (edges comprising a single node) and the empty set.
    Several datasets will not include such interactions by construction.
    To circumvent this issue, we use a relaxed definition of
    downward closure that excludes edges of a certain size or smaller
    wherever it makes sense. By default, we set the minimum size
    to be 2 since some datasets do not contain singletons.

    2. Hyperedges we call “minimal faces” may significantly skew the
    simpliciality of a dataset. The minimal faces of a hypergraph :math:`H`
    are the edges of the minimal size, i.e., :math:`|e| = \min(K)`, where :math:`K`
    is the set of sizes that we consider based on note 1.
    (In a traditional simplicial complex, the minimal faces are singletons).
    With the size restrictions in place, the minimal faces of a hypergraph
    are always simplices because, by definition, there are no smaller edges
    for these edges to include. When measuring the simpliciality of a dataset,
    it is most meaningful to focus on the faces for which inclusion is possible,
    and so, by default, we exclude these minimal faces when counting potential
    simplices.

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    t = Trie()
    t.build_trie(H.edges.filterby("size", min_size, "geq").members())

    max_faces = (
        H.edges.maximal().filterby("size", min_size + exclude_min_size, "geq").members()
    )
    avg_d = 0
    for e in max_faces:
        if len(e) >= min_size:
            d = _count_missing_subfaces(t, e, min_size=min_size)  # missing subfaces
            m = _max_number_of_subfaces(min_size, len(e))
            if normalize and m != 0:
                d *= 1.0 / m
            avg_d += d / len(max_faces)
    return avg_d


def simplicial_fraction(H, min_size=2, exclude_min_size=True):
    r"""Computing the simplicial fraction for a hypergraph.

    What fraction of the hyperedges are simplices?

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    min_size: int, optional
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces. For more details, see
        the Notes below. By default, 2.
    exclude_min_size : bool, optional
        Whether to exclude minimal simplices when counting simplices.
        For more detailed information, see the Notes below. By default, True.

    Returns
    -------
    float
        The simplicial fraction

    Notes
    -----
    1. The formal definition of a simplicial complex can be unnecessarily
    strict when used to represent perfect inclusion structures.
    By definition, a simplex always contains singletons
    (edges comprising a single node) and the empty set.
    Several datasets will not include such interactions by construction.
    To circumvent this issue, we use a relaxed definition of
    downward closure that excludes edges of a certain size or smaller
    wherever it makes sense. By default, we set the minimum size
    to be 2 since some datasets do not contain singletons.

    2. Hyperedges we call “minimal faces” may significantly skew the
    simpliciality of a dataset. The minimal faces of a hypergraph :math:`H`
    are the edges of the minimal size, i.e., :math:`|e| = \min(K)`, where :math:`K`
    is the set of sizes that we consider based on note 1.
    (In a traditional simplicial complex, the minimal faces are singletons).
    With the size restrictions in place, the minimal faces of a hypergraph
    are always simplices because, by definition, there are no smaller edges
    for these edges to include. When measuring the simpliciality of a dataset,
    it is most meaningful to focus on the faces for which inclusion is possible,
    and so, by default, we exclude these minimal faces when counting potential
    simplices.

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    try:
        ns = _count_simplices(H, min_size, exclude_min_size)
        ps = _potential_simplices(H, min_size, exclude_min_size)
        return ns / ps
    except ZeroDivisionError:
        return np.nan


#### Helper functions
def _powerset(iterable, min_size=1, max_size=None):
    """Generates a modified powerset.

    User can specify the maximum and minimum size
    of the sets in the powerset.

    Parameters
    ----------
    iterable : iterable
        The set for which to compute the powerset.
    min_size: int, default: 1
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.
    max_size : int, default: None.
        The maximum size to include when computing
        the power set. When max_size=None, it generates
        the powerset including the edge itself.

    Returns
    -------
    itertools.chain
        a generator of the sets in the powerset.
    """
    s = iterable
    if max_size is None:
        max_size = len(s)

    return chain.from_iterable(
        combinations(s, r) for r in range(min_size, max_size + 1)
    )


def _count_missing_subfaces(t, face, min_size=1):
    """Computing the edit distance for a single face.

    Parameters
    ----------
    t : Trie
        The trie representing the hypergraph
    face : iterable
        The edge for which to find the edit distance
    min_size: int, default: 1
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.

    Returns
    -------
    int
        The edit distance
    """
    sub_edges = list(_powerset(face, min_size=min_size, max_size=len(face) - 1))
    count = 0
    for e in sub_edges:
        if not t.search(e):
            count += 1
    return count


def _missing_subfaces(t, face, min_size=1):
    """Computing the edit distance for a single face.

    Parameters
    ----------
    t : Trie
        The trie representing the hypergraph
    face : iterable
        The edge for which to find the edit distance
    min_size: int, default: 1
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.

    Returns
    -------
    int
        The edit distance
    """
    sub_edges = list(_powerset(face, min_size=min_size, max_size=len(face) - 1))
    ms = set()
    for e in sub_edges:
        if not t.search(e):
            ms.add(frozenset(e))
    return ms


def _max_number_of_subfaces(min_size, max_size):
    d = 2**max_size - 2  # subtract 2 for the face itself and the empty set
    for i in range(1, min_size):
        d -= binom(max_size, i)
    return int(d)


def _potential_simplices(H, min_size=2, exclude_min_size=True):
    # record total number of hyperedges that are potential simplices
    return len(H.edges.filterby("size", min_size + exclude_min_size, "geq"))


def _count_simplices(H, min_size=2, exclude_min_size=True):
    # build trie data structure
    t = Trie()
    all_edges = H.edges.members()
    t.build_trie(all_edges)

    edges = H.edges.filterby("size", min_size + exclude_min_size, "geq").members()

    # for each hyperedge, determine if it's a simplex
    count = 0
    # The following loop is embarassingly parallel, so parallelize to increase speed would be good
    for e in edges:
        if _is_simplex(t, e, min_size):
            count += 1
    return count


def _is_simplex(t, edge, min_size=2):
    for e in _powerset(edge, min_size):
        if not t.search(e):
            return False
    return True
