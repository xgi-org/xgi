"""Read from and write to JSON."""
import json

from ..convert import dict_to_hypergraph
from ..exception import XGIError

__all__ = ["write_json", "read_json"]


def write_json(H, path):
    """
    A function to write a file in a standardized JSON format.

    Parameters
    ----------
    H: Hypergraph object
        The specified hypergraph object
    path: string
        The path of the file to read from

    """
    # initialize empty data
    data = {}

    # name always gets written (default is an empty string)
    data["hypergraph-data"] = {}
    data["hypergraph-data"].update(H._hypergraph)

    # get node data
    try:
        data["node-data"] = {str(idx): H.nodes[idx] for idx in H.nodes}
    except KeyError:
        raise XGIError("Node attributes not saved!")

    try:
        data["edge-data"] = {str(idx): H.edges[idx] for idx in H.edges}
    except KeyError:
        raise XGIError("Edge attributes not saved!")

    # hyperedge dict
    data["edge-dict"] = {
        str(idx): [str(n) for n in H.edges.members(idx)] for idx in H.edges
    }

    datastring = json.dumps(data, indent=2)

    with open(path, "w") as output_file:
        output_file.write(datastring)


def read_json(path, nodetype=None, edgetype=None):
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

    return dict_to_hypergraph(data, nodetype=nodetype, edgetype=edgetype)
