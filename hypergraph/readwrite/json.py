import json

def to_hypergraph_json(H, filename):

    # initialize empty data
    data = dict()
    data["hypergraph"]  = dict()
    data["nodes"] = dict()
    data["hyperedges"] = dict()

    # get overall hypergraph attributes, name always gets written (default is an empty string)
    data["hypergraph"]["name"] = H.name
    data["hypergraph"].update(H.hypergraph)

    # get node data
    data["nodes"]["node-labels"] = {n : {} for n in H.nodes}

    # get edge data
    data["hyperedges"]["hyperedge-list"] = {uid : tuple(H.edges[uid]) for uid in H.edges}

    datastring = json.dumps(data)

    with open(filename, "w") as output_file:
        output_file.write(datastring)