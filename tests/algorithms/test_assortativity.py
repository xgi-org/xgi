import numpy as np
import pytest

import xgi
from xgi.algorithms.assortativity import _choose_degrees
from xgi.exception import XGIError


def test_dynamical_assortativity(edgelist1, edgelist6, edgelist9, edgelist10):
    H = xgi.Hypergraph()
    with pytest.raises(XGIError):
        xgi.dynamical_assortativity(H)

    H.add_nodes_from([0, 1, 2])

    with pytest.raises(XGIError):
        xgi.dynamical_assortativity(H)

    # must be uniform
    with pytest.raises(XGIError):
        H = xgi.Hypergraph(edgelist1)
        xgi.dynamical_assortativity(H)

    # no singleton edges
    with pytest.raises(XGIError):
        H = xgi.Hypergraph(edgelist10)
        xgi.dynamical_assortativity(H)

    H = xgi.Hypergraph(edgelist6)
    assert abs(xgi.dynamical_assortativity(H) - -0.0526) < 1e-3

    H = xgi.Hypergraph(edgelist9)
    assert abs(xgi.dynamical_assortativity(H) - -0.0526) < 1e-3


def test_degree_assortativity(edgelist1, edgelist5):
    H1 = xgi.Hypergraph(edgelist1)
    assert -1 <= xgi.degree_assortativity(H1, kind="uniform") <= 1
    assert -1 <= xgi.degree_assortativity(H1, kind="top-2") <= 1
    assert -1 <= xgi.degree_assortativity(H1, kind="top-bottom") <= 1

    H2 = xgi.Hypergraph(edgelist5)
    assert -1 <= xgi.degree_assortativity(H2, kind="uniform") <= 1
    assert -1 <= xgi.degree_assortativity(H2, kind="top-2") <= 1
    assert -1 <= xgi.degree_assortativity(H2, kind="top-bottom") <= 1

    # test "exact" keyword
    assert -1 <= xgi.degree_assortativity(H1, kind="uniform", exact=True) <= 1
    assert -1 <= xgi.degree_assortativity(H1, kind="top-2", exact=True) <= 1
    assert -1 <= xgi.degree_assortativity(H1, kind="top-bottom", exact=True) <= 1

    # check that exact returns the same
    rho1 = xgi.degree_assortativity(H1, kind="uniform", exact=True)
    rho2 = xgi.degree_assortativity(H1, kind="uniform", exact=True)
    assert rho1 == rho2

    rho1 = xgi.degree_assortativity(H1, kind="top-2", exact=True)
    rho2 = xgi.degree_assortativity(H1, kind="top-2", exact=True)
    assert rho1 == rho2

    rho1 = xgi.degree_assortativity(H1, kind="top-bottom", exact=True)
    rho2 = xgi.degree_assortativity(H1, kind="top-bottom", exact=True)
    assert rho1 == rho2

    # test empty
    H = xgi.Hypergraph()
    with pytest.raises(XGIError):
        xgi.degree_assortativity(H)

    H.add_nodes_from([0, 1, 2])
    with pytest.raises(XGIError):
        xgi.degree_assortativity(H)

    # test wrong kind
    with pytest.raises(XGIError):
        xgi.degree_assortativity(H1, kind="no-idea")
    with pytest.raises(XGIError):
        xgi.degree_assortativity(H1, kind="no-idea", exact=True)


def test_choose_degrees(edgelist1, edgelist6):
    H1 = xgi.Hypergraph(edgelist1)
    k = H1.degree()

    # test singleton edges
    with pytest.raises(XGIError):
        e = H1.edges.members(1)
        _choose_degrees(e, k)

    # invalid choice function
    with pytest.raises(XGIError):
        e = H1.edges.members(0)
        _choose_degrees(e, k, "test")

    e = H1.edges.members(0)
    assert np.all(np.array(_choose_degrees(e, k)) == 1)

    e = H1.edges.members(3)
    assert set(_choose_degrees(e, k, kind="top-2")) == {1, 2}
    assert set(_choose_degrees(e, k, kind="top-bottom")) == {1, 2}

    H2 = xgi.Hypergraph(edgelist6)
    e = H2.edges.members(2)
    k = H2.degree()
    assert set(_choose_degrees(e, k, kind="top-2")) == {2, 3}
    assert set(_choose_degrees(e, k, kind="top-bottom")) == {1, 3}
