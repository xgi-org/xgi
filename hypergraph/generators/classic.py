"""Generators for some classic graphs.
The typical graph builder function is called as follows:
>>> G = nx.complete_graph(100)
returning the complete graph on n nodes labeled 0, .., 99
as a simple graph. Except for `empty_graph`, all the functions
in this module return a Graph class (i.e. a simple, undirected graph).
"""

import itertools

import hypergraph as hg
from hypergraph.classes import Hypergraph
from hypergraph.exception import HypergraphError

__all__ = [
    "empty_hypergraph",
]


def empty_hypergraph(create_using=None, default=Hypergraph):
    """Returns the empty graph with n nodes and zero edges.
    Parameters
    ----------
    n : int or iterable container of nodes (default = 0)
        If n is an integer, nodes are from `range(n)`.
        If n is a container of nodes, those nodes appear in the graph.
    create_using : Graph Instance, Constructor or None
        Indicator of type of graph to return.
        If a Graph-type instance, then clear and use it.
        If None, use the `default` constructor.
        If a constructor, call it to create an empty graph.
    default : Graph constructor (optional, default = nx.Graph)
        The constructor to use if create_using is None.
        If None, then nx.Graph is used.
        This is used when passing an unknown `create_using` value
        through your home-grown function to `empty_graph` and
        you want a default constructor other than nx.Graph.
    Examples
    --------
    >>> G = nx.empty_graph(10)
    >>> G.number_of_nodes()
    10
    >>> G.number_of_edges()
    0
    >>> G = nx.empty_graph("ABC")
    >>> G.number_of_nodes()
    3
    >>> sorted(G)
    ['A', 'B', 'C']
    Notes
    -----
    The variable create_using should be a Graph Constructor or a
    "graph"-like object. Constructors, e.g. `nx.Graph` or `nx.MultiGraph`
    will be used to create the returned graph. "graph"-like objects
    will be cleared (nodes and edges will be removed) and refitted as
    an empty "graph" with nodes specified in n. This capability
    is useful for specifying the class-nature of the resulting empty
    "graph" (i.e. Graph, DiGraph, MyWeirdGraphClass, etc.).
    The variable create_using has three main uses:
    Firstly, the variable create_using can be used to create an
    empty digraph, multigraph, etc.  For example,
    >>> n = 10
    >>> G = nx.empty_graph(n, create_using=nx.DiGraph)
    will create an empty digraph on n nodes.
    Secondly, one can pass an existing graph (digraph, multigraph,
    etc.) via create_using. For example, if G is an existing graph
    (resp. digraph, multigraph, etc.), then empty_graph(n, create_using=G)
    will empty G (i.e. delete all nodes and edges using G.clear())
    and then add n nodes and zero edges, and return the modified graph.
    Thirdly, when constructing your home-grown graph creation function
    you can use empty_graph to construct the graph by passing a user
    defined create_using to empty_graph. In this case, if you want the
    default constructor to be other than nx.Graph, specify `default`.
    >>> def mygraph(n, create_using=None):
    ...     G = nx.empty_graph(n, create_using, nx.MultiGraph)
    ...     G.add_edges_from([(0, 1), (0, 1)])
    ...     return G
    >>> G = mygraph(3)
    >>> G.is_multigraph()
    True
    >>> G = mygraph(3, nx.Graph)
    >>> G.is_multigraph()
    False
    See also create_empty_copy(G).
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

    # n_name, nodes = n
    # H.add_nodes_from(nodes)
    return H
