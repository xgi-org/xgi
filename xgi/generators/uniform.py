"""Generate random uniform hypergraphs."""
import warnings

from ..utils import py_random_state
from .classic import empty_hypergraph

__all__ = ["uniform_hypergraph_configuration_model"]


@py_random_state(2)
def uniform_hypergraph_configuration_model(k, m, seed=None):
    """
    A function to generate an m-uniform configuration model

    Parameters
    ----------
    k : dictionary
        This is a dictionary where the keys are node ids
        and the values are node degrees.
    m : int
        specifies the hyperedge size
    seed : integer, random_state, or None (default)
            Indicator of random number generation state.

    Returns
    -------
    Hypergraph object
        The generated hypergraph

    Warns
    -----
    warnings.warn
        If the sums of the degrees are not divisible by m, the
        algorithm still runs, but raises a warning and adds an
        additional connection to random nodes to satisfy this
        condition.

    Notes
    -----
    This algorithm normally creates multi-edges and loopy hyperedges.
    We remove the loopy hyperedges.

    References
    ----------
    "The effect of heterogeneity on hypergraph contagion models"
    by Nicholas W. Landry and Juan G. Restrepo
    https://doi.org/10.1063/5.0020034


    Example
    -------
    >>> import xgi
    >>> import random
    >>> n = 1000
    >>> m = 3
    >>> k = {1: 1, 2: 2, 3: 3, 4: 3}
    >>> H = xgi.uniform_hypergraph_configuration_model(k, m)

    """
    # Making sure we have the right number of stubs
    remainder = sum(k.values()) % m
    if remainder != 0:
        warnings.warn(
            "This degree sequence is not realizable. Increasing the degree of random nodes so that it is."
        )
        random_ids = seed.sample(list(k.keys()), int(round(m - remainder)))
        for id in random_ids:
            k[id] = k[id] + 1

    stubs = []
    # Creating the list to index through
    for id in k:
        stubs.extend([id] * int(k[id]))

    H = empty_hypergraph()
    H.add_nodes_from(k.keys())

    while len(stubs) != 0:
        u = seed.sample(range(len(stubs)), m)
        edge = set()
        for index in u:
            edge.add(stubs[index])
        if len(edge) == m:
            H.add_edge(edge)

        for index in sorted(u, reverse=True):
            del stubs[index]

    return H
