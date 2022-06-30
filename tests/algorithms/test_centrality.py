import numpy as np
import pytest
from numpy.linalg import norm

import xgi
from xgi.exception import XGIError


def test_cec_centrality():
    H = xgi.sunflower(3, 1, 3)
    c = H.nodes.cec_centrality.asnumpy()
    assert norm(c[1:] - c[1]) < 1e-4
    assert abs(c[0] / c[1] - ratio(3, 3, kind="CEC")) < 1e-4

    H = xgi.sunflower(5, 1, 7)
    c = H.nodes.cec_centrality.asnumpy()
    assert norm(c[1:] - c[1]) < 1e-4
    assert abs(c[0] / c[1] - ratio(5, 7, kind="CEC")) < 1e-4


@pytest.mark.slow
def test_hec_centrality():
    H = xgi.sunflower(3, 1, 5)
    c = H.nodes.hec_centrality(max_iter=1000).asnumpy()
    assert norm(c[1:] - c[1]) < 1e-4
    assert abs(c[0] / c[1] - ratio(3, 5, kind="HEC")) < 1e-4

    H = xgi.sunflower(5, 1, 7)
    c = H.nodes.hec_centrality(max_iter=1000).asnumpy()
    assert norm(c[1:] - c[1]) < 1e-4
    assert abs(c[0] / c[1] - ratio(5, 7, kind="HEC")) < 1e-4

    with pytest.raises(XGIError):
        H = xgi.Hypergraph([[1, 2], [2, 3, 4]])
        H.nodes.hec_centrality.asnumpy()


def test_node_edge_centrality():
    H = xgi.Hypergraph([[0, 1, 2, 3, 4]])
    c = H.nodes.node_edge_centrality.asnumpy()
    assert norm(c - c[0]) < 1e-6

    c = H.edges.node_edge_centrality.asnumpy()
    assert c == 1

    H = xgi.Hypergraph([[0, 1], [1, 2]])
    c = H.edges.node_edge_centrality.asnumpy()
    assert abs(c[0] - c[1]) < 1e-6


def ratio(r, m, kind="CEC"):
    """Generate the ratio between largest and second largest centralities
    for the sunflower hypergraph with one core node.

    Parameters
    ----------
    r : int
        Number of petals
    m : int
        Size of edges
    kind : str, default: "CEC"
        "CEC", "HEC", or "ZEC"

    Returns
    -------
    float
        Ratio

    Raises
    ------
    XGIError
        If edge size is too small for ZEC

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    if kind == "CEC":
        return 2 * r * (m - 1) / (np.sqrt(m**2 + 4 * (m - 1) * (r - 1)) + m - 2)
    elif kind == "ZEC":
        if m > 4:
            raise XGIError("Choose a larger m value.")
        return r**0.5
    elif kind == "HEC":
        return r ** (1.0 / m)
