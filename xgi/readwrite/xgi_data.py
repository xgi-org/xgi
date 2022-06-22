import requests

from .. import convert
from ..exception import XGIError

__all__ = ["load_xgi_data"]

def load_xgi_data(dataset, nodetype=None, edgetype=None):
    """_summary_

    Parameters
    ----------
    dataset : str
        Dataset name. Valid options are the top-level tags of the
        index.json file in the xgi-data repository.

    nodetype : type, optional
        type to cast the node ID to
    edgetype : type, optional
        type to cast the edge ID to

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
        raise XGIError("Invalid dataset specifier!")

    r = requests.get(index[dataset]["url"])

    return convert.dict_to_hypergraph(r.json(), nodetype=nodetype, edgetype=edgetype)