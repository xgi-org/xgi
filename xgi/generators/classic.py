"""Generators for some classic hypergraphs. All the functions
in this module return a Hypergraph class (i.e. a simple, undirected hypergraph).
"""

from xgi.classes import Hypergraph

__all__ = [
    "empty_hypergraph",
]


def empty_hypergraph(create_using=None, default=Hypergraph):
    """Returns the empty hypergraph with zero nodes and edges.

    Parameters
    ----------
    create_using : Hypergraph Instance, Constructor or None
        If None, use the `default` constructor.
        If a constructor, call it to create an empty hypergraph.
    default : Hypergraph constructor (optional, default = xgi.Hypergraph)
        The constructor to use if create_using is None.
        If None, then xgi.Hypergraph is used.

    Returns
    -------
    Hypergraph object
        An empty hypergraph

    Examples
    --------
    >>> import xgi
    >>> H = xgi.empty_hypergraph()
    >>> H.num_nodes
    0
    >>> H.num_edges
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
