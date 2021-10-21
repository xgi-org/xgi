import hypergraph as hg
from hypergraph.exception import HypergraphError
import random
import warnings

def uniform_hypergraph_configuration_model(k, m):
    # Making sure we have the right number of stubs
    if (sum(k) % m) != 0:
        warnings.warn("This degree sequence is not realizable. Increasing the degree of random nodes so that it is.")
        remainder = sum(k) % m
        for i in range(int(round(m - remainder))):
            j = random.randrange(len(k))
            k[j] = k[j] + 1

    stubs = []
    edgelist = []
    # Creating the list to index through
    for index in range(len(k)):
        stubs.extend([index]*int(k[index]))

    while len(stubs) != 0:
        u = random.sample(range(len(stubs)), m)
        edge = []
        for index in u:
            edge.append(stubs[index])
        edgelist.append(edge)

        for index in sorted(u, reverse=True):
            del stubs[index]

    return hg.Hypergraph(edgelist)