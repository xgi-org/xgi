import numpy as np

import xgi


def test_single_source_shortest_path_length(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    dists1 = xgi.single_source_shortest_path_length(H, 1)
    dists4 = xgi.single_source_shortest_path_length(H, 4)
    dists5 = xgi.single_source_shortest_path_length(H, 5)
    assert dists1[2] == 1
    assert dists1[4] == np.inf  # unconnected nodes
    assert dists5[8] == 2

    return


def test_shortest_path_length(edgelist1):
    H = xgi.Hypergraph(edgelist1)
    for source, dists in xgi.shortest_path_length(H):
        # check symetry between 5 and 8
        if source == 5:
            assert dists[8] == 2
        elif source == 8:
            assert dists[5] == 2
        # check unconnected nodes
        elif source == 4:
            assert dists[1] == np.inf
            assert dists[4] == 0
    return
