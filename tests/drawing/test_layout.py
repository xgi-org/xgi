import numpy as np
import pytest

import xgi
from xgi.exception import XGIError


def test_random_layout():
    H = xgi.random_hypergraph(10, [0.2], seed=1)

    # seed
    pos1 = xgi.random_layout(H, seed=1)
    pos2 = xgi.random_layout(H, seed=2)
    pos3 = xgi.random_layout(H, seed=2)
    assert pos1.keys() == pos2.keys()
    assert pos2.keys() == pos3.keys()
    assert not np.allclose(list(pos1.values()), list(pos2.values()))
    assert np.allclose(list(pos2.values()), list(pos3.values()))

    assert len(pos1) == H.num_nodes

    # simplicial complex
    S = xgi.random_flag_complex_d2(10, 0.2)
    pos = xgi.random_layout(S)
    assert len(pos) == S.num_nodes


def test_pairwise_spring_layout():
    H = xgi.random_hypergraph(10, [0.2], seed=1)

    # seed
    pos1 = xgi.pairwise_spring_layout(H, seed=1)
    pos2 = xgi.pairwise_spring_layout(H, seed=2)
    pos3 = xgi.pairwise_spring_layout(H, seed=2)
    assert pos1.keys() == pos2.keys()
    assert pos2.keys() == pos3.keys()
    assert not np.allclose(list(pos1.values()), list(pos2.values()))
    assert np.allclose(list(pos2.values()), list(pos3.values()))

    assert len(pos1) == H.num_nodes

    # simplicial complex
    S = xgi.random_flag_complex_d2(10, 0.2, seed=1)
    pos = xgi.pairwise_spring_layout(S, seed=1)


def test_barycenter_spring_layout(hypergraph1):
    H = xgi.random_hypergraph(10, [0.2], seed=1)

    # seed
    pos1 = xgi.barycenter_spring_layout(H, seed=1)
    pos2 = xgi.barycenter_spring_layout(H, seed=2)
    pos3 = xgi.barycenter_spring_layout(H, seed=2)
    assert pos1.keys() == pos2.keys()
    assert pos2.keys() == pos3.keys()
    assert not np.allclose(list(pos1.values()), list(pos2.values()))
    assert np.allclose(list(pos2.values()), list(pos3.values()))

    assert len(pos1) == H.num_nodes

    # phantom
    pos4, G = xgi.barycenter_spring_layout(H, return_phantom_graph=True, seed=1)
    pos5 = xgi.barycenter_spring_layout(H, return_phantom_graph=False, seed=1)
    assert pos4.keys() == pos5.keys()
    assert np.allclose(list(pos4.values()), list(pos5.values()))

    # simplicial complex
    S = xgi.random_flag_complex_d2(10, 0.2)
    pos = xgi.barycenter_spring_layout(S)
    assert len(pos) == S.num_nodes

    # str nodes
    pos = xgi.barycenter_spring_layout(hypergraph1)
    assert len(pos) == hypergraph1.num_nodes

    # larger hyperedges
    H = xgi.random_hypergraph(10, [0.2, 0.1])
    pos = xgi.barycenter_spring_layout(H)
    assert len(pos) == H.num_nodes


def test_weighted_barycenter_spring_layout(hypergraph1):
    H = xgi.random_hypergraph(10, [0.2], seed=1)

    # seed
    pos1 = xgi.weighted_barycenter_spring_layout(H, seed=1)
    pos2 = xgi.weighted_barycenter_spring_layout(H, seed=2)
    pos3 = xgi.weighted_barycenter_spring_layout(H, seed=2)
    assert pos1.keys() == pos2.keys()
    assert pos2.keys() == pos3.keys()
    assert not np.allclose(list(pos1.values()), list(pos2.values()))
    assert np.allclose(list(pos2.values()), list(pos3.values()))

    assert len(pos1) == H.num_nodes

    # phantom
    pos4, G = xgi.weighted_barycenter_spring_layout(
        H, return_phantom_graph=True, seed=1
    )
    pos5 = xgi.weighted_barycenter_spring_layout(H, return_phantom_graph=False, seed=1)
    assert pos4.keys() == pos5.keys()
    assert np.allclose(list(pos4.values()), list(pos5.values()))

    # simplicial complex
    S = xgi.random_flag_complex_d2(10, 0.2)
    pos = xgi.weighted_barycenter_spring_layout(S)
    assert len(pos) == S.num_nodes

    # str nodes
    pos = xgi.weighted_barycenter_spring_layout(hypergraph1)
    assert len(pos) == hypergraph1.num_nodes

    # larger hyperedges
    H = xgi.random_hypergraph(10, [0.2, 0.1])
    pos = xgi.weighted_barycenter_spring_layout(H)
    assert len(pos) == H.num_nodes


def test_pca_transform():
    pos1 = {1: [0, 0], 2: [1, 0]}
    transform1_pos1 = xgi.pca_transform(pos1)
    assert np.allclose(transform1_pos1[1], np.array([0, 0]))
    assert np.allclose(transform1_pos1[2], np.array([-1, 0]))

    transform2_pos1 = xgi.pca_transform(pos1, theta=30)
    assert np.allclose(transform2_pos1[1], np.array([0, 0]))
    assert np.allclose(transform2_pos1[2], np.array([-0.5 * np.sqrt(3), -0.5]))

    transform3_pos1 = xgi.pca_transform(pos1, theta=np.pi / 6, degrees=False)
    assert np.allclose(transform3_pos1[1], np.array([0, 0]))
    assert np.allclose(transform3_pos1[2], np.array([-0.5 * np.sqrt(3), -0.5]))

    pos2 = {1: [-0.5, 0.5], 2: [1, 2], 3: [4, -2]}
    transform1_pos2 = xgi.pca_transform(pos2)
    assert np.allclose(transform1_pos2[1], np.array([-0.67296626, -0.21706316]))
    assert np.allclose(transform1_pos2[2], np.array([-0.02177678, -2.23596193]))
    assert np.allclose(transform1_pos2[3], np.array([4.47192387, -0.04355357]))
