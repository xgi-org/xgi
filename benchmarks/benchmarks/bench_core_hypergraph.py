from .common import Benchmark

import os
import xgi
import pandas as pd

class CoreHypergraph(Benchmark):
    def setup(self):
        self.enron_hypergraph = xgi.load_xgi_data("email-enron")
        self.enron_edgelist = xgi.to_hyperedge_list(self.enron_hypergraph)

    def time_construction(self):
        xgi.Hypergraph(self.enron_edgelist)
    
    def time_node_memberships(self):
        [self.enron_hypergraph.nodes.memberships(n) for n in self.enron_hypergraph.nodes]
    
    def time_edge_members(self):
        [self.enron_hypergraph.edges.members(e) for e in self.enron_hypergraph.edges]
    
    def time_node_attributes(self):
        [self.enron_hypergraph.nodes[n] for n in self.enron_hypergraph.nodes]

    def time_edge_attributes(self):
        [self.enron_hypergraph.edges[e] for e in self.enron_hypergraph.edges]
    
    def time_degree(self):
        self.enron_hypergraph.degree()
    
    def time_edge_size(self):
        self.enron_hypergraph.edge_size()