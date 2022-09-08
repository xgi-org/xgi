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
