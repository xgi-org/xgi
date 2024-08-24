import networkx as nx
import numpy as np
import pandas as pd
import pytest

import xgi
from xgi.exception import IDNotFound, XGIError
from xgi.utils import IDDict


def test_iddict(edgelist1):
    H = xgi.Hypergraph()
    with pytest.raises(IDNotFound):
        H.nodes[0]
    with pytest.raises(IDNotFound):
        H.edges[0]

    H = xgi.Hypergraph(edgelist1)
    with pytest.raises(IDNotFound):
        H.nodes[0]
    with pytest.raises(IDNotFound):
        H.edges[4]

    assert H.edges[0] == dict()

    with pytest.raises(XGIError):
        H._edge[None] = {1, 2, 3}

    with pytest.raises(IDNotFound):
        del H._node["test"]

    with pytest.raises(TypeError):
        H._node[[0, 1, 2]] = [0, 1]

    a = IDDict({1: 2})
    b = IDDict({3: 4})
    c = {5: 6}
    assert a + b == IDDict({1: 2, 3: 4})
    assert b + a == IDDict({1: 2, 3: 4})
    assert a + c == IDDict({1: 2, 5: 6})
    with pytest.raises(TypeError):
        c + a


def test_neighbors():
    H = xgi.Hypergraph()
    with pytest.raises(IDNotFound):
        H.nodes.neighbors(0)
    with pytest.raises(IDNotFound):
        H.remove_node(0)
    with pytest.raises(IDNotFound):
        H.remove_edge(0)


def test_dual_dict(dict5):
    dual = xgi.dual_dict(dict5)
    assert dual[0] == {0}
    assert dual[1] == {0}
    assert dual[2] == {0}
    assert dual[3] == {0}
    assert dual[4] == {1}
    assert dual[5] == {2}
    assert dual[6] == {2, 3}
    assert dual[7] == {3}
    assert dual[8] == {3}


def test_powerset():
    edge = [1, 2, 3, 4]

    PS = xgi.powerset(edge)
    PS1 = xgi.powerset(edge, include_empty=True)
    PS2 = xgi.powerset(edge, include_empty=True, include_full=True)

    out = [
        (1,),
        (2,),
        (3,),
        (4,),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
        (1, 2, 3),
        (1, 2, 4),
        (1, 3, 4),
        (2, 3, 4),
    ]

    assert list(PS) == out
    assert list(PS1) == [()] + out
    assert list(PS2) == [()] + out + [tuple(edge)]


def test_find_triangles():
    G = nx.erdos_renyi_graph(20, 0.2, seed=0)
    triangles = xgi.find_triangles(G)

    cliques = [
        {8, 9, 17},
        {8, 9, 19},
        {9, 16, 19},
        {8, 13, 17},
        {6, 17, 18},
        {2, 6, 12},
        {7, 8, 13},
        {2, 6, 18},
    ]

    num_tri = sum(nx.triangles(G).values()) / 3

    assert triangles == cliques
    assert num_tri == len(cliques)


def test_min_where():
    vals = {"a": 1.0, "b": 0.0, "c": np.inf, "d": 2.0}

    where = {"a": True, "b": False, "c": True, "d": True}
    assert (
        xgi.utils.utilities.min_where(vals, where) == 1
    )  # replace with xgi.min_where (it seems not to work...)

    where = {"a": False, "b": False, "c": False, "d": False}
    assert xgi.utils.utilities.min_where(vals, where) == np.inf


def test_subfaces(edgelist5):
    assert xgi.subfaces(edgelist5) == [
        (0,),
        (1,),
        (2,),
        (3,),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
        (5,),
        (6,),
        (8,),
        (6,),
        (7,),
        (8, 6),
        (8, 7),
        (6, 7),
    ]

    assert xgi.subfaces(edgelist5, order=-1) == [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
        (5,),
        (6,),
        (8, 6),
        (8, 7),
        (6, 7),
    ]

    assert xgi.subfaces(edgelist5, order=0) == [
        (0,),
        (1,),
        (2,),
        (3,),
        (5,),
        (6,),
        (8,),
        (6,),
        (7,),
    ]

    assert xgi.subfaces(edgelist5, order=1) == [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
        (5, 6),
        (8, 6),
        (8, 7),
        (6, 7),
    ]

    assert xgi.subfaces(edgelist5, order=2) == [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
        (8, 6, 7),
    ]

    assert xgi.subfaces(edgelist5, order=3) == [(0, 1, 2, 3)]

    with pytest.raises(XGIError):
        xgi.subfaces(
            edgelist5, order=4
        )  # order cannot be larger than maximum order in edgelist


def test_convert_labels_to_integers(
    hypergraph1, hypergraph2, simplicialcomplex1, dihypergraph1
):

    # test hypergraph stuff
    H1 = xgi.convert_labels_to_integers(hypergraph1)
    H2 = xgi.convert_labels_to_integers(hypergraph2)
    H3 = xgi.convert_labels_to_integers(hypergraph1, "old_ids")

    assert isinstance(H1, xgi.Hypergraph)

    assert set(H1.nodes) == {0, 1, 2}
    assert set(H1.edges) == {0, 1, 2}

    assert H1.nodes[0]["label"] == "a"
    assert H1.nodes[1]["label"] == "b"
    assert H1.nodes[2]["label"] == "c"

    assert H1.edges[0]["label"] == "e1"
    assert H1.edges[1]["label"] == "e2"
    assert H1.edges[2]["label"] == "e3"

    assert H1.edges.members(0) == {0, 1}
    assert H1.edges.members(1) == {0, 1, 2}
    assert H1.edges.members(2) == {2}

    assert H1.nodes.memberships(0) == {0, 1}
    assert H1.nodes.memberships(1) == {0, 1}
    assert H1.nodes.memberships(2) == {1, 2}

    assert set(H2.nodes) == {0, 1, 2}
    assert set(H2.edges) == {0, 1, 2}

    assert H2.nodes[0]["label"] == "b"
    assert H2.nodes[1]["label"] == "c"
    assert H2.nodes[2]["label"] == 0

    assert H2.edges[0]["label"] == "e1"
    assert H2.edges[1]["label"] == "e2"
    assert H2.edges[2]["label"] == "e3"

    assert H2.edges.members(0) == {0, 2}
    assert H2.edges.members(1) == {1, 2}
    assert H2.edges.members(2) == {0, 1, 2}

    assert H2.nodes.memberships(0) == {0, 2}
    assert H2.nodes.memberships(1) == {1, 2}
    assert H2.nodes.memberships(2) == {0, 1, 2}

    assert H3.nodes[0]["old_ids"] == "a"
    assert H3.edges[0]["old_ids"] == "e1"

    # test simplicial complex stuff
    S1 = xgi.convert_labels_to_integers(simplicialcomplex1)

    assert isinstance(S1, xgi.SimplicialComplex)
    assert set(S1.nodes) == {0, 1, 2}
    assert set(S1.edges) == {0, 1, 2, 3}

    assert S1.edges.members(0) == {0, 2}
    assert S1.edges.members(1) == {1, 2}
    assert S1.edges.members(2) == {0, 1, 2}
    assert S1.edges.members(3) == {0, 1}

    assert S1.nodes[0]["label"] == "b"
    assert S1.edges[0]["label"] == "e1"

    # test dihypergraph stuff
    DH1 = xgi.convert_labels_to_integers(dihypergraph1)
    assert set(DH1.nodes) == {0, 1, 2, 3}
    assert set(DH1.edges) == {0, 1, 2}

    assert isinstance(DH1, xgi.DiHypergraph)
    assert DH1.edges.dimembers(0) == ({0, 1}, {2})
    assert DH1.edges.dimembers(1) == ({1}, {2, 3})
    assert DH1.edges.dimembers(2) == ({1}, {2})

    assert DH1.nodes[0]["label"] == "a"
    assert DH1.edges[0]["label"] == "e1"


def test_hist():
    vals = [1, 10, 100, 1000]
    df = xgi.hist(vals)
    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) == 2
    assert len(df.index) == 10

    df = xgi.hist(vals, bins=3)
    true_x = np.array([167.5, 500.5, 833.5])
    assert np.allclose(df["bin_center"], true_x)
    true_y = np.array([3, 0, 1])
    assert np.allclose(df["value"], true_y)

    df = xgi.hist(vals, bins=3, density=True)
    assert np.allclose(df["bin_center"], true_x)
    true_y = np.array([0.00225225, 0.0, 0.00075075])
    assert np.allclose(df["value"], true_y)

    df = xgi.hist(vals, bins=3, log_binning=True)
    true_x = np.array([5.5, 55.0, 550.0])
    assert np.allclose(df["bin_center"], true_x)
    true_y = np.array([1, 1, 2])
    assert np.allclose(df["value"], true_y)

    df = xgi.hist(vals, bins=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 1000], bin_edges=True)
    true_x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 55.0, 550.0])
    assert np.allclose(df["bin_center"], true_x)
    true_y = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2])
    assert np.allclose(df["value"], true_y)
    assert np.allclose(df["bin_lo"], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100])
    assert np.allclose(df["bin_hi"], [2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 1000])

    with pytest.raises(XGIError):
        xgi.hist(vals, bins=(0, 1, 2))

    with pytest.raises(XGIError):
        xgi.hist(vals, bins="ten")


def test_binomial_sequence():

    # ask for more ones than available characters
    output = xgi.binomial_sequence(3, 2)
    expected_output = set()
    assert output == expected_output

    # ask for an empty string
    output = xgi.binomial_sequence(0, 0)
    expected_output = {""}
    assert output == expected_output

    # ask for only zeros
    output = xgi.binomial_sequence(0, 2)
    expected_output = {"00"}
    assert output == expected_output

    # regular output
    output = xgi.binomial_sequence(2, 4)
    expected_output = {"1100", "1001", "0011", "1010", "0101", "0110"}
    assert output == expected_output
