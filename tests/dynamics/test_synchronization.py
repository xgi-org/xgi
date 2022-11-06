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
            0.48298713,
            0.58247076,
            0.65693086,
            0.70298299,
            0.73837991,
            0.76462604,
            0.78566456,
            0.80211222,
            0.81432231,
            0.82400277,
            0.83181786,
            0.83817456,
            0.84340249,
            0.84795055,
            0.85299006,
            0.86023346,
            0.86451316,
            0.86632849,
            0.86817522,
            0.86988353,
            0.87141939,
            0.87278711,
            0.87400027,
            0.8750739,
            0.87602224,
            0.876858,
            0.87759225,
            0.87823449,
            0.8787927,
            0.87927347,
        ]
    )

    assert norm(r - output) < 1e-07
