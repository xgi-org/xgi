from functools import lru_cache

import requests

from .. import convert
from ..exception import XGIError

__all__ = ["load_xgi_data"]


def load_xgi_data(dataset, nodetype=None, edgetype=None, max_order=None, cache=True):
    """Loads a hypergraph from the XGI-DATA repository

    Parameters
    ----------
    dataset : str
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository.

    nodetype : type, optional
        Type to cast the node ID to, default None.
    edgetype : type, optional
        Type to cast the edge ID to, default None.
    max_order : int, optional
        Maximum order of edges to add to the hypergraph, default None.
    cache : bool, optional
        Whether or not to cache the output.


    Returns
    -------
    Hypergraph
        The loaded hypergraph.

    Raises
    ------
    XGIError
       The specified dataset does not exist.
    """
    if cache:
        return _load_xgi_data_cached(dataset, nodetype, edgetype, max_order)
    else:
        _load_xgi_data_cached.cache_clear()
        return _load_xgi_data_new(dataset, nodetype, edgetype, max_order)


def _load_xgi_data_new(dataset, nodetype=None, edgetype=None, max_order=None):
    """Loads a hypergraph from the XGI-DATA repository

    Parameters
    ----------
    dataset : str
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository.

    nodetype : type, optional
        Type to cast the node ID to, default None.
    edgetype : type, optional
        Type to cast the edge ID to, default None.
    max_order : int, optional
        Maximum order of edges to add to the hypergraph, default None.
    cache : bool, optional
        Whether or not to cache the output.

    Returns
    -------
    Hypergraph
        The loaded hypergraph.

    Raises
    ------
    XGIError
       The specified dataset does not exist.
    """
    index_url = "https://raw.githubusercontent.com/ComplexGroupInteractions/xgi-data/main/index.json"
    index = requests.get(index_url).json()
    if dataset not in index:
        print("Valid dataset names:")
        print(*index, sep="\n")
        raise XGIError("Must choose a valid dataset name!")

    r = requests.get(index[dataset]["url"])

    return convert.dict_to_hypergraph(
        r.json(), nodetype=nodetype, edgetype=edgetype, max_order=max_order
    )


@lru_cache
def _load_xgi_data_cached(dataset, nodetype=None, edgetype=None, max_order=None):
    """Same as _load_xgi_data_new but with a decorator to cache the output."""
    return _load_xgi_data_new(dataset, nodetype, edgetype, max_order)
