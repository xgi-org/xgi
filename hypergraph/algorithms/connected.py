import networkx as nx
import hypergraph as hg
from hypergraph.exception import HypergraphError
import scipy.sparse as sparse


def is_connected(H, s=1):
    A = sparse.find(hg.clique_motif_matrix(H) >= s)
    print(A)
    return nx.is_connected(nx.Graph(zip(A.row, A.col)))


def connected_components(H, s=1):
    A = sparse.find(hg.clique_motif_matrix(H) >= s)
    return nx.connected_components(nx.Graph(A))


def number_connected_components(H, s=1):
    return len(connected_components(H, s=s))


def node_connected_component(H, n, s=1):
    A = sparse.find(hg.clique_motif_matrix(H) >= s)
    return nx.node_connected_component(nx.Graph(A), n)