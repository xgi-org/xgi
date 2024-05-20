"""Load a data set from the xgi-data repository or a local file."""
from os.path import dirname, exists, join
from warnings import warn

from ..convert import dict_to_hypergraph
from ..exception import XGIError
from ..utils import request_json_from_url, request_json_from_url_cached

__all__ = ["load_xgi_data"]#, "download_xgi_data"]


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
    dataset : str, optional
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository. If None (default), prints
        the list of available datasets.
    cache : bool, optional
        Whether to cache the input data, by default True.
    read : bool, optional
        If read==True, search for a local copy of the data set. Use the local
        copy if it exists, otherwise use the xgi-data repository.
        By default, False.
    path : str, optional
        Path to a local copy of the data set
    nodetype : type, optional
        Type to cast the node ID to, by default None.
    edgetype : type, optional
        Type to cast the edge ID to, by default None.
    max_order: int, optional
        Maximum order of edges to add to the hypergraph, by default None.

    Returns
    -------
    Hypergraph
        The loaded hypergraph.

    Raises
    ------
    XGIError
       The specified dataset does not exist.
    """
    index_url = "https://raw.githubusercontent.com/xgi-org/xgi-data/main/index.json"

    if read:
        cfp = join(path, dataset + ".json")
        if exists(cfp):
            from ..readwrite import read_json
            return read_json(cfp, nodetype=nodetype, edgetype=edgetype)
        else:
            warn(
                f"No local copy was found at {cfp}. The data is requested "
                "from the xgi-data repository instead. To download a local "
                "copy, use `download_xgi_data`."
            )

    # If no dataset is specified, print a list of the available datasets.
    index_data = request_json_from_url(index_url)
    if dataset is None:
        print("Available datasets are the following:")
        print(*index_data, sep="\n")
        return

    key = dataset.lower()
    if key not in index_data:
        print("Valid dataset names:")
        print(*index_data, sep="\n")
        raise XGIError("Must choose a valid dataset name!")
    url = index_data[key]["url"]

    return _request_from_xgi_data(
        url, nodetype=nodetype, edgetype=edgetype, max_order=max_order, cache=cache
    )


# def download_xgi_data(dataset, path=""):
#     """Make a local copy of a dataset in the xgi-data repository.

#     Parameters
#     ----------
#     dataset : str
#         Dataset name. Valid options are the top-level tags of the
#         index.json file in the xgi-data repository.

#     path : str, optional
#         Path to where the local copy should be saved. If none is given, save
#         file to local directory.
#     """
#     index_url = "https://raw.githubusercontent.com/xgi-org/xgi-data/main/index.json"

#     jsondata = _request_from_xgi_data(index_url, dataset)

#     if jsondata["type"] == "collection":
#         jsonfile = open(join(path, f"{dataset}_collection_data.json"), "w")
#         json.dump(jsondata, jsonfile, indent=2)
#         jsonfile.close()

#         for name, data in jsondata["datasets"].items():
#             relpath = data["relative-path"]
#             jsondata = request_json_from_url(join(dirname(url), relpath))
#             jsonfile = open(join(path, f"{dataset}_{name}.json"), "w")
#             json.dump(jsondata, jsonfile, indent=2)
#             jsonfile.close()


def _request_from_xgi_data(
    url, nodetype=None, edgetype=None, max_order=None, cache=True
):
    """Request a dataset from xgi-data.

    Parameters
    ----------
    dataset : str, optional
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository. If None, prints
        the list of available datasets.
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
    if cache:
        jsondata = request_json_from_url_cached(url)
    else:
        jsondata = request_json_from_url(url)

    if "type" in jsondata and jsondata["type"] == "collection":
        collection = {}
        for name, data in jsondata["datasets"].items():
            relpath = data["relative-path"]
            H = _request_from_xgi_data(
                join(dirname(url), relpath),
                nodetype=nodetype,
                edgetype=edgetype,
                max_order=max_order,
                cache=cache,
            )
            collection[name] = H
        return collection

    return dict_to_hypergraph(
       jsondata, nodetype=nodetype, edgetype=edgetype, max_order=max_order
    )
