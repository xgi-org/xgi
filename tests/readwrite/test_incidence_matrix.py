import tempfile

import pytest

import xgi

dataset_folder = "tests/readwrite/data/"


incidence_matrix_spaces_string = """1 0 0 0
1 0 0 0
1 0 0 0
1 0 0 0
# Comment
0 1 0 0
0 0 1 0
0 0 1 1
0 0 0 1
0 0 0 1"""

incidence_matrix_commas_string = """1,0,0,0
1,0,0,0
1,0,0,0
# Comment
1,0,0,0
0,1,0,0
0,0,1,0
0,0,1,1
0,0,0,1
0,0,0,1"""


@pytest.mark.parametrize(
    ("file_string", "extra_kwargs"),
    (
        (incidence_matrix_spaces_string, {}),
        (incidence_matrix_commas_string, {"delimiter": ","}),
    ),
)
def test_read_incidence_matrix(file_string, extra_kwargs):
    _, filename = tempfile.mkstemp()

    with open(filename, "w") as file:
        file.write(file_string)

    H = xgi.read_incidence_matrix(filename, **extra_kwargs)
    int_edgelist = [{0, 1, 2, 3}, {4}, {5, 6}, {6, 7, 8}]
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
