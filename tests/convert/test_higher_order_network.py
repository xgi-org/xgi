import pytest

import xgi
from xgi.exception import XGIError


def test_convert_empty_hypergraph():
    H = xgi.to_hypergraph(None)
    assert H.num_nodes == 0
    assert H.num_edges == 0


def test_convert_empty_dihypergraph():
    H = xgi.to_dihypergraph(None)
    assert H.num_nodes == 0
    assert H.num_edges == 0


def test_convert_simplicial_complex_to_hypergraph():
    SC = xgi.SimplicialComplex()
    SC.add_simplices_from([[3, 4, 5], [3, 6], [6, 7, 8, 9], [1, 4, 10, 11, 12], [1, 4]])
    H = xgi.to_hypergraph(SC)
    assert isinstance(H, xgi.Hypergraph)
    assert SC.nodes == H.nodes
    assert SC.edges.members() == H.edges.members()


def test_convert_list_to_hypergraph(edgelist2):
    H = xgi.to_hypergraph(edgelist2)
    assert isinstance(H, xgi.Hypergraph)
    assert set(H.nodes) == {1, 2, 3, 4, 5, 6}
    assert H.edges.members() == [{1, 2}, {3, 4}, {4, 5, 6}]


def test_convert_pandas_dataframe_to_hypergraph(dataframe5):
    H = xgi.to_hypergraph(dataframe5)
    assert isinstance(H, xgi.Hypergraph)
    assert set(H.nodes) == set(dataframe5["col1"])
    assert H.edges.members() == [{0, 1, 2, 3}, {4}, {5, 6}, {8, 6, 7}]


def test_convert_empty_simplicial_complex():
    S = xgi.to_simplicial_complex(None)
    assert S.num_nodes == 0
    assert S.num_edges == 0


def test_convert_hypergraph_to_simplicial_complex():
    H = xgi.Hypergraph()
    H.add_edges_from([[1, 2, 3], [3, 4], [4, 5, 6, 7], [7, 8, 9, 10, 11]])
    SC = xgi.to_simplicial_complex(H)
    assert isinstance(SC, xgi.SimplicialComplex)
    assert H.nodes == SC.nodes
    assert H.edges.members() == SC.edges.maximal().members()


def test_convert_dihypergraph_to_hypergraph(diedgelist2):
    DH = xgi.DiHypergraph(diedgelist2)
    H = xgi.to_hypergraph(DH)
    assert isinstance(H, xgi.Hypergraph)
    assert H.nodes == DH.nodes
    assert H.edges.members() == [{0, 1, 2}, {1, 2, 4}, {2, 3, 4, 5}]


def test_convert_list_to_simplicial_complex(edgelist2):
    SC = xgi.to_simplicial_complex(edgelist2)
    assert isinstance(SC, xgi.SimplicialComplex)
    assert set(SC.nodes) == {1, 2, 3, 4, 5, 6}
    assert SC.edges.maximal().members() == [{1, 2}, {3, 4}, {4, 5, 6}]


def test_convert_pandas_dataframe_to_simplicial_complex(dataframe5):
    SC = xgi.to_simplicial_complex(dataframe5)
    assert isinstance(SC, xgi.SimplicialComplex)
    assert set(SC.nodes) == set(dataframe5["col1"])
    assert SC.edges.maximal().members() == [{0, 1, 2, 3}, {4}, {5, 6}, {8, 6, 7}]


def test_cut_to_order(edgelist1, edgelist3):
    H = xgi.Hypergraph(edgelist1)
    H_cut = xgi.cut_to_order(H, 1)
    edges_cut = [frozenset({4}), frozenset({5, 6})]
    assert H_cut.edges.members() == edges_cut

    with pytest.raises(XGIError):
        xgi.cut_to_order(H, 5)

    H1 = xgi.Hypergraph(edgelist3)
    H1_cut = xgi.cut_to_order(H1, 0)
    assert H1_cut.num_edges == 0
