import xgi
import random
import warnings

__all__ = ["uniform_hypergraph_configuration_model"]


def uniform_hypergraph_configuration_model(k, m):
    """
    A function to generate an m-uniform configuration model

    Parameters
    ----------
    k : dictionary
        This is a dictionary where the keys are node ids
        and the values are node degrees.
    m : int
        specifies the hyperedge size

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
    Creates multi-edges and self-loops.

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
    >>> k = {i: random.randint(10, 20) for i in range(n)}
    >>> H = xgi.uniform_hypergraph_configuration_model(k, m)
    """
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

    H = xgi.empty_hypergraph()

    while len(stubs) != 0:
        u = random.sample(range(len(stubs)), m)
        edge = []
        for index in u:
            edge.append(stubs[index])
        H.add_edge(edge)

        for index in sorted(u, reverse=True):
            del stubs[index]

    return H
