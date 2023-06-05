"""Load a data set from the xgi-data repository or a local file."""

from functools import lru_cache

import requests

from ..exception import XGIError
from ..utils import request_json_from_url, request_json_from_url_cached

__all__ = ["load_bigg_data"]


def load_bigg_data(
    dataset=None,
    cache=True,
):
    """Load a data set from the xgi-data repository or a local file.

    Parameters
    ----------
    dataset : str, default: None
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository. If None, prints
        the list of available datasets.
    cache : bool, optional
        Whether to cache the input data
    nodetype : type, optional
        Type to cast the node ID to
    edgetype : type, optional
        Type to cast the edge ID to
    max_order: int, optional
        Maximum order of edges to add to the hypergraph

    Returns
    -------
    DiHypergraph
        The loaded dihypergraph.

    Raises
    ------
    XGIError
       The specified dataset does not exist.
    """

    indexurl = "http://bigg.ucsd.edu/api/v2/models"
    baseurl = "http://bigg.ucsd.edu/static/models/"

    # If no dataset is specified, print a list of the available datasets.
    if dataset is None:
        index_data = request_json_from_url(indexurl)
        ids = []
        for entry in index_data["results"]:
            ids.append(entry["bigg_id"])
        print("Available datasets are the following:")
        print(*ids, sep="\n")
        return

    if cache:
        data = request_json_from_url_cached(baseurl + dataset + ".json")
    else:
        data = request_json_from_url(baseurl + dataset + ".json")

    return _bigg_to_dihypergraph(data)


def _bigg_to_dihypergraph(d):
    """Convert a BIGG-formatted dict to dihypergraph.

    Parameters
    ----------
    d : dict
        A BIGG-formatted dict

    Returns
    -------
    DiHypergraph
        The dihypergraph from the selected BIGG model.
    """
    from .. import DiHypergraph

    DH = DiHypergraph()

    for m in d["metabolites"]:
        DH.add_node(m["id"], name=m["name"])

    for r in d["reactions"]:
        head = set()
        tail = set()
        for m, val in r["metabolites"].items():
            if val > 0:
                head.add(m)
            else:
                tail.add(m)

        DH.add_edge((tail, head), id=r["id"])

    return DH
