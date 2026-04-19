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
                -4.44089210e-19,
                4.01599731e-06,
                1.20638793e-05,
                2.41594195e-05,
                4.03182764e-05,
                6.05559922e-05,
                8.48879914e-05,
                1.13329580e-04,
                1.45895943e-04,
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
                4.71638898e00,
                4.72038896e00,
                4.72438890e00,
                4.72838876e00,
                4.73238850e00,
                4.73638810e00,
                4.74038753e00,
                4.74438675e00,
                4.74838573e00,
            ],
            [
                6.28318531e00,
                6.28518531e00,
                6.28718131e00,
                6.28917332e00,
                6.29116137e00,
                6.29314547e00,
                6.29512563e00,
                6.29710187e00,
                6.29907421e00,
                6.30104266e00,
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

    output = np.array(
        [
            0.2,
            0.2004,
            0.20079999,
            0.20119995,
            0.20159987,
            0.20199975,
            0.20239957,
            0.20279931,
            0.20319897,
            0.20359852,
        ]
    )
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
            0.47005502,
            0.56683261,
            0.63844096,
            0.69180272,
            0.73030803,
            0.76480033,
            0.79048649,
            0.80693615,
            0.81954013,
            0.82987289,
            0.83840891,
            0.84549773,
            0.85140735,
            0.85634508,
            0.86046997,
            0.8639017,
            0.86672724,
            0.86901084,
            0.87083161,
            0.87246323,
            0.87505791,
            0.88012588,
            0.88129515,
            0.88101446,
            0.88097426,
            0.8809488,
            0.88082989,
            0.88086594,
            0.88330025,
            0.888143,
        ]
    )

    assert norm(r - output) < 1e-07
