import numpy as np
import xgi
from xgi.exception import XGIError
from itertools import combinations
import random

__all__ = [
    "dynamical_assortativity",
    "degree_assortativity"
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
    
    degs = H.degree()
    k1 = np.mean([degs[n] for n in H.nodes])
    k2 = np.mean([degs[n]**2 for n in H.nodes])
    kk1 = np.mean([degs[n1]*degs[n2] for e in H.edges for n1, n2 in combinations(H.edges.members(e), 2)])
    
    return kk1*k1**2/k2**2 - 1


def degree_assortativity(H, type="uniform", exact=False, num_samples=1000):
    degs = H.degree()
    if exact:
        k1k2 = [choose_nodes(e, degs, type) for e in H.edges if len(H.edges.members(e)) > 1]
    else:
        edges = list([e for e in H.edges if len(H.edges.members(e)) > 1])
        k1k2 = list()

        samples = 0
        while samples < num_samples:
            e = random.choice(edges)
            k1k2.append(choose_nodes(H.edges.members(e), degs, type))
            samples += 1
    return np.corrcoef(np.array(k1k2).T)[0, 1]


def choose_nodes(e, k, type="uniform"):
    if type == "uniform":
        i = np.random.randint(len(e))
        j = i
        while i == j:
            j = np.random.randint(len(e))
        return (np.array([k[e[i]], k[e[j]]]))
    
    elif type == "top-2":
        degs = sorted([k[i] for i in e])[-2:]
        random.shuffle(degs)
        return (degs)
    
    elif type == "top-bottom":
        degs = sorted([k[i] for i in e])[::len(e)-1] 
        random.shuffle(degs)
        return (degs)
    
    else:
        raise XGIError("Invalid choice function!")
