import pytest

import xgi
from xgi.exception import XGIError
from xgi.utils import load_xgi_data


def test_load_xgi_data():
    H = load_xgi_data("email-enron")
    assert H.num_nodes == 148
    assert H.num_edges == 10885
    assert H["name"] == "email-Enron"
    assert H.nodes["4"]["name"] == "robert.badeer@enron.com"
    assert H.edges["0"]["timestamp"] == "2000-01-11T10:29:00"


def test_get_dual(dict5):
    dual = xgi.utils.get_dual(dict5)
    assert dual[0] == [0]
    assert dual[1] == [0]
    assert dual[2] == [0]
    assert dual[3] == [0]
    assert dual[4] == [1]
    assert dual[5] == [2]
    assert dual[6] == [2, 3]
    assert dual[7] == [3]
    assert dual[8] == [3]


def test_xgi_counter():
    count = xgi.XGICounter()
    assert count() == 0
    assert count() == 1