import numpy as np
from numpy.linalg import norm

import xgi


def test_simulate_kuramoto():
    N = 5
    n_steps = 10
    dt = 0.002
    theta0 = np.linspace(0, 2 * np.pi, N)
    H1 = xgi.random_hypergraph(N, [0.05, 0.001], seed=0)
    theta_time, times = xgi.simulate_kuramoto(H1, 1, 1, np.ones(N), theta0, n_steps, dt)

    assert theta_time.shape == (n_steps, N)
    assert np.all(times == np.arange(n_steps) * dt)

    output = np.array(
        [
            [
                0.00000000e00,
                2.00000000e-03,
                4.00000000e-03,
                6.00000000e-03,
                8.00000000e-03,
                1.00000000e-02,
                1.20000000e-02,
                1.40000000e-02,
                1.60000000e-02,
                1.80000000e-02,
            ],
            [
                1.57079633e00,
                1.57279633e00,
                1.57479633e00,
                1.57679633e00,
                1.57879633e00,
                1.58079633e00,
                1.58279633e00,
                1.58479633e00,
                1.58679633e00,
                1.58879633e00,
            ],
            [
                3.14159265e00,
                3.14359265e00,
                3.14559265e00,
                3.14759265e00,
                3.14959265e00,
                3.15159265e00,
                3.15359265e00,
                3.15559265e00,
                3.15759265e00,
                3.15959265e00,
            ],
            [
                4.71238898e00,
                4.71438898e00,
                4.71638898e00,
                4.71838898e00,
                4.72038898e00,
                4.72238898e00,
                4.72438898e00,
                4.72638898e00,
                4.72838898e00,
                4.73038898e00,
            ],
            [
                6.28318531e00,
                6.28518531e00,
                6.28718531e00,
                6.28918531e00,
                6.29118531e00,
                6.29318531e00,
                6.29518531e00,
                6.29718531e00,
                6.29918531e00,
                6.30118531e00,
            ],
        ]
    )

    assert norm(theta_time - output.T) < 1e-07


def test_compute_kuramoto_order_parameter():
    N = 5
    n_steps = 10
    dt = 0.002
    theta0 = np.linspace(0, 2 * np.pi, N)
    H1 = xgi.random_hypergraph(N, [0.05, 0.001], seed=0)
    theta_time, times = xgi.simulate_kuramoto(H1, 1, 1, np.ones(N), theta0, n_steps, dt)

    r_time = xgi.compute_kuramoto_order_parameter(theta_time)

    output = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2])
    assert norm(r_time - output) < 1e-07


def test_simulate_simplicial_kuramoto():
    S = xgi.random_simplicial_complex(40, [0.08, 0.03], seed=0)
    n0 = len(S.nodes)
    n1 = len(S.edges.filterby("order", 1))
    n2 = len(S.edges.filterby("order", 2))

    theta, theta_minus, theta_plus = xgi.simulate_simplicial_kuramoto(
        S, None, 1, np.ones((n1, 1)), 1, np.ones((n1, 1)), 1, 30, False
    )
    r = xgi.compute_simplicial_order_parameter(theta_minus, theta_plus)

    assert np.shape(theta) == (n1, 30)
    assert np.shape(theta_minus) == (n0, 30)
    assert np.shape(theta_plus) == (n2, 30)
    assert len(r) == 30

    output = np.array(
        [
            0.49621306,
            0.60580058,
            0.67907764,
            0.72321992,
            0.75639763,
            0.78366991,
            0.80717782,
            0.82273716,
            0.83467922,
            0.84446529,
            0.85249769,
            0.85912003,
            0.86461448,
            0.86920235,
            0.87305585,
            0.87630931,
            0.87906825,
            0.88141629,
            0.88342032,
            0.88513433,
            0.88660225,
            0.88786016,
            0.88893787,
            0.88986022,
            0.89064801,
            0.89131879,
            0.89188742,
            0.89236657,
            0.89276710,
            0.89309833,
        ]
    )

    assert norm(r - output) < 1e-07
