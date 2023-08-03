"""Methods for converting to and from a Pandas dataframe."""

from collections import defaultdict

import pandas as pd

from ..core import SimplicialComplex
from ..exception import XGIError
from ..generators import empty_hypergraph

__all__ = ["from_bipartite_pandas_dataframe", "to_bipartite_pandas_dataframe"]


def from_bipartite_pandas_dataframe(
    df, create_using=None, node_column=0, edge_column=1
):
    """Create a hypergraph from a pandas dataframe given
    specified node and edge columns.

    Parameters
    ----------
    df : Pandas dataframe
        A dataframe where specified columns list the node IDs
        and the associated edge IDs
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None
    node_column : hashable, optional
        The column with the node IDs, by default 0
        Can specify names or indices
    edge_column : hashable, optional
        The column with the edge IDs, by default 1
        Can specify names or indices

    Returns
    -------
    Hypergraph object
        The constructed hypergraph

    Raises
    ------
    XGIError
        Raises an error if the user specifies invalid column names
    """
    H = empty_hypergraph(create_using)

    # try to get by labels first
    try:
        d = df[[node_column, edge_column]]
    except KeyError:
        # try to index the labels
        try:
            columns = list(df.columns)
            d = df[[columns[node_column], columns[edge_column]]]
        except (KeyError, TypeError):
            raise XGIError("Invalid columns specified")

    if isinstance(H, SimplicialComplex):
        simplex_list = defaultdict(list)
        for line in d.itertuples(index=False):
            if line[0] not in simplex_list[line[1]]:
                simplex_list[line[1]].append(line[0])

        H.add_simplices_from(list(simplex_list.values()))
    else:
        for line in d.itertuples(index=False):
            node = line[0]
            edge = line[1]
            H.add_node_to_edge(edge, node)

    return H


def to_bipartite_pandas_dataframe(H):
    """Create a two column dataframe from a hypergraph.

    Parameters
    ----------
    H : Hypergraph or Simplicial Complex
        A dataframe where specified columns list the node IDs
        and the associated edge IDs

    Returns
    -------
    Pandas Dataframe object
        A two column dataframe

    Raises
    ------
    XGIError
        Raises an error if the user specifies invalid column names
    """
    data = []
    for id1, members in H._node.items():
        for id2 in members:
            data.append([id1, id2])
    return pd.DataFrame(data, columns=["Node ID", "Edge ID"])
