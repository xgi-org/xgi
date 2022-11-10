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
            0.01007709,
            0.01018308,
            0.01031791,
            0.01048129,
            0.0106727,
            0.01089141,
            0.01113656,
            0.01140716,
            0.01170212,
            0.01202031,
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
            0.48800684,
            0.58176984,
            0.6528394,
            0.69638475,
            0.73065502,
            0.76009443,
            0.78405005,
            0.80234513,
            0.81540735,
            0.82504422,
            0.83282817,
            0.84067907,
            0.85091969,
            0.85401828,
            0.85752481,
            0.86057596,
            0.86319571,
            0.86544075,
            0.86736011,
            0.86899474,
            0.87037706,
            0.87153129,
            0.87247324,
            0.87320944,
            0.87373521,
            0.8740324,
            0.8740721,
            0.87385746,
            0.87370112,
            0.87535058,
        ]
    )

    assert norm(r - output) < 1e-07
