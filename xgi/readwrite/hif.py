"""Read from and write to the HIF Standard.

For more information on the HIF standard, see the
HIF `project <https://github.com/pszufe/HIF_validators>`_.
"""

import json

from ..convert import from_hif_dict, to_hif_dict

__all__ = ["write_hif", "read_hif"]


def write_hif(H, path):
    """
    A function to write a higher-order network according to the HIF standard.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    H: Hypergraph, DiHypergraph, or SimplicialComplex object
        The specified higher-order network
    path: string
        The path of the file to read from
    """
    # initialize empty data
    data = to_hif_dict(H)

    datastring = json.dumps(data, indent=2)

    with open(path, "w") as output_file:
        output_file.write(datastring)


def read_hif(path, nodetype=None, edgetype=None):
    """
    A function to read a file created according to the HIF format.

    For more information, see the HIF `project <https://github.com/pszufe/HIF_validators>`_.

    Parameters
    ----------
    data: dict
        A dictionary in the hypergraph JSON format
    nodetype: type, optional
        type that the node IDs will be cast to
    edgetype: type, optional
        type that the edge IDs will be cast to

    Returns
    -------
    A Hypergraph, SimplicialComplex, or DiHypergraph object
        The loaded network
    """
    with open(path) as file:
        data = json.loads(file.read())

    return from_hif_dict(data, nodetype=nodetype, edgetype=edgetype)
