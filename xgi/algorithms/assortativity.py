import random
from itertools import combinations

import numpy as np

import xgi
from xgi.exception import XGIError

__all__ = ["dynamical_assortativity", "degree_assortativity"]


def dynamical_assortativity(H):
    """Computes the dynamical assortativity of a uniform hypergraph.

    Parameters
    ----------
    H : xgi.Hypergraph
        Hypergraph of interest

    Returns
    -------
    float
        The dynamical assortativity

    Raises
    ------
    XGIError
        If the hypergraph is not uniform, or if there are no nodes
        or no edges

    References
    ----------
    Nicholas Landry and Juan G. Restrepo,
    Hypergraph assortativity: A dynamical systems perspective,
    Chaos 2022.
    DOI: 10.1063/5.0086905

    """
    if not xgi.is_uniform(H):
        raise XGIError("Hypergraph must be uniform!")

    if H.num_nodes == 0 or H.num_edges == 0:
        raise XGIError("Hypergraph must contain nodes and edges!")

    degs = H.degree()
    k1 = np.mean([degs[n] for n in H.nodes])
    k2 = np.mean([degs[n] ** 2 for n in H.nodes])
    kk1 = np.mean(
        [
            degs[n1] * degs[n2]
            for e in H.edges
            for n1, n2 in combinations(H.edges.members(e), 2)
        ]
    )

    return kk1 * k1**2 / k2**2 - 1


def degree_assortativity(H, type="uniform", exact=False, num_samples=1000):
    """Computes the degree assortativity of a hypergraph

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    type : str, default: "uniform"
        the type of degree assortativity. valid choices are
        "uniform", "top-2", and "top-bottom".
    exact : bool, default: False
        whether to compute over all edges or
        sample randomly from the set of edges
    num_samples : int, default: 1000
        if not exact, specify the number of samples for the computation.

    Returns
    -------
    float
        the degree assortativity

    References
    ----------
    Phil Chodrow,
    Configuration models of random hypergraphs,
    Journal of Complex Networks 2020.
    DOI: 10.1093/comnet/cnaa018
    """
    degs = H.degree()
    if exact:
        k1k2 = [
            choose_degrees(e, degs, type)
            for e in H.edges
            if len(H.edges.members(e)) > 1
        ]
    else:
        edges = list([e for e in H.edges if len(H.edges.members(e)) > 1])
        k1k2 = list()

        samples = 0
        while samples < num_samples:
            e = random.choice(edges)
            k1k2.append(choose_degrees(H.edges.members(e), degs, type))
            samples += 1
    return np.corrcoef(np.array(k1k2).T)[0, 1]


def choose_degrees(e, k, type="uniform"):
    """Choose the degrees of two nodes in a hyperedge.

    Parameters
    ----------
    e : iterable
        the members in a hyperedge
    k : dict
        the degrees where keys are node IDs and values are degrees
    type : str, default: "uniform"
        the type of degree assortativity

    Returns
    -------
    tuple
        two degrees selected from the edge

    Raises
    ------
    XGIError
        if invalid assortativity function chosen

    References
    ----------
    Phil Chodrow,
    Configuration models of random hypergraphs,
    Journal of Complex Networks 2020.
    DOI: 10.1093/comnet/cnaa018
    """
    if len(e) > 1:
        if type == "uniform":
            i = np.random.randint(len(e))
            j = i
            while i == j:
                j = np.random.randint(len(e))
            return np.array([k[e[i]], k[e[j]]])

        elif type == "top-2":
            degs = sorted([k[i] for i in e])[-2:]
            random.shuffle(degs)
            return degs

        elif type == "top-bottom":
            degs = sorted([k[i] for i in e])[:: len(e) - 1]
            random.shuffle(degs)
            return degs

        else:
            raise XGIError("Invalid choice function!")
    else:
        raise XGIError("Edge must have more than one member!")
