"""Generators for some classic hypergraphs. All the functions
in this module return a Hypergraph class (i.e. a simple, undirected hypergraph).
"""

from hypergraph.classes import Hypergraph
from hypergraph.exception import HypergraphError

__all__ = [
    "empty_hypergraph",
]


def empty_hypergraph(create_using=None, default=Hypergraph):
    """Returns the empty hypergraph with zero nodes and edges.

    Parameters
    ----------
    create_using : Hypergraph Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty graph.
    default : Hypergraph constructor (optional, default = hg.Hypergraph)
        The constructor to use if create_using is None.
        If None, then hg.Hypergraph is used.

    Example
    -------
        >>> import hypergraph as hg
        >>> H = hg.empty_hypergraph()
        >>> H.number_of_nodes()
        0
        >>> H.number_of_edges()
        0
    """
    if create_using is None:
        H = default()
    elif hasattr(create_using, "_node"):
        # create_using is a Hypergraph object
        create_using.clear()
        H = create_using
    else:
        # try create_using as constructor
        H = create_using()
    return H
