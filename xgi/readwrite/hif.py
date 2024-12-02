"""Read from and write to the HIF Standard.

For more information on the HIF standard, see the
HIF `project <https://github.com/pszufe/HIF_validators>`_.
"""

import json
from collections import defaultdict
from os.path import dirname, join

from ..convert import from_hif_dict, to_hif_dict
from ..exception import XGIError

__all__ = ["write_hif", "write_hif_collection", "read_hif", "read_hif_collection"]


def write_hif(H, path):
    """
    A function to write a higher-order network according to the HIF standard.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    H: Hypergraph, DiHypergraph, or SimplicialComplex object
        The specified higher-order network
    path: string
        The path of the file to read from
    """
    data = to_hif_dict(H)

    datastring = json.dumps(data, indent=2)

    with open(path, "w") as output_file:
        output_file.write(datastring)


def write_hif_collection(H, path, collection_name=""):
    """
    A function to write a collection of higher-order network according to the HIF standard.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    H: list or dict of Hypergraph, DiHypergraph, or SimplicialComplex objects
        The specified higher-order network
    path: string
        The path of the file to read from
    """
    if isinstance(H, list):
        collection_data = defaultdict(dict)
        for i, H in enumerate(H):
            fname = f"{path}/{collection_name}_{i}.json"
            collection_data["datasets"][i] = {
                "relative-path": f"{collection_name}_{i}.json"
            }
            write_hif(H, fname)
        collection_data["type"] = "collection"
        datastring = json.dumps(collection_data, indent=2)
        with open(
            f"{path}/{collection_name}_collection_information.json", "w"
        ) as output_file:
            output_file.write(datastring)

    elif isinstance(H, dict):
        collection_data = defaultdict(dict)
        for name, H in H.items():
            fname = f"{path}/{collection_name}_{name}.json"
            collection_data["datasets"][name] = {
                "relative-path": f"{collection_name}_{name}.json"
            }
            write_hif(H, fname)
        collection_data["type"] = "collection"
        datastring = json.dumps(collection_data, indent=2)
        with open(
            f"{path}/{collection_name}_collection_information.json", "w"
        ) as output_file:
            output_file.write(datastring)


def read_hif(path, nodetype=None, edgetype=None):
    """
    A function to read a file created according to the HIF format.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    path: str
        The path to the json file
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

    return from_hif_dict(data, nodetype=nodetype, edgetype=edgetype)


def read_hif_collection(path, nodetype=None, edgetype=None):
    """
    A function to read a collection of files created according to the HIF format.

    There must be a collection information JSON file which has a top-level field "datasets"
    with subfields "relative-path", indicating each dataset's location relative to the
    collection file

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    path: str
        A path to the collection json file.
    nodetype: type, optional
        type that the node IDs will be cast to
    edgetype: type, optional
        type that the edge IDs will be cast to

    Returns
    -------
    A dictionary of Hypergraph, SimplicialComplex, or DiHypergraph objects
        The collection of networks
    """
    with open(path) as file:
        jsondata = json.loads(file.read())

    try:
        collection = {}
        for name, data in jsondata["datasets"].items():
            relpath = data["relative-path"]
            H = read_hif(
                join(dirname(path), relpath), nodetype=nodetype, edgetype=edgetype
            )
            collection[name] = H
        return collection
    except KeyError:
        raise XGIError("Data collection is in the wrong format!")
