"""Method for converting from a standardized dictionary."""

from collections import Counter

from ..exception import XGIError
from ..generators import empty_hypergraph
from ..utils import get_network_type

__all__ = ["to_hypergraph_dict", "from_hypergraph_dict"]


def to_hypergraph_dict(H):
    """A method to convert a hypergraph into a standard dictionary format.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph to convert

    Returns
    -------
    dict
        A dictionary of the form described in https://github.com/xgi-org/xgi-data.

    Raises
    ------
    XGIError
        If node IDs will be collapsed when casting to a string.
    XGIError
        If edge Ids will be collapsed when casting to a string.

    See Also
    --------
    ~xgi.readwrite.json.read_json
    ~xgi.readwrite.json.write_json
    """
    data = {}
    data["type"] = get_network_type(H)
    # name always gets written (default is an empty string)
    data["hypergraph-data"] = {}
    data["hypergraph-data"].update(H._net_attr)

    # get node data
    data["node-data"] = {str(idx): H.nodes[idx] for idx in H.nodes}

    if len(data["node-data"]) != H.num_nodes:
        dups = [
            item
            for item, count in Counter([str(n) for n in H.nodes]).items()
            if count > 1
        ]
        raise XGIError(
            f"When casting node IDs to strings, ID(s) {', '.join(dups)} have conflicting IDs!"
        )

    data["edge-data"] = {str(idx): H.edges[idx] for idx in H.edges}

    if len(data["edge-data"]) != H.num_edges:
        dups = [
            item
            for item, count in Counter([str(n) for n in H.edges]).items()
            if count > 1
        ]
        raise XGIError(
            f"When casting edge IDs to strings, ID(s) {', '.join(dups)} have conflicting IDs!"
        )

    # hyperedge dict
    data["edge-dict"] = {
        str(idx): [str(n) for n in sorted(H.edges.members(idx))] for idx in H.edges
    }
    return data


def from_hypergraph_dict(data, nodetype=None, edgetype=None, max_order=None):
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
    ~xgi.readwrite.json.read_json
    ~xgi.readwrite.json.write_json

    """
    H = empty_hypergraph()
    try:
        H._net_attr.update(data["hypergraph-data"])
    except KeyError:
        raise XGIError("Failed to get hypergraph data attributes.")

    try:
        for id, dd in data["node-data"].items():
            if nodetype is not None:
                try:
                    id = nodetype(id)
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert edge IDs to type {nodetype}."
                    ) from e
            H.add_node(id, **dd)
    except KeyError:
        raise XGIError("Failed to import node attributes.")

    try:
        for id, edge in data["edge-dict"].items():
            if max_order and len(edge) > max_order + 1:
                continue
            if edgetype is not None:
                try:
                    id = edgetype(id)
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert the edge with ID {id} to type {edgetype}."
                    ) from e

            if nodetype is not None:
                try:
                    edge = {nodetype(n) for n in edge}
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert nodes to type {nodetype}."
                    ) from e
            H.add_edge(edge, id)

    except KeyError as e:
        raise XGIError("Failed to import edge dictionary.") from e

    try:
        if edgetype is None:
            edge_data = {
                key: val for key, val in data["edge-data"].items() if key in H.edges
            }
        else:
            edge_data = {
                edgetype(e): dd
                for e, dd in data["edge-data"].items()
                if edgetype(e) in H.edges
            }

        H.set_edge_attributes(edge_data)
    except KeyError as e:
        raise XGIError("Failed to import edge attributes.") from e

    return H
