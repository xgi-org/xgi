import numpy as np
import pytest

import xgi
from xgi.algorithms.assortativity import choose_degrees
from xgi.exception import XGIError


def test_dynamical_assortativity(edgelist1, edgelist6):

    H = xgi.Hypergraph()
    with pytest.raises(XGIError):
        xgi.dynamical_assortativity(H)

    H.add_nodes_from([0, 1, 2])

    with pytest.raises(XGIError):
        xgi.dynamical_assortativity(H)

    with pytest.raises(XGIError):
        H1 = xgi.Hypergraph(edgelist1)
        xgi.dynamical_assortativity(H1)

    H1 = xgi.Hypergraph(edgelist6)

    assert abs(xgi.dynamical_assortativity(H1) - -0.0526) < 1e-3


def test_degree_assortativity(edgelist1, edgelist6):
    H1 = xgi.Hypergraph(edgelist1)
    assert -1 <= xgi.degree_assortativity(H1, kind="uniform") <= 1
    assert -1 <= xgi.degree_assortativity(H1, kind="top-2") <= 1
    assert -1 <= xgi.degree_assortativity(H1, kind="top-bottom") <= 1

    H2 = xgi.Hypergraph(edgelist6)
    assert -1 <= xgi.degree_assortativity(H2, kind="uniform") <= 1
    assert -1 <= xgi.degree_assortativity(H2, kind="top-2") <= 1
    assert -1 <= xgi.degree_assortativity(H2, kind="top-bottom") <= 1


def test_choose_degrees(edgelist1, edgelist6):
    H1 = xgi.Hypergraph(edgelist1)
    k = H1.degree()

    with pytest.raises(XGIError):
        e = H1.edges.members(1)
        choose_degrees(e, k)

    e = H1.edges.members(0)
    assert np.all(np.array(choose_degrees(e, k)) == 1)


    e = H1.edges.members(3)
    assert set(choose_degrees(e, k, kind="top-2")) == {1, 2}
    assert set(choose_degrees(e, k, kind="top-bottom")) == {1, 2}

    H2 = xgi.Hypergraph(edgelist6)
    e = H2.edges.members(2)
    k = H2.degree()
    assert set(choose_degrees(e, k, kind="top-2")) == {2, 3}
    assert set(choose_degrees(e, k, kind="top-bottom")) == {1, 3}
