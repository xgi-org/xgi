import pytest
import tempfile
import os
import xgi

dataset_folder = "tests/readwrite/data/"


@pytest.mark.parametrize(
    ("filename", "extra_kwargs"),
    (
        (os.path.join(dataset_folder, "incidence_matrix_spaces.txt"), {}),
        (
            os.path.join(dataset_folder, "incidence_matrix_commas.txt"),
            {"delimiter": ","},
        ),
    ),
)
def test_read_incidence_matrix(filename, extra_kwargs):
    H = xgi.read_incidence_matrix(filename, **extra_kwargs)
    int_edgelist = [[0, 1, 2, 3], [4], [5, 6], [6, 7, 8]]
    assert [H.edges.members(id) for id in H.edges] == int_edgelist


def test_write_incidence_matrix(edgelist5):
    _, fname = tempfile.mkstemp()
    H1 = xgi.Hypergraph(edgelist5)
    xgi.write_incidence_matrix(H1, fname)
    H2 = xgi.read_incidence_matrix(fname)
    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges
    assert [H1.edges.members(id) for id in H1.edges] == [
        H2.edges.members(id) for id in H2.edges
    ]
