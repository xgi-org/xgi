"""Read from and write to the HIF Standard.

For more information on the HIF standard, see the
HIF `project <https://github.com/pszufe/HIF_validators>`_.
"""

import json
from collections import defaultdict

from ..convert import to_bipartite_edgelist
from ..core import DiHypergraph, Hypergraph, SimplicialComplex
from ..utils import IDDict

__all__ = ["write_hif", "read_hif"]


def write_hif(G, path):
    """
    A function to write a higher-order network according to the HIF standard.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    G: Hypergraph, DiHypergraph, or SimplicialComplex object
        The specified higher-order network
    path: string
        The path of the file to read from
    """
    # initialize empty data
    data = defaultdict(list)

    data["metadata"] = {}
    data["metadata"].update(G._net_attr)

    if isinstance(G, SimplicialComplex):
        data["network-type"] = "asc"
    elif isinstance(G, Hypergraph):
        data["network-type"] = "undirected"
    elif isinstance(G, DiHypergraph):
        data["network-type"] = "directed"

    # get node data
    isolates = set(G.nodes.isolates())
    nodes_with_attrs = set(n for n in G.nodes if G.nodes[n])
    for n in isolates.union(nodes_with_attrs):
        attr = {"attrs": G.nodes[n]} if G.nodes[n] else {}
        data["nodes"].append(IDDict({"node": n}) + attr)

    empty = set(G.edges.empty())
    edges_with_attrs = set(e for e in G.edges if G.edges[e])
    for e in empty.union(edges_with_attrs):
        attr = {"attrs": G.edges[e]} if G.edges[e] else {}
        data["edges"].append(IDDict({"edge": e}) + attr)

    # hyperedge dict
    if data["network-type"] == "directed":
        _convert_d = lambda d: "tail" if d == "in" else "head"
        data["incidences"] = [
            IDDict({"edge": e, "node": n, "direction": _convert_d(d)})
            for n, e, d in to_bipartite_edgelist(G)
        ]
    elif data["network-type"] in {"undirected", "asc"}:
        data["incidences"] = [
            IDDict({"edge": e, "node": n}) for n, e in to_bipartite_edgelist(G)
        ]

    datastring = json.dumps(data, indent=2)

    with open(path, "w") as output_file:
        output_file.write(datastring)


def read_hif(path, nodetype=None, edgetype=None):
    """
    A function to read a file created according to the HIF format.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

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
    A Hypergraph, SimplicialComplex, or DiHypergraph object
        The loaded network
    """
    with open(path) as file:
        data = json.loads(file.read())

    return _from_dict(data, nodetype=nodetype, edgetype=edgetype)


def _from_dict(data, nodetype=None, edgetype=None):
    """
    A helper function to read a file created according to the HIF format.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    data: dict
        A dictionary in the hypergraph JSON format
    nodetype: type, optional
        Type that the node IDs will be cast to
    edgetype: type, optional
        Type that the edge IDs will be cast to

    Returns
    -------
    A Hypergraph, SimplicialComplex, or DiHypergraph object
        The loaded network
    """

    def _empty_edge(network_type):
        if network_type in {"asc", "undirected"}:
            return set()
        else:
            return (set(), set())

    def _convert_id(i, idtype):
        if idtype:
            try:
                return idtype(i)
            except ValueError as e:
                raise TypeError(f"Failed to convert ID {i} to type {idtype}.") from e
        else:
            return i

    _convert_d = lambda d: "in" if d == "tail" else "out"

    if "network-type" in data:
        network_type = data["network-type"]
    else:
        network_type = "undirected"

    if network_type in {"asc", "undirected"}:
        G = Hypergraph()
    elif network_type == "directed":
        G = DiHypergraph()

    # Import network metadata
    if "metadata" in data:
        G._net_attr.update(data["metadata"])

    for record in data["incidences"]:
        n = _convert_id(record["node"], nodetype)
        e = _convert_id(record["edge"], edgetype)

        if network_type == "directed":
            d = record["direction"]
            d = _convert_d(d)  # convert from head/tail to in/out
            G.add_node_to_edge(e, n, d)
        else:
            G.add_node_to_edge(e, n)

    # import node attributes if they exist
    if "nodes" in data:
        for record in data["nodes"]:
            n = _convert_id(record["node"], nodetype)
            if "attrs" in record:
                attr = record["attrs"]
            else:
                attr = {}

            if n not in G._node:
                G.add_node(n, **attr)
            else:
                G.set_node_attributes({n: attr})

    # import edge attributes if they exist
    if "edges" in data:
        for record in data["edges"]:
            e = _convert_id(record["edge"], edgetype)
            if "attrs" in record:
                attr = record["attrs"]
            else:
                attr = {}
            if e not in G._edge:
                G.add_edge(_empty_edge(network_type), e, **attr)
            else:
                G.set_edge_attributes({e: attr})

    if network_type == "asc":
        G = SimplicialComplex(G)
    return G
