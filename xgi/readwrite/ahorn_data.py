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
    catalog = request_from_url(_CATALOG_URL)["datasets"]
    index_data = list(catalog)

    if dataset is None:
        print("Available datasets are the following:")
        print(*index_data, sep="\n")
        return index_data

    if dataset not in index_data:
        print("Valid dataset names:")
        print(*index_data, sep="\n")
        raise XGIError(f"Dataset '{dataset}' does not exist in AHORN.")

    return _request_from_ahorn_data(
        dataset,
        nodetype=nodetype,
        edgetype=edgetype,
        max_order=max_order,
        cache=cache,
        catalog=catalog,
    )


def _request_from_ahorn_data(
    dataset,
    nodetype=None,
    edgetype=None,
    max_order=None,
    cache=True,
    catalog=None,
):
    """Request a data set from AHORN."""
    dataset_data = _get_dataset_data(dataset, catalog=catalog)

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


def _get_dataset_data(dataset, catalog=None):
    """Get metadata for a dataset from the AHORN catalog.

    If ``catalog`` is provided, use it directly; otherwise fetch it.
    """
    if catalog is None:
        catalog = request_from_url(_CATALOG_URL)["datasets"]

    key = dataset.lower()
    datasets = {name.lower(): name for name in catalog}

    if key not in datasets:
        raise XGIError(f"Dataset '{dataset}' does not exist in AHORN.")

    return catalog[datasets[key]]


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
    """Parse a hypergraph from an AHORN plain-text payload.

    Parameters
    ----------
    data : str
        The decoded AHORN text payload.
    nodetype : type, optional
        Type to cast node IDs to. Defaults to ``int``, matching the AHORN
        text format's numeric-string convention.
    edgetype : type, optional
        Currently unused. Edges receive auto-assigned ids from the
        ``Hypergraph`` and the text format does not carry explicit edge
        ids to cast.

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

    _cast_node = nodetype if nodetype is not None else int

    for line in lines:
        # Split the node/edge specification from its metadata
        ids, metadata_str = line.split(maxsplit=1)
        metadata = json.loads(metadata_str)

        # Node
        if "," not in ids:
            H.add_node(_cast_node(ids), **metadata)

        # Hyperedge
        else:
            edge = [_cast_node(node) for node in ids.split(",")]
            H.add_edge(edge, **metadata)

    return H
