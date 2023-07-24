"""Simulation of the Kuramoto model."""

import numpy as np

import xgi

from ..exception import XGIError
from ..linalg.hodge_matrix import boundary_matrix

__all__ = [
    "simulate_kuramoto",
    "compute_kuramoto_order_parameter",
    "simulate_simplicial_kuramoto",
    "compute_simplicial_order_parameter",
]


def simulate_kuramoto(H, k2, k3, omega=None, theta=None, timesteps=10000, dt=0.002):
    """Simulates the Kuramoto model on hypergraphs.
    This solves the Kuramoto model ODE on hypergraphs with edges of sizes 2 and 3
    using the Euler Method. It returns timeseries of the phases.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph on which you run the Kuramoto model
    k2 : float
        The coupling strength for links
    k3 : float
        The coupling strength for triangles
    omega : numpy array of real values
        The natural frequency of the nodes. If None (default), randomly drawn from a
        normal distribution
    theta : numpy array of real values
        The initial phase distribution of nodes. If None (default), drawn from a random
        uniform distribution on [0, 2pi[.
    timesteps : int greater than 1, default: 10000
        The number of timesteps for Euler Method.
    dt : float greater than 0, default: 0.002
        The size of timesteps for Euler Method.

    Returns
    -------
    theta_time: numpy array of floats
        Timeseries of phases from the Kuramoto model, of dimension (T, N)
    times: numpy array of floats
        Times corresponding to the simulate phases

    References
    ----------
    "Synchronization of phase oscillators on complex hypergraphs"
    by Sabina Adhikari, Juan G. Restrepo and Per Sebastian Skardal
    https://doi.org/10.48550/arXiv.2208.00909

    Examples
    --------
    >>> import numpy as np
    >>> import xgi
    >>> n = 50
    >>> H = xgi.random_hypergraph(n, [0.05, 0.001], seed=None)
    >>> omega = 2*np.ones(n)
    >>> theta = np.linspace(0, 2*np.pi, n)
    >>> theta_time, times = simulate_kuramoto(H, k2=2, k3=3, omega=omega, theta=theta)

    """
    from ..utils import convert_labels_to_integers

    H_int = convert_labels_to_integers(H, "label")

    links = H_int.edges.filterby("size", 2).members()
    triangles = H_int.edges.filterby("size", 3).members()
    n = H_int.num_nodes

    theta_time = np.zeros((timesteps, n))
    times = np.arange(timesteps) * dt

    if omega is None:
        omega = np.random.normal(0, 1, n)

    if theta is None:
        theta = np.random.random(n) * 2 * np.pi

    for t in range(timesteps):
        theta_time[t] = theta

        r1 = np.zeros(n, dtype=complex)
        r2 = np.zeros(n, dtype=complex)

        for i, j in links:
            r1[i] += np.exp(1j * theta[j])
            r1[j] += np.exp(1j * theta[i])

        for i, j, k in triangles:
            r2[i] += np.exp(2j * theta[j] - 1j * theta[k]) + np.exp(
                2j * theta[k] - 1j * theta[j]
            )
            r2[j] += np.exp(2j * theta[i] - 1j * theta[k]) + np.exp(
                2j * theta[k] - 1j * theta[i]
            )
            r2[k] += np.exp(2j * theta[i] - 1j * theta[j]) + np.exp(
                2j * theta[j] - 1j * theta[i]
            )

        d_theta = (
            omega
            + k2 * np.multiply(r1, np.exp(-1j * theta)).imag
            + k3 * np.multiply(r2, np.exp(-1j * theta)).imag
        )
        theta_new = theta + d_theta * dt
        theta = theta_new

    return theta_time, times


def compute_kuramoto_order_parameter(theta_time):
    """Calculate the order parameter for the Kuramoto model on hypergraphs.

    Calculation proceeds from time series, and the output is a measure of synchrony.

    Parameters
    ----------
    theta_time: numpy array of floats
        Timeseries of phases from the Kuramoto model, of dimension (T, N)

    Returns
    -------
    r_time : numpy array of floats
        Timeseries for Kuramoto model order parameter

    """

    z = np.mean(np.exp(1j * theta_time), axis=1)
    r_time = np.abs(z)

    return r_time


def simulate_simplicial_kuramoto(
    S,
    orientations=None,
    order=1,
    omega=[],
    sigma=1,
    theta0=[],
    T=10,
    n_steps=10000,
    index=False,
):
    """Simulate the simplicial Kuramoto model's dynamics on an oriented simplicial
    complex using explicit Euler numerical integration scheme.

    Parameters
    ----------
    S: simplicial complex object
        The simplicial complex on which you
        run the simplicial Kuramoto model
    orientations: dict, Default : None
        Dictionary mapping non-singleton simplices IDs to their boolean orientation
    order: integer
        The order of the oscillating simplices
    omega: numpy.ndarray
        The simplicial oscillators' natural frequencies, has dimension
        (n_simplices of given order, 1)
    sigma: positive real value
        The coupling strength
    theta0: numpy.ndarray
        The initial phase distribution, has dimension
        (n_simplices of given order, 1)
    T: positive real value
        The final simulation time.
    n_steps: integer greater than 1
        The number of integration timesteps for the explicit Euler method.
    index: bool, default: False
        Specifies whether to output dictionaries mapping the node and edge IDs to
        indices.

    Returns
    -------
    theta: numpy.ndarray
        Timeseries of the simplicial oscillators' phases, has dimension
        (n_simplices of given order, n_steps)
    theta_minus: numpy array of floats
        Timeseries of the projection of the phases onto lower order simplices,
        has dimension (n_simplices of given order - 1, n_steps)
    theta_plus: numpy array of floats
        Timeseries of the projection of the phases onto higher order simplices,
        has dimension (n_simplices of given order + 1, n_steps)
    om1_dict: dict
        The dictionary mapping indices to (order-1)-simplices IDs, if index is True
    o_dict: dict
        The dictionary mapping indices to (order)-simplices IDs, if index is True
    op1_dict: dict
        The dictionary mapping indices to (order+1)-simplices IDs, if index is True

    References
    ----------
    "Explosive Higher-Order Kuramoto Dynamics on Simplicial Complexes"
    by Ana P. Millán, Joaquín J. Torres, and Ginestra Bianconi
    https://doi.org/10.1103/PhysRevLett.124.218301

    """

    # Notation:
    # B_o - boundary matrix acting on (order)-simplices
    # D_o - adjoint boundary matrix acting on (order)-simplices
    # om1 = order - 1
    # op1 = order + 1

    if not isinstance(S, xgi.SimplicialComplex):
        raise XGIError(
            "The simplicial Kuramoto model can be simulated "
            "only on a SimplicialComplex object"
        )

    if index:
        B_o, om1_dict, o_dict = boundary_matrix(S, order, orientations, True)
    else:
        B_o = boundary_matrix(S, order, orientations, False)
    D_om1 = np.transpose(B_o)

    if index:
        B_op1, __, op1_dict = boundary_matrix(S, order + 1, orientations, True)
    else:
        B_op1 = boundary_matrix(S, order + 1, orientations, False)
    D_o = np.transpose(B_op1)

    # Compute the number of oscillating simplices
    n_o = np.shape(B_o)[1]

    dt = T / n_steps
    theta = np.zeros((n_o, n_steps))
    theta[:, [0]] = theta0
    for t in range(1, n_steps):
        theta[:, [t]] = theta[:, [t - 1]] + dt * (
            omega
            - sigma * D_om1 @ np.sin(B_o @ theta[:, [t - 1]])
            - sigma * B_op1 @ np.sin(D_o @ theta[:, [t - 1]])
        )
    theta_minus = B_o @ theta
    theta_plus = D_o @ theta
    if index:
        return theta, theta_minus, theta_plus, om1_dict, o_dict, op1_dict
    else:
        return theta, theta_minus, theta_plus


def compute_simplicial_order_parameter(theta_minus, theta_plus):
    """
    This function computes the simplicial order parameter of a
    simplicial Kuramoto dynamics simulation.

    Parameters
    ----------
    theta_minus: numpy.ndarray
        Timeseries of the projection of the phases onto
        lower order simplices, has dimension
        (n_simplices of given order - 1, n_steps)

    theta_plus: numpy.ndarray
        Timeseries of the projection of the phases onto
        higher order simplices, has dimension
        (n_simplices of given order + 1, n_steps)

    Returns
    -------
    R : numpy.ndarray
        Timeseries of the simplicial order parameter,
        has dimension (1, n_steps)

    References
    ----------
    "Connecting Hodge and Sakaguchi-Kuramoto through a mathematical
    framework for coupled oscillators on simplicial complexes"
    by Alexis Arnaudon, Robert L. Peach, Giovanni Petri, and Paul Expert
    https://doi.org/10.1038/s42005-022-00963-7

    """

    C = np.size(theta_minus, 0) + np.size(theta_plus, 0)
    R = (np.sum(np.cos(theta_minus), 0) + np.sum(np.cos(theta_plus), 0)) / C
    return R
