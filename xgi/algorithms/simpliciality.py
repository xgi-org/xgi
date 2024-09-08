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
    """Computes the edit simpliciality.

    The number of edges needed to be added
    to a hypergraph to make it a simplicial complex.

    Parameters
    ----------
    H : xgi.Hypergraph
        The hypergraph of interest
    min_size: int, default: 2
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.
    exclude_min_size : bool, optional
        Whether to include minimal simplices when counting simplices, by default True

    Returns
    -------
    float
        The edit simpliciality

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

    ms = 0
    for id1, e in maxH.edges.members(dtype=dict).items():
        redundant_missing_faces = set()
        for id2 in maxH.edges.neighbors(id1):
            if id2 < id1:
                c = maxH._edge[id2].intersection(e)
                if len(c) >= min_size:
                    redundant_missing_faces.update(_missing_subfaces(t, c, min_size))

                    # we don't have to worry about the intersection being a max face
                    # because a) there are no multiedges and b) these are all maximal
                    # faces so no inclusions.
                    if not t.search(c):
                        redundant_missing_faces.add(frozenset(c))

        nm = _max_number_of_subfaces(min_size, len(e))
        nf = _count_subfaces(t, e, min_size)
        rmf = len(redundant_missing_faces)
        ms += nm - nf - rmf

    try:
        s = len(edges)
        return s / (ms + s)
    except ZeroDivisionError:
        return np.nan


def simplicial_edit_distance(H, min_size=2, exclude_min_size=True, normalize=True):
    """Computes the simplicial edit distance.

    The number of edges needed to be added
    to a hypergraph to make it a simplicial complex.

    Parameters
    ----------
    H : xgi.Hypergraph
        The hypergraph of interest
    min_size: int, default: 2
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.
    exclude_min_size : bool, optional
        Whether to include minimal simplices when counting simplices, by default True
    normalize : bool, optional
        Whether to normalize by the total number of edges

    Returns
    -------
    float
        The edit simpliciality

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

    ms = 0
    for id1, e in maxH.edges.members(dtype=dict).items():
        redundant_missing_faces = set()
        for id2 in maxH.edges.neighbors(id1):
            if id2 < id1:
                c = maxH._edge[id2].intersection(e)
                if len(c) >= min_size:
                    redundant_missing_faces.update(_missing_subfaces(t, c, min_size))

                    # we don't have to worry about the intersection being a max face
                    # because a) there are no multiedges and b) these are all maximal
                    # faces so no inclusions.
                    if not t.search(c):
                        redundant_missing_faces.add(frozenset(c))

        nm = _max_number_of_subfaces(min_size, len(e))
        nf = _count_subfaces(t, e, min_size)
        rmf = len(redundant_missing_faces)
        ms += nm - nf - rmf

    try:
        if normalize:
            s = len(edges)
            return ms / (ms + s)
        else:
            return ms
    except ZeroDivisionError:
        return np.nan


def face_edit_simpliciality(H, min_size=2, exclude_min_size=True):
    """Computes the face edit simpliciality.

    The average number of edges needed to be added
    to a hyperedge to make it a simplex.

    Parameters
    ----------
    H : xgi.Hypergraph
        The hypergraph of interest
    min_size: int, default: 2
        The minimum hyperedge size to include when
        calculating whether a hyperedge is a simplex
        by counting subfaces.
    exclude_min_size : bool, optional
        Whether to include minimal simplices when counting simplices, by default True

    Returns
    -------
    float
        The face edit simpliciality

    References
    ----------
    "The simpliciality of higher-order order networks"
    by Nicholas Landry, Jean-Gabriel Young, and Nicole Eikmeier,
    *EPJ Data Science* **13**, 17 (2024).
    """
    edges = (
        H.edges.maximal().filterby("size", min_size + exclude_min_size, "geq").members()
    )
    t = Trie()
    t.build_trie(H.edges.filterby("size", min_size, "geq").members())

    if not edges:
        return np.nan

    fes = 0
    for e in edges:
        n = _count_subfaces(t, e, min_size=min_size)
        d = _max_number_of_subfaces(min_size, len(e))
        # happens when you include the minimal faces when counting simplices
        try:
            fes += float(n / (d * len(edges)))
        except ZeroDivisionError:
            fes += 1.0 / len(edges)
    return fes


def mean_face_edit_distance(H, min_size=2, exclude_min_size=True, normalize=True):
    """Computes the mean face edit distance

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    min_size : int, optional
        The minimum size to be considered a simplex, by default 2
    exclude_min_size : bool, optional
        Whether to include minimal simplices when counting simplices, by default True
    normalize : bool, optional
        Whether to normalize the face edit distance, by default True

    Returns
    -------
    float
        The mean face edit distance

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
            s = _count_subfaces(t, e, min_size=min_size)
            m = _max_number_of_subfaces(min_size, len(e))
            d = m - s
            if normalize:
                d *= 1.0 / m
            avg_d += d / len(max_faces)
    return avg_d


def simplicial_fraction(H, min_size=2, exclude_min_size=True):
    """Computing the simplicial fraction for a hypergraph.

    What fraction of the hyperedges are simplices?

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    min_size : int, optional
        The minimum edge size to consider a simplex, by default 2
    exclude_min_size : bool, optional
        Whether to include minimal simplices when counting simplices, by default True

    Returns
    -------
    float
        The simplicial fraction

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


def _count_subfaces(t, face, min_size=1):
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
        if t.search(e):
            count += 1

    return count


def _count_subfaces(t, face, min_size=1):
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
        if t.search(e):
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
