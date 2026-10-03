import gzip
import json
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import pytest

from xgi import load_hypergraphx_data
from xgi.exception import XGIError
from xgi.readwrite.hypergraphx_data import (
    _download,
    _download_cached,
    _load_hypergraph,
    _parse_remote_dataset_catalog,
)


@pytest.fixture(autouse=True)
def _clear_download_cache():
    """Reset the download cache between tests so patches take effect."""
    _download_cached.cache_clear()
    yield
    _download_cached.cache_clear()


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


def test_load_hypergraph_edge_without_explicit_id():
    """Edges without a 'metadata.id' get an auto-assigned uid."""
    jsondata = [
        {"type": "node", "idx": 1},
        {"type": "node", "idx": 2},
        {"type": "edge", "interaction": [1, 2]},
    ]

    H = _load_hypergraph(jsondata)

    assert set(H.nodes) == {1, 2}
    assert H.num_edges == 1


def test_load_hypergraph_ignores_unknown_record_type():
    """Records with an unrecognized 'type' field are ignored, not raised on."""
    jsondata = [
        {"type": "node", "idx": 1},
        {"type": "node", "idx": 2},
        {"type": "unknown-thing", "foo": "bar"},
        {"type": "edge", "interaction": [1, 2]},
    ]

    H = _load_hypergraph(jsondata)

    assert set(H.nodes) == {1, 2}
    assert H.num_edges == 1


def test_parse_remote_dataset_catalog_invalid_json():
    with pytest.raises(TypeError, match="not valid JSON"):
        _parse_remote_dataset_catalog(b"this is not json {{{")


def test_parse_remote_dataset_catalog_window_prefix_but_invalid_body():
    with pytest.raises(TypeError):
        _parse_remote_dataset_catalog(
            b"window.RELATED_DATASETS = this is not json;"
        )


def test_parse_remote_dataset_catalog_wrong_shape():
    with pytest.raises(TypeError, match="must be a list"):
        _parse_remote_dataset_catalog(b'{"unrelated": "value"}')


def test_parse_remote_dataset_catalog_skips_items_without_name():
    payload = b'[{"name": "keep"}, {"no_name_field": true}, "string_item"]'
    result = _parse_remote_dataset_catalog(payload)
    assert result == ["keep"]


def test_load_hypergraphx_data_listing(capfd):
    catalog_payload = b'[{"name": "dataset-a"}, {"name": "dataset-b"}]'

    with patch(
        "xgi.readwrite.hypergraphx_data.request_from_url",
        return_value=catalog_payload,
    ):
        result = load_hypergraphx_data()

    assert result == ["dataset-a", "dataset-b"]
    out, _ = capfd.readouterr()
    assert "Available datasets are the following:" in out
    assert "dataset-a" in out


def test_load_hypergraphx_data_invalid_dataset(capfd):
    catalog_payload = b'[{"name": "dataset-a"}]'

    with patch(
        "xgi.readwrite.hypergraphx_data.request_from_url",
        return_value=catalog_payload,
    ):
        with pytest.raises(XGIError, match="does not exist in hypergraphx-data"):
            load_hypergraphx_data("nonexistent")

    out, _ = capfd.readouterr()
    assert "Valid dataset names:" in out


def test_load_hypergraphx_data_cache_false_bypasses_cache():
    """When ``cache=False`` the loader must call `_download` directly, not
    the memoized wrapper."""
    catalog_payload = b'[{"name": "dataset-a"}]'
    hgx_payload = [
        {"type": "node", "idx": 1},
        {"type": "node", "idx": 2},
        {"type": "edge", "interaction": [1, 2]},
    ]
    gzipped = gzip.compress(json.dumps(hgx_payload).encode("utf-8"))

    def _fail_if_called(*args, **kwargs):
        raise AssertionError("_download_cached should not run when cache=False")

    with (
        patch(
            "xgi.readwrite.hypergraphx_data.request_from_url",
            return_value=catalog_payload,
        ),
        patch(
            "xgi.readwrite.hypergraphx_data._download",
            return_value=gzipped,
        ),
        patch(
            "xgi.readwrite.hypergraphx_data._download_cached",
            side_effect=_fail_if_called,
        ),
    ):
        H = load_hypergraphx_data("dataset-a", cache=False)

    assert H.num_nodes == 2


def test_load_hypergraphx_data_cache_true_reuses_result():
    """When ``cache=True`` (the default) repeated calls hit `_download` once."""
    catalog_payload = b'[{"name": "dataset-a"}]'
    hgx_payload = [
        {"type": "node", "idx": 1},
        {"type": "edge", "interaction": [1]},
    ]
    gzipped = gzip.compress(json.dumps(hgx_payload).encode("utf-8"))

    download_calls = []

    def _record(url):
        download_calls.append(url)
        return gzipped

    with (
        patch(
            "xgi.readwrite.hypergraphx_data.request_from_url",
            return_value=catalog_payload,
        ),
        patch(
            "xgi.readwrite.hypergraphx_data._download",
            side_effect=_record,
        ),
    ):
        load_hypergraphx_data("dataset-a")
        load_hypergraphx_data("dataset-a")

    assert len(download_calls) == 1


def test_load_hypergraphx_data_dispatches_to_downloader():
    catalog_payload = b'[{"name": "dataset-a"}]'
    hgx_payload = [
        {"hypergraph_type": "undirected", "hypergraph_metadata": {"name": "test"}},
        {"type": "node", "idx": 1},
        {"type": "node", "idx": 2},
        {"type": "edge", "interaction": [1, 2]},
    ]
    gzipped = gzip.compress(json.dumps(hgx_payload).encode("utf-8"))

    with (
        patch(
            "xgi.readwrite.hypergraphx_data.request_from_url",
            return_value=catalog_payload,
        ),
        patch(
            "xgi.readwrite.hypergraphx_data._download",
            return_value=gzipped,
        ),
    ):
        H = load_hypergraphx_data("dataset-a")

    assert H["name"] == "test"
    assert set(H.nodes) == {1, 2}
    assert H.num_edges == 1


def test_load_hypergraphx_data_max_order_truncates():
    catalog_payload = b'[{"name": "dataset-a"}]'
    hgx_payload = [
        {"type": "node", "idx": 1},
        {"type": "node", "idx": 2},
        {"type": "node", "idx": 3},
        {"type": "edge", "interaction": [1, 2]},
        {"type": "edge", "interaction": [1, 2, 3]},
    ]
    gzipped = gzip.compress(json.dumps(hgx_payload).encode("utf-8"))

    with (
        patch(
            "xgi.readwrite.hypergraphx_data.request_from_url",
            return_value=catalog_payload,
        ),
        patch(
            "xgi.readwrite.hypergraphx_data._download",
            return_value=gzipped,
        ),
    ):
        H = load_hypergraphx_data("dataset-a", max_order=1)

    # order 1 = size 2; only the 2-node edge should survive
    assert len(H.edges.filterby("order", 1, mode="gt")) == 0


def test_download_success():
    fake_response = _FakeResponse(b"payload bytes")

    with patch(
        "xgi.readwrite.hypergraphx_data.urlopen",
        return_value=fake_response,
    ):
        result = _download("https://example.com/data.gz")

    assert result == b"payload bytes"


def test_download_http_error_wraps_message():
    def _raise_http(*args, **kwargs):
        raise HTTPError("https://example.com", 404, "Not Found", {}, None)

    with patch(
        "xgi.readwrite.hypergraphx_data.urlopen",
        side_effect=_raise_http,
    ):
        with pytest.raises(HTTPError, match="Could not download dataset"):
            _download("https://example.com/data.gz")


def test_download_url_error_wraps_message():
    def _raise_url(*args, **kwargs):
        raise URLError("host unreachable")

    with patch(
        "xgi.readwrite.hypergraphx_data.urlopen",
        side_effect=_raise_url,
    ):
        with pytest.raises(URLError, match="Could not reach"):
            _download("https://example.com/data.gz")


class _FakeResponse:
    """Minimal context-managed stand-in for urllib's response object."""

    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._payload
