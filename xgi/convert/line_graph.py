"""Method for converting to a line graph."""

from collections import defaultdict
from itertools import combinations

import networkx as nx

from ..exception import XGIError

__all__ = ["to_line_graph"]


def to_line_graph(H, s=1, weights=None):
    """The s-line graph of the hypergraph.

    The s-line graph of the hypergraph `H` is the graph whose
    nodes correspond to each hyperedge in `H`, linked together
    if they share at least s vertices.

    Optional edge weights correspond to the size of the
    intersection between the hyperedges, optionally
    normalized by the size of the smaller hyperedge.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    s : int
        The intersection size to consider edges
        as connected, by default 1.
    weights : str or None
        Specify whether to return a weighted line graph. If None,
        returns an unweighted line graph. If 'absolute', includes
        edge weights corresponding to the size of intersection
        between hyperedges. If 'normalized', includes edge weights
        normalized by the size of the smaller hyperedge.

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
    if weights not in [None, "absolute", "normalized"]:
        raise XGIError(
            f"{weights} not a valid weights option. Choices are "
            "None, 'absolute', and 'normalized'."
        )
    LG = nx.Graph()

    LG.add_nodes_from([(k, {"original_hyperedge": v}) for k, v in H._edge.items()])
    edge_order = {edge: idx for idx, edge in enumerate(H._edge)}

    # Preserve the current behavior for s <= 0, which includes disjoint pairs.
    if s <= 0:
        for e1, e2 in combinations(H._edge, 2):
            intersection_size = len(H._edge[e1].intersection(H._edge[e2]))
            if not weights:
                LG.add_edge(e1, e2)
            else:
                weight = intersection_size
                if weights == "normalized":
                    weight /= min(len(H._edge[e1]), len(H._edge[e2]))
                LG.add_edge(
                    e1,
                    e2,
                    weight=weight,
                )
        return LG

    overlap_sizes = defaultdict(int)

    for memberships in H._node.values():
        if len(memberships) < 2:
            continue

        for e1, e2 in combinations(memberships, 2):
            if edge_order[e1] > edge_order[e2]:
                e1, e2 = e2, e1
            overlap_sizes[(e1, e2)] += 1

    if weights == "normalized":
        edge_sizes = {e: len(members) for e, members in H._edge.items()}

    for e1, e2 in sorted(
        overlap_sizes, key=lambda pair: (edge_order[pair[0]], edge_order[pair[1]])
    ):
        intersection_size = overlap_sizes[(e1, e2)]
        if intersection_size < s:
            continue

        if not weights:
            # Add unweighted edge
            LG.add_edge(e1, e2)
        else:
            # Compute the (normalized) weight
            weight = intersection_size
            if weights == "normalized":
                weight /= min(edge_sizes[e1], edge_sizes[e2])
            # Add edge with weight
            LG.add_edge(
                e1,
                e2,
                weight=weight,
            )

    return LG
