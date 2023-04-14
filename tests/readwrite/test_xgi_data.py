import tempfile
import time
from os.path import join

import pytest

from xgi import download_xgi_data, load_xgi_data, read_json
from xgi.exception import XGIError


@pytest.mark.webtest
@pytest.mark.slow
def test_load_xgi_data():
    # test loading the online data
    H1 = load_xgi_data("email-enron", cache=False)
    assert H1.num_nodes == 148
    assert H1.num_edges == 10885
    assert H1["name"] == "email-Enron"
    assert H1.nodes["4"]["name"] == "robert.badeer@enron.com"
    assert H1.edges["0"]["timestamp"] == "2000-01-11T10:29:00"

    H2 = load_xgi_data("email-enron", max_order=2, cache=True)

    assert len(H2.edges.filterby("order", 2, mode="gt")) == 0
    assert len(H1.edges.filterby("order", 2, mode="gt")) == 1283

    H3 = load_xgi_data("email-enron", max_order=2)

    assert H2.edges.members() == H3.edges.members()

    with pytest.raises(XGIError):
        load_xgi_data("test")

    # test the empty argument
    assert load_xgi_data() is None

    with pytest.warns(Warning):
        load_xgi_data("email-enron", read=True)

    dir = tempfile.mkdtemp()
    download_xgi_data("email-enron", dir)
    H4 = load_xgi_data("email-enron", read=True, path=dir)
    assert H1.edges.members() == H4.edges.members()


def test_download_xgi_data():
    dir = tempfile.mkdtemp()
    download_xgi_data("email-enron", dir)
    H = read_json(join(dir, "email-enron.json"))
    H_online = load_xgi_data("email-enron")
    assert H.edges.members() == H_online.edges.members()
