import numpy as np
import pytest

import xgi
from xgi.exception import XGIError


class TestKMeans:
    def test_k_is_1(self):
        X = np.random.random((3, 3))
        clusters = xgi.communities.spectral._kmeans(X, 1, seed=37)

        assert len(clusters) == 3
        assert np.all(map(lambda v: v == 1, clusters.values()))
        assert np.all(map(lambda v: isinstance(v, int), clusters.values()))

    def test_perfectly_separable_low_dimensions(self):
        X = np.zeros((10, 10))
        X[:5, :] = np.random.random((5, 10))
        X[5:10, :] = 37 + np.random.random((5, 10))

        clusters = xgi.communities.spectral._kmeans(X, 2, seed=37)
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

        clusters = xgi.communities.spectral._kmeans(X, 2, seed=37)
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

    def test_perfectly_separable_low_dimensions(self):
        H = xgi.Hypergraph(
            [
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [1, 3],
                [2, 4],
                [1, 5],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [6, 8],
                [7, 9],
                [6, 10],
            ]
        )

        clusters = xgi.spectral_clustering(H, 2, seed=37)
        assert len(clusters) == 10

        c1 = list(filter(lambda node: clusters[node] == 0, clusters.keys()))
        c2 = list(filter(lambda node: clusters[node] == 1, clusters.keys()))
        assert len(c1) == 5
        assert len(c2) == 5
        assert (set(c1) == {1, 2, 3, 4, 5} and set(c2) == {6, 7, 8, 9, 10}) or (
            set(c2) == {1, 2, 3, 4, 5} and set(c1) == {6, 7, 8, 9, 10}
        )

    def test_strongly_separable_low_dimensions(self):
        H = xgi.Hypergraph(
            [
                [1, 2, 3],
                [4, 5],
                [1, 3],
                [2, 4],
                [1, 5],
                [4, 9],
                [6, 7, 8],
                [7, 8],
                [8, 9],
                [9, 10],
                [6, 8],
                [7, 9],
                [6, 10],
            ]
        )

        clusters = xgi.spectral_clustering(H, 2, seed=37)
        assert len(clusters) == 10

        # Some nodes obviously in same cluster
        assert clusters[1] == clusters[2]
        assert clusters[2] == clusters[3]

        # Some nodes obviously not
        assert clusters[1] != clusters[8]
        assert clusters[2] != clusters[7]

    def test_strongly_separable_sbm(self):
        p = np.array([[0.3, 0.01], [0.01, 0.3]])
        H = xgi.uniform_HSBM(100, 2, p, [50, 50])

        clusters = xgi.spectral_clustering(H, 2, seed=37)

        group_a = []
        group_b = []
        for node, group in clusters.items():
            if group == 0:
                group_a.append(node)
            else:
                group_b.append(node)

        assert len(group_a) == len(group_b)
