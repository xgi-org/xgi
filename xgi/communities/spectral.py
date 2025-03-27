"""Community detection via clustering of Laplacian eigenvectors."""

import numpy as np
from scipy.sparse.linalg import eigsh

from ..exception import XGIError
from ..linalg.laplacian_matrix import normalized_hypergraph_laplacian

__all__ = [
    "spectral_clustering",
]


def spectral_clustering(H, k=2, max_iter=1_000, seed=None):
    """Computes a spectral clustering in :math:`k` partitions of the input
    hypergraph according to the heuristic presented in [1].

    This is done by computing the normalized Laplacian of the input hypergraph
    and then applying :math:`k`-means clustering on the hypergraph vertices
    represented in the :math:`k`-dimensional Euclidian space generated
    by the eigenvectors corresponding to the :math:`k` smallest eigenvalues of the
    normalized Laplacian.

    Parameters
    ----------
    H : Hypergraph
        Hypergraph
    k : int, optional
        Number of clusters to find, default 2.
    max_iter : int, optional.
        Maximum number of cluster updates to compute, default 1,000.
    seed : int, optional
        Seed used to initialize clusters, optional.

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
    _clusters = _kmeans(X, k, max_iter, seed)

    # Remap to node ids
    clusters = {rowdict[id]: cluster for id, cluster in _clusters.items()}

    return clusters


def _kmeans(X, k, max_iter=1_000, seed=None):
    """Simple k-means clustering of vectors X.

    Uses Forgy method for selecting initial centroids.

    Parameters
    ----------
    X : (n, k) array
        Vectors to cluster.
    k : int
        Number of clusters to find.
    max_iter : int, optional.
        Maximum number of cluster updates to compute, default 10,000.
    seed : int, optional
        Seed used to initialize clusters, optional.

    Returns
    -------
    dict
        A dictionary mapping node ids to their clusters. Clusters begin at 0.
    """
    rng = np.random.default_rng(seed=seed)

    # Handle edge cases
    if k == 1:
        return {node_idx: 1 for node_idx in range(X.shape[0])}

    # Initialize stopping criterion
    num_cluster_changes = np.inf
    num_iterations = 0

    # Instantiate random centers
    centroids = rng.choice(X, size=k, replace=False)

    # Instantiate random clusters
    previous_clusters = {node: rng.integers(0, k) for node in range(X.shape[0])}

    # Iterate main kmeans computation
    while (num_cluster_changes > 0) and (num_iterations < max_iter):
        # Find nearest centroid to each point
        clusters = dict()
        vectors = {cluster: [] for cluster in range(k)}
        for node, vector in enumerate(X):
            distances = [np.linalg.norm(vector - centroid) for centroid in centroids]
            closest_centroid = np.argmin(distances)
            clusters[node] = closest_centroid
            vectors[closest_centroid].append(vector)

        # Update centroids
        centroids = [np.mean(vectors[cluster_id]) for cluster_id in vectors]

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
