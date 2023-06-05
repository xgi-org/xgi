"""Load a metabolic network from the BiGG models database."""

from ..utils import request_json_from_url, request_json_from_url_cached

__all__ = ["load_bigg_data"]


def load_bigg_data(
    dataset=None,
    cache=True,
):
    """Load a metabolic network from the BiGG models database.

    The Biochemical, Genetic and Genomic (BiGG) knowledge base
    is hosted at http://bigg.ucsd.edu/. It contains metabolic
    reaction networks at the genome scale.

    Parameters
    ----------
    dataset : str, default: None
        Dataset name. Valid options are the "bigg_id" tags in
        http://bigg.ucsd.edu/api/v2/models. If None, prints
        the list of available datasets.
    cache : bool, optional
        Whether to cache the input data

    Returns
    -------
    DiHypergraph
        The loaded dihypergraph.

    Raises
    ------
    XGIError
       The specified dataset does not exist.

    References
    ----------
    Zachary A. King, Justin Lu, Andreas Dräger,
    Philip Miller, Stephen Federowicz, Joshua A. Lerman,
    Ali Ebrahim, Bernhard O. Palsson, Nathan E. Lewis
    Nucleic Acids Research, Volume 44, Issue D1,
    4 January 2016, Pages D515–D522,
    https://doi.org/10.1093/nar/gkv1049
    """

    index_url = "http://bigg.ucsd.edu/api/v2/models"
    base_url = "http://bigg.ucsd.edu/static/models/"

    # If no dataset is specified, print a list of the available datasets.
    if dataset is None:
        index_data = request_json_from_url(index_url)
        ids = []
        for entry in index_data["results"]:
            ids.append(entry["bigg_id"])
        print("Available datasets are the following:")
        print(*ids, sep="\n")
        return

    if cache:
        data = request_json_from_url_cached(base_url + dataset + ".json")
    else:
        data = request_json_from_url(base_url + dataset + ".json")

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

    DH["name"] = d["id"]

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

        DH.add_edge((tail, head), id=r["id"], name=r["name"])

    return DH
