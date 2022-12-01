"""Algorithms for finding the degree assortativity of a hypergraph."""
import random
from itertools import combinations

import numpy as np

from ..classes import is_uniform, unique_edge_sizes
from ..exception import XGIError

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
    if H.num_nodes == 0 or H.num_edges == 0:
        raise XGIError("Hypergraph must contain nodes and edges!")

    if not is_uniform(H):
        raise XGIError("Hypergraph must be uniform!")

    if 1 in unique_edge_sizes(H):
        raise XGIError("No singleton edges!")

    d = H.nodes.degree
    degs = d.asdict()
    k1 = d.mean()
    k2 = d.moment(2)
    kk1 = np.mean(
        [
            degs[n1] * degs[n2]
            for e in H.edges
            for n1, n2 in combinations(H.edges.members(e), 2)
        ]
    )

    return kk1 * k1**2 / k2**2 - 1


def degree_assortativity(H, kind="uniform", exact=False, num_samples=1000):
    """Computes the degree assortativity of a hypergraph

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    kind : str, default: "uniform"
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
            choose_degrees(H.edges.members(e), degs, kind)
            for e in H.edges
            if len(H.edges.members(e)) > 1
        ]
    else:
        edges = [e for e in H.edges if len(H.edges.members(e)) > 1]
        k1k2 = [
            choose_degrees(H.edges.members(random.choice(edges)), degs, kind)
            for _ in range(num_samples)
        ]

    rho = np.corrcoef(np.array(k1k2).T)[0, 1]
    if np.isnan(rho):
        return 0
    return rho


def choose_degrees(e, k, kind="uniform"):
    """Choose the degrees of two nodes in a hyperedge.

    Parameters
    ----------
    e : iterable
        the members in a hyperedge
    k : dict
        the degrees where keys are node IDs and values are degrees
    kind : str, default: "uniform"
        the type of degree assortativity, options are
        "uniform", "top-2", and "top-bottom".

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
    e = list(e)
    if len(e) > 1:
        if kind == "uniform":
            i = np.random.randint(len(e))
            j = i
            while i == j:
                j = np.random.randint(len(e))
            return (k[e[i]], k[e[j]])

        elif kind == "top-2":
            degs = sorted([k[i] for i in e])[-2:]
            random.shuffle(degs)
            return degs

        elif kind == "top-bottom":
            # this selects the largest and smallest degrees in one line
            degs = sorted([k[i] for i in e])[:: len(e) - 1]
            random.shuffle(degs)
            return degs

        else:
            raise XGIError("Invalid choice function!")
    else:
        raise XGIError("Edge must have more than one member!")
