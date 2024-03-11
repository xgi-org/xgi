import numpy as np
import pandas as pd
import pytest

import xgi

## di-node stat specific tests


def test_degree(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    degs = {0: 1, 1: 2, 2: 3, 4: 2, 3: 1, 5: 1}
    assert H.degree() == degs
    assert H.degree(order=2) == {0: 1, 1: 2, 2: 2, 4: 1, 3: 0, 5: 0}
    assert H.nodes.degree.asdict() == degs


def test_in_degree(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    degs = {0: 1, 1: 2, 2: 2, 4: 1, 3: 1, 5: 0}
    assert H.in_degree() == degs
    assert H.in_degree(order=2) == {0: 1, 1: 2, 2: 1, 4: 0, 3: 0, 5: 0}
    assert H.nodes.in_degree.asdict() == degs


def test_out_degree(diedgelist2):
    H = xgi.DiHypergraph(diedgelist2)
    degs = {0: 0, 1: 0, 2: 1, 4: 2, 3: 0, 5: 1}
    assert H.out_degree() == degs
    assert H.out_degree(order=2) == {0: 0, 1: 0, 2: 1, 4: 1, 3: 0, 5: 0}
    assert H.nodes.out_degree.asdict() == degs
