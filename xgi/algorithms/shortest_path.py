"""Algorithms for computing shortest paths in a hypergraph."""

import numpy as np

from ..utils import utilities

__all__ = ["single_source_shortest_path_length", "shortest_path_length"]


def single_source_shortest_path_length(H, source):
    """
    Returns the distances from source to every other node in hypergraph H.

    Parameters
    ----------
    H : xgi.Hypergraph
        Hypergraph on which to compute the distances. Node indexes must be integers.
    source : int
        Index of the node from which to compute the distance to every other node.

    Returns
    -------
    dists : dict
        Dictionary where keys are node indexes and values are the distances from source.
    """

    # 1. Mark all nodes unvisited.
    is_unseen = dict()
    for node in H.nodes:
        is_unseen[node] = True
    n_unseen = len(H.nodes)

    # 2. Assign to every node a tentative distance value.
    dists = dict()
    for node in H.nodes:
        dists[node] = np.inf
    dists[source] = 0
    is_unseen[source] = False
    n_unseen -= 1
    current = source

    # 3. Consider all of unvisited neighbors of current node and calculate their tentative distances to the current node.
    stop_condition = False
    while not stop_condition:
        for ngb in H.nodes.neighbors(current):
            if is_unseen[ngb]:
                increment = 1  # increment = weight(ngb, current) if weighted
                new_dist = dists[current] + increment
                if new_dist < dists[ngb]:
                    dists[ngb] = new_dist
                else:
                    pass
            else:
                pass

        # 4. Mark the current node as visited and remove it from the unvisited set.
        is_unseen[current] = False
        n_unseen -= 1

        # 5. Check for stop condition.
        stop_condition = (n_unseen == 0) or (
            utilities.min_where(dists, is_unseen) == np.inf
        )

        # 6. Otherwise, select the unvisited node that is marked with the smallest tentative distance, set it as the new current node, and go back to step 3.
        min_val = np.inf
        argmin = current
        for node in dists.keys():
            if is_unseen[node]:
                if dists[node] < min_val:
                    min_val = dists[node]
                    argmin = node
                else:
                    pass
            else:
                pass
        current = argmin

    return dists


def shortest_path_length(H):
    """
    Returns a generator of tuples (source, dists) where dists is a dictonary
    containing the distances from source to every other node in hypergraph H,
    for all possible source in H.

    Parameters
    ----------
    H : xgi.Hypergraph
        Hypergraph on which to compute the distances. Node indexes must be integers.

    Returns
    -------
    paths : generator of tuples
        Every tuple is of the form (source, dict_of_lengths), for every possible source.
    """

    for source in H.nodes:
        dists = single_source_shortest_path_length(H, source)
        yield (source, dists)
