import numpy as np
import pytest
from numpy.linalg import norm

import xgi
from xgi.exception import XGIError


@pytest.mark.slow
def test_compute_kuramoto_order_parameter():
    H1 = xgi.random_hypergraph(100, [0.05, 0.001], seed=0)
    r = xgi.compute_kuramoto_order_parameter(
        H1, 1, 1, np.ones(100), np.linspace(0, 2 * np.pi, 100), 10, 0.002
    )

    assert len(r) == 10
    assert np.all(r >= 0)

    output = np.array(
        [
            0.01050032,
            0.01101978,
            0.01155656,
            0.01210898,
            0.01267545,
            0.01325451,
            0.01384479,
            0.01444504,
            0.01505404,
            0.01567069,
        ]
    )

    assert norm(r - output) < 1e-07


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
            0.47106854,
            0.57126832,
            0.64109353,
            0.68264783,
            0.71617815,
            0.7453313,
            0.77187175,
            0.78919788,
            0.80052008,
            0.80960317,
            0.81703077,
            0.82328629,
            0.82981654,
            0.84030481,
            0.84730904,
            0.85380854,
            0.85703066,
            0.85947532,
            0.86171806,
            0.86520105,
            0.8707219,
            0.87138854,
            0.87226304,
            0.87316166,
            0.87400814,
            0.87477437,
            0.87544216,
            0.87599709,
            0.87642391,
            0.87670566,
        ]
    )

    assert norm(r - output) < 1e-07
