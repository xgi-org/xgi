import pytest

from xgi import load_xgi_data

@pytest.mark.webtest
@pytest.mark.slow
def test_load_xgi_data():
    H = load_xgi_data("email-enron")
    assert H.num_nodes == 148
    assert H.num_edges == 10885
    assert H["name"] == "email-Enron"
    assert H.nodes["4"]["name"] == "robert.badeer@enron.com"
    assert H.edges["0"]["timestamp"] == "2000-01-11T10:29:00"