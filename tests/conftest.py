import networkx as nx
import numpy as np
import pandas as pd
import pytest

import xgi


@pytest.fixture
def edgelist1():
    return [{1, 2, 3}, {4}, {5, 6}, {6, 7, 8}]


@pytest.fixture
def edgelist2():
    return [{1, 2}, {3, 4}, {4, 5, 6}]


@pytest.fixture
def edgelist3():
    return [{1, 2, 3}, {3, 4}, {4, 5, 6}]


@pytest.fixture
def edgelist4():
    return [{1, 2, 3}, {2, 3, 4, 5}, {3, 4, 5}]


@pytest.fixture
def edgelist5():
    return [{0, 1, 2, 3}, {4}, {5, 6}, {6, 7, 8}]


@pytest.fixture
def edgelist6():
    return [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}]


@pytest.fixture
def edgelist7():
    return [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}, {4}]


@pytest.fixture
def edgelist8():
    return [
        {0, 1},
        {0, 1, 2},
        {0, 2, 3},
        {0, 1, 2, 3, 4},
        {2, 4, 5},
        {1, 3, 5},
        {0, 3, 4},
        {1, 6},
        {0, 6},
    ]


@pytest.fixture
def edgelist9():
    return [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}]


@pytest.fixture
def edgelist10():
    return [{1}, {2}, {3}]


@pytest.fixture
def dict5():
    return {0: {0, 1, 2, 3}, 1: {4}, 2: {5, 6}, 3: {6, 7, 8}}


@pytest.fixture
def incidence5():
    I = np.zeros((9, 4))
    I[0, 0] = I[1, 0] = I[2, 0] = I[3, 0] = I[4, 1] = 1
    I[5, 2] = I[6, 2] = I[6, 3] = I[7, 3] = I[8, 3] = 1
    return I


@pytest.fixture
def dataframe5():
    data = [
        [0, 0],
        [1, 0],
        [2, 0],
        [3, 0],
        [4, 1],
        [5, 2],
        [6, 2],
        [6, 3],
        [7, 3],
        [8, 3],
    ]
    df = pd.DataFrame(data)
    df.columns = ["col1", "col2"]
    return df


@pytest.fixture
def bipartite_graph1():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4], bipartite=0)
    G.add_nodes_from(["a", "b", "c"], bipartite=1)
    G.add_edges_from([(1, "a"), (1, "b"), (2, "b"), (2, "c"), (3, "c"), (4, "a")])
    return G


@pytest.fixture
def bipartite_graph2():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4], bipartite=0)
    G.add_nodes_from(["a", "b", "c"], bipartite=2)
    G.add_edges_from([(1, "a"), (1, "b"), (2, "b"), (2, "c"), (3, "c"), (4, "a")])
    return G


@pytest.fixture
def bipartite_graph3():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    G.add_nodes_from(["a", "b", "c"])
    G.add_edges_from([(1, "a"), (1, "b"), (2, "b"), (2, "c"), (3, "c"), (4, "a")])
    return G


@pytest.fixture
def bipartite_graph4():
    # this is to test when the bipartite condition is not true
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4], bipartite=0)
    G.add_nodes_from(["a", "b", "c"], bipartite=1)
    G.add_edges_from([(1, "a"), ("a", "b"), (2, "b"), (2, "c"), (3, "c"), (4, "a")])
    return G


@pytest.fixture
def attr0():
    return {"color": "brown", "name": "camel"}


@pytest.fixture
def attr1():
    return {"color": "red", "name": "horse"}


@pytest.fixture
def attr2():
    return {"color": "blue", "name": "pony"}


@pytest.fixture
def attr3():
    return {"color": "yellow", "name": "zebra"}


@pytest.fixture
def attr4():
    return {"color": "red", "name": "orangutan", "age": 20}


@pytest.fixture
def attr5():
    return {"color": "blue", "name": "fish", "age": 2}


@pytest.fixture
def hyperwithdupsandattrs(attr1, attr2, attr3, attr4, attr5):
    edges = [
        ({1, 2}, {"color": "blue"}),
        ({1, 2}, {"color": "red", "weight": 2}),
        ({1, 2}, {"color": "yellow"}),
        ({3, 4, 5}, {"color": "purple"}),
        ({3, 4, 5}, {"color": "purple", "name": "test"}),
    ]
    H = xgi.Hypergraph()
    H.add_edges_from(edges)
    H.add_nodes_from(
        [
            (1, attr1),
            (2, attr2),
            (3, attr3),
            (4, attr4),
            (5, attr5),
        ]
    )
    return H


@pytest.fixture
def hyperwithattrs(edgelist4, attr1, attr2, attr3, attr4, attr5):
    H = xgi.Hypergraph(edgelist4)
    H.add_nodes_from(
        [
            (1, attr1),
            (2, attr2),
            (3, attr3),
            (4, attr4),
            (5, attr5),
        ]
    )
    return H


@pytest.fixture
def hypergraph1():
    H = xgi.Hypergraph()
    H.add_nodes_from(["a", "b", "c"])
    H.add_edges_from({"e1": ["a", "b"], "e2": ["a", "b", "c"], "e3": ["c"]})
    return H


@pytest.fixture
def hypergraph2():
    H = xgi.Hypergraph()
    H.add_nodes_from(["b", "c", 0])
    H.add_edges_from({"e1": [0, "b"], "e2": [0, "c"], "e3": [0, "b", "c"]})
    return H


@pytest.fixture
def simplicialcomplex1():
    S = xgi.SimplicialComplex()
    S.add_nodes_from(["b", "c", 0])
    S.add_simplices_from(
        {"e1": [0, "b"], "e2": [0, "c"], "e3": [0, "b", "c"], "e4": ["b", "c"]}
    )
    return S


@pytest.fixture
def dihypergraph1():
    H = xgi.DiHypergraph()
    H.add_nodes_from(["a", "b", "c", "d"])
    H.add_edges_from(
        {"e1": [{"a", "b"}, {"c"}], "e2": [{"b"}, {"c", "d"}], "e3": [{"b"}, {"c"}]}
    )
    return H


@pytest.fixture
def diedgelist1():
    return [({1, 2, 3}, {4}), ({5, 6}, {6, 7, 8})]


@pytest.fixture
def diedgelist2():
    return [({0, 1}, {2}), ({1, 2}, {4}), ({2, 3, 4}, {4, 5})]


@pytest.fixture
def diedgedict1():
    return {0: ({1, 2, 3}, {4}), 1: ({5, 6}, {6, 7, 8})}


@pytest.fixture
def dihyperwithattrs(diedgelist2, attr0, attr1, attr2, attr3, attr4, attr5):
    H = xgi.DiHypergraph()
    H.add_nodes_from(
        [
            (0, attr0),
            (1, attr1),
            (2, attr2),
            (3, attr3),
            (4, attr4),
            (5, attr5),
        ]
    )
    H.add_edges_from(diedgelist2)
    H.set_edge_attributes({0: attr3, 1: attr4, 2: attr5})
    return H


### Fixtures for simpliciality


@pytest.fixture
def sc1_with_singletons():
    return xgi.Hypergraph([{1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}])


@pytest.fixture
def h_missing_one_singleton():
    return xgi.Hypergraph([{1}, {2}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}])


@pytest.fixture
def h_missing_one_link():
    return xgi.Hypergraph([{1}, {2}, {3}, {1, 3}, {2, 3}, {1, 2, 3}])


@pytest.fixture
def h_links_and_triangles():
    return xgi.Hypergraph([{1, 3}, {2, 3}, {1, 2, 3}])


@pytest.fixture
def h_links_and_triangles2():
    return xgi.Hypergraph([{1, 3}, {2, 3}, {1, 2, 3}, {1, 4}, {2, 3, 4}, {2, 4}])


@pytest.fixture
def h1():
    return xgi.Hypergraph([{1, 2, 3}, {2, 3, 4, 5}, {5, 6, 7}, {5, 6}])
