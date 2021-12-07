import pytest
import xgi
import numpy as np

def test_incidence_matrix():
    edgelist1 = [[1,2,3],[4],[5,6],[6,7,8]]
    edgelist2 = [[1,2,3],[3,4],[4,5,6]]
    edgelist3 = [[1,2,3],[2,3,4,5],[3,4,5]]
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)

    I1 = xgi.incidence_matrix(H1, index=True)
    I1[0, 0] = I1[1, 0] = I1[2, 0] = I1[3, 1] = I1[4, 2] = I1[5, 2] = I1[5, 3] = I1[6, 3] = I1[7, 3] = 1

    assert xgi.incidence_matrix(H1, sparse=False) == I1