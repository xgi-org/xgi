"""Algorithms for computing the centralities of nodes (and edges) in a hypergraph."""
from warnings import warn

import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import eigsh

from ..classes import convert_labels_to_integers, is_uniform
from ..exception import XGIError
from ..linalg import clique_motif_matrix, incidence_matrix

__all__ = ["CEC_centrality", "HEC_centrality", "ZEC_centrality", "node_edge_centrality"]


def CEC_centrality(H, tol=1e-6):
    """Compute the CEC centrality of a hypergraph.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.
    tol : float, default: 1e-6
        The tolerance when computing the eigenvector.

    Returns
    -------
    dict
        Centrality, where keys are node IDs and values are centralities.

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    W, node_dict = clique_motif_matrix(H, index=True)
    _, v = eigsh(W.asfptype(), k=1, which="LM", tol=tol)
    return {node_dict[n]: v[n].item() for n in node_dict}


def ZEC_centrality(H, max_iter=100, tol=1e-6):
    """Compute the ZEC centrality of a hypergraph.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.
    max_iter : int, default: 100
        The maximum number of iterations before the algorithm terminates.
    tol : float > 0, default: 1e-6
        The desired L2 error in the centrality vector.

    Returns
    -------
    dict
        Centrality, where keys are node IDs and values are centralities.

    Notes
    -----
    As noted in the corresponding reference, the eigenvectors may not be unique,
    i.e., the algorithm may converge to different values for each run.

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    new_H = convert_labels_to_integers(H, "old-label")

    g = lambda v, e: np.prod(v[list(e)])

    x = np.random.uniform(size=(new_H.num_nodes))
    for iter in range(max_iter):
        new_x = apply(new_H, x, g)
        new_x = new_x / norm(new_x)
        if norm(x - new_x) <= tol:
            break
        x = new_x.copy()
    else:
        warn("Iteration did not converge!")
    return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, new_x)}


def HEC_centrality(H, max_iter=100, tol=1e-6):
    """Compute the HEC centrality of a uniform hypergraph.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.
    max_iter : int, default: 100
        The maximum number of iterations before the algorithm terminates.
    tol : float > 0, default: 1e-6
        The desired L2 error in the centrality vector.

    Returns
    -------
    dict
        Centrality, where keys are node IDs and values are centralities.

    Raises
    ------
    XGIError
        If the hypergraph is not uniform.

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    new_H = convert_labels_to_integers(H, "old-label")

    m = is_uniform(H)
    if not m:
        raise XGIError("This method is not defined for non-uniform hypergraphs.")
    f = lambda v, m: np.power(v, 1.0 / m)
    g = lambda v, x: np.prod(v[list(x)])

    x = np.random.uniform(size=(new_H.num_nodes))
    for iter in range(max_iter):
        new_x = apply(new_H, x, g)
        new_x = f(new_x, m)
        new_x = new_x / norm(new_x)
        if norm(x - new_x) <= tol:
            break
        x = new_x.copy()
    else:
        warn("Iteration did not converge!")
    return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, new_x)}


def apply(H, x, g=lambda v, e: np.sum(v[list(e)])):
    """Apply a vector to the hypergraph given a function.

    Parameters
    ----------
    H : Hypergraph
        Hypergraph of interest.
    x : 1D numpy array
        1D vector
    g : lambda function, default: sum
        function to apply

    Returns
    -------
    1D numpy array
        vector post application
    """
    new_x = np.zeros(H.num_nodes)
    for edge in H.edges.members():
        edge = list(edge)
        # ordered permutations
        for shift in range(len(edge)):
            new_x[edge[shift]] += g(x, edge[shift + 1 :] + edge[:shift])
    return new_x


def node_edge_centrality(
    H,
    f=lambda x: np.power(x, 2),
    g=lambda x: np.power(x, 0.5),
    phi=lambda x: np.power(x, 2),
    psi=lambda x: np.power(x, 0.5),
    max_iter=100,
    tol=1e-6,
):
    """Computes the node and edge centralities

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    f : lambda function, default: x^2
        The function f as described in Tudisco and Higham.
        Must accept a numpy array.
    g : lambda function, default: x^0.5
        The function g as described in Tudisco and Higham.
        Must accept a numpy array.
    phi : lambda function, default: x^2
        The function phi as described in Tudisco and Higham.
        Must accept a numpy array.
    psi : lambda function, default: x^0.5
        The function psi as described in Tudisco and Higham.
        Must accept a numpy array.
    max_iter : int, default: 100
        Number of iterations at which the algorithm terminates
        if convergence is not reached.
    tol : float > 0, default: 1e-6
        The total allowable error in the node and edge centralities.

    Returns
    -------
    dict, dict
        The node centrality where keys are node IDs and values are associated
        centralities and the edge centrality where keys are the edge IDs and
        values are associated centralities.

    Notes
    -----
    In the paper from which this was taken, it is more general in that it includes
    general functions for both nodes and edges, nodes and edges may be weighted,
    and one can choose different norms for normalization.

    References
    ----------
    Node and edge nonlinear eigenvector centrality for hypergraphs,
    Francesco Tudisco & Desmond J. Higham,
    https://doi.org/10.1038/s42005-021-00704-2
    """

    n = H.num_nodes
    m = H.num_edges
    x = np.ones(n) / n
    y = np.ones(m) / m

    I, node_dict, edge_dict = incidence_matrix(H, index=True)

    check = np.inf

    for iter in range(max_iter):
        u = np.multiply(x, g(I * f(y)))
        v = np.multiply(y, psi(I.T * phi(x)))
        new_x = u / norm(u)
        new_y = v / norm(v)

        check = norm(new_x - x) + norm(new_y - y)
        if check < tol:
            break
        x = new_x.copy()
        y = new_y.copy()
    else:
        warn("Iteration did not converge!")
    return {node_dict[n]: new_x[n] for n in node_dict}, {
        edge_dict[e]: new_y[e] for e in edge_dict
    }
