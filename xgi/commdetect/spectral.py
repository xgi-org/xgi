import numpy as np
from scipy.sparse.linalg import eigsh

from ..core import Hypergraph
from ..linalg.laplacian_matrix import normalized_hypergraph_laplacian

from ..exception import XGIError


def _kmeans(X, k):
    if k == 1:
        return np.ones(X.shape[0], dtype=int)
    pass
