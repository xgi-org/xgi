import pandas as pd
import pytest

import xgi
from xgi.exception import XGIError


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
