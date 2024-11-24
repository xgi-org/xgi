import random

import numpy as np
import pandas as pd
import pytest

import xgi


def test_construct_from_edgelist(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H.edges.members(),), {}

    benchmark.pedantic(xgi.Hypergraph, setup=setup, rounds=10)


def test_construct_from_edgedict(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H.edges.members(dtype=dict),), {}

    benchmark.pedantic(xgi.Hypergraph, setup=setup, rounds=10)


def test_construct_from_df(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (xgi.to_bipartite_pandas_dataframe(H),), {}

    benchmark.pedantic(xgi.Hypergraph, setup=setup, rounds=10)


def test_node_memberships(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def node_memberships(H):
        [H.nodes.memberships(n) for n in H.nodes]

    benchmark.pedantic(node_memberships, setup=setup, rounds=10)


def test_edge_members(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def edge_members(H):
        [H.edges.members(eid) for eid in H.edges]

    benchmark.pedantic(edge_members, setup=setup, rounds=10)


def test_node_attributes(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def node_attributes(H):
        [H.nodes[nid] for nid in H.nodes]

    benchmark.pedantic(node_attributes, setup=setup, rounds=10)


def test_edge_attributes(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def edge_attributes(H):
        [H.edges[eid] for eid in H.edges]

    benchmark.pedantic(edge_attributes, setup=setup, rounds=10)


def test_degree(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def degree(H):
        H.degree()

    benchmark.pedantic(degree, setup=setup, rounds=10)


def test_nodestats_degree(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def degree(H):
        H.nodestats.degree.asnumpy()

    benchmark.pedantic(degree, setup=setup, rounds=10)


def test_nodestats_degree(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def degree(H):
        H.nodes.degree.asnumpy()

    benchmark.pedantic(degree, setup=setup, rounds=10)


def test_edge_size(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def degree(H):
        H.edges.size.asnumpy()

    benchmark.pedantic(degree, setup=setup, rounds=10)


def test_isolates(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def isolates(H):
        H.nodes.isolates()

    benchmark.pedantic(isolates, setup=setup, rounds=10)


def test_singletons(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def singletons(H):
        H.edges.singletons()

    benchmark.pedantic(singletons, setup=setup, rounds=10)


def test_copy(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def copy(H):
        H.copy()

    benchmark.pedantic(copy, setup=setup, rounds=10)


def test_dual(benchmark):
    def setup():
        H = xgi.read_hif("benchmarks/email-enron.json")
        return (H,), {}

    def dual(H):
        H.dual()

    benchmark.pedantic(dual, setup=setup, rounds=10)
