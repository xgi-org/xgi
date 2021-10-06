import json
import hypergraph as hg
from hypergraph.classes.hypergraph import Hypergraph
from hypergraph.exception import HypergraphError
from hypergraph.utils.utilities import get_dual


__all__ = [
    "write_hypergraph_json",
    "read_hypergraph_json"
]


def write_hypergraph_json(H, path):

    # initialize empty data
    data = dict()

    # get overall hypergraph attributes, name always gets written (default is an empty string)
    data["hypergraph"] = {"name" : H.name}
    data["hypergraph"].update(H._hypergraph)

    # get node data
    data["node-data"] = {id : H._node_attr[id] for id in H.nodes}

    # get edge data
    data["hyperedge-data"] = {id : H._edge_attr[id] for id in H.edges}

    # hyperedge list
    data["hyperedges"] = {id : tuple(H.edges[id]) for id in H.edges}

    datastring = json.dumps(data)

    with open(path, "w") as output_file:
        output_file.write(datastring)


def read_hypergraph_json(path):
    with open(path) as file:
        data = json.loads(file.read())
    H = hg.empty_hypergraph()
    try:
        H._hypergraph = data["hypergraph"]
        H._node_attr = data["node-data"]
        H._edge_attr = data["hyperedge-data"]
        H._edge = {id : set(val) for id, val in data["hyperedges"].items()}
        H._node = get_dual(H._edge)
    except:
        raise HypergraphError("Invalid data structure!")

    return H