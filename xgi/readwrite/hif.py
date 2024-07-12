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
    data = {}

    # name always gets written (default is an empty string)
    data["metadata"] = {}
    data["metadata"].update(G._net_attr)

    if isinstance(G, SimplicialComplex):
        data["type"] = "asc"
    elif isinstance(G, Hypergraph):
        data["type"] = "undirected"
    elif isinstance(G, DiHypergraph):
        data["type"] = "directed"

    # get node data
    try:
        data["nodes"] = [
            IDDict({"uid": idx}) + {"attrs": G.nodes[idx]} for idx in G.nodes
        ]
    except KeyError:
        raise XGIError("Node attributes not saved!")

    try:
        data["edges"] = [
            IDDict({"uid": idx}) + {"attrs": G.edges[idx]} for idx in G.edges
        ]

    except KeyError:
        raise XGIError("Edge attributes not saved!")

    # hyperedge dict
    if data["type"] == "directed":
        data["incidences"] = [
            IDDict({"edge": e, "node": n, "direction": d}) + {"attrs": []}
            for n, e, d in to_bipartite_edgelist(G)
        ]
    elif data["type"] == "undirected":
        data["incidences"] = [
            IDDict({"edge": e, "node": n}) + {"attrs": []}
            for n, e in to_bipartite_edgelist(G)
        ]
    elif data["type"] == "asc":
        # get maximal edges and edges with attributes
        edges_with_attrs = {eid for eid in G.edges if G.edges[eid]}
        maximal_edges = set(G.edges.maximal())
        eids = edges_with_attrs.intersection(maximal_edges)

        data["incidences"] = [
            IDDict({"edge": e, "node": n}) + {"attrs": []}
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
    if not max_order:
        max_order = np.inf

    if data["type"] == "asc":
        G = SimplicialComplex()
        G.add_edge = G.add_simplex
    elif data["type"] == "undirected":
        G = Hypergraph()
    elif data["type"] == "directed":
        G = DiHypergraph()

    try:
        G._net_attr.update(data["metadata"])
    except KeyError:
        raise XGIError("Failed to get metadata.")

    try:
        if data["type"] == "directed":
            edgedict = defaultdict(lambda: {"in": set(), "out": set()})
        else:
            edgedict = defaultdict(set)

        for record in data["incidences"]:
            eid = record["edge"]
            nid = record["node"]
            if edgetype:
                try:
                    eid = edgetype(eid)
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert the edge with ID {eid} to type {edgetype}."
                    ) from e

            if nodetype:
                try:
                    eid = edgetype(eid)
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert node with ID {nid} to type {nodetype}."
                    ) from e

            if data["type"] == "directed":
                direction = data["direction"]
                edgedict[eid][direction].add(nid)
            else:
                edgedict[eid].add(nid)

        for eid, e in edgedict.items():
            if data["type"] == "directed":
                order = len(e["in"].union(e["out"])) - 1
            else:
                order = len(e) - 1

            if order <= max_order:
                G.add_edge(e, eid)

    except KeyError as e:
        raise XGIError("Failed to import incidences.") from e

    try:
        for record in data["nodes"]:
            nid = record["uid"]
            attrs = record["attrs"]
            if nodetype:
                try:
                    nid = nodetype(nid)
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert node IDs to type {nodetype}."
                    ) from e
            G._node_attr[nid] = attrs
    except KeyError:
        raise XGIError("Failed to import node attributes.")

    try:
        for record in data["edges"]:
            eid = record["uid"]
            attrs = record["attrs"]
            if edgetype:
                try:
                    eid = edgetype(eid)
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert edge IDs to type {edgetype}."
                    ) from e
            G._edge_attr[eid] = attrs
    except KeyError:
        raise XGIError("Failed to import edge attributes.")

    return G
