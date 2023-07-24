from ..core import Hypergraph, SimplicialComplex
from ..exception import XGIError
from ..generators import empty_simplicial_complex

__all__ = ["from_simplex_dict", "from_max_simplices"]


def from_simplex_dict(d, create_using=None):
    """Creates a Simplicial Complex from a dictionary of simplices,
    if the subfaces of existing simplices are not given in the dict
    then the function adds them with integer IDs.


    Parameters
    ----------
    d : dict
        A dictionary where the keys are simplex IDs and the values
        are containers of nodes specifying the simplices.
    create_using : SimplicialComplex constructor, optional
        The simplicial complex object to add the data to, by default None

    Returns
    -------
    SimplicialComplex object
        The constructed simplicial complex object

    """
    SC = empty_simplicial_complex(create_using)
    SC.add_simplices_from((members, uid) for uid, members in d.items())
    return SC


def from_max_simplices(SC):
    """Returns a hypergraph constructed from the
    maximal simplices of the provided simplicial complex.

    Parameters
    ----------
    SC : SimplicialComplex

    Returns
    -------
    Hypergraph

    """
    if type(SC) != SimplicialComplex:
        raise XGIError("The input must be a SimplicialComplex")

    max_simplices = SC.edges.maximal()
    H = Hypergraph()
    H.add_nodes_from(SC.nodes)  # to keep node order and isolated nodes
    H.add_edges_from([list(SC.edges.members(e)) for e in max_simplices])
    return H
