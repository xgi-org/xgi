"""Simulation of the Kuramoto model."""

import numpy as np
from scipy.integrate import solve_ivp

import xgi

from ..exception import XGIError

__all__ = [
    "compute_kuramoto_order_parameter",
    "simulate_simplicial_kuramoto",
    "simulate_simplicial_sakaguchi_kuramoto",
    "compute_simplicial_order_parameter",
]


def compute_kuramoto_order_parameter(H, k2, k3, w, theta, timesteps=10000, dt=0.002):
    """This function calculates the order parameter for the Kuramoto model on hypergraphs.
    This solves the Kuramoto model ODE on hypergraphs with edges of sizes 2 and 3
    using the Euler Method. It returns an order parameter which is a measure of synchrony.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph on which you run the Kuramoto model
    k2 : float
        The coupling strength for links
    k3 : float
        The coupling strength for triangles
    w : numpy array of real values
        The natural frequency of the nodes.
    theta : numpy array of real values
        The initial phase distribution of nodes.
    timesteps : int greater than 1, default: 10000
        The number of timesteps for Euler Method.
    dt : float greater than 0, default: 0.002
        The size of timesteps for Euler Method.

    Returns
    -------
    r_time : numpy array of floats
        timeseries for Kuramoto model order parameter

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
    >>> w = 2*np.ones(n)
    >>> theta = np.linspace(0, 2*np.pi, n)
    >>> R = compute_kuramoto_order_parameter(H, k2 = 2, k3 = 3, w = w, theta = theta)

    """
    H_int = xgi.convert_labels_to_integers(H, "label")

    links = H_int.edges.filterby("size", 2).members()
    triangles = H_int.edges.filterby("size", 3).members()
    n = H_int.num_nodes

    r_time = np.zeros(timesteps)

    for t in range(timesteps):

        r1 = np.zeros(n, dtype=complex)
        r2 = np.zeros(n, dtype=complex)

        for i, j in links:

            r1[i] += np.exp(1j * theta[j])
            r1[j] += np.exp(1j * theta[i])

        for i, j, k in triangles:

            r2[i] += np.exp(2j * theta[j] - 1j * theta[k]) + np.exp(2j * theta[k] - 1j * theta[j])
            r2[j] += np.exp(2j * theta[i] - 1j * theta[k]) + np.exp(2j * theta[k] - 1j * theta[i])
            r2[k] += np.exp(2j * theta[i] - 1j * theta[j]) + np.exp(2j * theta[j] - 1j * theta[i])

        d_theta = (
            w
            + k2 * np.multiply(r1, np.exp(-1j * theta)).imag
            + k3 * np.multiply(r2, np.exp(-1j * theta)).imag
        )
        theta_new = theta + d_theta * dt
        theta = theta_new
        z = np.mean(np.exp(1j * theta))
        r_time[t] = abs(z)

    return r_time


def simulate_simplicial_kuramoto(
    S,
    orientations=None,
    order=1,
    omega=None,
    sigma=1,
    theta0=None,
    T=10,
    n_steps=10000,
    index=False,
    integrator="explicit_euler",
):
    """
    This function simulates the simplicial Kuramoto model's dynamics on an oriented simplicial
    complex using explicit Euler numerical integration scheme, or scipy.integrate.solve_ivp.

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
        The simplicial oscillators' natural frequencies, has dimension of n_simplices of given order
        if None, random will be chosen
    sigma: positive real value
        The coupling strength
    theta0: numpy.ndarray
        The initial phase distribution, has dimension n_simplices of given order
        if None, random will be chosen
    T: positive real value
        The final simulation time.
    n_steps: integer greater than 1
        The number of integration timesteps.
    index: bool, default: False
        Specifies whether to output dictionaries mapping the node and edge IDs to indices
    integrator: str, default: explicit_euler
        Speficies the type of numerical integrator to use, can be explicit_euler,
        or any available via scipy.integrate.solve_ivp (BDF is recomended)

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
            "The simplicial Kuramoto model can be simulated only on a SimplicialComplex object"
        )

    if index:
        B_o, om1_dict, o_dict = xgi.matrix.boundary_matrix(S, order, orientations, True)
    else:
        B_o = xgi.matrix.boundary_matrix(S, order, orientations, False)
    D_om1 = np.transpose(B_o)
    if index:
        B_op1, __, op1_dict = xgi.matrix.boundary_matrix(S, order + 1, orientations, True)
    else:
        B_op1 = xgi.matrix.boundary_matrix(S, order + 1, orientations, False)
    D_o = np.transpose(B_op1)

    # Compute the number of oscillating simplices
    n_o = np.shape(B_o)[1]

    if omega is None:
        omega = np.random.normal(0, 1, n_o)

    if theta0 is None:
        theta0 = np.random.normal(0, 1, n_o)

    def rhs(_, _theta):
        return omega - sigma * (D_om1 @ np.sin(B_o @ _theta) + B_op1 @ np.sin(D_o @ _theta))

    theta = np.zeros((n_o, n_steps))
    theta[:, 0] = theta0

    if integrator == "explicit_euler":
        dt = T / n_steps
        for t in range(1, n_steps):
            theta[:, t] = theta[:, t - 1] + dt * rhs(0, theta[:, t - 1])
    else:
        theta = solve_ivp(
            rhs,
            [0, T],
            theta0,
            t_eval=np.linspace(0, T, n_steps),
            method=integrator,
            rtol=1.0e-8,
            atol=1.0e-8,
        ).y

    theta_minus = B_o @ theta
    theta_plus = D_o @ theta
    if index:
        return theta, theta_minus, theta_plus, om1_dict, o_dict, op1_dict
    else:
        return theta, theta_minus, theta_plus


def simulate_simplicial_sakaguchi_kuramoto(
    S,
    orientations=None,
    order=1,
    omega=None,
    alpha=0,
    orientation_preserving=True,
    sigma=1,
    theta0=None,
    T=10,
    n_steps=10000,
    index=False,
    integrator="explicit_euler",
):
    """
    This function simulates the simplicial Kuramoto model's dynamics on an oriented simplicial
    complex using explicit Euler numerical integration scheme, or scipy.integrate.solve_ivp.

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
        The simplicial oscillators' natural frequencies, has dimension of n_simplices of given order
        if None, random will be chosen
    alpha: float/numpy.ndarray
        Frustration, has to be of double (order+1) size if orientation_preserving=True,
        else (order) size
    orientation_preserving: bool
        Set to False to not have orientation preserving frustration
    sigma: positive real value
        The coupling strength
    theta0: numpy.ndarray
        The initial phase distribution, has dimension n_simplices of given order
        if None, random will be chosen
    T: positive real value
        The final simulation time.
    n_steps: integer greater than 1
        The number of integration timesteps.
    index: bool, default: False
        Specifies whether to output dictionaries mapping the node and edge IDs to indices
    integrator: str, default: explicit_euler
        Speficies the type of numerical integrator to use, can be explicit_euler,
        or any available via scipy.integrate.solve_ivp (BDF is recomended)

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
    "Connecting Hodge and Sakaguchi-Kuramoto through a mathematical
    framework for coupled oscillators on simplicial complexes"
    by Alexis Arnaudon, Robert L. Peach, Giovanni Petri, and Paul Expert
    https://doi.org/10.1038/s42005-022-00963-7

    """
    if not isinstance(S, xgi.SimplicialComplex):
        raise XGIError(
            "The simplicial Kuramoto model can be simulated only on a SimplicialComplex object"
        )

    if index:
        B_o, om1_dict, o_dict = xgi.matrix.boundary_matrix(S, order, orientations, True)
    else:
        B_o = xgi.matrix.boundary_matrix(S, order, orientations, False)
    D_om1 = np.transpose(B_o)
    if index:
        B_op1, __, op1_dict = xgi.matrix.boundary_matrix(S, order + 1, orientations, True)
    else:
        B_op1 = xgi.matrix.boundary_matrix(S, order + 1, orientations, False)
    D_o = np.transpose(B_op1)

    # Compute the number of oscillating simplices
    n_o = np.shape(B_o)[1]
    n_o_up = np.shape(D_o)[0]

    if omega is None:
        omega = np.random.normal(0, 1, n_o)

    if theta0 is None:
        theta0 = np.random.normal(0, 1, n_o)

    def neg(matrix):
        """Return negative part of matrix."""
        _matrix = matrix.copy()
        _matrix[_matrix > 0] = 0
        return _matrix

    if orientation_preserving:
        V2 = np.concatenate((np.eye(n_o_up), -np.eye(n_o_up)), axis=0)
        LD_o = V2 @ D_o
        LB_op1 = neg(B_op1 @ V2.T)
    else:
        LD_o = D_o
        LB_op1 = B_op1

    def rhs(_, _theta):
        return omega - sigma * (
            D_om1 @ np.sin(B_o @ _theta) + LB_op1 @ np.sin(LD_o @ _theta + alpha)
        )

    theta = np.zeros((n_o, n_steps))
    theta[:, 0] = theta0
    if integrator == "explicit_euler":
        dt = T / n_steps
        for t in range(1, n_steps):
            theta[:, t] = theta[:, t - 1] + dt * rhs(0, theta[:, t - 1])
    else:
        theta = solve_ivp(
            rhs,
            [0, T],
            theta0,
            t_eval=np.linspace(0, T, n_steps),
            method=integrator,
            rtol=1.0e-8,
            atol=1.0e-8,
        ).y

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
