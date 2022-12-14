import numpy as np
import pytest
from numpy.linalg import norm

import xgi


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
        S, None, 1, np.ones(n1), 1, np.ones(n1), 1, 30, False
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


def test_simulate_simplicial_sakaguchi_kuramoto():
    S = xgi.random_simplicial_complex(40, [0.08, 0.03], seed=0)
    n0 = len(S.nodes)
    n1 = len(S.edges.filterby("order", 1))
    n2 = len(S.edges.filterby("order", 2))

    theta, theta_minus, theta_plus = xgi.simulate_simplicial_sakaguchi_kuramoto(
        S, None, 1, np.ones(n1), 1.0, True, 1, np.ones(n1), 1, 30, False
    )
    r = xgi.compute_simplicial_order_parameter(theta_minus, theta_plus)

    assert np.shape(theta) == (n1, 30)
    assert np.shape(theta_minus) == (n0, 30)
    assert np.shape(theta_plus) == (n2, 30)
    assert len(r) == 30

    output = np.array(
        [
            0.49621306,
            0.52948851,
            0.52363131,
            0.51321491,
            0.51583117,
            0.51208825,
            0.49988031,
            0.49549666,
            0.51100881,
            0.51125107,
            0.50711096,
            0.49553279,
            0.48854057,
            0.47552711,
            0.47991634,
            0.47462188,
            0.47454695,
            0.46251969,
            0.46332552,
            0.47221073,
            0.4716475,
            0.45471295,
            0.44471146,
            0.44260013,
            0.43455512,
            0.43517392,
            0.44323849,
            0.44135109,
            0.43016681,
            0.42665677,
        ]
    )
    assert norm(r - output) < 1e-07

    # without orientation preserving
    theta, theta_minus, theta_plus = xgi.simulate_simplicial_sakaguchi_kuramoto(
        S, None, 1, np.ones(n1), 1.0, False, 1, np.ones(n1), 1, 30, False
    )
    r = xgi.compute_simplicial_order_parameter(theta_minus, theta_plus)

    assert np.shape(theta) == (n1, 30)
    assert np.shape(theta_minus) == (n0, 30)
    assert np.shape(theta_plus) == (n2, 30)
    assert len(r) == 30

    output = np.array(
        [
            0.49621306,
            0.6126584,
            0.70094599,
            0.76249214,
            0.81016895,
            0.84569572,
            0.87019944,
            0.88023566,
            0.88174598,
            0.87795785,
            0.87079713,
            0.86174925,
            0.8518659,
            0.84183632,
            0.83208089,
            0.82283363,
            0.81420588,
            0.80623202,
            0.79890078,
            0.792176,
            0.78601005,
            0.78035222,
            0.77515394,
            0.77037188,
            0.76596964,
            0.76191855,
            0.75819768,
            0.75479313,
            0.75169662,
            0.74890335,
        ]
    )
    assert norm(r - output) < 1e-07
