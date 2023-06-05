import pytest

from xgi import load_bigg_data
from xgi.exception import XGIError


@pytest.mark.webtest
@pytest.mark.slow
def test_load_bigg_data(capfd):
    # test loading the online data
    H1 = load_bigg_data("iAF1260", cache=False)
    assert H1.num_nodes == 1668
    assert H1.num_edges == 2382
    assert H1["name"] == "iAF1260"
    assert H1.nodes["2agpg161_c"] == {'name': '2-Acyl-sn-glycero-3-phosphoglycerol (n-C16:1)'}

    H2 = load_bigg_data("iAF1260", cache=True)
    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges

    load_bigg_data()
    out, _ = capfd.readouterr()
    assert "Available datasets are the following:" in out
    assert "iAF1260" in out

    with pytest.raises(XGIError):
        load_bigg_data("test")