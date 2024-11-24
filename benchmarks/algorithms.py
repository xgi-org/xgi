import xgi

rounds = 10
fname = "benchmarks/email-enron.json"


def test_connected(benchmark):
    def setup():
        H = xgi.read_hif(fname)
        return (H,), {}

    benchmark.pedantic(xgi.is_connected, setup=setup, rounds=rounds)


def test_clustering_coefficient(benchmark):
    def setup():
        H = xgi.read_hif(fname)
        return (H,), {}

    benchmark.pedantic(xgi.clustering_coefficient, setup=setup, rounds=rounds)
