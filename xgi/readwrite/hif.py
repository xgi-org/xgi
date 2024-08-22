"""Read from and write to JSON."""

import json
from collections import defaultdict

import numpy as np

from ..convert import to_bipartite_edgelist
from ..core import DiHypergraph, Hypergraph, SimplicialComplex
from ..exception import XGIError
from ..utils import IDDict

__all__ = ["to_hif", "from_hif"]


def to_hif(G, path):
    """
    A function to write a file in a standardized JSON format.

    Parameters
    ----------
    G: Hypergraph, DiHypergraph, or SimplicialComplex object
        The specified higher-order network
    path: string
        The path of the file to read from

    Raises
    ------
    XGIError
        If the node or edge IDs have conflicts after casting
        to strings, e.g., node IDs "2" and 2.

    """
    # initialize empty data
    data = defaultdict(list)

    # name always gets written (default is an empty string)
    data["metadata"] = {}
    data["metadata"].update(G._net_attr)

    if isinstance(G, SimplicialComplex):
        data["network-type"] = "asc"
    elif isinstance(G, Hypergraph):
        data["network-type"] = "undirected"
    elif isinstance(G, DiHypergraph):
        data["network-type"] = "directed"

    # get node data
    try:
        isolates = set(G.nodes.isolates())
        nodes_with_attrs = set(n for n in G.nodes if G.nodes[n])
        for n in isolates.union(nodes_with_attrs):
            attr = {"attr": G.nodes[n]} if G.nodes[n] else {}
            data["nodes"].append(IDDict({"node": n}) + attr)

    except KeyError:
        raise XGIError("Node attributes not saved!")

    try:
        empty = set(G.edges.empty())
        edges_with_attrs = set(e for e in G.edges if G.edges[e])
        for e in empty.union(edges_with_attrs):
            attr = {"attr": G.edges[e]} if G.edges[e] else {}
            data["edges"].append(IDDict({"edge": e}) + attr)

    except KeyError:
        raise XGIError("Edge attributes not saved!")

    # hyperedge dict
    if data["network-type"] == "directed":
        data["incidences"] = [
            IDDict({"edge": e, "node": n, "direction": d})
            for n, e, d in to_bipartite_edgelist(G)
        ]
    elif data["network-type"] == "undirected":
        data["incidences"] = [
            IDDict({"edge": e, "node": n}) for n, e in to_bipartite_edgelist(G)
        ]
    elif data["network-type"] == "asc":
        # get maximal edges and edges with attributes
        edges_with_attrs = {eid for eid in G.edges if G.edges[eid]}
        maximal_edges = set(G.edges.maximal())
        eids = edges_with_attrs.intersection(maximal_edges)

        data["incidences"] = [
            IDDict({"edge": e, "node": n})
            for n, e in to_bipartite_edgelist(G)
            if e in eids
        ]

    datastring = json.dumps(data, indent=2)

    with open(path, "w") as output_file:
        output_file.write(datastring)


def from_hif(path, nodetype=None, edgetype=None):
    """
    A function to read a file in a standardized JSON format.

    Parameters
    ----------
    data: dict
        A dictionary in the hypergraph JSON format
    nodetype: type, optional
        type that the node IDs will be cast to
    edgetype: type, optional
        type that the edge IDs will be cast to

    Returns
    -------
    A Hypergraph object
        The loaded hypergraph

    Raises
    ------
    XGIError
        If the JSON is not in a format that can be loaded.

    """
    with open(path) as file:
        data = json.loads(file.read())

    return _from_dict(data, nodetype=nodetype, edgetype=edgetype)


def _from_dict(data, nodetype=None, edgetype=None, max_order=None):
    """
    A function to read a file in a standardized JSON format.

    Parameters
    ----------
    data: dict
        A dictionary in the hypergraph JSON format
    nodetype: type, optional
        Type that the node IDs will be cast to
    edgetype: type, optional
        Type that the edge IDs will be cast to
    max_order: int, optional
        Maximum order of edges to add to the hypergraph

    Returns
    -------
    A Hypergraph object
        The loaded hypergraph

    Raises
    ------
    XGIError
        If the JSON is not in a format that can be loaded.

    See Also
    --------
    read_json

    """

    def _empty_edge(network_type):
        if network_type in {"asc", "undirected"}:
            return set()
        else:
            return {"in": set(), "out": set()}

    if "network-type" in data:
        network_type = data["network-type"]
    else:
        network_type = "undirected"

    if network_type == "asc":
        # Convert to simplicial complex after
        G = Hypergraph()
    elif network_type == "undirected":
        G = Hypergraph()
        network_type = "undirected"
    elif network_type == "directed":
        G = DiHypergraph()
    else:
        XGIError("Invalid type")

    # Import network metadata
    if "metadata" in G:
        G._net_attr.update(data["metadata"])

    # Import network structure through incidence records
    try:
        if network_type == "directed":
            edgedict = defaultdict(lambda: {"in": set(), "out": set()})
        else:
            edgedict = defaultdict(set)

        for record in data["incidences"]:
            n = record["node"]
            e = record["edge"]
            if "attr" in record:
                attr = record["attr"]
            else:
                attr = {}

            if network_type == "directed":
                d = record["direction"]
                G.add_node_to_edge(n, e, d, **attr)
            else:
                G.add_node_to_edge(n, e, **attr)

    except KeyError as e:
        raise XGIError("Failed to import incidences.") from e

    # import node attributes if they exist
    if "nodes" in data:
        for record in data["nodes"]:
            n = record["node"]
            if "attr" in record:
                attr = record["attr"]
            else:
                attr = {}
        if n not in G._node:
            G.add_node(n, **attr)
        else:
            G.set_node_attributes({n: attr})

    # import edge attributes if they exist
    if "edges" in data:
        for record in data["edges"]:
            e = record["edge"]
            if "attr" in record:
                attr = record["attr"]
            else:
                attr = {}
            if e not in G._edge:
                G.add_edge(_empty_edge(network_type), e, **attr)
            else:
                G.set_edge_attributes({e: attr})

    if network_type == "asc":
        G = SimplicialComplex(G)
    return G
