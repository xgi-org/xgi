import pytest

from xgi.utils import convert_labels_to_integers, get_dual, load_xgi_data


@pytest.mark.webtest
@pytest.mark.slow
def test_load_xgi_data():
    H = load_xgi_data("email-enron")
    assert H.num_nodes == 148
    assert H.num_edges == 10885
    assert H["name"] == "email-Enron"
    assert H.nodes["4"]["name"] == "robert.badeer@enron.com"
    assert H.edges["0"]["timestamp"] == "2000-01-11T10:29:00"


def test_get_dual(dict5):
    dual = get_dual(dict5)
    assert dual[0] == [0]
    assert dual[1] == [0]
    assert dual[2] == [0]
    assert dual[3] == [0]
    assert dual[4] == [1]
    assert dual[5] == [2]
    assert dual[6] == [2, 3]
    assert dual[7] == [3]
    assert dual[8] == [3]


def test_convert_labels_to_integers(hypergraph1):
    H = convert_labels_to_integers(hypergraph1)

    assert set(H.nodes) == {0, 1, 2}
    assert set(H.edges) == {0, 1, 2}

    assert H.nodes[0]["label"] == "a"
    assert H.nodes[1]["label"] == "b"
    assert H.nodes[2]["label"] == "c"

    assert H.edges[0]["label"] == "e1"
    assert H.edges[1]["label"] == "e2"
    assert H.edges[2]["label"] == "e3"

    assert H.edges.members(0) == [0, 1]
    assert H.edges.members(1) == [0, 1, 2]
    assert H.edges.members(2) == [2]

    assert H.nodes.memberships(0) == [0, 1]
    assert H.nodes.memberships(1) == [0, 1]
    assert H.nodes.memberships(2) == [1, 2]
