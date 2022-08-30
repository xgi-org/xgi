import pytest

import xgi
from xgi.exception import XGIError
import numpy as np

@pytest.mark.slow
def test_compute_kuramoto_order_parameter():
    H1 = xgi.random_hypergraph(100, [0.05, 0.001], seed=0)
    r = xgi.compute_kuramoto_order_parameter(H1, 1, 1, np.ones(100), 10, 0.002)
   
    assert len(r) == 10
