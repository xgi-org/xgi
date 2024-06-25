"""Read from and write to JSON."""

import json
from collections import defaultdict
from os.path import dirname, join

from ..convert import from_hypergraph_dict, to_hypergraph_dict
from ..core import Hypergraph, SimplicialComplex

__all__ = ["write_json", "read_json"]


def write_json(H, path, collection_name=""):
    """
    A function to write a file in a standardized JSON format.

    If the dataset is a collection, makes local copies of all the
    datasets in the collection and a main file pointing to all of
    the datasets.

    Parameters
    ----------
    H: Hypergraph object
        The specified hypergraph object
    path: string
        The path of the file to write to. If the data is a collection,
        it is the directory in which to put all the files.
    collection_name : str
        The name of the collection of data (if any). If `H` is not
        a collection, this argument is unused.

    Raises
    ------
    XGIError
        If the node or edge IDs have conflicts after casting
        to strings, e.g., node IDs "2" and 2.

    """
    if collection_name:
        collection_name += "_"

    if isinstance(H, list):
        collection_data = defaultdict(dict)
        for i, H in enumerate(H):
            fname = f"{path}/{collection_name}{i}.json"
            collection_data["datasets"][i] = {
                "relative-path": f"{collection_name}{i}.json"
            }
            write_json(H, fname)
        collection_data["type"] = "collection"
        datastring = json.dumps(collection_data, indent=2)
        with open(
            f"{path}/{collection_name}collection_information.json", "w"
        ) as output_file:
            output_file.write(datastring)

    elif isinstance(H, dict):
        collection_data = defaultdict(dict)
        for name, H in H.items():
            fname = f"{path}/{collection_name}{name}.json"
            collection_data["datasets"][name] = {
                "relative-path": f"{collection_name}{name}.json"
            }
            write_json(H, fname)
        collection_data["type"] = "collection"
        datastring = json.dumps(collection_data, indent=2)
        with open(
            f"{path}/{collection_name}collection_information.json", "w"
        ) as output_file:
            output_file.write(datastring)

    elif isinstance(H, (Hypergraph, SimplicialComplex)):
        data = to_hypergraph_dict(H)
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
    Hypergraph
        The loaded hypergraph. If the dataset chosen is a collection,
        returns a dictionary of Hypergraph objects.

    Raises
    ------
    XGIError
        If the JSON is not in a format that can be loaded.

    """
    with open(path) as file:
        jsondata = json.loads(file.read())

    if "type" in jsondata and jsondata["type"] == "collection":
        collection = {}
        for name, data in jsondata["datasets"].items():
            relpath = data["relative-path"]
            H = read_json(
                join(dirname(path), relpath), nodetype=nodetype, edgetype=edgetype
            )
            collection[name] = H
        return collection

    return from_hypergraph_dict(jsondata, nodetype=nodetype, edgetype=edgetype)
