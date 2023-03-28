import tempfile

import pytest

import xgi
from xgi.exception import XGIError

bipartite_edgelist_spaces_string = """0 0
# Comment
1 0
2 0
3 0
4 1
5 2
6 2
6 3
7 3
8 3"""

bipartite_edgelist_commas_string = """0,0
# Comment
1,0
2,0
3,0
4,1
5,2
6,2
6,3
7,3
8,3"""


@pytest.mark.parametrize(
    ("file_string", "extra_kwargs"),
    (
        (bipartite_edgelist_spaces_string, {}),
        (
            bipartite_edgelist_commas_string,
            {"delimiter": ","},
        ),
    ),
)
def test_read_bipartite_edgelist(file_string, extra_kwargs):
    _, filename = tempfile.mkstemp()

    with open(filename, "w") as file:
        file.write(file_string)

    H = xgi.read_bipartite_edgelist(filename, nodetype=int, **extra_kwargs)
    int_edgelist = [{0, 1, 2, 3}, {4}, {5, 6}, {6, 7, 8}]
    assert [H.edges.members(id) for id in H.edges] == int_edgelist
    H = xgi.read_bipartite_edgelist(filename, nodetype=str, **extra_kwargs)
    str_edgelist = [{"0", "1", "2", "3"}, {"4"}, {"5", "6"}, {"6", "7", "8"}]
    assert [H.edges.members(id) for id in H.edges] == str_edgelist


def test_parse_bipartite_edgelist():
    lines = ["0 0", "1 0", "2 0", "3 0", "4 1", "5 2", "6 2", "6 3", "7 3", "8 3"]
    bad_lines1 = ["0", "1 0", "2 0", "3 0", "4 1", "5 2", "6 2", "6 3", "7 3", "8 3"]
    bad_lines2 = [
        "test 0",
        "1 0",
        "2 0",
        "3 0",
        "4 1",
        "5 test",
        "6 test",
        "6 3",
        "7 3",
        "8 3",
    ]
    bad_lines3 = [
        "0 0",
        "1 0",
        "2 0",
        "3 0",
        "4 1",
        "5 test",
        "6 test",
        "6 3",
        "7 3",
        "8 3",
    ]

    H = xgi.parse_bipartite_edgelist(lines, nodetype=int)
    assert list(H.nodes) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert list(H.edges) == ["0", "1", "2", "3"]
    H = xgi.parse_bipartite_edgelist(lines, edgetype=int)
    assert list(H.nodes) == ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    assert list(H.edges) == [0, 1, 2, 3]

    H = xgi.parse_bipartite_edgelist(lines, nodetype=int, edgetype=int)
    assert list(H.nodes) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert list(H.edges) == [0, 1, 2, 3]
    assert [H.edges.members(id) for id in H.edges] == [
        {0, 1, 2, 3},
        {4},
        {5, 6},
        {6, 7, 8},
    ]

    H = xgi.parse_bipartite_edgelist(lines, nodetype=int, edgetype=int, dual=True)
    assert list(H.nodes) == [0, 1, 2, 3]
    assert list(H.edges) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    print([H.edges.members(id) for id in H.edges])
    assert [H.edges.members(id) for id in H.edges] == [
        {0},
        {0},
        {0},
        {0},
        {1},
        {2},
        {2, 3},
        {3},
        {3},
    ]

    # test less than two entries per line
    with pytest.raises(XGIError):
        xgi.parse_bipartite_edgelist(bad_lines1)

    # test failed nodetype conversion
    with pytest.raises(TypeError):
        xgi.parse_bipartite_edgelist(bad_lines2, nodetype=int)

    # test failed edgetype conversion
    with pytest.raises(TypeError):
        xgi.parse_bipartite_edgelist(bad_lines3, edgetype=int)


def test_write_bipartite_edgelist(edgelist1):
    _, filename = tempfile.mkstemp()
    H1 = xgi.Hypergraph(edgelist1)
    xgi.write_bipartite_edgelist(H1, filename)
    H2 = xgi.read_bipartite_edgelist(filename, nodetype=int, edgetype=int)
    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges
    assert [H1.edges.members(id) for id in H1.edges] == [
        H2.edges.members(id) for id in H2.edges
    ]
