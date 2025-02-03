import xgi

rounds = 10
iterations = 1


def test_erdos_renyi(benchmark):

    def erdos_renyi():
        xgi.random_hypergraph(100, [0.1, 0.001])

    benchmark.pedantic(erdos_renyi, rounds=rounds, iterations=iterations)


def test_fast_erdos_renyi(benchmark):

    def fast_erdos_renyi():
        xgi.fast_random_hypergraph(100, [0.1, 0.001])

    benchmark.pedantic(fast_erdos_renyi, rounds=rounds, iterations=iterations)
