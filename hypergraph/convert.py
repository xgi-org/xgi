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
]


def convert_to_hypergraph(data, create_using=None):
    """Make a hypergraph from a known data structure.
    The preferred way to call this is automatically
    from the class constructor

    Parameters
    ----------
    data : object to be converted
        Current known types are:
         any Hypergraph object
         list-of-lists
         dict-of-lists
         container (e.g. set, list, tuple) of edges
         iterator (e.g. itertools.chain) that produces edges
         generator of edges
         Pandas DataFrame (row per edge)
         numpy matrix
         numpy ndarray
         scipy sparse matrix
         pygraphviz agraph
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
    multigraph_input : bool (default False)
        If True and  data is a dict_of_dicts,
        try to create a multigraph assuming dict_of_dict_of_lists.
        If data and create_using are both multigraphs then create
        a multigraph from a multigraph.
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


def from_hyperedge_list(d, create_using=None, weighted=False):
    H = hg.empty_hypergraph(create_using)
    H.add_edges_from(d)
    return H


def to_hyperedge_list(H):
    return [list(H.edges[edge_id]) for edge_id in H.edges]


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
    nodes = hg.Hypergraph.node_dict_factory()
    node_attrs = hg.Hypergraph.node_attr_dict_factory()
    edges = hg.Hypergraph.hyperedge_dict_factory()
    edge_attrs = hg.Hypergraph.hyperedge_attr_dict_factory()

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

        try:
            nodes[node].add(edge)
        except:
            nodes[node] = {edge}
            node_attrs[node] = {}

        try:
            edges[edge].add(node)
        except:
            edges[edge] = {node}
            edge_attrs[edge] = {}

    H = hg.empty_hypergraph(create_using)
    H._node = nodes
    H._node = node_attrs
    H._edge = edges
    H._edge_attr = edge_attrs
    return H


def from_incidence_matrix(d, create_using=None):
    I = coo_matrix(d)
    nodes = hg.Hypergraph.node_dict_factory()
    node_attrs = hg.Hypergraph.node_attr_dict_factory()
    edges = hg.Hypergraph.hyperedge_dict_factory()
    edge_attrs = hg.Hypergraph.hyperedge_attr_dict_factory()

    for node, edge in zip(I.row, I.col):
        try:
            nodes[node].add(edge)
        except:
            nodes[node] = {edge}
            node_attrs[node] = {}

        try:
            edges[edge].add(node)
        except:
            edges[edge] = {node}
            edge_attrs[edge] = {}
    H = hg.empty_hypergraph(create_using)
    H._node = nodes
    H._node = node_attrs
    H._edge = edges
    H._edge_attr = edge_attrs
    return H
