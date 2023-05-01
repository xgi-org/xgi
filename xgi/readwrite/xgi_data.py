"""Load a data set from the xgi-data repository or a local file."""
import json
import os
from functools import lru_cache
from warnings import warn

import requests

from .. import convert
from ..exception import XGIError

__all__ = ["load_xgi_data", "download_xgi_data"]


def load_xgi_data(
    dataset=None,
    cache=True,
    read=False,
    path="",
    nodetype=None,
    edgetype=None,
    max_order=None,
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
    read : bool, optional
        If read==True, search for a local copy of the data set. Use the local
        copy if it exists, otherwise use the  xgi-data repository.
    path : str, optional
        Path to a local copy of the data set
    nodetype : type, optional
        Type to cast the node ID to
    edgetype : type, optional
        Type to cast the edge ID to
    max_order: int, optional
        Maximum order of edges to add to the hypergraph

    Returns
    -------
    Hypergraph
        The loaded hypergraph.

    Raises
    ------
    XGIError
       The specified dataset does not exist.
    """

    # If no dataset is specified, print a list of the available datasets.
    if dataset is None:
        index_url = "https://gitlab.com/complexgroupinteractions/xgi-data/-/raw/main/index.json?inline=false"
        index_data = _request_json_from_url(index_url)
        print("Available datasets are the following:")
        print(*index_data, sep="\n")
        return

    if read:
        cfp = os.path.join(path, dataset + ".json")
        if os.path.exists(cfp):
            data = json.load(open(cfp, "r"))

            return convert.dict_to_hypergraph(
                data, nodetype=nodetype, edgetype=edgetype, max_order=max_order
            )
        else:
            warn(
                f"No local copy was found at {cfp}. The data is requested "
                "from the xgi-data repository instead. To download a local "
                "copy, use `download_xgi_data`."
            )
    if cache:
        data = _request_from_xgi_data_cached(dataset)
    else:
        data = _request_from_xgi_data(dataset)

    return convert.dict_to_hypergraph(
        data, nodetype=nodetype, edgetype=edgetype, max_order=max_order
    )


def download_xgi_data(dataset, path=""):
    """Make a local copy of a dataset in the xgi-data repository.

    Parameters
    ----------
    dataset : str
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository.

    path : str, optional
        Path to where the local copy should be saved. If none is given, save
        file to local directory.
    """

    jsondata = _request_from_xgi_data(dataset)
    jsonfile = open(os.path.join(path, dataset + ".json"), "w")
    json.dump(jsondata, jsonfile)
    jsonfile.close()


def _request_from_xgi_data(dataset=None):
    """Request a dataset from xgi-data.

    Parameters
    ----------
    dataset : str, default: None
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository. If None, prints
        the list of available datasets.

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

    index_url = "https://gitlab.com/complexgroupinteractions/xgi-data/-/raw/main/index.json?inline=false"
    index_data = _request_json_from_url(index_url)

    key = dataset.lower()
    if key not in index_data:
        print("Valid dataset names:")
        print(*index_data, sep="\n")
        raise XGIError("Must choose a valid dataset name!")

    return _request_json_from_url(index_data[key]["url"])


@lru_cache(maxsize=None)
def _request_from_xgi_data_cached(dataset):
    """Request a dataset from xgi-data and cache the result.

    Wraps `_request_from_xgi_data` in an lru_cache decorator.

    Parameters
    ----------
    dataset : str
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository.

    Returns
    -------
    Data
        The requested data loaded from a json file.

    See also
    ---------
    load_xgi_data
    """

    return _request_from_xgi_data(dataset)


def _request_json_from_url(url):
    """HTTP request json file and return as dict.

    Parameters
    ----------
    url : str
        The url where the json file is located.

    Returns
    -------
    dict
        A dictionary of the JSON requested.

    Raises
    ------
    XGIError
        If the connection fails or if there is a bad HTTP request.
    """

    try:
        r = requests.get(url)
    except requests.ConnectionError:
        raise XGIError("Connection Error!")

    if r.ok:
        return r.json()
    else:
        raise XGIError(f"Error: HTTP response {r.status_code}")
