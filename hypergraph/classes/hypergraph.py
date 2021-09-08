from hypergraph.classes.entity import EntitySet

class Hypergraph:
    def __init__(self, data, name=""):
        self._name = name
        self._edges = EntitySet(data)
        self._nodes = self._edges.dual()

    def __iter__(self):
        return iter(self.nodes)

    def __contains__(self, node):
        try:
            return node in self.nodes
        except TypeError:
            return False

    def __len__(self):
        return len(self.nodes)

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    def number_of_nodes(self):
        return len(self.nodes)

    def has_node(self, node):
        try:
            return node in self.nodes
        except TypeError:
            return False

    
    # def add_node(self, edge):
    #     print("under dev")  

    # def add_edge(self, edge):
    #     print("under dev")  

    # def addEdges(self, hyperedges, weightedEdges):
    #     # unweighted format for hyperedges: {"id0":{"members":(1,2,3)}, "id1":{"members":(1,2)},...}
    #     # weighted format for hyperedges: {"id0":{"members":(1,2,3),"weight":1.1}, "id1":{"members":(1,2),"weight":0.5},...}
    #     self.weightedEdges = weightedEdges
    #     self.nodes = dict()
    #     nodes = set()
    #     # if list of tuples
    #     if isinstance(hyperedges, list):
    #         self.hyperedges = dict()
    #         uid = 0
    #         for hyperedge in hyperedges:
    #             if self.weightedEdges:
    #                 self.hyperedges[uid] = {"members":hyperedge[:-1],"weight":hyperedge[-1]}
    #             else:
    #                 self.hyperedges[uid] = {"members":hyperedge}
    #                 nodes.update(hyperedge)
    #             uid += 1

    #     elif isinstance(hyperedges, dict):
    #         self.hyperedges = hyperedges.copy()
    #         for edgeData in self.hyperedges.values():
    #             nodes.update(edgeData["members"])

    #     for nodeLabel in list(nodes):
    #         self.nodes[nodeLabel] = dict()
    #     # need a better way to check whether the format is correct

    # def addNodeAttributes(self, nodeAttributes):
    #     # find unique nodes in the hyperedges
    #     for label, attribute in nodeAttributes.items():
    #         try:
    #             self.nodes[label] = attribute
    #         except:
    #             print("invalid label")

    # def deleteDegenerateHyperedges(self):
    #     cleanedHyperedges = dict()
    #     for uid, hyperedge in self.hyperedges.items():
    #         if len(hyperedge["members"]) >= 2:
    #             cleanedHyperedges[uid] = hyperedge
    #     self.hyperedges = cleanedHyperedges

    