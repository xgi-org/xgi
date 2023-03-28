import pandas as pd
import pytest

import xgi
from xgi.exception import XGIError


def test_convert_empty_hypergraph():
    H = xgi.convert_to_hypergraph(None)
    assert H.num_nodes == 0
    assert H.num_edges == 0


def test_convert_empty_simplicial_complex():
    S = xgi.convert_to_simplicial_complex(None)
    assert S.num_nodes == 0
    assert S.num_edges == 0


def test_convert_to_graph(edgelist2, edgelist5):
    H1 = xgi.Hypergraph(edgelist2)
    H2 = xgi.Hypergraph(edgelist5)

    G1 = xgi.convert_to_graph(H1)
    assert set(G1.nodes) == {1, 2, 3, 4, 5, 6}
    assert set(G1.edges) == {(1, 2), (3, 4), (4, 5), (4, 6), (5, 6)}

    G2 = xgi.convert_to_graph(H2)
    assert set(G2.nodes) == {0, 1, 2, 3, 4, 5, 6, 7, 8}
    assert {frozenset(e) for e in G2.edges} == {
        frozenset({0, 1}),
        frozenset({0, 2}),
        frozenset({0, 3}),
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({2, 3}),
        frozenset({5, 6}),
        frozenset({6, 7}),
        frozenset({6, 8}),
        frozenset({7, 8}),
    }


def test_to_hyperedge_list(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert xgi.to_hyperedge_list(H) == [set(e) for e in edgelist1]


def test_to_hyperedge_dict(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    assert xgi.to_hyperedge_dict(H) == {i: set(d) for i, d in enumerate(edgelist1)}


def test_from_bipartite_pandas_dataframe(dataframe5):
    H1 = xgi.from_bipartite_pandas_dataframe(
        dataframe5, node_column="col2", edge_column="col1"
    )
    H2 = xgi.from_bipartite_pandas_dataframe(dataframe5, node_column=1, edge_column=0)

    assert H1.edges.members() == H2.edges.members()

    with pytest.raises(XGIError):
        xgi.from_bipartite_pandas_dataframe(
            dataframe5, node_column="test1", edge_column=1
        )

    with pytest.raises(XGIError):
        xgi.from_bipartite_pandas_dataframe(
            dataframe5, node_column=0, edge_column="test2"
        )


def test_to_bipartite_pandas_dataframe():
    true_bi_el1 = [
        [1, 0],
        [2, 0],
        [3, 0],
        [4, 1],
        [5, 2],
        [6, 2],
        [6, 3],
        [7, 3],
        [8, 3],
    ]

    true_bi_el2 = [[1, 0], [2, 0], [3, 0], [3, 1], [4, 1], [4, 2], [5, 2], [6, 2]]

    true_df1 = pd.DataFrame(true_bi_el1, columns=["Node ID", "Edge ID"])
    H1 = xgi.Hypergraph(true_df1)

    df1 = xgi.to_bipartite_pandas_dataframe(H1)

    assert df1.shape == true_df1.shape
    assert df1.equals(true_df1)

    true_df2 = pd.DataFrame(true_bi_el2, columns=["Node ID", "Edge ID"])
    H2 = xgi.Hypergraph(true_df2)

    df2 = xgi.to_bipartite_pandas_dataframe(H2)

    assert df2.shape == true_df2.shape
    assert df2.equals(true_df2)


def test_to_bipartite_graph(edgelist1, edgelist3, edgelist4):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist3)
    H3 = xgi.Hypergraph(edgelist4)

    true_bi_el1 = [
        [1, 0],
        [2, 0],
        [3, 0],
        [4, 1],
        [5, 2],
        [6, 2],
        [6, 3],
        [7, 3],
        [8, 3],
    ]
    true_bi_el2 = [[1, 0], [2, 0], [3, 0], [3, 1], [4, 1], [4, 2], [5, 2], [6, 2]]
    true_bi_el3 = [
        [1, 0],
        [2, 0],
        [3, 0],
        [2, 1],
        [3, 1],
        [4, 1],
        [5, 1],
        [3, 2],
        [4, 2],
        [5, 2],
    ]

    G1, node_dict, edge_dict = xgi.to_bipartite_graph(H1)
    bi_el1 = [[node_dict[u], edge_dict[v]] for u, v in G1.edges]

    assert sorted(bi_el1) == sorted(true_bi_el1)

    G2, node_dict, edge_dict = xgi.to_bipartite_graph(H2)
    bi_el2 = [[node_dict[u], edge_dict[v]] for u, v in G2.edges]

    assert sorted(bi_el2) == sorted(true_bi_el2)

    G3, node_dict, edge_dict = xgi.to_bipartite_graph(H3)
    bi_el3 = [[node_dict[u], edge_dict[v]] for u, v in G3.edges]

    assert sorted(bi_el3) == sorted(true_bi_el3)


def test_from_bipartite_graph(
    bipartite_graph1, bipartite_graph2, bipartite_graph3, bipartite_graph4
):
    H = xgi.from_bipartite_graph(bipartite_graph1)

    assert set(H.nodes) == {1, 2, 3, 4}
    assert set(H.edges) == {"a", "b", "c"}
    assert H.edges.members("a") == {1, 4}
    assert H.edges.members("b") == {1, 2}
    assert H.edges.members("c") == {2, 3}

    H = xgi.from_bipartite_graph(bipartite_graph1, dual=True)

    assert set(H.nodes) == {"a", "b", "c"}
    assert set(H.edges) == {1, 2, 3, 4}
    assert H.edges.members(1) == {"a", "b"}
    assert H.edges.members(2) == {"b", "c"}
    assert H.edges.members(3) == {"c"}
    assert H.edges.members(4) == {"a"}

    # incorrect bipartite label
    with pytest.raises(XGIError):
        H = xgi.from_bipartite_graph(bipartite_graph2, dual=True)

    # no bipartite label
    with pytest.raises(XGIError):
        H = xgi.from_bipartite_graph(bipartite_graph3, dual=True)

    # not bipartite
    with pytest.raises(XGIError):
        H = xgi.from_bipartite_graph(bipartite_graph4, dual=True)
