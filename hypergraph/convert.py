from pandas.core.algorithms import isin
import hypergraph as hg
from hypergraph.exception import HypergraphException, HypergraphError
from collections import defaultdict
import pandas as pd

__all__ = [
    "convert_to_hypergraph",
    "from_list_of_lists",
    "from_bipartite_pandas_dataframe",
    "to_dict_of_dicts",
    "from_dict_of_lists",
    "to_dict_of_lists",
    "from_edgelist",
    "to_edgelist",
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
        hg.empty_hypergraph(create_using)

    if isinstance(data, hg.Hypergraph):
        H = hg.empty_hypergraph(create_using)
        # copy hypergraph
        H._node = data._node.copy()
        H._edge = data._edge.copy()
        H.hypergraph = data.hypergraph.copy()

    elif isinstance(data, list):
        # edge list
        from_list_of_lists(data, create_using)

    elif isinstance(data, pd.DataFrame):
        from_bipartite_pandas_dataframe(data, create_using)

    # elif isinstance(data, dict):
    #     # edge dict in the form we need
    #     _edges = data._edges
    #     _nodes = dict()
    #     for uid, edge in _edges.items():
    #         for node in edge["members"]:
    #             try:
    #                 _nodes[node]["members"].add(uid)
    #             except:
    #                 _nodes[node] = {"members": {uid}}

    # return _nodes, _edges


def from_list_of_lists(d, create_using=None, weighted=False):
    H = hg.empty_hypergraph(create_using)
    H.add_edges_from(d)

def from_bipartite_pandas_dataframe(df, create_using=None, node_column=0, edge_column=1):
    """
    Pandas dataframe. If two columns, assume it's a bipartite edge list, otherwise it's an incidence matrix
    """
    nodes = dict()
    edges = dict()

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
            nodes[node]["members"].add(edge)
        except:
            nodes[node] = {"members" : {edge}}
        
        try:
            edges[edge]["members"].add(node)
        except:
            edges[edge] = {"members" : {node}}

    H = hg.empty_hypergraph(create_using)
    H._node = nodes
    H._edge = edges

def from_dict_of_lists(d, create_using=None):
    """
    Pandas dataframe. If two columns, assume it's a bipartite edge list, otherwise it's an incidence matrix
    """
    H = hg.empty_hypergraph(create_using)
    H.add_edges_from(d.values())

def from_numpy_array(H):
    print("Under dev")

# From incidence matrix, numpy/scipy
# From edge dictionary
# From bipartite network