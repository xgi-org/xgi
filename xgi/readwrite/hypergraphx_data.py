"""Load data sets from the hypergraphx-data repository."""

import gzip
import json
import re
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..convert import cut_to_order
from ..core import Hypergraph
from ..utils import request_from_url

__all__ = ["load_hypergraphx_data"]

_BASE_URL = "https://cricca.disi.unitn.it/datasets/hypergraphx-data"
_CATALOG_URL = "https://hgx-team.github.io/hypergraphx-data/static/js/related-data.js"


def load_hypergraphx_data(
    dataset=None,
    nodetype=None,
    edgetype=None,
    max_order=None,
):
    """Load a data set from the hypergraphx-data repository.

    Parameters
    ----------
    dataset : str, optional
        Dataset name. If None (default), prints and returns the list of
        available datasets.
    nodetype : type, optional
        Type to cast the node ID to, by default None.
    edgetype : type, optional
        Type to cast the edge ID to, by default None.
    max_order : int, optional
        Maximum order of edges to add to the hypergraph, by default None.

    Returns
    -------
    Hypergraph
        The loaded hypergraph.

    Raises
    ------
    XGIError
        If the specified dataset does not exist.
    """
    raw_catalog = request_from_url(_CATALOG_URL, mode="raw")
    index_data = _parse_remote_dataset_catalog(raw_catalog)

    if dataset is None:
        print("Available datasets are the following:")
        print(*index_data, sep="\n")
        return index_data

    if dataset not in index_data:
        print("Valid dataset names:")
        print(*index_data, sep="\n")
        raise KeyError("Must choose a valid dataset name!")

    url = f"{_BASE_URL}/{dataset}/{dataset}.json.gz"

    return _request_from_hypergraphx_data(
        url,
        nodetype=nodetype,
        edgetype=edgetype,
        max_order=max_order,
    )


def _request_from_hypergraphx_data(
    url,
    nodetype=None,
    edgetype=None,
    max_order=None,
):
    """Request a data set from hypergraphx-data."""
    rawdata = _download(url)

    jsondata = json.loads(gzip.decompress(rawdata).decode("utf-8"))

    H = _load_hypergraph(
        jsondata,
        nodetype=nodetype,
        edgetype=edgetype,
    )

    if max_order:
        H = cut_to_order(H, order=max_order)

    return H


def _load_hypergraph(jsondata, nodetype=None, edgetype=None):
    """Load an XGI Hypergraph from a HyperGraphX JSON serialization."""
    H = Hypergraph()

    for item in jsondata:
        record_type = item.get("type")

        if "hypergraph_type" in item:
            metadata = item.get("hypergraph_metadata", {})
            for key, value in metadata.items():
                H[key] = value

        elif record_type == "node":
            node_id = item["idx"]

            if nodetype:
                node_id = nodetype(node_id)

            H.add_node(
                node_id,
                **item.get("metadata", {}),
            )

        elif record_type == "edge":
            interaction = item["interaction"]

            if nodetype:
                interaction = [nodetype(node) for node in interaction]

            interaction = set(interaction)

            metadata = item.get("metadata", {})
            e_id = metadata.pop("id", None)

            if edgetype and e_id:
                e_id = edgetype(e_id)

            if e_id:
                H.add_edge(interaction, idx=e_id, **metadata)
            else:
                H.add_edge(interaction, **metadata)

    return H


def _parse_remote_dataset_catalog(payload):
    """Parse the HyperGraphX remote dataset catalog."""
    text = payload.decode("utf-8").strip()

    if text.startswith("window.RELATED_DATASETS"):
        match = re.match(
            r"window\.RELATED_DATASETS\s*=\s*(.*?);?\s*$",
            text,
            re.S,
        )

        if not match:
            raise TypeError("Could not parse remote dataset catalog.")

        text = match.group(1)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise TypeError("Remote dataset catalog is not valid JSON.") from exc

    if isinstance(parsed, dict):
        items = parsed.get("datasets")
    else:
        items = parsed

    if not isinstance(items, list):
        raise TypeError(
            "Remote dataset catalog must be a list or contain " "a 'datasets' list."
        )

    return [item["name"] for item in items if isinstance(item, dict) and "name" in item]


def _download(url, *, timeout=30, verify_ssl=False):
    """Download raw data from a URL."""
    try:
        if verify_ssl:
            context = ssl.create_default_context()

            try:
                import certifi

                context = ssl.create_default_context(cafile=certifi.where())
            except ImportError:
                pass
        else:
            context = ssl._create_unverified_context()

        request = Request(
            url,
            headers={"User-Agent": "xgi-hypergraphx-data-loader/1.0"},
        )

        with urlopen(request, timeout=timeout, context=context) as response:
            return response.read()

    except HTTPError as exc:
        raise HTTPError(
            f"Could not download dataset from {url} " f"(HTTP {exc.code})."
        ) from exc

    except URLError as exc:
        raise URLError(f"Could not reach {url}: {exc.reason}.") from exc
