import gzip
import json
import re
import ssl
from os.path import dirname, join
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import xopen

from ..convert import cut_to_order, from_hif_dict
from ..core import Hypergraph
from ..utils import request_json_from_url, request_json_from_url_cached

_BASE = "https://cricca.disi.unitn.it/datasets/hypergraphx-data"
_CATALOG_URL = "https://hgx-team.github.io/hypergraphx-data/static/js/related-data.js"


def load_hypergraphx_data(
    dataset=None,
    cache=True,
    nodetype=None,
    edgetype=None,
    max_order=None,
):
    """Load a dataset from hypergraphx-data.

    Parameters
    ----------
    dataset : str, optional
        Name of the dataset to load. If None, a list of available datasets is printed.
    cache : bool, optional
        Whether or not to cache the output.
    nodetype : type, optional
        Type to which node labels should be converted. If None, no conversion is performed.
    edgetype : type, optional
        Type to which edge labels should be converted. If None, no conversion is performed.
    max_order : int, optional
        Maximum order of the hypergraph to load. If None, all orders are loaded.

    Returns
    -------
    Hypergraph or dict of Hypergraphs
        The requested hypergraph or a dictionary of hypergraphs if the dataset is a collection.

    Raises
    ------
    XGIError
        The specified dataset does not exist.
    """
    raw_data = _download(_CATALOG_URL)
    index_data = _parse_remote_dataset_catalog(raw_data)

    if dataset is None:
        print("Available datasets are the following:")
        print(*index_data, sep="\n")
        return index_data

    if dataset not in index_data:
        print("Valid dataset names:")
        print(*index_data, sep="\n")
        raise KeyError("Must choose a valid dataset name!")
    url = f"{_BASE}/{dataset}/{dataset}.json.gz"

    return _request_from_hypergraphx_data(
        url, nodetype=nodetype, edgetype=edgetype, max_order=max_order, cache=cache
    )


def _decompress_gzip_if_needed(raw: bytes) -> bytes:
    try:
        return gzip.decompress(raw).decode("utf-8")
    except OSError:
        return raw


def _request_from_hypergraphx_data(
    url, nodetype=None, edgetype=None, max_order=None, cache=True
):
    """Request a dataset from xgi-data.

    Parameters
    ----------
    url : str
        Address of the dataset in the xgi-data repository.
    cache : bool, optional
        Whether or not to cache the output

    Returns
    -------
    Data
        The requested data loaded from a json file.

    Raises
    ------
    XGIError
        If the HTTP request is not successful or the dataset does not exist.

    See also
    ---------
    load_xgi_data
    """
    rawdata = _download(url)
    jsondata = json.loads(_decompress_gzip_if_needed(rawdata))

    H = _load_hypergraph(jsondata)
    if max_order:
        H = cut_to_order(H, order=max_order)
    return H


def _load_hypergraph(jsondata):
    """Load an XGI Hypergraph from its JSON serialization."""

    H = Hypergraph()

    for item in jsondata:
        record_type = item.get("type")

        # ------------------------------------------------------------
        # Hypergraph metadata
        # ------------------------------------------------------------
        if "hypergraph_type" in item:
            metadata = item.get("hypergraph_metadata", {})
            for key, value in metadata.items():
                H[key] = value

        # ------------------------------------------------------------
        # Node
        # ------------------------------------------------------------
        elif record_type == "node":
            node_id = item["idx"]
            metadata = item.get("metadata", {})

            H.add_node(node_id, **metadata)

        # ------------------------------------------------------------
        # Edge
        # ------------------------------------------------------------
        elif record_type == "edge":
            interaction = item["interaction"]
            metadata = item.get("metadata", {})

            # Hyperedges are sets, so remove duplicate nodes.
            interaction = set(interaction)

            # The edge ID is stored separately from the attributes.
            edge_id = metadata.get("id")

            # Preserve all remaining edge metadata.
            attributes = {key: value for key, value in metadata.items() if key != "id"}

            if edge_id is None:
                H.add_edge(interaction, **attributes)
            else:
                H.add_edge(interaction, id=edge_id, **attributes)
    return H


def _parse_remote_dataset_catalog(payload: bytes):
    text = payload.decode("utf-8")
    text = text.strip()

    if text.startswith("window.RELATED_DATASETS"):
        match = re.match(r"window\.RELATED_DATASETS\s*=\s*(.*?);?\s*$", text, re.S)
        if not match:
            raise TypeError("Could not parse remote dataset catalog.")
        text = match.group(1)

    try:
        parsed = json.loads(text)
    except Exception as exc:
        raise TypeError("Remote dataset catalog is not valid JSON.") from exc

    if isinstance(parsed, dict):
        items = parsed.get("datasets")
    else:
        items = parsed

    if not isinstance(items, list):
        raise TypeError(
            "Remote dataset catalog must be a list or contain a 'datasets' list."
        )

    datasets = []
    for item in items:
        if not isinstance(item, dict) or "name" not in item:
            raise TypeError("Remote dataset catalog entries must contain names.")
        dataset = dict(item)
        datasets.append(dataset["name"])
    return datasets


def _download(url: str, *, timeout: int = 30, verify_ssl: bool = False) -> bytes:
    try:
        if verify_ssl:
            context = ssl.create_default_context()
            try:
                import certifi  # type: ignore

                context = ssl.create_default_context(cafile=certifi.where())
            except Exception:
                pass
        else:
            context = ssl._create_unverified_context()  # noqa: SLF001
        req = Request(url, headers={"User-Agent": "hypergraphx-loader/1.0"})
        with urlopen(req, timeout=timeout, context=context) as resp:
            return resp.read()
    except HTTPError as exc:
        raise FileNotFoundError(f"Not found at {url} (HTTP {exc.code}).") from exc
    except URLError as exc:
        raise ConnectionError(
            f"Network error reaching {url}: {exc.reason}. "
            "Are you offline? For offline use, download the dataset and use load_hypergraph(...) on a local file."
        ) from exc
