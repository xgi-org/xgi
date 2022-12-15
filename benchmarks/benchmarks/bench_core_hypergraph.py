import pandas as pd

import xgi

from .common import Benchmark


class CoreHypergraph(Benchmark):
    def setup(self):
        self.hypergraph = xgi.load_xgi_data("email-enron")
        self.enron_edgelist = xgi.to_hyperedge_list(self.hypergraph)
        self.enron_edgedict = xgi.to_hyperedge_dict(self.hypergraph)
        self.enron_df = xgi.to_bipartite_pandas_dataframe(self.hypergraph)

    def time_edgelist_construction(self):
        xgi.Hypergraph(self.enron_edgelist)

    def time_edgedict_construction(self):
        xgi.Hypergraph(self.enron_edgedict)

    def time_df_construction(self):
        xgi.Hypergraph(self.enron_df)

    def time_node_memberships(self):
        [self.hypergraph.nodes.memberships(n) for n in self.hypergraph.nodes]

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
