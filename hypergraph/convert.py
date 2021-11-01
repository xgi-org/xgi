import hypergraph as hg
from hypergraph.exception import HypergraphException, HypergraphError
from collections import defaultdict
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix, csc_matrix, lil_matrix
from numpy import ndarray, matrix
from copy import deepcopy
from hypergraph.utils.utilities import get_dual

__all__ = [
    "convert_to_hypergraph",
    "from_hyperedge_list",
    "to_hyperedge_list",
    "from_hyperedge_dict",
    "to_hyperedge_dict",
    "from_bipartite_pandas_dataframe",
    "from_incidence_matrix",
    "to_incidence_matrix",
]


def convert_to_hypergraph(data, create_using=None):
    """Make a hypergraph from a known data structure.
    The preferred way to call this is automatically
    from the class constructor

    Parameters
    ----------
    data : object to be converted
        Current known types are:
         * a Hypergraph object
         * list-of-lists
         * dict-of-lists
         * Pandas DataFrame (bipartite edgelist)
         * numpy matrix
         * numpy ndarray
         * scipy sparse matrix
    create_using : Hypergraph graph constructor, optional (default=hg.Hypergraph)
        Hypergraph type to create. If hypergraph instance, then cleared before populated.
    """

    if data is None:
        print("1")
        hg.empty_hypergraph(create_using)

    elif isinstance(data, hg.Hypergraph):
        print("2")
        H = hg.empty_hypergraph(create_using)
        # copy hypergraph
        H._node = deepcopy(data._node)
        H._node_attr = deepcopy(data._node_attr)
        H._edge = deepcopy(data._edge)
        H._edge_attr = deepcopy(data._edge_attr)
        H.hypergraph = deepcopy(data.hypergraph)

    elif isinstance(data, list):
        # edge list
        from_hyperedge_list(data, create_using)

    elif isinstance(data, pd.DataFrame):
        from_bipartite_pandas_dataframe(data, create_using)

    elif isinstance(data, dict):
        # edge dict in the form we need
        from_hyperedge_dict(data, create_using)

    elif isinstance(
        data, (ndarray, matrix, csr_matrix, csc_matrix, coo_matrix, lil_matrix)
    ):
        from_incidence_matrix(data, create_using)


def from_hyperedge_list(d, create_using=None):
    H = hg.empty_hypergraph(create_using)
    H.add_edges_from(d)
    return H


def to_hyperedge_list(H):
    return list(H.edges.values())


def from_hyperedge_dict(d, create_using=None, weighted=False):
    H = hg.empty_hypergraph(create_using)
    H._edge = d
    H._edge_attr = {id: dict() for id in H.edges}
    H._node = get_dual(d)
    H._node = {id: dict() for id in H.nodes}
    return H


def to_hyperedge_dict(H):
    return deepcopy(H._edge)


def from_bipartite_pandas_dataframe(
    df, create_using=None, node_column=0, edge_column=1
):
    """
    Pandas dataframe assuming it's a bipartite edge list.
    """
    H = hg.empty_hypergraph(create_using)
    # try to get by labels first
    try:
        d = df[[node_column, edge_column]]
    except Exception:
        # try to index the labels
        try:
            columns = list(df.columns)
            d = df[[columns[node_column], columns[edge_column]]]
        except:
            raise HypergraphError("Invalid columns specified")

    for line in d.itertuples(index=False):
        node = line[0]
        edge = line[1]
        H.add_node_to_edge(edge, node)

    return H


def from_incidence_matrix(d, create_using=None, nodelabels=None, edgelabels=None):
    I = coo_matrix(d)
    n, m = I.shape

    if nodelabels is None:
        nodedict = dict(zip(range(n), range(n)))
    elif nodelabels is not None and len(nodelabels) != n:
        raise HypergraphError("Node dictionary is the wrong size.")
    else:
        nodedict = dict(zip(range(n), nodelabels))

    if edgelabels is None:
        edgedict = dict(zip(range(m), range(m)))
    elif edgelabels is not None and len(edgelabels) != m:
        raise HypergraphError("Edge dictionary is the wrong size.")
    else:
        edgedict = dict(zip(range(m), edgelabels))

    H = hg.empty_hypergraph(create_using)

    for node, edge in zip(I.row, I.col):
        node = nodedict[node]
        edge = edgedict[edge]
        H.add_node_to_edge(edge, node)
    
    return H


def to_incidence_matrix(H, sparse=True, index=False):
    return hg.incidence_matrix(H, sparse=sparse, index=index)
