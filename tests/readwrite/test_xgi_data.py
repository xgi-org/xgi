import platform
import sys
import tempfile
from os.path import join

import pytest

from xgi import download_xgi_data, load_xgi_data, read_json
from xgi.exception import XGIError


@pytest.mark.skipif(
    sys.version_info != (3, 12) and not platform.system() == "Linux",
    reason="only need one test",
)
@pytest.mark.webtest
@pytest.mark.slow
def test_load_xgi_data(capfd):
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

    load_xgi_data()
    out, _ = capfd.readouterr()
    assert "Available datasets are the following:" in out
    assert "email-enron" in out
    assert "congress-bills" in out

    # test collection
    collection = load_xgi_data("hyperbard")
    assert len(collection) == 37
    assert isinstance(collection, dict)
    assert collection["as-you-like-it"].num_nodes == 30
    assert collection["as-you-like-it"].num_edges == 80


@pytest.mark.skipif(
    sys.version_info != (3, 12) and not platform.system() == "Linux",
    reason="only need one test",
)
@pytest.mark.webtest
@pytest.mark.slow
def test_download_xgi_data():
    dir = tempfile.mkdtemp()
    download_xgi_data("email-enron", dir)
    H = read_json(join(dir, "email-enron.json"))
    H_online = load_xgi_data("email-enron")
    assert H.edges.members() == H_online.edges.members()

    dir = tempfile.mkdtemp()
    download_xgi_data("hyperbard", dir)
    collection = read_json(join(dir, "collection_information.json"))

    print(collection)
    assert len(collection) == 37
    assert isinstance(collection, dict)
    assert collection["as-you-like-it"].num_nodes == 30
    assert collection["as-you-like-it"].num_edges == 80
