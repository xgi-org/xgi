import pytest
import tempfile
import os
import xgi

dataset_folder = "tests/readwrite/data/"

@pytest.mark.parametrize(
    ("filename", "extra_kwargs"),
    (
        (os.path.join(dataset_folder, "edges_spaces.txt"), {}),
        (os.path.join(dataset_folder, "edges_commas.txt"), {"delimiter": ","}),
    ),
)
def test_read_edgelist(filename, extra_kwargs):
    H = xgi.read_edgelist(filename, nodetype=int, **extra_kwargs)
    int_edgelist = [[1, 2], [2, 3, 4], [1, 4, 7, 8], [2, 3]]
    assert [H.edges.members(id) for id in H.edges] == int_edgelist
    H = xgi.read_edgelist(filename, nodetype=str, **extra_kwargs)
    str_edgelist = [["1", "2"], ["2", "3", "4"], ["1", "4", "7", "8"], ["2", "3"]]
    assert [H.edges.members(id) for id in H.edges] == str_edgelist


def test_parse_edgelist():
    H = xgi.parse_edgelist(["1 2", "2 3 4", "1 4 7 8", "2 3"], nodetype=int)
    assert list(H.nodes) == [1, 2, 3, 4, 7, 8]
    assert list(H.edges) == [0, 1, 2, 3]
    assert [H.edges.members(id) for id in H.edges] == [[1, 2], [2, 3, 4], [1, 4, 7, 8], [2, 3]]


def test_write_edgelist(edgelist1):
    _, fname = tempfile.mkstemp()
    H1 = xgi.Hypergraph(edgelist1)
    xgi.write_edgelist(H1, fname)
    H2 = xgi.read_edgelist(fname, nodetype=int)
    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges
    assert [H1.edges.members(id) for id in H1.edges] == [H2.edges.members(id) for id in H2.edges]