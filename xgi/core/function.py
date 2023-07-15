"""Functional interface to hypergraph methods and assorted utilities."""

from copy import deepcopy

from .hypergraph import Hypergraph

__all__ = [
    "convert_labels_to_integers",
]


def convert_labels_to_integers(H, label_attribute="label"):
    """Relabel node and edge IDs to be sequential integers.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest

    label_attribute : string, default: "label"
        The attribute name that stores the old node and edge labels

    Returns
    -------
    Hypergraph
        A new hypergraph with nodes and edges with sequential IDs starting at 0.
        The old IDs are stored in the "label" attribute for both nodes and edges.

    Notes
    -----
    The "relabeling" will occur even if the node/edge IDs are sequential.
    Because the old IDs are stored in the "label" attribute for both nodes and edges,
    the old "label" values (if they exist) will be overwritten.
    """
    node_dict = dict(zip(H.nodes, range(H.num_nodes)))
    edge_dict = dict(zip(H.edges, range(H.num_edges)))
    temp_H = Hypergraph()
    temp_H._hypergraph = deepcopy(H._hypergraph)

    temp_H.add_nodes_from((id, deepcopy(H.nodes[n])) for n, id in node_dict.items())
    temp_H.set_node_attributes(
        {n: {label_attribute: id} for id, n in node_dict.items()}
    )

    temp_H.add_edges_from(
        (
            {node_dict[n] for n in e},
            edge_dict[id],
            deepcopy(H.edges[id]),
        )
        for id, e in H.edges.members(dtype=dict).items()
    )
    temp_H.set_edge_attributes(
        {e: {label_attribute: id} for id, e in edge_dict.items()}
    )

    return temp_H
