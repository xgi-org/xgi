"""Generate random uniform hypergraphs."""
import random
import warnings

from .classic import empty_hypergraph

__all__ = ["uniform_hypergraph_configuration_model"]


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
    seed : integer or None (default)
        The seed for the random number generator

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
    if seed is not None:
        random.seed(seed)

    # Making sure we have the right number of stubs
    remainder = sum(k.values()) % m
    if remainder != 0:
        warnings.warn(
            "This degree sequence is not realizable. Increasing the degree of random nodes so that it is."
        )
        random_ids = random.sample(list(k.keys()), int(round(m - remainder)))
        for id in random_ids:
            k[id] = k[id] + 1

    stubs = []
    # Creating the list to index through
    for id in k:
        stubs.extend([id] * int(k[id]))

    H = empty_hypergraph()
    H.add_nodes_from(k.keys())

    while len(stubs) != 0:
        u = random.sample(range(len(stubs)), m)
        edge = set()
        for index in u:
            edge.add(stubs[index])
        if len(edge) == m:
            H.add_edge(edge)

        for index in sorted(u, reverse=True):
            del stubs[index]

    return H
