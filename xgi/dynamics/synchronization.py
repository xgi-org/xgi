"""Simulation of the Kuramoto model."""

import numpy as np

import xgi

__all__ = ["compute_kuramoto_order_parameter"]


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
