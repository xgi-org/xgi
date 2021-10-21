import networkx as nx
import hypergraph as hg
from hypergraph.exception import HypergraphError
import scipy.sparse as sparse


def is_connected(H, s=1):
    data = sparse.find(hg.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.is_connected(nx.Graph(zip(rows, cols)))


def connected_components(H, s=1):
    data = sparse.find(hg.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.connected_components(nx.Graph(zip(rows, cols)))


def number_connected_components(H, s=1):
    return len(connected_components(H, s=s))


def node_connected_component(H, n, s=1):
    data = sparse.find(hg.clique_motif_matrix(H) >= s)
    rows = data[0]
    cols = data[1]
    return nx.node_connected_component(nx.Graph(zip(rows, cols)), n)
