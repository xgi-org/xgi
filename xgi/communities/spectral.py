import numpy as np
from scipy.sparse.linalg import eigsh

from ..core import Hypergraph
from ..linalg.laplacian_matrix import normalized_hypergraph_laplacian

from ..exception import XGIError

__all__ = [
    "spectral_clustering",
]



def spectral_clustering(H, k=None):
    """Cluster into k-many groups using spectral techniques.

    Compute a spectral clustering according to the heuristic suggested in [1].

    Parameters
    ----------
    H : Hypergraph
        Hypergraph
    k : int, optional
        Number of clusters to find. If unspecified, computes spectral gap.

    Returns
    -------
    dict
        A dictionary mapping node ids to their clusters. Clusters begin at 0.

    Raises
    ------
    XGIError
        If more groups are specified than nodes in the hypergraph.


    References
    ----------
    .. [1] Zhou, D., Huang, J., & Schölkopf, B. (2006).
        Learning with Hypergraphs: Clustering, Classification, and Embedding
        Advances in Neural Information Processing Systems.

    """
    if k > H.num_nodes:
        raise XGIError(
            "The number of desired clusters cannot exceed the number of nodes!"
        )

    # Compute normalize Laplacian and its spectra
    L, rowdict = normalized_hypergraph_laplacian(H, index=True)
    evals, eigs = eigsh(L, k=k, which="SA")

    # Form metric space representation
    X = np.array(eigs)

    # Apply k-means clustering
    _clusters = _kmeans(X, k)

    # Remap to node ids
    clusters = {rowdict[id]: cluster for id, cluster in _clusters.items()}

    return clusters


def _kmeans(X, k, max_iter=1_000, seed=None):
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

    centroids = width * rng.random((k, X.shape[1]))

    # Instantiate random clusters
    previous_clusters = {node: rng.integers(0, k) for node in range(X.shape[0])}

    # Iterate main kmeans computation
    while (num_cluster_changes > 0) and (num_iterations < max_iter):
        # Find nearest centroid to each point
        clusters = dict()
        for node, vector in enumerate(X):
            distances = list(
                map(lambda centroid: np.linalg.norm(vector - centroid), centroids)
            )
            closest_centroid = np.argmin(distances)
            clusters[node] = closest_centroid

        # Update convergence condition
        cluster_changes = {
            node: clusters[node] != previous_clusters[node]
            for node in range(X.shape[0])
        }
        num_cluster_changes = len(
            list(filter(lambda diff: diff, cluster_changes.values()))
        )
        num_iterations += 1

    return clusters
