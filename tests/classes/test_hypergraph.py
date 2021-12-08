import pytest
import xgi

from xgi.classes.hypergraph import Hypergraph
from xgi.exception import XGIError


def test_constructor(edgelist5, dict5, incidence5, dataframe5):
    el = edgelist5
    d = dict5
    i = incidence5
    df = dataframe5

    H_list = xgi.Hypergraph(el)
    H_dict = xgi.Hypergraph(d)
    H_mat = xgi.Hypergraph(i)
    H_df = xgi.Hypergraph(df)

    assert H_list.shape == H_dict.shape == H_mat.shape == H_df.shape
    assert (
        list(H_list.nodes)
        == list(H_dict.nodes)
        == list(H_mat.nodes)
        == list(H_df.nodes)
    )
    assert (
        list(H_list.edges)
        == list(H_dict.edges)
        == list(H_mat.edges)
        == list(H_df.edges)
    )
    assert (
        list(H_list.edges[0])
        == list(H_dict.edges[0])
        == list(H_mat.edges[0])
        == list(H_df.edges[0])
    )


def test_name():
    H = xgi.Hypergraph()
    assert H.name == ""
    H.name = "test"
    assert H.name == "test"
    H = xgi.Hypergraph(name="test")
    assert H.name == "test"


def test_contains(edgelist1):
    el1 = edgelist1
    H = xgi.Hypergraph(el1)
    unique_nodes = list({node for edge in el1 for node in edge})
    for node in unique_nodes:
        assert node in H

    assert 0 not in H


def test_len(edgelist1, edgelist2):
    el1 = edgelist1
    el2 = edgelist2
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    assert len(H1) == 8
    assert len(H2) == 6


def test_shape(edgelist1, edgelist2):
    el1 = edgelist1
    el2 = edgelist2
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    assert H1.shape == (8, 4)
    assert H2.shape == (6, 3)


def test_neighbors(edgelist1, edgelist2):
    el1 = edgelist1
    el2 = edgelist2
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    assert H1.neighbors(1) == {2, 3}
    assert H1.neighbors(4) == set()
    assert H1.neighbors(6) == {5, 7, 8}
    assert H2.neighbors(4) == {3, 5, 6}
    assert H2.neighbors(1) == {2}


def test_dual(edgelist1, edgelist2, edgelist4):
    el1 = edgelist1
    el2 = edgelist2
    el4 = edgelist4
    H1 = xgi.Hypergraph(el1)
    H2 = xgi.Hypergraph(el2)
    H3 = xgi.Hypergraph(el4)

    D1 = H1.dual()
    D2 = H2.dual()
    D3 = H3.dual()
    assert D1.shape == (4, 8)
    assert D2.shape == (3, 6)
    assert D3.shape == (3, 5)
