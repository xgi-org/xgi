import pytest
import tempfile
import os
import xgi

dataset_folder = "tests/readwrite/data/"

@pytest.mark.parametrize(
    ("filename", "extra_kwargs"),
    (
        (os.path.join(dataset_folder, "bipartite_edgelist_spaces.txt"), {}),
        (os.path.join(dataset_folder, "bipartite_edgelist_commas.txt"), {"delimiter": ","}),
    ),
)
def test_read_bipartite_edgelist(filename, extra_kwargs):
    H = xgi.read_bipartite_edgelist(filename, nodetype=int, **extra_kwargs)
    int_edgelist = [[0, 1, 2, 3], [4], [5, 6], [6, 7, 8]]
    assert [H.edges.members(id) for id in H.edges] == int_edgelist
    H = xgi.read_bipartite_edgelist(filename, nodetype=str, **extra_kwargs)
    str_edgelist = [["0", "1", "2", "3"], ["4"], ["5", "6"], ["6", "7", "8"]]
    assert [H.edges.members(id) for id in H.edges] == str_edgelist


def test_parse_bipartite_edgelist():
    lines = ["0 0", "1 0", "2 0", "3 0", "4 1", "5 2", "6 2", "6 3", "7 3", "8 3"]
    H = xgi.parse_bipartite_edgelist(lines, nodetype=int)
    assert list(H.nodes) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert list(H.edges) == ["0", "1", "2", "3"]
    H = xgi.parse_bipartite_edgelist(lines, edgetype=int)
    assert list(H.nodes) == ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    assert list(H.edges) == [0, 1, 2, 3]

    H = xgi.parse_bipartite_edgelist(lines, nodetype=int, edgetype=int)
    assert list(H.nodes) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert list(H.edges) == [0, 1, 2, 3]
    assert [H.edges.members(id) for id in H.edges] == [[0, 1, 2, 3], [4], [5, 6], [6, 7, 8]]

    H = xgi.parse_bipartite_edgelist(lines, nodetype=int, edgetype=int, dual=True)
    assert list(H.nodes) == [0, 1, 2, 3]
    assert list(H.edges) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    print([H.edges.members(id) for id in H.edges])
    assert [H.edges.members(id) for id in H.edges] == [[0], [0], [0], [0], [1], [2], [2, 3], [3], [3]]


def test_write_bipartite_edgelist(edgelist1):
    _, fname = tempfile.mkstemp()
    H1 = xgi.Hypergraph(edgelist1)
    xgi.write_bipartite_edgelist(H1, fname)
    H2 = xgi.read_bipartite_edgelist(fname, nodetype=int, edgetype=int)
    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges
    assert [H1.edges.members(id) for id in H1.edges] == [H2.edges.members(id) for id in H2.edges]