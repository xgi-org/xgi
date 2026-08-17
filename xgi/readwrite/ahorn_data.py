"""Load data sets from the AHORN dataset repository."""

import gzip
import json

from ..convert import cut_to_order, from_hif_dict
from ..core import Hypergraph
from ..exception import XGIError
from ..utils import request_from_url, request_from_url_cached

__all__ = ["load_ahorn_data"]

_CATALOG_URL = "https://ahorn.rwth-aachen.de/api/datasets.json"


def load_ahorn_data(
    dataset=None,
    cache=True,
    nodetype=None,
    edgetype=None,
    max_order=None,
):
    """Load a data set from the AHORN repository.

    Parameters
    ----------
    dataset : str, optional
        Dataset slug. If None (default), prints and returns the list of
        available datasets.
    cache : bool, optional
        Whether to cache the input data, by default True.
    nodetype : type, optional
        Type to cast node IDs to, by default None.
    edgetype : type, optional
        Type to cast edge IDs to, by default None.
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
    index_data = list(request_from_url(_CATALOG_URL)["datasets"].keys())

    if dataset is None:
        print("Available datasets are the following:")
        print(*index_data, sep="\n")
        return index_data

    if dataset not in index_data:
        print("Valid dataset names:")
        print(*index_data, sep="\n")
        raise KeyError("Must choose a valid dataset name!")

    return _request_from_ahorn_data(
        dataset,
        nodetype=nodetype,
        edgetype=edgetype,
        max_order=max_order,
        cache=cache,
    )


def _request_from_ahorn_data(
    dataset,
    nodetype=None,
    edgetype=None,
    max_order=None,
    cache=True,
):
    """Request a data set from AHORN."""
    dataset_data = _get_dataset_data(dataset)

    format, url = _get_dataset_url(dataset_data)

    if cache:
        rawdata = request_from_url_cached(url, mode="raw")
    else:
        rawdata = request_from_url(url, mode="raw")

    if format == "hif":
        jsondata = json.loads(gzip.decompress(rawdata).decode("utf-8"))
        H = from_hif_dict(
            jsondata,
            nodetype=nodetype,
            edgetype=edgetype,
        )
    elif format == "ahorn":
        data = gzip.decompress(rawdata).decode("utf-8")
        H = _from_ahorn_text(
            data,
            nodetype=nodetype,
            edgetype=edgetype,
        )

    if max_order:
        H = cut_to_order(H, order=max_order)

    return H


def _get_dataset_data(dataset):
    """Get metadata for a dataset from the AHORN catalog."""
    index_data = request_from_url(_CATALOG_URL)["datasets"]

    key = dataset.lower()
    datasets = {name.lower(): name for name in index_data}

    if key not in datasets:
        raise XGIError(f"Dataset '{dataset}' does not exist in AHORN.")

    return index_data[datasets[key]]


def _get_dataset_url(dataset_data, revision=None):
    """Get the download URL for an AHORN dataset."""
    attachments = dataset_data["attachments"]

    revisions = [key for key in attachments if key.startswith("revision-")]

    if not revisions:
        raise XGIError(
            f"Dataset '{dataset_data['slug']}' does not contain "
            "any revision attachments."
        )

    if revision is None:
        revision = max(int(key.split("-")[1]) for key in revisions)

    revision_key = f"revision-{revision}"

    if revision_key not in attachments:
        available = sorted(int(key.split("-")[1]) for key in revisions)
        raise XGIError(
            f"Dataset '{dataset_data['slug']}' does not have "
            f"revision {revision}. Available revisions: {available}"
        )

    formats = attachments[revision_key]

    if "hif" in formats:
        return "hif", formats["hif"]["url"]
    elif "ahorn" in formats:
        return "ahorn", formats["ahorn"]["url"]
    else:
        raise XGIError(
            f"Dataset '{dataset_data['slug']}' revision {revision} "
            f"does not provide format 'hif'. "
            f"Available formats: {sorted(formats)}"
        )


def _from_ahorn_text(data, nodetype=None, edgetype=None):
    """Parse a hypergraph from a requests.Response object.

    Parameters
    ----------
    response : requests.Response
        Response returned by requests.get() containing the hypergraph
        in the expected text format.

    Returns
    -------
    xgi.Hypergraph
        Parsed XGI hypergraph.
    """
    H = Hypergraph()

    lines = data.splitlines()

    # Skip blank lines
    lines = (line.strip() for line in lines if line.strip())

    # First line contains hypergraph metadata
    metadata = json.loads(next(lines))

    # Store metadata on the hypergraph
    H._net_attr.update(metadata)

    for line in lines:
        # Split the node/edge specification from its metadata
        ids, metadata_str = line.split(maxsplit=1)
        metadata = json.loads(metadata_str)

        # Node
        if "," not in ids:
            node = int(ids)
            H.add_node(node, **metadata)

        # Hyperedge
        else:
            edge = [int(node) for node in ids.split(",")]
            H.add_edge(edge, **metadata)

    return H
