"""Algorithms for computing the centralities of nodes (and edges) in a hypergraph."""

from warnings import warn

import networkx as nx
import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import eigsh

from ..convert import to_line_graph
from ..exception import XGIError
from ..linalg import clique_motif_matrix, incidence_matrix
from ..utils import convert_labels_to_integers, pairwise_incidence, ttsv1, ttsv2
from .connected import is_connected
from .properties import is_uniform

__all__ = [
    "clique_eigenvector_centrality",
    "h_eigenvector_centrality",
    "z_eigenvector_centrality",
    "node_edge_centrality",
    "line_vector_centrality",
    "katz_centrality",
    "uniform_h_eigenvector_centrality",
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
    z_eigenvector_centrality

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    # if there aren't any nodes, return an empty dict
    if H.num_nodes == 0:
        return dict()
    # if the hypergraph is not connected,
    # this metric doesn't make sense and should return nan.
    if not is_connected(H):
        return {n: np.nan for n in H.nodes}
    W, node_dict = clique_motif_matrix(H, index=True)
    _, v = eigsh(W.astype(float), k=1, which="LM", tol=tol)

    # multiply by the sign to try and enforce positivity
    v = np.sign(v[0]) * v / norm(v, 1)
    return {node_dict[n]: v[n].item() for n in node_dict}


def node_edge_centrality(
    H,
    f=lambda x: np.power(x, 2),
    g=lambda x: np.power(x, 0.5),
    phi=lambda x: np.power(x, 2),
    psi=lambda x: np.power(x, 0.5),
    max_iter=100,
    tol=1e-6,
):
    r"""Computes the node and edge centralities

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    f : lambda function, optional
        The function f as described in Tudisco and Higham.
        Must accept a numpy array. By default, :math:`f(x) = x^2`.
    g : lambda function, optional
        The function g as described in Tudisco and Higham.
        Must accept a numpy array. By default, :math`g(x) = \sqrt{x}`.
    phi : lambda function, optional
        The function phi as described in Tudisco and Higham.
        Must accept a numpy array. By default :math:`\phi(x) = x^2`.
    psi : lambda function, optional
        The function psi as described in Tudisco and Higham.
        Must accept a numpy array. By default: :math:`\psi(x) = \sqrt{x}`.
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
    # if the hypergraph is not connected or is empty,
    # this metric doesn't make sense and should return nan.
    if H.num_nodes == 0 or H.num_edges == 0 or not is_connected(H):
        return {n: np.nan for n in H.nodes}, {e: np.nan for e in H.edges}

    n = H.num_nodes
    m = H.num_edges
    x = np.ones(n) / n
    y = np.ones(m) / m

    I, node_dict, edge_dict = incidence_matrix(H, index=True)

    check = np.inf

    for it in range(max_iter):
        u = (x * g(I @ f(y))) ** 0.5
        v = (y * psi(I.T @ phi(x))) ** 0.5
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


def katz_centrality(H, cutoff=100):
    r"""Returns the Katz-centrality vector of a non-empty hypergraph H.

    The Katz-centrality measures the relative importance of a node by counting
    how many distinct walks start from it. The longer the walk is the smaller
    its contribution will be (attenuation factor :math:`\alpha`).
    Initially defined for graphs, the Katz-centrality is here generalized to
    hypergraphs using the most basic definition of neighbors: two nodes that
    share an hyperedge.

    Parameters
    ----------
    H : xgi.Hypergraph
        Hypergraph on which to compute the Katz-centralities.
    cutoff : int
        Power at which to stop the series :math:`A + \alpha A^2 + \alpha^2 A^3 + \dots`
        Default value is 100.

    Returns
    -------
    c : dict
        `c` is a dictionary with node IDs as keys and centrality values
        as values. The centralities are 1-normalized.

    Raises
    ------
    XGIError
        If the hypergraph is empty.

    Notes
    -----
    [1] The Katz-centrality is defined as

    .. math::
        c = [(I - \alpha A^{t})^{-1} - I]{\bf 1},

    where :math:`A` is the adjacency matrix of the the (hyper)graph.
    Since :math:`A^{t} = A` for undirected graphs (our case), we have:


    .. math::
        &[I + A + \alpha A^2 + \alpha^2 A^3 + \dots](I - \alpha A^{t})

        & = [I + A + \alpha A^2 + \alpha^2 A^3 + \dots](I - \alpha A)

        & = (I + A + \alpha A^2 + \alpha^2 A^3 + \dots) - A - \alpha A^2

        & - \alpha^2 A^3 - \alpha^3 A^4 - \dots

        & = I

    And :math:`(I - \alpha A^{t})^{-1} = I + A + \alpha A^2 + \alpha^2 A^3 + \dots`
    Thus we can use the power series to compute the Katz-centrality.
    [2] The Katz-centrality of isolated nodes (no hyperedges contains them) is
    zero. The Katz-centrality of an empty hypergraph is not defined.

    References
    ----------
    See https://en.wikipedia.org/wiki/Katz_centrality#Alpha_centrality (visited
    May 20 2023) for a clear definition of Katz centrality.
    """
    n = H.num_nodes
    m = H.num_edges

    if n == 0:  # no nodes
        raise XGIError("The Katz-centrality of an empty hypergraph is not defined.")
    elif m == 0:
        c = np.zeros(n)
    else:  # there is at least one edge, both N and M are non-zero
        A = clique_motif_matrix(H)
        alpha = 1 / 2**n
        mat = A
        for power in range(1, cutoff):
            mat = alpha * mat.dot(A) + A
        u = 1 / n * np.ones(n)
        c = mat.dot(u)
        c *= 1 / norm(c, 1)
    nodedict = dict(zip(range(n), H.nodes))
    return {nodedict[idx]: c[idx] for idx in nodedict}


def h_eigenvector_centrality(H, max_iter=100, tol=1e-6):
    """Compute the H-eigenvector centrality of a hypergraph.

    The H-eigenvector terminology comes from Qi (2005) which
    defines a "tensor H-eigenpair".

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.
    max_iter : int, optional
        The maximum number of iterations before the algorithm terminates.
        By default, 100.
    tol : float > 0, optional
        The desired convergence tolerance. By default, 1e-6.

    Returns
    -------
    dict
        Centrality, where keys are node IDs and values are centralities. The
        centralities are 1-normalized.

    See Also
    --------
    clique_eigenvector_centrality
    z_eigenvector_centrality
    uniform_h_eigenvector_centrality

    References
    ----------
    Scalable Tensor Methods for Nonuniform Hypergraphs,
    Sinan Aksoy, Ilya Amburg, Stephen Young,
    https://doi.org/10.1137/23M1584472

    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031

    Computing tensor Z-eigenvectors with dynamical systems
    Austin R. Benson and David F. Gleich
    https://doi.org/10.1137/18M1229584

    Liqun Qi
    "Eigenvalues of a real supersymmetric tensor"
    Journal of Symbolic Computation, **40**, *6* (2005).
    https://doi.org/10.1016/j.jsc.2005.05.007.
    """
    # if there aren't any nodes, return an empty dict
    if H.num_nodes == 0:
        return dict()
    # if the hypergraph is not connected,
    # this metric doesn't make sense and should return nan.
    if not is_connected(H):
        return {n: np.nan for n in H.nodes}

    new_H = convert_labels_to_integers(H, "old-label")
    edge_dict = new_H.edges.members(dtype=dict)
    node_dict = new_H.nodes.memberships()
    r = new_H.edges.size.max()

    x = np.random.uniform(size=(new_H.num_nodes))
    x = x / norm(x, 1)
    y = np.abs(np.array(ttsv1(node_dict, edge_dict, r, x)))

    converged = False
    it = 0
    while it < max_iter and not converged:
        y_scaled = [_y ** (1 / (r - 1)) for _y in y]
        x = y_scaled / norm(y_scaled, 1)
        y = np.abs(np.array(ttsv1(node_dict, edge_dict, r, x)))
        s = [a / (b ** (r - 1)) for a, b in zip(y, x)]
        if (np.max(s) - np.min(s)) / np.min(s) < tol:
            break
        it += 1
    else:
        warn("Iteration did not converge!")
    return {
        new_H.nodes[n]["old-label"]: c.item()
        for n, c in zip(new_H.nodes, x / norm(x, 1))
    }


def z_eigenvector_centrality(H, max_iter=100, tol=1e-6):
    """Compute the Z-eigenvector centrality of a hypergraph.

    The Z-eigenvector terminology comes from Qi (2005) which
    defines a "tensor Z-eigenpair".

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest.
    max_iter : int, optional
        The maximum number of iterations before the algorithm terminates.
        By default, 100.
    tol : float > 0, optional
        The desired convergence tolerance. By default, 1e-6.

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
    h_eigenvector_centrality

    References
    ----------
    Scalable Tensor Methods for Nonuniform Hypergraphs,
    Sinan Aksoy, Ilya Amburg, Stephen Young,
    https://doi.org/10.1137/23M1584472

    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031

    Liqun Qi
    "Eigenvalues of a real supersymmetric tensor"
    Journal of Symbolic Computation, **40**, *6* (2005).
    https://doi.org/10.1016/j.jsc.2005.05.007.
    """
    # if there aren't any nodes, return an empty dict
    n = H.num_nodes
    if n == 0:
        return dict()

    # if the hypergraph is not connected,
    # this metric doesn't make sense and should return nan.
    if not is_connected(H):
        return {n: np.nan for n in H.nodes}
    new_H = convert_labels_to_integers(H, "old-label")
    max_size = new_H.edges.size.max()
    edge_dict = new_H.edges.members(dtype=dict)
    pairs_dict = pairwise_incidence(edge_dict, max_size)

    r = H.edges.size.max()

    def LR_evec(A):
        """Compute the largest real eigenvalue of the matrix A"""
        _, v = eigsh(A, k=1, which="LM", tol=1e-5, maxiter=200)
        evec = np.array([_v for _v in v[:, 0]])
        if evec[0] < 0:
            evec = -evec
        return evec / norm(evec, 1)

    def f(u):
        return LR_evec(ttsv2(pairs_dict, edge_dict, r, u, n)) - u

    x = np.ones(n) / n

    h = 0.5
    converged = False
    it = 0
    while it < max_iter and not converged:
        x_new = x + h * f(x)
        s = np.array([a / b for a, b in zip(x_new, x)])
        if (np.max(s) - np.min(s)) / np.min(s) < tol:
            break
        x = x_new
        it += 1
    else:
        warn("Iteration did not converge!")
    return {
        new_H.nodes[n]["old-label"]: c.item()
        for n, c in zip(new_H.nodes, x / norm(x, 1))
    }


def uniform_h_eigenvector_centrality(H, max_iter=100, tol=1e-6):
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
        x_new = apply(new_H, x, g)
        x_new = f(x_new, m)
        # multiply by the sign to try and enforce positivity
        x_new = np.sign(x_new[0]) * x_new / norm(x_new, 1)
        if norm(x - x_new) <= tol:
            break
        x = x_new.copy()
    else:
        warn("Iteration did not converge!")
    return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, x_new)}


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
