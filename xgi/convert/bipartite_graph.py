"""Methods for converting to and from bipartite graphs."""

import networkx as nx
from networkx import bipartite

from ..exception import XGIError
from ..generators import empty_hypergraph

__all__ = ["from_bipartite_graph", "to_bipartite_graph"]


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
    Hypergraph
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

    H = empty_hypergraph(create_using)
    H.add_nodes_from(nodes)
    for edge in edges:
        nodes_in_edge = list(G.neighbors(edge))
        H.add_edge(nodes_in_edge, id=edge)
    return H.dual() if dual else H


def to_bipartite_graph(H, index=False):
    """Create a NetworkX bipartite network from a hypergraph.

    Parameters
    ----------
    H: xgi.Hypergraph
        The XGI hypergraph object of interest
    index: bool (default False)
        If False (default), return only the graph.  If True, additionally return the
        index-to-node and index-to-edge mappings.

    Returns
    -------
    nx.Graph[, dict, dict]
        The resulting equivalent bipartite graph, and optionally the index-to-unit
        mappings.

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
    >>> G, itn, ite = xgi.to_bipartite_graph(H, index=True)

    """
    G = nx.Graph()

    n = H.num_nodes
    m = H.num_edges

    node_dict = dict(zip(H.nodes, range(n)))
    edge_dict = dict(zip(H.edges, range(n, n + m)))
    G.add_nodes_from(node_dict.values(), bipartite=0)
    G.add_nodes_from(edge_dict.values(), bipartite=1)
    for node in H.nodes:
        for edge in H.nodes.memberships(node):
            G.add_edge(node_dict[node], edge_dict[edge])

    if index:
        return (
            G,
            dict(zip(range(n), H.nodes)),
            dict(zip(range(n, n + m), H.edges)),
        )
    else:
        return G
