import numpy as np
import pytest
from numpy.linalg import norm

import xgi
from xgi.exception import XGIError


def test_clique_eigenvector_centrality():
    # test empty hypergraph
    H = xgi.Hypergraph()
    assert xgi.clique_eigenvector_centrality(H) == dict()

    # Test no edges
    H.add_nodes_from([0, 1, 2])
    cec = xgi.clique_eigenvector_centrality(H)
    assert set(cec) == {0, 1, 2}
    for i in cec:
        assert np.isnan(cec[i])

    # test disconnected
    H.add_edge([0, 1])
    cec = xgi.clique_eigenvector_centrality(H)
    assert set(cec) == {0, 1, 2}
    for i in cec:
        assert np.isnan(cec[i])

    H = xgi.sunflower(3, 1, 3)
    c = H.nodes.clique_eigenvector_centrality.asnumpy()
    assert norm(c[1:] - c[1]) < 1e-4
    assert abs(c[0] / c[1] - ratio(3, 3, kind="CEC")) < 1e-4

    H = xgi.sunflower(5, 1, 7)
    c = H.nodes.clique_eigenvector_centrality.asnumpy()
    assert norm(c[1:] - c[1]) < 1e-4
    assert abs(c[0] / c[1] - ratio(5, 7, kind="CEC")) < 1e-4


@pytest.mark.slow
def test_h_eigenvector_centrality():
    # test empty hypergraph
    H = xgi.Hypergraph()
    c = xgi.h_eigenvector_centrality(H)
    assert c == dict()

    # Test no edges
    H.add_nodes_from([0, 1, 2])
    hec = xgi.h_eigenvector_centrality(H)
    for i in hec:
        assert np.isnan(hec[i])

    # test disconnected
    H.add_edge([0, 1])
    hec = xgi.h_eigenvector_centrality(H)
    assert set(hec) == {0, 1, 2}
    for i in hec:
        assert np.isnan(hec[i])

    H = xgi.sunflower(3, 1, 5)
    c = H.nodes.h_eigenvector_centrality(max_iter=1000).asnumpy()
    assert norm(c[1:] - c[1]) < 1e-4
    assert abs(c[0] / c[1] - ratio(3, 5, kind="HEC")) < 1e-4

    H = xgi.sunflower(5, 1, 7)
    c = H.nodes.h_eigenvector_centrality(max_iter=1000).asnumpy()
    assert norm(c[1:] - c[1]) < 1e-4
    assert abs(c[0] / c[1] - ratio(5, 7, kind="HEC")) < 1e-4

    with pytest.raises(XGIError):
        H = xgi.Hypergraph([[1, 2], [2, 3, 4]])
        H.nodes.h_eigenvector_centrality.asnumpy()


def test_node_edge_centrality():
    # test empty hypergraph
    H = xgi.Hypergraph()
    assert xgi.node_edge_centrality(H) == (dict(), dict())

    # Test no edges
    H.add_nodes_from([0, 1, 2])
    nc, ec = xgi.node_edge_centrality(H)
    assert set(nc) == {0, 1, 2}
    for i in nc:
        assert np.isnan(nc[i])
    assert ec == dict()

    # test disconnected
    H.add_edge([0, 1])
    nc, ec = xgi.node_edge_centrality(H)
    assert set(nc) == {0, 1, 2}
    for i in nc:
        assert np.isnan(nc[i])
    assert set(ec) == {0}
    for i in ec:
        assert np.isnan(ec[i])

    H = xgi.Hypergraph([[0, 1, 2, 3, 4]])
    c = H.nodes.node_edge_centrality.asnumpy()
    assert norm(c - c[0]) < 1e-6

    c = H.edges.node_edge_centrality.asnumpy()
    assert c == 1

    H = xgi.Hypergraph([[0, 1], [1, 2]])
    c = H.edges.node_edge_centrality.asnumpy()
    assert abs(c[0] - c[1]) < 1e-6


def test_line_vector_centrality():
    H = xgi.Hypergraph()
    c = xgi.line_vector_centrality(H)
    assert c == dict()

    with pytest.raises(XGIError):
        H = xgi.Hypergraph()
        H.add_nodes_from([0, 1, 2])
        H.add_edge([0, 1])
        xgi.line_vector_centrality(H)

    H = xgi.sunflower(3, 1, 3) << xgi.sunflower(3, 1, 5)
    c = xgi.line_vector_centrality(H)
    assert len(c[0]) == 4  # sizes 2 through 5
    assert np.allclose(c[0], [0, 0.40824829, 0, 0.24494897])
    assert set(c.keys()) == set(H.nodes)

    with pytest.raises(Exception):
        H = xgi.Hypergraph([["a", "b"], ["b", "c"], ["a", "c"]])
        xgi.line_vector_centrality(H)


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
        "CEC" or "HEC"

    Returns
    -------
    float
        Ratio

    References
    ----------
    Three Hypergraph Eigenvector Centralities,
    Austin R. Benson,
    https://doi.org/10.1137/18M1203031
    """
    if kind == "CEC":
        return 2 * r * (m - 1) / (np.sqrt(m**2 + 4 * (m - 1) * (r - 1)) + m - 2)
    elif kind == "HEC":
        return r ** (1.0 / m)


def test_katz_centrality(edgelist1, edgelist8):
    # test hypergraph with no edge
    H = xgi.Hypergraph()
    H.add_nodes_from([1, 2, 3])
    c = xgi.katz_centrality(H)
    expected_c = {1: 0, 2: 0, 3: 0}
    assert c == expected_c

    # test numerical values
    H = xgi.Hypergraph(edgelist1)
    c = xgi.katz_centrality(H)
    expected_c = {
        1: 0.1427771519858862,
        2: 0.1427771519858862,
        3: 0.1427771519858862,
        4: 0.0,
        5: 0.07166636106392883,
        6: 0.21389013015822952,
        8: 0.14305602641009146,
        7: 0.14305602641009146,
    }
    assert c == expected_c

    # test with difference cutoff
    H = xgi.Hypergraph(edgelist8)
    c = xgi.katz_centrality(H, cutoff=5)
    expected_c = {
        0: 0.21358389796604274,
        1: 0.1779789506060754,
        2: 0.17880254869172216,
        3: 0.17880254869172216,
        4: 0.14321435302156882,
        5: 0.07147345362079142,
        6: 0.03614424740207708,
    }
    for n in c:
        assert np.allclose(c[n], expected_c[n])
