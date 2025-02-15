import numpy as np
from scipy.sparse.linalg import eigsh

from ..core import Hypergraph
from ..linalg.laplacian_matrix import normalized_hypergraph_laplacian

from ..exception import XGIError

__all__ = [
    "spectral_clustering",
]


def spectral_clustering(H, k=None):
    if k is None:
        raise NotImplementedError(
            "Choosing a number of clusters organically is currently unsupported. Please specify an integer value for paramater 'k'!"
        )
    else:
        if k > H.num_nodes:
            raise XGIError(
                "The number of desired clusters cannot exceed the number of nodes!"
            )

    # Compute normalize Laplacian and its spectra
    L, rowdict = normalized_hypergraph_laplacian(H, index=True)
    evals, eigs = eigsh(L, k=k, which="SA")

    # Form metric space representation
    X = np.array(eigs).T  # array instantiates iterable as rows by default

    # Apply k-means clustering
    clusters = _kmeans(X, k)
    pass


def _kmeans(X, k):
    if k == 1:
        return {node_idx: 1 for node_idx in range(X.shape[0])}
    pass
