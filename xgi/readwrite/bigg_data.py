"""Load a metabolic network from the BiGG models database."""

from warnings import warn

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

    We represent metabolites as nodes and metabolic reactions
    as directed edges where reactants are the tail of the directed
    edge and the products are the head of the directed edge.

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

    index_data = request_json_from_url(index_url)

    # If no dataset is specified, print a list of the available datasets.
    if dataset is None:
        ids = []
        for entry in index_data["results"]:
            ids.append(entry["bigg_id"])
        print("Available datasets are the following:")
        print(*ids, sep="\n")
        return

    if cache:
        model_data = request_json_from_url_cached(base_url + dataset + ".json")
    else:
        model_data = request_json_from_url(base_url + dataset + ".json")

    return _bigg_to_dihypergraph(index_data, model_data)


def _bigg_to_dihypergraph(d_index, d_model):
    """Convert a BIGG-formatted dict to dihypergraph.

    Parameters
    ----------
    d : dict
        A BIGG-formatted dict

    Returns
    -------
    DiHypergraph
        The dihypergraph from the selected BIGG model.

    Notes
    -----
    The code for parsing a metabolic reaction is rewritten
    from a function by @pietrotraversa.

    We use the `lower_bound` and `upper_bound` variables to
    determine whether a reaction is a forward, reverse,
    or reversible reaction.
    """
    from .. import DiHypergraph

    DH = DiHypergraph()

    id = d_model["id"]

    DH["name"] = id

    info = next((item for item in d_index["results"] if item["bigg_id"] == id), None)
    DH["organism"] = info["organism"]

    for m in d_model["metabolites"]:
        DH.add_node(m["id"], name=m["name"])

    for r in d_model["reactions"]:
        l = r["lower_bound"]
        u = r["upper_bound"]

        reactants = set()
        products = set()

        # forward direction
        if l >= 0 and u > 0:
            for m, val in r["metabolites"].items():
                if val > 0:
                    products.add(m)
                elif val <= 0:
                    reactants.add(m)

            if not reactants and not products:
                warn(f"{r['id']} is an empty reaction!")
                continue
            DH.add_edge((reactants, products), id=r["id"], name=r["name"])

        # reverse direction
        if l < 0 and u <= 0:
            for m, val in r["metabolites"].items():
                if val >= 0:
                    reactants.add(m)
                elif val < 0:
                    products.add(m)

            if not reactants and not products:
                warn(f"{r['id']} is an empty reaction!")
                continue
            DH.add_edge((reactants, products), id=r["id"], name=r["name"])

        # reversible
        if l < 0 and u > 0:
            for m, val in r["metabolites"].items():
                if val > 0:
                    products.add(m)
                elif val < 0:
                    reactants.add(m)

            if not reactants and not products:
                warn(f"{r['id']} is an empty reaction!")
                continue
            # add forward reaction
            DH.add_edge((reactants, products), id=r["id"], name=r["name"])
            # add reverse reaction
            DH.add_edge(
                (products, reactants), id=str(r["id"]) + "_reverse", name=r["name"]
            )

    return DH
