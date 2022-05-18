import pytest

import xgi
from xgi.exception import XGIError


def test_filterby_wrong_stat():
    H = xgi.Hypergraph()
    with pytest.raises(AttributeError):
        H.nodes.filterby("__I_DO_NOT_EXIST__", None)
