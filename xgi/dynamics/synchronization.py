"""Simulation of the Kuramoto model."""

import numpy as np

import xgi

__all__ = ["compute_kuramoto_order_parameter","simulate_simplicial_kuramoto","compute_simplicial_order_parameter"]


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
            w
            + k2 * np.multiply(r1, np.exp(-1j * theta)).imag
            + k3 * np.multiply(r2, np.exp(-1j * theta)).imag
        )
        theta_new = theta + d_theta * dt
        theta = theta_new
        z = np.mean(np.exp(1j * theta))
        r_time[t] = abs(z)

    return r_time


def simulate_simplicial_kuramoto(S, orientations = None, order=1,omega = [],sigma=1,theta0=[],T=10,n_steps=10000,index=False):
    """
    This function simulates the simplicial Kuramoto model's dynamics on an oriented simplicial complex 
    using explicit Euler numerical integration scheme.

    Parameters
    ----------
    S : oriented simplicial complex
        The simplicial complex on which you 
        run the simplicial Kuramoto model
    orientations :  binary list
        Specifies the orientations of the 
        simplices in the complex
    order : integer
        The order of the oscillating simplices
    omega : numpy array of real values
        The simplicial oscillators' natural frequencies
    sigma : positive real value
        The coupling strength
    theta0 : numpy array of real values
        The initial phase distribution.
    T : positive real value
        The final simulation time.
    n_steps : integer greater than 1
        The number of integration timesteps for
        the explicit Euler method.

    Returns
    -------
    theta : numpy array of floats
        Timeseries of the simplicial oscillators' phases
    theta_minus : numpy array of floats
        Timeseries of the projection of the phases onto 
        lower order simplices
    theta_plus : numpy array of floats
        Timeseries of the projection of the phases onto 
        higher order simplices

    """
    if index:
        Bk, km1_dict, k_dict = xgi.matrix.boundary_matrix(S, order, orientations,True)
    else:
        Bk = xgi.matrix.boundary_matrix(S, order, orientations,False)
    Dkm1 = np.transpose(Bk)
    if index:
        Bkp1, __, kp1_dict = xgi.matrix.boundary_matrix(S, order+1, orientations,True)
    else:
        Bkp1 = xgi.matrix.boundary_matrix(S, order+1, orientations,False)
    Dk = np.transpose(Bkp1)

    # Compute the number of oscillating simplices
    nk = np.shape(Bk)[1]

    dt = T/n_steps
    theta = np.zeros((nk,n_steps))
    theta[:,[0]] = theta0
    for t in range(1,n_steps):
        theta[:,[t]] = theta[:,[t-1]] + dt*(omega - sigma*Dkm1@np.sin(Bk@theta[:,[t-1]]) - sigma*Bkp1@np.sin(Dk@theta[:,[t-1]]))
    theta_minus = Bk@theta
    theta_plus = Dk@theta
    if index:
        return theta, theta_minus, theta_plus, km1_dict, k_dict, kp1_dict
    else:
        return theta, theta_minus, theta_plus

def compute_simplicial_order_parameter(theta_minus,theta_plus):
    """
    This function computes the simplicial order parameter of a
    simplicial Kuramoto dynamics simulation.

    Parameters
    ----------
    theta_minus: numpy array of floats
        Timeseries of the projection of the phases onto 
        lower order simplices
    theta_plus:
        Timeseries of the projection of the phases onto 
        higher order simplices

    Returns
    -------
    R : numpy array of floats
        Timeseries of the simplicial order parameter

    """

    C = np.size(theta_minus,0)+np.size(theta_plus,0)
    R = (np.sum(np.cos(theta_minus),0)+np.sum(np.cos(theta_plus),0))/C
    return R