import gzip
import json
import platform
import sys
from unittest.mock import patch

import pytest

from xgi import load_ahorn_data
from xgi.exception import XGIError
from xgi.readwrite.ahorn_data import (
    _from_ahorn_text,
    _get_dataset_data,
    _get_dataset_url,
    _request_from_ahorn_data,
)


def _mock_catalog(datasets):
    """Build the AHORN catalog shape the code expects."""
    return {"datasets": datasets}


def _hif_payload(hypergraph_dict):
    """Encode a HIF dict as the gzipped bytes AHORN serves."""
    return gzip.compress(json.dumps(hypergraph_dict).encode("utf-8"))


@pytest.mark.skipif(
    sys.version_info != (3, 14) and not platform.system() == "Linux",
    reason="only need one test",
)
@pytest.mark.webtest
@pytest.mark.slow
def test_load_ahorn_data(capfd):
    # test loading an AHORN dataset
    H1 = load_ahorn_data("email-enron", cache=False)

    assert H1.num_nodes > 0
    assert H1.num_edges > 0

    # test max_order and caching path
    H2 = load_ahorn_data("email-enron", cache=True, max_order=2)

    assert len(H2.edges.filterby("order", 2, mode="gt")) == 0

    H3 = load_ahorn_data("email-enron", max_order=2)

    assert H2.edges.members() == H3.edges.members()

    # invalid dataset
    with pytest.raises(XGIError):
        load_ahorn_data("this-dataset-does-not-exist")

    # dataset listing
    datasets = load_ahorn_data()

    assert isinstance(datasets, list)
    assert len(datasets) > 0

    out, _ = capfd.readouterr()

    assert "Available datasets are the following:" in out
    assert len(out.splitlines()) > 1


def test_get_dataset_data():
    index_data = {
        "datasets": {
            "email-enron": {"slug": "email-enron"},
            "contact-high-school": {"slug": "contact-high-school"},
        }
    }

    with patch(
        "xgi.utils.request_from_url",
        return_value=index_data,
    ):
        data = _get_dataset_data("email-enron")

    assert data["slug"] == "email-enron"


def test_get_dataset_data_invalid_dataset():
    with patch(
        "xgi.utils.request_from_url",
        return_value={"datasets": {}},
    ):
        with pytest.raises(
            XGIError,
            match="does not exist in AHORN",
        ):
            _get_dataset_data("not-a-dataset")


@pytest.mark.parametrize(
    "attachments,expected",
    [
        (
            {
                "revision-1": {
                    "hif": {"url": "hif_url"},
                }
            },
            ("hif", "hif_url"),
        ),
        (
            {
                "revision-1": {
                    "ahorn": {"url": "ahorn_url"},
                }
            },
            ("ahorn", "ahorn_url"),
        ),
    ],
)
def test_get_dataset_url(attachments, expected):
    dataset_data = {
        "slug": "test",
        "attachments": attachments,
    }

    assert _get_dataset_url(dataset_data) == expected


def test_get_dataset_url_uses_latest_revision():
    dataset_data = {
        "slug": "test",
        "attachments": {
            "revision-1": {"hif": {"url": "old"}},
            "revision-3": {"hif": {"url": "new"}},
        },
    }

    assert _get_dataset_url(dataset_data) == ("hif", "new")


def test_get_dataset_url_specific_revision():
    dataset_data = {
        "slug": "test",
        "attachments": {
            "revision-1": {"hif": {"url": "old"}},
            "revision-2": {"hif": {"url": "new"}},
        },
    }

    assert _get_dataset_url(dataset_data, revision=1) == (
        "hif",
        "old",
    )


def test_get_dataset_url_missing_revision():
    dataset_data = {
        "slug": "test",
        "attachments": {
            "revision-1": {"hif": {"url": "url1"}},
            "revision-2": {"hif": {"url": "url2"}},
        },
    }

    with pytest.raises(
        XGIError,
        match=r"Available revisions: \[1, 2\]",
    ):
        _get_dataset_url(dataset_data, revision=3)


@pytest.mark.parametrize(
    "dataset_data,match",
    [
        (
            {
                "slug": "test",
                "attachments": {},
            },
            "does not contain any revision attachments",
        ),
        (
            {
                "slug": "test",
                "attachments": {
                    "revision-1": {
                        "csv": {"url": "foo"},
                    }
                },
            },
            "does not provide format 'hif'",
        ),
    ],
)
def test_get_dataset_url_errors(dataset_data, match):
    with pytest.raises(XGIError, match=match):
        _get_dataset_url(dataset_data)


def test_load_ahorn_data_listing(capfd):
    catalog = _mock_catalog({"email-enron": {}, "contact-high-school": {}})

    with patch(
        "xgi.readwrite.ahorn_data.request_from_url",
        return_value=catalog,
    ):
        result = load_ahorn_data()

    assert set(result) == {"email-enron", "contact-high-school"}
    out, _ = capfd.readouterr()
    assert "Available datasets are the following:" in out
    assert "email-enron" in out


def test_load_ahorn_data_invalid_dataset(capfd):
    catalog = _mock_catalog({"email-enron": {}})

    with patch(
        "xgi.readwrite.ahorn_data.request_from_url",
        return_value=catalog,
    ):
        with pytest.raises(XGIError, match="does not exist in AHORN"):
            load_ahorn_data("not-a-real-dataset")

    out, _ = capfd.readouterr()
    assert "Valid dataset names:" in out


def test_load_ahorn_data_fetches_catalog_once():
    """`load_ahorn_data` should hit the AHORN catalog exactly once per call."""
    hif_dict = {
        "network-type": "undirected",
        "incidences": [{"edge": 0, "node": 1}, {"edge": 0, "node": 2}],
        "nodes": [{"node": 1}, {"node": 2}],
        "edges": [{"edge": 0}],
    }
    catalog = _mock_catalog(
        {
            "example": {
                "slug": "example",
                "attachments": {
                    "revision-1": {"hif": {"url": "https://ahorn/example.hif.gz"}}
                },
            }
        }
    )

    call_count = 0

    def _catalog_or_data(url, mode="json"):
        nonlocal call_count
        if url == "https://ahorn.rwth-aachen.de/api/datasets.json":
            call_count += 1
            return catalog
        return _hif_payload(hif_dict)

    with (
        patch(
            "xgi.readwrite.ahorn_data.request_from_url",
            side_effect=_catalog_or_data,
        ),
        patch(
            "xgi.readwrite.ahorn_data.request_from_url_cached",
            return_value=_hif_payload(hif_dict),
        ),
    ):
        load_ahorn_data("example")

    assert call_count == 1


def test_load_ahorn_data_hif_format():
    hif_dict = {
        "network-type": "undirected",
        "incidences": [
            {"edge": 0, "node": 1},
            {"edge": 0, "node": 2},
            {"edge": 1, "node": 2},
            {"edge": 1, "node": 3},
        ],
        "nodes": [{"node": 1}, {"node": 2}, {"node": 3}],
        "edges": [{"edge": 0}, {"edge": 1}],
    }
    catalog = _mock_catalog(
        {
            "example": {
                "slug": "example",
                "attachments": {
                    "revision-1": {"hif": {"url": "https://ahorn/example.hif.gz"}}
                },
            }
        }
    )

    with (
        patch(
            "xgi.readwrite.ahorn_data.request_from_url",
            return_value=catalog,
        ),
        patch(
            "xgi.readwrite.ahorn_data.request_from_url_cached",
            return_value=_hif_payload(hif_dict),
        ),
    ):
        H = load_ahorn_data("example")

    assert set(H.nodes) == {1, 2, 3}
    assert H.num_edges == 2


def test_load_ahorn_data_cache_false_uses_uncached():
    hif_dict = {
        "network-type": "undirected",
        "incidences": [{"edge": 0, "node": 1}, {"edge": 0, "node": 2}],
        "nodes": [{"node": 1}, {"node": 2}],
        "edges": [{"edge": 0}],
    }
    catalog = _mock_catalog(
        {
            "example": {
                "slug": "example",
                "attachments": {
                    "revision-1": {"hif": {"url": "https://ahorn/example.hif.gz"}}
                },
            }
        }
    )

    call_log = []

    def _uncached(url, mode="json"):
        if mode == "raw":
            call_log.append(("uncached", url))
            return _hif_payload(hif_dict)
        return catalog

    with (
        patch(
            "xgi.readwrite.ahorn_data.request_from_url",
            side_effect=_uncached,
        ),
        patch(
            "xgi.readwrite.ahorn_data.request_from_url_cached",
            side_effect=AssertionError(
                "request_from_url_cached should not be called when cache=False"
            ),
        ),
    ):
        H = load_ahorn_data("example", cache=False)

    assert H.num_nodes == 2
    assert any(entry[0] == "uncached" for entry in call_log)


def test_request_from_ahorn_data_ahorn_text_format():
    """The ahorn-text branch of _request_from_ahorn_data."""
    text = (
        '{"name": "toy"}\n'
        '1 {"color": "red"}\n'
        '2 {"color": "blue"}\n'
        '3 {}\n'
        '1,2,3 {"weight": 4}\n'
    )
    catalog = _mock_catalog(
        {
            "toy": {
                "slug": "toy",
                "attachments": {
                    "revision-1": {"ahorn": {"url": "https://ahorn/toy.txt.gz"}}
                },
            }
        }
    )

    with (
        patch(
            "xgi.readwrite.ahorn_data.request_from_url",
            return_value=catalog,
        ),
        patch(
            "xgi.readwrite.ahorn_data.request_from_url_cached",
            return_value=gzip.compress(text.encode("utf-8")),
        ),
    ):
        H = _request_from_ahorn_data("toy")

    assert set(H.nodes) == {1, 2, 3}
    assert H.num_edges == 1
    assert H["name"] == "toy"


def test_request_from_ahorn_data_max_order_truncates():
    hif_dict = {
        "network-type": "undirected",
        "incidences": [
            {"edge": 0, "node": 1},
            {"edge": 0, "node": 2},
            {"edge": 1, "node": 1},
            {"edge": 1, "node": 2},
            {"edge": 1, "node": 3},
            {"edge": 1, "node": 4},
        ],
        "nodes": [{"node": 1}, {"node": 2}, {"node": 3}, {"node": 4}],
        "edges": [{"edge": 0}, {"edge": 1}],
    }
    catalog = _mock_catalog(
        {
            "example": {
                "slug": "example",
                "attachments": {
                    "revision-1": {"hif": {"url": "https://ahorn/example.hif.gz"}}
                },
            }
        }
    )

    with (
        patch(
            "xgi.readwrite.ahorn_data.request_from_url",
            return_value=catalog,
        ),
        patch(
            "xgi.readwrite.ahorn_data.request_from_url_cached",
            return_value=_hif_payload(hif_dict),
        ),
    ):
        H = load_ahorn_data("example", max_order=1)

    # order 1 edges have 2 members, order 2+ have 3+ members
    assert len(H.edges.filterby("order", 1, mode="gt")) == 0


def test_from_ahorn_text_parses_metadata_nodes_and_edges():
    text = (
        '{"name": "toy", "note": "hello"}\n'
        '1 {"color": "red"}\n'
        '2 {}\n'
        '1,2 {"weight": 3}\n'
    )
    H = _from_ahorn_text(text)

    assert H["name"] == "toy"
    assert H["note"] == "hello"
    assert set(H.nodes) == {1, 2}
    assert H.nodes[1]["color"] == "red"
    assert H.num_edges == 1
    assert H.edges.members(0) == {1, 2}
    assert H.edges[0]["weight"] == 3


def test_from_ahorn_text_skips_blank_lines():
    text = (
        '{}\n'
        '\n'
        '   \n'
        '1 {}\n'
        '\n'
        '2 {}\n'
    )
    H = _from_ahorn_text(text)

    assert set(H.nodes) == {1, 2}


def test_from_ahorn_text_respects_nodetype():
    """When `nodetype` is passed, node IDs are cast to that type."""
    text = (
        '{}\n'
        '1 {}\n'
        '2 {}\n'
        '1,2 {}\n'
    )
    H = _from_ahorn_text(text, nodetype=str)

    assert set(H.nodes) == {"1", "2"}
    assert H.edges.members(0) == {"1", "2"}
