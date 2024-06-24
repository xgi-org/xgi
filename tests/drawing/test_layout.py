import numpy as np

import xgi


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


def test_pairwise_spring_layout_hypergraph():
    H = xgi.random_hypergraph(10, [0.2], seed=1)

    pos1 = xgi.pairwise_spring_layout(H, seed=1)
    pos2 = xgi.pairwise_spring_layout(H, seed=2)
    pos3 = xgi.pairwise_spring_layout(H, seed=2)
    assert pos1.keys() == pos2.keys() == pos3.keys()
    assert not np.allclose(list(pos1.values()), list(pos2.values()))
    assert np.allclose(list(pos2.values()), list(pos3.values()))
    assert len(pos1) == H.num_nodes

    # simplicial complex


def test_pairwise_spring_layout_simplicial_complex():
    S = xgi.random_flag_complex_d2(10, 0.2, seed=1)

    pos1 = xgi.pairwise_spring_layout(S, seed=1)
    pos2 = xgi.pairwise_spring_layout(S, seed=2)
    pos3 = xgi.pairwise_spring_layout(S, seed=2)
    assert pos1.keys() == pos2.keys() == pos3.keys()
    assert not np.allclose(list(pos1.values()), list(pos2.values()))
    assert np.allclose(list(pos2.values()), list(pos3.values()))
    assert len(pos1) == S.num_nodes


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


def test_circular_layout():
    # hypergraph
    H = xgi.random_hypergraph(10, [0.2], seed=1)
    pos = xgi.circular_layout(H)
    assert len(pos) == H.num_nodes

    # empty hypergraph
    H = xgi.empty_hypergraph()
    pos = xgi.circular_layout(H)
    assert pos == {}

    # single node hypergraph
    H = xgi.trivial_hypergraph()
    pos = xgi.circular_layout(H, center=[1, 1])
    assert pos[0] == [1, 1]

    # test center
    H = xgi.random_hypergraph(10, [0.2], seed=1)
    center = [2.0, 1.0]
    pos = xgi.circular_layout(H, center=center)
    for i in pos.keys():
        assert (
            np.round(
                np.sqrt((pos[i][0] - center[0]) ** 2 + (pos[i][1] - center[1]) ** 2), 1
            )
            == 1.0
        )

    # test radius
    H = xgi.random_hypergraph(10, [0.2], seed=1)
    pos = xgi.circular_layout(H, radius=2.0)
    for i in pos.keys():
        assert np.round(np.sqrt(pos[i][0] ** 2 + pos[i][1] ** 2), 1) == 2.0

    # simplicial complex
    S = xgi.random_flag_complex_d2(10, 0.2)
    pos = xgi.circular_layout(S)
    assert len(pos) == S.num_nodes


def test_spiral_layout():
    # hypergraph
    H = xgi.random_hypergraph(10, [0.2], seed=1)
    pos1 = xgi.spiral_layout(H)
    pos2 = xgi.spiral_layout(H, equidistant=True)
    assert pos1.keys() == pos2.keys()
    assert len(pos1) == H.num_nodes
    assert len(pos2) == H.num_nodes

    # empty hypergraph
    H = xgi.empty_hypergraph()
    pos = xgi.spiral_layout(H)
    assert pos == {}

    # single node hypergraph
    H = xgi.trivial_hypergraph()
    pos = xgi.spiral_layout(H, center=[1, 1])
    assert pos[0] == [1, 1]

    # simplicial complex
    S = xgi.random_flag_complex_d2(10, 0.2)
    pos = xgi.spiral_layout(S)
    assert len(pos) == S.num_nodes


def test_barycenter_kamada_kawai_layout(hypergraph1):
    H = xgi.random_hypergraph(10, [0.2], seed=1)

    pos1 = xgi.barycenter_kamada_kawai_layout(H)
    assert len(pos1) == H.num_nodes

    # phantom
    pos2, G = xgi.barycenter_kamada_kawai_layout(H, return_phantom_graph=True)
    pos3 = xgi.barycenter_kamada_kawai_layout(H, return_phantom_graph=False)
    assert pos3.keys() == pos3.keys()
    assert np.allclose(list(pos3.values()), list(pos3.values()))

    # simplicial complex
    S = xgi.random_flag_complex_d2(10, 0.2)
    pos = xgi.barycenter_kamada_kawai_layout(H)
    assert len(pos) == S.num_nodes


def test_bipartite_spring_layout(edgelist1):
    H = xgi.Hypergraph(edgelist1)

    pos1 = xgi.bipartite_spring_layout(H, seed=0)
    assert len(pos1) == 2
    assert len(pos1[0]) == H.num_nodes
    assert len(pos1[1]) == H.num_edges

    pos2 = xgi.bipartite_spring_layout(H, seed=0)

    for n in pos1[0]:
        assert np.allclose(pos1[0][n], pos2[0][n])

    for e in pos1[1]:
        assert np.allclose(pos1[1][e], pos2[1][e])


def test_edge_positions_from_barycenters(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    pos = np.random.random([H.num_nodes, 2])

    node_pos = {n: pos[i] for i, n in enumerate(H.nodes)}
    edge_pos = xgi.edge_positions_from_barycenters(H, node_pos)

    assert len(edge_pos) == H.num_edges
    for id, e in H.edges.members(dtype=dict).items():
        mean_pos = np.mean([node_pos[n] for n in e], axis=0)
        assert np.allclose(edge_pos[id], mean_pos)
