import platform
import sys
from unittest.mock import patch

import pytest

from xgi import load_ahorn_data
from xgi.exception import XGIError
from xgi.readwrite.ahorn_data import _get_dataset_data, _get_dataset_url


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
    with pytest.raises(KeyError):
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
