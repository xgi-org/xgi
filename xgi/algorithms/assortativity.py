"""Algorithms for finding the degree assortativity of a hypergraph."""

import random
from itertools import combinations, permutations

import numpy as np

from ..exception import XGIError
from .properties import is_uniform, unique_edge_sizes

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

    See Also
    --------
    degree_assortativity

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
    if H.num_nodes == 0:
        raise XGIError("Hypergraph must contain nodes")
    elif H.num_edges == 0:
        raise XGIError("Hypergraph must contain edges!")

    if not is_uniform(H):
        raise XGIError("Hypergraph must be uniform!")

    if 1 in unique_edge_sizes(H):
        raise XGIError("No singleton edges!")

    d = H.nodes.degree
    members = H.edges.members(dtype=dict)
    k = d.asdict()
    k1 = d.mean()
    k2 = d.moment(2)
    kk1 = np.mean(
        [k[n1] * k[n2] for e in H.edges for n1, n2 in combinations(members[e], 2)]
    )

    return kk1 * k1**2 / k2**2 - 1


def degree_assortativity(H, kind="uniform", exact=False, num_samples=1000):
    """Computes the degree assortativity of a hypergraph

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    kind : str, optional
        the type of degree assortativity. valid choices are
        "uniform", "top-2", and "top-bottom". By default, "uniform".
    exact : bool, optional
        whether to compute over all edges or sample randomly from the
        set of edges. By default, False.
    num_samples : int, optional
        if not exact, specify the number of samples for the computation.
        By default, 1000.

    Returns
    -------
    float
        the degree assortativity

    Raises
    ------
    XGIError
        If there are no nodes or no edges

    See Also
    --------
    dynamical_assortativity

    References
    ----------
    Phil Chodrow,
    Configuration models of random hypergraphs,
    Journal of Complex Networks 2020.
    DOI: 10.1093/comnet/cnaa018
    """

    if H.num_nodes == 0:
        raise XGIError("Hypergraph must contain nodes")
    elif H.num_edges == 0:
        raise XGIError("Hypergraph must contain edges!")

    k = H.degree()
    members = H.edges.members(dtype=dict)
    if exact:
        if kind == "uniform":
            k1k2 = [
                [k[n1], k[n2]]
                for e in H.edges
                for n1, n2 in permutations(members[e], 2)
                if n1 != n2 and len(members[e]) > 1
                # permutations is so that k1 and k2 have the same variance
            ]
        elif kind == "top-2":
            k1k2 = [
                d
                for e in H.edges
                if len(members[e]) > 1
                for d in permutations(_choose_degrees(members[e], k, "top-2"), 2)
                # permutations is so that k1 and k2 have the same variance
            ]
        elif kind == "top-bottom":
            k1k2 = [
                d
                for e in H.edges
                if len(members[e]) > 1
                for d in permutations(_choose_degrees(members[e], k, "top-bottom"), 2)
                # permutations is so that k1 and k2 have the same variance
            ]
        else:
            raise XGIError("Invalid type of degree assortativity!")
    else:
        edges = [e for e in H.edges if len(H.edges.members(e)) > 1]
        k1k2 = [
            np.random.permutation(
                _choose_degrees(members[random.choice(edges)], k, kind)
            )
            for _ in range(num_samples)
        ]

    rho = np.corrcoef(np.array(k1k2).T)[0, 1]
    if np.isnan(rho):
        return 0
    return rho


def _choose_degrees(e, k, kind="uniform"):
    """Choose the degrees of two nodes in a hyperedge.

    Parameters
    ----------
    e : iterable
        the members in a hyperedge
    k : dict
        the degrees where keys are node IDs and values are degrees
    kind : str, optional
        the type of degree assortativity, options are "uniform", "top-2",
        and "top-bottom". By default, "uniform".

    Returns
    -------
    tuple
        two degrees selected from the edge

    Raises
    ------
    XGIError
        if invalid assortativity function chosen

    See Also
    --------
    degree_assortativity

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
            return sorted([k[i] for i in e])[-2:]

        elif kind == "top-bottom":
            # this selects the largest and smallest degrees in one line
            return sorted([k[i] for i in e])[:: len(e) - 1]

        else:
            raise XGIError("Invalid type of degree assortativity!")
    else:
        raise XGIError("Edge must have more than one member!")
