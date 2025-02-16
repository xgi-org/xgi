import numpy as np

import pytest

import xgi
from xgi.exception import XGIError


class TestKMeans:
    def test_k_is_1(self):
        X = np.random.random((3, 3))
        clusters = xgi.communities.spectral._kmeans(X, 1)

        assert len(clusters) == 3
        assert np.all(map(lambda v: v == 1, clusters.values()))
        assert np.all(map(lambda v: isinstance(v, int), clusters.values()))

    def test_perfectly_separable_low_dimensions(self):
        X = np.zeros((10, 10))
        X[:5, :] = np.random.random((5, 10))
        X[5:10, :] = 37 + np.random.random((5, 10))

        clusters = xgi.communities.spectral._kmeans(X, 2, seed=2)
        assert len(clusters) == 10

        c1 = list(filter(lambda node: clusters[node] == 0, clusters.keys()))
        c2 = list(filter(lambda node: clusters[node] == 1, clusters.keys()))
        assert len(c1) == 5
        assert len(c2) == 5
        assert (set(c1) == {0, 1, 2, 3, 4} and set(c2) == {5, 6, 7, 8, 9}) or (
            set(c2) == {0, 1, 2, 3, 4} and set(c1) == {5, 6, 7, 8, 9}
        )

    def test_perfectly_separable_high_dimensions(self):
        X = np.zeros((10, 100))
        X[:5, :] = np.random.random((5, 100))
        X[5:10, :] = 37 + np.random.random((5, 100))

        clusters = xgi.communities.spectral._kmeans(X, 2, seed=2)
        assert len(clusters) == 10

        c1 = list(filter(lambda node: clusters[node] == 0, clusters.keys()))
        c2 = list(filter(lambda node: clusters[node] == 1, clusters.keys()))
        assert len(c1) == 5
        assert len(c2) == 5
        assert (set(c1) == {0, 1, 2, 3, 4} and set(c2) == {5, 6, 7, 8, 9}) or (
            set(c2) == {0, 1, 2, 3, 4} and set(c1) == {5, 6, 7, 8, 9}
        )


class TestSpectralClustering:
    def test_errors_num_clusters(self):
        H = xgi.complete_hypergraph(5, order=2)

        with pytest.raises(XGIError):
            xgi.spectral_clustering(H, 6)

    def test_spectral(self):
        pass
