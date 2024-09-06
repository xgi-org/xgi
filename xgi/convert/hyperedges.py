"""Methods for converting to and from hyperedge lists."""

from ..core import SimplicialComplex
from ..generators import empty_hypergraph

__all__ = [
    "from_hyperedge_dict",
    "to_hyperedge_dict",
    "from_hyperedge_list",
    "to_hyperedge_list",
]


def from_hyperedge_dict(d, create_using=None):
    """Creates a hypergraph from a dictionary of hyperedges

    Parameters
    ----------
    d : dict
        A dictionary where the keys are edge IDs and the values
        are containers of nodes specifying the edges.
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None

    Returns
    -------
    Hypergraph object
        The constructed hypergraph object

    See Also
    --------
    to_hyperedge_dict
    from_hyperedge_list
    to_hyperedge_list
    """
    H = empty_hypergraph(create_using)
    H.add_edges_from((members, uid) for uid, members in d.items())
    return H


def to_hyperedge_dict(H):
    """Outputs a hyperedge dictionary

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    dict
        A dictionary where the keys are edge IDs and the values
        are sets of nodes specifying the edges.

    See Also
    --------
    from_hyperedge_dict
    to_hyperedge_list
    from_hyperedge_list
    """
    return H.edges.members(dtype=dict)


def from_hyperedge_list(d, create_using=None, max_order=None):
    """Generate a hypergraph from a list of lists.

    Parameters
    ----------
    d : list of iterables
        A hyperedge list
    create_using : Hypergraph constructor, optional
        The hypergraph to add the edges to, by default None

    Returns
    -------
    Hypergraph object
        The constructed hypergraph object

    See Also
    --------
    to_hyperedge_list
    from_hyperedge_dict
    to_hyperedge_dict
    """
    H = empty_hypergraph(create_using)
    if isinstance(H, SimplicialComplex):
        H.add_simplices_from(d, max_order=max_order)
    else:
        H.add_edges_from(d)
    return H


def to_hyperedge_list(H):
    """Generate a hyperedge list from a hypergraph.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest

    Returns
    -------
    list of sets
        The hyperedge list

    See Also
    --------
    from_hyperedge_list
    to_hyperedge_dict
    from_hyperedge_dict
    """
    return H.edges.members()
