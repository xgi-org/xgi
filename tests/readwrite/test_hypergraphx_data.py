import pytest

from xgi.readwrite.hypergraphx_data import (
    _load_hypergraph,
    _parse_remote_dataset_catalog,
)


@pytest.mark.parametrize(
    "payload,expected",
    [
        (
            b'[{"name": "dataset1"}, {"name": "dataset2"}]',
            ["dataset1", "dataset2"],
        ),
        (
            b'{"datasets": [{"name": "dataset1"}, {"name": "dataset2"}]}',
            ["dataset1", "dataset2"],
        ),
        (
            b'window.RELATED_DATASETS = [{"name": "dataset1"}];',
            ["dataset1"],
        ),
    ],
)
def test_parse_remote_dataset_catalog(payload, expected):
    assert _parse_remote_dataset_catalog(payload) == expected


def test_load_hypergraph():
    jsondata = [
        {
            "hypergraph_type": "undirected",
            "hypergraph_metadata": {
                "name": "test graph",
            },
        },
        {
            "type": "node",
            "idx": 1,
            "metadata": {"color": "red"},
        },
        {
            "type": "node",
            "idx": 2,
            "metadata": {"color": "blue"},
        },
        {
            "type": "edge",
            "interaction": [1, 2],
            "metadata": {
                "id": 10,
                "weight": 5,
            },
        },
    ]

    H = _load_hypergraph(jsondata)

    assert H["name"] == "test graph"

    assert H.nodes[1]["color"] == "red"
    assert H.nodes[2]["color"] == "blue"

    assert set(H.edges.members(10)) == {1, 2}
    assert H.edges[10]["weight"] == 5


def test_load_hypergraph_types():
    jsondata = [
        {
            "type": "node",
            "idx": "1",
        },
        {
            "type": "node",
            "idx": "2",
        },
        {
            "type": "edge",
            "interaction": ["1", "2"],
            "metadata": {"id": "100"},
        },
    ]

    H = _load_hypergraph(
        jsondata,
        nodetype=int,
        edgetype=int,
    )

    assert set(H.nodes) == {1, 2}
    assert 100 in H.edges
