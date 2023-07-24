import numpy as np

import xgi


def test_to_incidence_matrix(edgelist5, incidence5):
    H = xgi.Hypergraph(edgelist5)
    assert np.all(xgi.to_incidence_matrix(H) == incidence5)


def test_from_incidence_matrix(edgelist5, incidence5):
    H = xgi.from_incidence_matrix(incidence5)
    assert H.edges.members() == edgelist5
