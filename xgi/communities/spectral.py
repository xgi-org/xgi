import numpy as np
from scipy.sparse.linalg import eigsh

from ..core import Hypergraph
from ..linalg.laplacian_matrix import normalized_hypergraph_laplacian

from ..exception import XGIError

__all__ = [
    "spectral_clustering",
]

MAX_ITERATIONS = 10_000


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


def _kmeans(X, k, seed=37):
    rng = np.random.default_rng(seed=seed)

    # Handle edge cases
    if k == 1:
        return {node_idx: 1 for node_idx in range(X.shape[0])}

    # Initialize stopping criterion
    num_cluster_changes = np.inf
    num_iterations = 0

    # Instantiate random centers
    bounds_inf = X.min(axis=0)
    bounds_sup = X.max(axis=0)
    width = bounds_sup - bounds_inf

    # NOTE: Want Hadamard product here
    centroids = width * rng.random((k, X.shape[1]))

    # Instantiate random clusters
    previous_clusters = {node: rng.integers(0, k) for node in range(X.shape[0])}

    # Iterate main kmeans computation
    while (num_cluster_changes > 0) and (num_iterations < MAX_ITERATIONS):
        # Find nearest centroid to each point
        next_clusters = dict()
        for node, vector in enumerate(X):
            distances = list(
                map(lambda centroid: np.linalg.norm(vector - centroid), centroids)
            )
            closest_centroid = np.argmin(distances)
            next_clusters[node] = closest_centroid

        # Update convergence condition
        cluster_changes = {
            node: next_clusters[node] != previous_clusters[node]
            for node in range(X.shape[0])
        }
        num_cluster_changes = len(
            list(filter(lambda diff: diff, cluster_changes.values()))
        )
        num_iterations += 1

    return next_clusters
