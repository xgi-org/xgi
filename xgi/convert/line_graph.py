from itertools import combinations

import networkx as nx

__all__ = ["to_line_graph"]


def to_line_graph(H, s=1):
    """The s-line graph of the hypergraph.

    The line graph of the hypergraph `H` is the graph whose
    nodes correspond to each hyperedge in `H`, linked together
    if they share at least one vertex.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    s : int
        The intersection size to consider edges
        as connected, by default 1.

    Returns
    -------
    LG : networkx.Graph
         The line graph associated to the Hypergraph

    References
    ----------
    "Hypernetwork science via high-order hypergraph walks", by Sinan G. Aksoy, Cliff
    Joslyn, Carlos Ortiz Marrero, Brenda Praggastis & Emilie Purvine.
    https://doi.org/10.1140/epjds/s13688-020-00231-0

    """
    LG = nx.Graph()

    edge_label_dict = {tuple(edge): index for index, edge in H._edge.items()}

    LG.add_nodes_from(H.edges)

    for edge1, edge2 in combinations(H.edges.members(), 2):
        if len(edge1.intersection(edge2)) >= s:
            LG.add_edge(edge_label_dict[tuple(edge1)], edge_label_dict[tuple(edge2)])

    return LG
