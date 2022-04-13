from copy import deepcopy

import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite
from numpy import matrix, ndarray
from scipy.sparse import coo_matrix, csc_matrix, csr_matrix, lil_matrix

import xgi
from xgi.exception import XGIError
from xgi.utils.utilities import get_dual

__all__ = [
    "convert_to_hypergraph",
    "convert_to_graph",
    "from_hyperedge_list",
    "to_hyperedge_list",
    "from_hyperedge_dict",
    "to_hyperedge_dict",
    "from_bipartite_pandas_dataframe",
    "from_incidence_matrix",
    "to_incidence_matrix",
    "from_bipartite_graph",
    "to_bipartite_graph",
]


def convert_to_hypergraph(data, create_using=None):
    """Make a hypergraph from a known data structure.
    The preferred way to call this is automatically
    from the class constructor.

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
    create_using : Hypergraph graph constructor, optional (default=xgi.Hypergraph)
        Hypergraph type to create. If hypergraph instance, then cleared before populated.

    Returns
    -------
    Hypergraph object
        A hypergraph constructed from the data
    """

    if data is None:
        xgi.empty_hypergraph(create_using)

    elif isinstance(data, xgi.Hypergraph):
        H = xgi.empty_hypergraph(create_using)
        # copy hypergraph
        H._node = deepcopy(data._node)
        H._node_attr = deepcopy(data._node_attr)
        H._edge = deepcopy(data._edge)
        H._edge_attr = deepcopy(data._edge_attr)
        H._hypergraph = deepcopy(data._hypergraph)

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


def convert_to_graph(H):
    """Graph projection (1-skeleton) of the hypergraph H.
    Weights are not considered.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    G : networkx.Graph
        The graph projection
    """

    A = xgi.adjacency_matrix(H)  # This is unweighted by design
    G = nx.from_scipy_sparse_matrix(A)
    G = nx.relabel_nodes(G, {i: node for i, node in enumerate(H.nodes)})
    return G


def from_hyperedge_list(d, create_using=None):
    """Generate a hypergraph from a list of lists.

    Parameters
    ----------
    d : list of lists
        A hyperedge list
    create_using : Hypergraph constructor, optional
        The hypergraph to add the edges to, by default None

    Returns
    -------
    Hypergraph object
        The constructed hypergraph object

    See Also
    --------
    to_hyperedge_list
    """
    H = xgi.empty_hypergraph(create_using)
    H.add_edges_from(d)
    return H


def to_hyperedge_list(H):
    """Generate a hyperedge list from a hypergraph.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    list of lists
        The hyperedge list

    See Also
    --------
    from_hyperedge_list
    """
    return list(H.edges.values())


def from_hyperedge_dict(d, create_using=None):
    """Creates a hypergraph from a dictionary of hyperedges

    Parameters
    ----------
    d : dict
        A dictionary where the keys are edge IDs and the values
        are containers of nodes specifying the edges.
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None

    Returns
    -------
    Hypergraph object
        The constructed hypergraph object

    See Also
    --------
    to_hyperedge_dict
    """
    H = xgi.empty_hypergraph(create_using)
    H._edge = d
    H._edge_attr = {id: dict() for id in H.edges}
    H._node = get_dual(d)
    H._node = {id: dict() for id in H.nodes}
    return H


def to_hyperedge_dict(H):
    """Outputs a hyperedge dictionary

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    dict
        A dictionary where the keys are edge IDs and the values
        are lists of nodes specifying the edges.

    See Also
    --------
    from_hyperedge_dict
    """
    return deepcopy(H._edge)


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
    H = xgi.empty_hypergraph(create_using)
    # try to get by labels first
    try:
        d = df[[node_column, edge_column]]
    except Exception:
        # try to index the labels
        try:
            columns = list(df.columns)
            d = df[[columns[node_column], columns[edge_column]]]
        except KeyError:
            raise XGIError("Invalid columns specified")

    for line in d.itertuples(index=False):
        node = line[0]
        edge = line[1]
        H.add_node_to_edge(edge, node)

    return H


def from_incidence_matrix(d, create_using=None, nodelabels=None, edgelabels=None):
    """Create a hypergraph from an incidence matrix

    Parameters
    ----------
    d : numpy array or a scipy sparse arrary
        The incidence matrix where rows specify nodes and columns specify edges.
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None
    nodelabels : list or 1D numpy array, optional
        The ordered list of node IDs to map the indices
        of the incidence matrix to, by default None
    edgelabels : list or 1D numpy array, optional
        The ordered list of edge IDs to map the indices
        of the incidence matrix to, by default None

    Returns
    -------
    Hypergraph object
        The constructed hypergraph

    Raises
    ------
    XGIError
        Raises an error if the specified labels are the wrong dimensions

    See Also
    --------
    incidence_matrix
    to_incidence_matrix
    """
    I = coo_matrix(d)
    n, m = I.shape

    if nodelabels is None:
        nodedict = dict(zip(range(n), range(n)))
    elif nodelabels is not None and len(nodelabels) != n:
        raise XGIError("Node dictionary is the wrong size.")
    else:
        nodedict = dict(zip(range(n), nodelabels))

    if edgelabels is None:
        edgedict = dict(zip(range(m), range(m)))
    elif edgelabels is not None and len(edgelabels) != m:
        raise XGIError("Edge dictionary is the wrong size.")
    else:
        edgedict = dict(zip(range(m), edgelabels))

    H = xgi.empty_hypergraph(create_using)

    for node, edge in zip(I.row, I.col):
        node = nodedict[node]
        edge = edgedict[edge]
        H.add_node_to_edge(edge, node)

    return H


def to_incidence_matrix(H, sparse=True, index=False):
    """Convert a hypergraph to an incidence matrix.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest
    sparse : bool, optional
        Whether the constructed incidence matrix
        should be sparse, by default True
    index : bool, optional
        Whether to return the corresponding
        node and edge labels, by default False

    Returns
    -------
    numpy.ndarray or scipy csr_matrix
        The incidence matrix
    dict
        The dictionary mapping indices to node IDs, if index is True
    dict
        The dictionary mapping indices to edge IDs, if index is True

    See Also
    --------
    incidence_matrix
    from_incidence_matrix
    """
    return xgi.incidence_matrix(H, sparse=sparse, index=index)


def from_bipartite_graph(G, create_using=None, dual=False):
    """
    Create a Hypergraph from a NetworkX bipartite graph.

    Any hypergraph may be represented as a bipartite graph where
    nodes in the first layer are nodes and nodes in the second layer
    are hyperedges.

    The default behavior is to create nodes in the hypergraph
    from the nodes in the bipartite graph where the attribute
    bipartite=0 and hyperedges in the hypergraph from the nodes
    in the bipartite graph with attribute bipartite=1. Setting the
    keyword `dual` reverses this behavior.


    Parameters
    ----------
    G : nx.Graph
        A networkx bipartite graph. Each node in the graph has a property
        'bipartite' taking the value of 0 or 1 indicating the type of node.

    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None

    dual : bool, default : False
        If True, get edges from bipartite=0 and nodes from bipartite=1

    Returns
    -------
    xgi.Hypergraph
        The equivalent hypergraph

    References
    ----------
    The Why, How, and When of Representations for Complex Systems,
    Leo Torres, Ann S. Blevins, Danielle Bassett, and Tina Eliassi-Rad,
    https://doi.org/10.1137/20M1355896

    Examples
    --------
    >>> import networkx as nx
    >>> import xgi
    >>> G = nx.Graph()
    >>> G.add_nodes_from([1, 2, 3, 4], bipartite=0)
    >>> G.add_nodes_from(['a', 'b', 'c'], bipartite=1)
    >>> G.add_edges_from([(1, 'a'), (1, 'b'), (2, 'b'), (2, 'c'), (3, 'c'), (4, 'a')])
    >>> H = xgi.from_bipartite_graph(G)

    """
    edges = []
    nodes = []
    for n, d in G.nodes(data=True):
        try:
            node_type = d["bipartite"]
        except KeyError as e:
            raise XGIError("bipartite property not set") from e

        if node_type == 0:
            nodes.append(n)
        elif node_type == 1:
            edges.append(n)
        else:
            raise XGIError("Invalid type specifier")

    if not bipartite.is_bipartite_node_set(G, nodes):
        raise XGIError("The network is not bipartite")

    H = xgi.empty_hypergraph(create_using)
    H.add_nodes_from(nodes)
    for edge in edges:
        nodes_in_edge = list(G.neighbors(edge))
        H.add_edge(nodes_in_edge, id=edge)
    return H.dual() if dual else H


def to_bipartite_graph(H):
    """
    Create a NetworkX bipartite network from a hypergraph.

    Parameters
    ----------
    H: xgi.Hypergraph
        The XGI hypergraph object of interest

    Returns
    -------
    nx.Graph
        The resulting equivalent bipartite graph

    References
    ----------
    The Why, How, and When of Representations for Complex Systems,
    Leo Torres, Ann S. Blevins, Danielle Bassett, and Tina Eliassi-Rad,
    https://doi.org/10.1137/20M1355896

    Examples
    --------
    >>> import xgi
    >>> hyperedge_list = [[1, 2], [2, 3, 4]]
    >>> H = xgi.Hypergraph(hyperedge_list)
    >>> G = xgi.to_bipartite_graph(H)
    """
    G = nx.Graph()

    node_dict = dict(zip(H.nodes, range(H.num_nodes)))
    edge_dict = dict(zip(H.edges, range(H.num_nodes, H.num_nodes + H.num_edges)))
    G.add_nodes_from(node_dict.values(), bipartite=0)
    G.add_nodes_from(edge_dict.values(), bipartite=1)
    for node in H.nodes:
        for edge in H.nodes.memberships(node):
            G.add_edge(node_dict[node], edge_dict[edge])

    return (
        G,
        dict(zip(range(H.num_nodes), H.nodes)),
        dict(zip(range(H.num_nodes, H.num_nodes + H.num_edges), H.edges)),
    )
