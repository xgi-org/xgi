"""Methods for converting to and from bipartite graphs."""

import networkx as nx

from ..core import DiHypergraph, Hypergraph
from ..exception import XGIError

__all__ = ["from_bipartite_graph", "to_bipartite_graph"]


def from_bipartite_graph(G, dual=False):
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

    dual : bool, default : False
        If True, get edges from bipartite=0 and nodes from bipartite=1

    Returns
    -------
    Hypergraph or DiHypergraph
        The equivalent hypergraph or directed hypergraph

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
    if isinstance(G, nx.DiGraph):
        directed = True
    else:
        directed = False

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

    if not _is_bipartite(G, nodes, edges):
        raise XGIError("The network is not bipartite")

    if directed:
        H = DiHypergraph()
    else:
        H = Hypergraph()

    H.add_nodes_from(nodes)

    for u, v in G.edges:
        if directed:
            if v in edges:
                H.add_node_to_edge(v, u, direction="in")
            else:
                H.add_node_to_edge(u, v, direction="out")
        else:
            H.add_node_to_edge(v, u)

    return H.dual() if dual else H


def _is_bipartite(G, nodes1, nodes2):
    """Assumption is that nodes1.union(nodes2) == G.nodes"""
    for i, j in G.edges:
        cond1 = i in nodes1
        cond2 = j in nodes2
        if not cond1 == cond2:  # if not both true or both false
            return False
    return True


def to_bipartite_graph(H, index=False):
    """Create a NetworkX bipartite network from a hypergraph.

    Parameters
    ----------
    H: xgi.Hypergraph or xgi.DiHypergraph
        The XGI hypergraph object of interest
    index: bool (default False)
        If False (default), return only the graph.  If True, additionally return the
        index-to-node and index-to-edge mappings.

    Returns
    -------
    if xgi.Hypergraph
        nx.Graph[, dict, dict]
            The resulting equivalent bipartite graph, and optionally the index-to-unit
            mappings.
    if xgi.Hypergraph
        nx.DiGraph[, dict, dict]
            The resulting equivalent directed bipartite graph, and optionally the index-to-unit
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
    if isinstance(H, DiHypergraph):
        directed = True
    else:
        directed = False

    n = H.num_nodes
    m = H.num_edges

    node_dict = dict(zip(H.nodes, range(n)))
    edge_dict = dict(zip(H.edges, range(n, n + m)))

    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    G.add_nodes_from(node_dict.values(), bipartite=0)
    G.add_nodes_from(edge_dict.values(), bipartite=1)

    if directed:
        for e in H.edges:
            for v in H.edges.tail(e):
                G.add_edge(node_dict[v], edge_dict[e])
            for v in H.edges.head(e):
                G.add_edge(edge_dict[e], node_dict[v])
    else:
        for e in H.edges:
            for v in H.edges.members(e):
                G.add_edge(node_dict[v], edge_dict[e])

    if index:
        return (
            G,
            {v: k for k, v in node_dict.items()},
            {v: k for k, v in edge_dict.items()},
        )
    else:
        return G
