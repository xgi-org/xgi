import pandas as pd

import xgi
import numpy as np
import random


import pytest

def test_construct_from_edgelist(benchmark):
    def setup():
        H = xgi.read_hif("email-enron.json")
        return (H.edges.members(),), {}
    
    benchmark.pedantic(xgi.Hypergraph, setup=setup, rounds=10)


def test_construct_from_edgedict(benchmark):
    def setup():
        H = xgi.read_hif("email-enron.json")
        return (H.edges.members(dtype=dict),), {}
    
    benchmark.pedantic(xgi.Hypergraph, setup=setup, rounds=10)


def test_construct_from_df(benchmark):
    def setup():
        H = xgi.read_hif("email-enron.json")
        return (xgi.to_bipartite_pandas_dataframe(H),), {}
    
    benchmark.pedantic(xgi.Hypergraph, setup=setup, rounds=10)

def test_node_memberships(benchmark):
    def setup():
        H = xgi.read_hif("email-enron.json")
        return (H,), {}
    
    def node_memberships(H):
        [H.nodes.memberships(n) for n in H.nodes]

    benchmark.pedantic(node_memberships, setup=setup, rounds=10)


def test_edge_members(benchmark):
    def setup():
        H = xgi.read_hif("email-enron.json")
        return (H,), {}
    
    def edge_members(H):
        [H.edges.members(eid) for eid in H.edges]

    benchmark.pedantic(edge_members, setup=setup, rounds=10)


# def setup_benchmarks():
#     random.seed(1)
#     # but will seed it nevertheless
#     np.random.seed(1)
#     self.hypergraph = xgi.load_xgi_data("email-enron")
#     self.enron_edgelist = xgi.to_hyperedge_list(self.hypergraph)
#     self.enron_edgedict = xgi.to_hyperedge_dict(self.hypergraph)
#     self.enron_df = xgi.to_bipartite_pandas_dataframe(self.hypergraph)


# class CoreHypergraph(Benchmark):
#     def setup(self):
#         self.hypergraph = xgi.load_xgi_data("email-enron")
#         self.enron_edgelist = xgi.to_hyperedge_list(self.hypergraph)
#         self.enron_edgedict = xgi.to_hyperedge_dict(self.hypergraph)
#         self.enron_df = xgi.to_bipartite_pandas_dataframe(self.hypergraph)

#     def time_node_attributes(self):
#         [self.hypergraph.nodes[n] for n in self.hypergraph.nodes]

#     def time_edge_attributes(self):
#         [self.hypergraph.edges[e] for e in self.hypergraph.edges]

#     def time_degree(self):
#         self.hypergraph.degree()

#     def time_nodestats_degree(self):
#         self.hypergraph.nodes.degree.asnumpy()

#     def time_edge_size(self):
#         self.hypergraph.edges.size.asnumpy()

#     def time_isolates(self):
#         self.hypergraph.nodes.isolates()

#     def time_singletons(self):
#         self.hypergraph.edges.singletons()

#     def time_copy(self):
#         self.hypergraph.copy()

#     def time_dual(self):
#         self.hypergraph.dual()
