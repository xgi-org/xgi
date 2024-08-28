import platform
import sys

import pytest

from xgi import load_bigg_data
from xgi.exception import XGIError


@pytest.mark.skipif(
    sys.version_info != (3, 12) and not platform.system() == "Linux",
    reason="Only need one test!",
)
@pytest.mark.webtest
@pytest.mark.slow
def test_load_bigg_data(capfd):
    # test loading the online data
    H1 = load_bigg_data("iAF1260", cache=False)
    assert H1.num_nodes == 1668
    assert H1.num_edges == 2953
    assert H1["name"] == "iAF1260"
    assert H1["organism"] == "Escherichia coli str. K-12 substr. MG1655"
    assert H1.nodes["2agpg161_c"] == {
        "name": "2-Acyl-sn-glycero-3-phosphoglycerol (n-C16:1)"
    }

    H2 = load_bigg_data("iAF1260", cache=True)
    assert H1.nodes == H2.nodes
    assert H1.edges == H2.edges

    load_bigg_data()
    out, _ = capfd.readouterr()
    assert "Available datasets are the following:" in out
    assert "iAF1260" in out

    with pytest.raises(XGIError):
        load_bigg_data("test")


@pytest.mark.skipif(
    sys.version_info != (3, 12) and not platform.system() == "Linux",
    reason="Only need one test!",
)
@pytest.mark.webtest
@pytest.mark.slow
def test_411():
    with pytest.warns(Warning):
        H = load_bigg_data("iCN718")
    assert H["name"] == "iCN718"
    assert H.num_nodes == 888
    assert H.num_edges == 1436


@pytest.mark.skipif(
    sys.version_info != (3, 12) and not platform.system() == "Linux",
    reason="Only need one test!",
)
@pytest.mark.webtest
@pytest.mark.slow
def test_458():
    H = load_bigg_data("e_coli_core")
    assert H.edges.dimembers("FORt") == ({"for_c"}, {"for_e"})
    assert H.edges.dimembers("PFK") == ({"atp_c", "f6p_c"}, {"adp_c", "fdp_c", "h_c"})

    assert H.edges.dimembers("CO2t") == ({"co2_e"}, {"co2_c"})
    assert H.edges.dimembers("CO2t_reverse") == ({"co2_c"}, {"co2_e"})
