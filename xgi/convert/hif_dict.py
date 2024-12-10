"""Methods for converting to/from HIF standard."""

from collections import defaultdict

from ..core import DiHypergraph, Hypergraph, SimplicialComplex
from ..utils import IDDict
from .bipartite_edges import to_bipartite_edgelist

__all__ = ["to_hif_dict", "from_hif_dict"]


def to_hif_dict(H):
    """
    A function to create a dictionary according to the HIF standard from a higher-order network.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    H: Hypergraph, DiHypergraph, or SimplicialComplex object
        The specified higher-order network

    Returns
    -------
    defaultdict
        A dict according to the HIF standard.
    """
    data = defaultdict(list)

    data["metadata"] = {}
    data["metadata"].update(H._net_attr)

    if isinstance(H, SimplicialComplex):
        data["network-type"] = "asc"
    elif isinstance(H, Hypergraph):
        data["network-type"] = "undirected"
    elif isinstance(H, DiHypergraph):
        data["network-type"] = "directed"

    # get node data
    isolates = set(H.nodes.isolates())
    nodes_with_attrs = set(n for n in H.nodes if H.nodes[n])
    for n in isolates.union(nodes_with_attrs):
        attr = {"attrs": H.nodes[n]} if H.nodes[n] else {}
        data["nodes"].append(IDDict({"node": n}) + attr)

    empty = set(H.edges.empty())
    edges_with_attrs = set(e for e in H.edges if H.edges[e])
    for e in empty.union(edges_with_attrs):
        attr = {"attrs": H.edges[e]} if H.edges[e] else {}
        data["edges"].append(IDDict({"edge": e}) + attr)

    # hyperedge dict
    if data["network-type"] == "directed":
        _convert_d = lambda d: "tail" if d == "in" else "head"
        data["incidences"] = [
            IDDict({"edge": e, "node": n, "direction": _convert_d(d)})
            for n, e, d in to_bipartite_edgelist(H)
        ]
    elif data["network-type"] in {"undirected", "asc"}:
        data["incidences"] = [
            IDDict({"edge": e, "node": n}) for n, e in to_bipartite_edgelist(H)
        ]
    return data


def from_hif_dict(data, nodetype=None, edgetype=None):
    """
    A function to read a dictionary that follows the HIF standard.

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
        H = Hypergraph()
    elif network_type == "directed":
        H = DiHypergraph()

    # Import network metadata
    if "metadata" in data:
        H._net_attr.update(data["metadata"])

    for record in data["incidences"]:
        n = _convert_id(record["node"], nodetype)
        e = _convert_id(record["edge"], edgetype)

        if network_type == "directed":
            d = record["direction"]
            d = _convert_d(d)  # convert from head/tail to in/out
            H.add_node_to_edge(e, n, d)
        else:
            H.add_node_to_edge(e, n)

    # import node attributes if they exist
    if "nodes" in data:
        for record in data["nodes"]:
            n = _convert_id(record["node"], nodetype)
            if "attrs" in record:
                attr = record["attrs"]
            else:
                attr = {}

            if n not in H._node:
                H.add_node(n, **attr)
            else:
                H.set_node_attributes({n: attr})

    # import edge attributes if they exist
    if "edges" in data:
        for record in data["edges"]:
            e = _convert_id(record["edge"], edgetype)
            if "attrs" in record:
                attr = record["attrs"]
            else:
                attr = {}
            if e not in H._edge:
                H.add_edge(_empty_edge(network_type), e, **attr)
            else:
                H.set_edge_attributes({e: attr})

    if network_type == "asc":
        H = SimplicialComplex(H)
    return H
