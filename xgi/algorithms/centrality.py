"""Algorithms for computing the centralities of nodes (and edges) in a hypergraph."""
from warnings import warn

import networkx as nx
import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import eigsh

from ..classes import convert_labels_to_integers, is_uniform
from ..convert import to_line_graph
from ..exception import XGIError
from ..linalg import clique_motif_matrix, incidence_matrix

__all__ = [
    "clique_eigenvector_centrality",
    "h_eigenvector_centrality",
    "node_edge_centrality",
    "line_vector_centrality",
]


def clique_eigenvector_centrality(H, tol=1e-6):
    """Compute the clique motif eigenvector centrality of a hypergraph.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.
    tol : float, optional
        The tolerance when computing the eigenvector. By default, 1e-6.

    Returns
    -------
    dict
        Centrality, where keys are node IDs and values are centralities. The
        centralities are 1-normalized.

    See Also
    --------
    h_eigenvector_centrality

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    from ..algorithms import is_connected

    # if there aren't any nodes, return an empty dict
    if H.num_nodes == 0:
        return dict()
    # if the hypergraph is not connected,
    # this metric doesn't make sense and should return nan.
    if not is_connected(H):
        return {n: np.nan for n in H.nodes}
    W, node_dict = clique_motif_matrix(H, index=True)
    _, v = eigsh(W.asfptype(), k=1, which="LM", tol=tol)

    # multiply by the sign to try and enforce positivity
    v = np.sign(v[0]) * v / norm(v, 1)
    return {node_dict[n]: v[n].item() for n in node_dict}


def h_eigenvector_centrality(H, max_iter=100, tol=1e-6):
    """Compute the H-eigenvector centrality of a uniform hypergraph.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.
    max_iter : int, optional
        The maximum number of iterations before the algorithm terminates.
        By default, 100.
    tol : float > 0, optional
        The desired L2 error in the centrality vector. By default, 1e-6.

    Returns
    -------
    dict
        Centrality, where keys are node IDs and values are centralities. The
        centralities are 1-normalized.

    Raises
    ------
    XGIError
        If the hypergraph is not uniform.

    See Also
    --------
    clique_eigenvector_centrality

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    from ..algorithms import is_connected

    # if there aren't any nodes, return an empty dict
    if H.num_nodes == 0:
        return dict()
    # if the hypergraph is not connected,
    # this metric doesn't make sense and should return nan.
    if not is_connected(H):
        return {n: np.nan for n in H.nodes}

    m = is_uniform(H)
    if not m:
        raise XGIError("This method is not defined for non-uniform hypergraphs.")

    new_H = convert_labels_to_integers(H, "old-label")

    f = lambda v, m: np.power(v, 1.0 / m)  # noqa: E731
    g = lambda v, x: np.prod(v[list(x)])  # noqa: E731

    x = np.random.uniform(size=(new_H.num_nodes))
    x = x / norm(x, 1)

    for iter in range(max_iter):
        new_x = apply(new_H, x, g)
        new_x = f(new_x, m)
        # multiply by the sign to try and enforce positivity
        new_x = np.sign(new_x[0]) * new_x / norm(new_x, 1)
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
    g : lambda function, optional
        function to apply. By default, sum.

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
    f : lambda function, optional
        The function f as described in Tudisco and Higham.
        Must accept a numpy array. By default, $x^2$.
    g : lambda function, optional
        The function g as described in Tudisco and Higham.
        Must accept a numpy array. By default, $\sqrt{x}$.
    phi : lambda function, optional
        The function phi as described in Tudisco and Higham.
        Must accept a numpy array. By default $x^2$.
    psi : lambda function, optional
        The function psi as described in Tudisco and Higham.
        Must accept a numpy array. By default: $\sqrt{x}$.
    max_iter : int, optional
        Number of iterations at which the algorithm terminates
        if convergence is not reached. By default, 100.
    tol : float > 0, optional
        The total allowable error in the node and edge centralities.
        By default, 1e-6.

    Returns
    -------
    dict, dict
        The node centrality where keys are node IDs and values are associated
        centralities and the edge centrality where keys are the edge IDs and
        values are associated centralities. The centralities of both the nodes
        and edges are 1-normalized.

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
    from ..algorithms import is_connected

    # if there aren't any nodes or edges, return an empty dict
    if H.num_nodes == 0 or H.num_edges == 0 or not is_connected(H):
        return {n: np.nan for n in H.nodes}, {e: np.nan for e in H.edges}
    # if the hypergraph is not connected,
    # this metric doesn't make sense and should return nan.
    # if not is_connected(H):
    #     return {n: np.nan for n in H.nodes}, {e: np.nan for e in H.edges}

    n = H.num_nodes
    m = H.num_edges
    x = np.ones(n) / n
    y = np.ones(m) / m

    I, node_dict, edge_dict = incidence_matrix(H, index=True)

    check = np.inf

    for iter in range(max_iter):
        u = np.multiply(x, g(I @ f(y)))
        v = np.multiply(y, psi(I.T @ phi(x)))
        # multiply by the sign to try and enforce positivity
        new_x = np.sign(u[0]) * u / norm(u, 1)
        new_y = np.sign(v[0]) * v / norm(v, 1)

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


def line_vector_centrality(H):
    """The vector centrality of nodes in the line graph of the hypergraph.
    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest

    Returns
    -------
    dict
        Centrality, where keys are node IDs and values are lists of centralities.

    References
    ----------
    "Vector centrality in hypergraphs", K. Kovalenko, M. Romance, E. Vasilyeva,
    D. Aleja, R. Criado, D. Musatov, A.M. Raigorodskii, J. Flores, I. Samoylenko,
    K. Alfaro-Bittner, M. Perc, S. Boccaletti,
    https://doi.org/10.1016/j.chaos.2022.112397

    """
    from ..algorithms import is_connected

    # If the hypergraph is empty, then return an empty dictionary
    if H.num_nodes == 0:
        return dict()

    if not is_connected(H):
        raise XGIError("This method is not defined for disconnected hypergraphs.")

    LG = to_line_graph(H)
    LGcent = nx.eigenvector_centrality(LG)

    vc = {node: [] for node in H.nodes}

    edge_label_dict = {tuple(edge): index for index, edge in H._edge.items()}

    hyperedge_dims = {tuple(edge): len(edge) for edge in H.edges.members()}

    D = H.edges.size.max()

    for k in range(2, D + 1):
        c_i = np.zeros(len(H.nodes))

        for edge, _ in list(filter(lambda x: x[1] == k, hyperedge_dims.items())):
            for node in edge:
                try:
                    c_i[node] += LGcent[edge_label_dict[edge]]
                except IndexError:
                    raise Exception(
                        "Nodes must be written with the Pythonic indexing (0,1,2...)"
                    )

        c_i *= 1 / k

        for node in H.nodes:
            vc[node].append(c_i[node])

    return vc
