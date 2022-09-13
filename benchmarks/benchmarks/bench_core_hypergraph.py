from .common import Benchmark

import xgi
import pandas as pd


class CoreHypergraph(Benchmark):
    def setup(self):
        fname = "../../data/disGene.txt"
        self.hypergraph = xgi.read_bipartite_edgelist(fname, delimiter=" ")
        self.disgene_edgelist = xgi.to_hyperedge_list(self.hypergraph)
        self.disgene_edgedict = xgi.to_hyperedge_dict(self.hypergraph)
        self.disgene_df = pd.read_csv(fname, delimiter=" ", header=None)

    def time_edgelist_construction(self):
        xgi.Hypergraph(self.disgene_edgelist)
    
    def time_edgedict_construction(self):
        xgi.Hypergraph(self.disgene_edgedict)
    
    def time_df_construction(self):
        xgi.Hypergraph(self.disgene_df)

    def time_node_memberships(self):
        [
            self.hypergraph.nodes.memberships(n)
            for n in self.hypergraph.nodes
        ]

    def time_edge_members(self):
        [self.hypergraph.edges.members(e) for e in self.hypergraph.edges]

    def time_node_attributes(self):
        [self.hypergraph.nodes[n] for n in self.hypergraph.nodes]

    def time_edge_attributes(self):
        [self.hypergraph.edges[e] for e in self.hypergraph.edges]

    def time_degree(self):
        self.hypergraph.degree()

    def time_nodestats_degree(self):
        self.hypergraph.nodes.degree.asnumpy()

    def time_edge_size(self):
        self.hypergraph.edges.size.asnumpy()

    def time_isolates(self):
        self.hypergraph.nodes.isolates()
    
    def time_singletons(self):
        self.hypergraph.edges.singletons()
    
    def time_copy(self):
        self.hypergraph.copy()
    
    def time_dual(self):
        self.hypergraph.dual()