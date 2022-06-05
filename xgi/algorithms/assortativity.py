import numpy as np
import xgi
from xgi.exception import XGIError
from itertools import combinations
import random

__all__ = [
    "dynamical_assortativity",
    "top_2_assortativity",
    "top_bottom_assortativity",
    "uniform_assortativity",
]

def dynamical_assortativity(H):
    """ Gets the dynamical assortativity of a uniform hypergraph.

    Parameters
    ----------
    H : xgi.Hypergraph
        Hypergraph of interest

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    XGIError
        _description_
    """
    if not xgi.is_uniform(H):
        raise XGIError("Hypergraph must be uniform!")
    
    k1 = np.mean([H.degree(n) for n in H.nodes])
    k2 = np.mean([H.degree(n)**2 for n in H.nodes])

    kk1 = np.mean([H.degree(n1)*H.degree(n2) for e in H.edges for n1, n2 in combinations(H.edges.members(e), 2)])
    return kk1*k1**2/k2**2 - 1


def top_2_assortativity(H):
    degrees = dict(H.degree())
    k1 = [max((degrees[n] for n in H.edges.members(e))) for e in H.edges]
    try:
        k2 = [sorted((degrees[n] for n in H.edges.members(e)))[-2] for e in H.edges]
    except IndexError:
        raise XGIError("Hypergraph must not have singleton edges.")
    return np.corrcoef(k1, k2)[0, 1]


def top_bottom_assortativity(H):
    degrees = dict(H.degree())
    k1 = [max((degrees[n] for n in H.edges.members(e))) for e in H.edges]
    k2 = [min((degrees[n] for n in H.edges.members(e))) for e in H.edges]
    return np.corrcoef(k1, k2)[0, 1]


def uniform_assortativity(H):
    degrees = dict(H.degree())
    try:
        k1k2 = [[degrees[n] for n in random.sample(H.edges.members(e), 2)] for e in H.edges]
    except IndexError:
        raise XGIError("Hypergraph must not have singleton edges.")

    return np.corrcoef(*k1k2)[0, 1]