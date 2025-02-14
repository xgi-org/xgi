import numpy as np

import pytest

import xgi
from xgi.exception import XGIError


class TestKMeans:
    def test_kmeans_k_is_1(self):
        X = np.random.random((3, 3))
        clusters = xgi.commdetect.spectral._kmeans(X, 1)

        assert len(clusters) == 3
        assert np.all(clusters == 1)
        assert clusters.dtype == int


class TestSpectralClustering:
    def test_errors_num_clusters(self):
        H = xgi.complete_hypergraph(5, order=2)

        with pytest.raises(XGIError):
            xgi.spectral_clustering(H, 6)

    def test_spectral(self):
        pass
