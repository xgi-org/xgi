import tempfile

import pytest

import xgi

edgelist_spaces_string = """# comment line
1 2
# comment line
2 3 4
1 4 7 8
2 3"""

edgelist_commas_string = """# comment line
1,2
# comment line
2,3,4
1,4,7,8
2,3"""


@pytest.mark.parametrize(
    ("file_string", "extra_kwargs"),
    (
        (edgelist_spaces_string, {}),
        (edgelist_commas_string, {"delimiter": ","}),
    ),
)
def test_read_edgelist(file_string, extra_kwargs):
    _, filename = tempfile.mkstemp()

    with open(filename, "w") as file:
        file.write(file_string)

    H = xgi.read_edgelist(filename, nodetype=int, **extra_kwargs)
    int_edgelist = [{1, 2}, {2, 3, 4}, {1, 4, 7, 8}, {2, 3}]
    assert [H.edges.members(id) for id in H.edges] == int_edgelist
    H = xgi.read_edgelist(filename, nodetype=str, **extra_kwargs)
    str_edgelist = [{"1", "2"}, {"2", "3", "4"}, {"1", "4", "7", "8"}, {"2", "3"}]
    assert [H.edges.members(id) for id in H.edges] == str_edgelist


def test_parse_edgelist():
    H = xgi.parse_edgelist(["1 2", "2 3 4", "1 4 7 8", "2 3"], nodetype=int)
    assert set(H.nodes) == {1, 2, 3, 4, 7, 8}
    assert set(H.edges) == {0, 1, 2, 3}
    assert [H.edges.members(id) for id in H.edges] == [
        {1, 2},
        {2, 3, 4},
        {1, 4, 7, 8},
        {2, 3},
    ]

    # This will fail because the "test" node ID can't be converted to int
    with pytest.raises(TypeError):
        xgi.parse_edgelist(["test 2", "2 3 4", "test 4 7 8", "2 3"], nodetype=int)


def test_write_edgelist(edgelist1):
    _, filename = tempfile.mkstemp()
    H1 = xgi.Hypergraph(edgelist1)
    xgi.write_edgelist(H1, filename)
    H2 = xgi.read_edgelist(filename, nodetype=int)
    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges
    assert [H1.edges.members(id) for id in H1.edges] == [
        H2.edges.members(id) for id in H2.edges
    ]
