"""Algorithms to compute node positions for drawing."""

import random

import networkx as nx
import numpy as np
from numpy.linalg import inv, svd

from .. import convert
from ..core import SimplicialComplex

__all__ = [
    "random_layout",
    "pairwise_spring_layout",
    "barycenter_spring_layout",
    "weighted_barycenter_spring_layout",
    "pca_transform",
    "circular_layout",
    "spiral_layout",
    "barycenter_kamada_kawai_layout",
]


def random_layout(H, center=None, seed=None):
    """Position nodes uniformly at random in the unit square.

    For every node, a position is generated by choosing each of dim coordinates
    uniformly at random on the interval [0.0, 1.0).  NumPy (http://scipy.org) is
    required for this function.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex
        A position will be assigned to every node in HG.
    center : array-like, optional
        Coordinate pair around which to center the layout.
        If None (default), does not center the positions.
    seed : int, optional
        Set the random state for deterministic node layouts.
        If int, `seed` is the seed used by the random number generator,
        If None (default), random numbers are sampled from the
        numpy random number generator without initialization.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node

    See Also
    --------
    pairwise_spring_layout
    barycenter_spring_layout
    weighted_barycenter_spring_layout

    Notes
    -----
    This function proceeds exactly as NetworkX does.

    Examples
    --------
    >>> import xgi
    >>> N = 50
    >>> ps = [0.1, 0.01]
    >>> H = xgi.random_hypergraph(N, ps)
    >>> pos = xgi.random_layout(H)

    """
    import numpy as np

    if isinstance(H, SimplicialComplex):
        H = convert.from_max_simplices(H)

    if seed is not None:
        np.random.seed(seed)

    H, center = nx.drawing.layout._process_params(H, center, 2)
    pos = np.random.rand(len(H), 2) + center
    pos = pos.astype(np.float32)
    pos = dict(zip(H, pos))

    return pos


def pairwise_spring_layout(H, seed=None, k=None, **kwargs):
    """
    Position the nodes using Fruchterman-Reingold force-directed
    algorithm using the graph projection of the hypergraph
    or the hypergraph constructed from the simplicial complex.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex
        A position will be assigned to every node in H.
    seed : int, optional
        Set the random state for deterministic node layouts.
        If int, `seed` is the seed used by the random number generator,
        If None (default), random numbers are sampled from the
        numpy random number generator without initialization.
    k : float
        The spring constant of the links. When k=None (default),
        k = 1/sqrt(N). For more information, see the documentation
        for the NetworkX spring_layout() function.
    kwargs :
        Optional arguments for the NetworkX spring_layout() function.
        See https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node

    See Also
    --------
    random_layout
    barycenter_spring_layout
    weighted_barycenter_spring_layout

    Notes
    -----
    If a simplicial complex is provided the results will be based on the
    hypergraph constructed from its maximal simplices.

    Examples
    --------
    >>> import xgi
    >>> N = 50
    >>> ps = [0.1, 0.01]
    >>> H = xgi.random_hypergraph(N, ps)
    >>> pos = xgi.pairwise_spring_layout(H)
    """

    if seed is not None:
        random.seed(seed)

    if isinstance(H, SimplicialComplex):
        H = convert.from_max_simplices(H)
    G = convert.convert_to_graph(H)
    pos = nx.spring_layout(G, seed=seed, k=k, **kwargs)
    return pos


def _augmented_projection(H, weighted=False):
    """Augmented version of the the graph projection of the hypergraph
    (or simplicial complex), where phantom nodes (barycenters) are created
    for each edge composed by more than two nodes.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex
    weighted : bool (default=False)
               If True weights are assigned to all hyperedges of order d=1 (links)
               and to all connections to phantom nodes within each hyperedge of
               order d>1 to keep them together. Weights scale as the order d.


    Returns
    -------
    G : networkx.Graph
        The augmented version of the graph projection
    """
    # Creating the projected networkx Graph, I will fill it manually
    G = nx.Graph()

    # Adding real nodes
    G.add_nodes_from(list(H.nodes), bipartite="node")

    # Adding phantom nodes and connections therein
    # I will start from the first int node-label available
    try:
        phantom_node_id = max([n for n in H.nodes if isinstance(n, int)]) + 1
    except ValueError:
        # The list of node-labels has no integers, so I start from 0
        phantom_node_id = 0

    edges = H.edges.filterby("order", 1, "geq")
    # Looping over the hyperedges of different order
    for he_id, members in edges.members(dtype=dict).items():
        d = len(members) - 1
        # Adding one phantom node for each hyperedge
        G.add_node(phantom_node_id, bipartite="hyperedge")
        # and linking it to the nodes of the hyperedge
        for n in members:
            if weighted:
                G.add_edge(phantom_node_id, n, weight=d)
            else:
                G.add_edge(phantom_node_id, n)
        phantom_node_id += 1
    return G


def barycenter_spring_layout(
    H, return_phantom_graph=False, seed=None, k=None, **kwargs
):
    """
    Position the nodes using Fruchterman-Reingold force-directed
    algorithm using an augmented version of the the graph projection
    of the hypergraph (or simplicial complex), where phantom nodes
    (barycenters) are created for each edge composed by more than two nodes.
    If a simplicial complex is provided the results will be based on the
    hypergraph constructed from its maximal simplices.

    Parameters
    ----------
    H : xgi Hypergraph or SimplicialComplex
        A position will be assigned to every node in H.
    return_phantom_graph: bool (default=False)
        If True the function returns also the augmented version of the
        the graph projection of the hypergraph (or simplicial complex).
    seed : int, RandomState instance or None  optional (default=None)
        Set the random state for deterministic node layouts.
        If int, `seed` is the seed used by the random number generator,
        If None (default), random numbers are sampled from the
        numpy random number generator without initialization.
    k : float
        The spring constant of the links. When k=None (default),
        k = 1/sqrt(N). For more information, see the documentation
        for the NetworkX spring_layout() function.
    kwargs :
        Optional arguments for the NetworkX spring_layout() function.
        See https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html


    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node

    See Also
    --------
    random_layout
    pairwise_spring_layout
    weighted_barycenter_spring_layout

    Examples
    --------
    >>> import xgi
    >>> N = 50
    >>> ps = [0.1, 0.01]
    >>> H = xgi.random_hypergraph(N, ps)
    >>> pos = xgi.barycenter_spring_layout(H)
    """
    if seed is not None:
        random.seed(seed)

    if isinstance(H, SimplicialComplex):
        H = convert.from_max_simplices(H)

    G = _augmented_projection(H)

    # Creating a dictionary for the position of the nodes with the standard spring
    # layout
    pos_with_phantom_nodes = nx.spring_layout(G, seed=seed, k=k, **kwargs)

    # Retaining only the positions of the real nodes
    pos = {k: pos_with_phantom_nodes[k] for k in list(H.nodes)}

    if return_phantom_graph:
        return pos, G
    else:
        return pos


def weighted_barycenter_spring_layout(
    H, return_phantom_graph=False, seed=None, k=None, **kwargs
):
    """Position the nodes using Fruchterman-Reingold force-directed algorithm.

    This uses an augmented version of the the graph projection of the hypergraph (or
    simplicial complex), where phantom nodes (barycenters) are created for each edge of
    order d>1 (composed by more than two nodes).  Weights are assigned to all hyperedges
    of order 1 (links) and to all connections to phantom nodes within each hyperedge to
    keep them together. Weights scale as the order d.  If a simplicial complex is
    provided the results will be based on the hypergraph constructed from its maximal
    simplices.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex
        A position will be assigned to every node in H.
    return_phantom_graph: bool (default=False)
        If True the function returns also the augmented version of the
        the graph projection of the hypergraph (or simplicial complex).
    seed : int, RandomState instance or None  optional (default=None)
        Set the random state for deterministic node layouts.
        If int, `seed` is the seed used by the random number generator,
        If None (default), random numbers are sampled from the
        numpy random number generator without initialization.
    k : float
        The spring constant of the links. When k=None (default),
        k = 1/sqrt(N). For more information, see the documentation
        for the NetworkX spring_layout() function.
    kwargs :
        Optional arguments for the NetworkX spring_layout() function.
        See https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html


    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node

    See Also
    --------
    random_layout
    pairwise_spring_layout
    barycenter_spring_layout

    Examples
    --------
    >>> import xgi
    >>> N = 50
    >>> ps = [0.1, 0.01]
    >>> H = xgi.random_hypergraph(N, ps)
    >>> pos = xgi.weighted_barycenter_spring_layout(H)

    """
    if seed is not None:
        random.seed(seed)

    if isinstance(H, SimplicialComplex):
        H = convert.from_max_simplices(H)

    G = _augmented_projection(H, weighted=True)

    # Creating a dictionary for node position with the standard spring layout
    pos_with_phantom_nodes = nx.spring_layout(
        G, weight="weight", seed=seed, k=k, **kwargs
    )

    # Retaining only the positions of the real nodes
    pos = {k: pos_with_phantom_nodes[k] for k in list(H.nodes)}

    if return_phantom_graph:
        return pos, G
    else:
        return pos


def pca_transform(pos, theta=0, degrees=True):
    """Transforms the positions of the nodes based on the
    principal components.

    Parameters
    ----------
    pos : dict of numpy arrays
        The output from any layout function
    theta : float, optional
        The angle between the horizontal axis and the principal axis
        measured counterclockwise, by default 0.
    degrees : bool, optional
        Whether the angle specified is in degrees (True)
        or in radians (False), by default True.

    Returns
    -------
    dict of numpy arrays
        The transformed positions.

    See Also
    --------
    random_layout
    pairwise_spring_layout
    barycenter_spring_layout
    weighted_barycenter_spring_layout
    """
    p = np.array(list(pos.values()))
    _, _, w = svd(p)

    pa = inv(w)

    if degrees:
        theta *= np.pi / 180

    r = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    t_p = p.dot(pa).dot(r).T
    x = t_p[0]
    y = t_p[1]

    return {n: np.array([x[i], y[i]]) for i, n in enumerate(pos.keys())}


def circular_layout(H, center=None, radius=None):
    """Position nodes on a circle.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex
        A position will be assigned to every node in H.
    center : array-like or None
        Coordinate pair around which to center the layout.
        If None set to [0,0]
    radius : float or None (default=None)
        Radius of the circle on which to draw the nodes,
        if None set to 1.0.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node
    """
    if center is None:
        center = [0, 0]

    if radius is None:
        radius = 1.0

    if H.num_nodes == 0:
        pos = {}
    elif H.num_nodes == 1:
        pos = {list(H.nodes)[0]: center}
    else:
        theta = np.linspace(0, 1, len(H) + 1)[:-1] * 2 * np.pi
        pos = np.column_stack(
            [radius * np.cos(theta) + center[0], radius * np.sin(theta) + center[1]]
        )
        pos = dict(zip(list(H.nodes), pos))

    return pos


def spiral_layout(H, center=None, resolution=0.35, equidistant=False):
    """Position nodes in a spiral layout.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex
        A position will be assigned to every node in H.
    center : array-like or None
        Coordinate pair around which to center the layout.
        If None set to [0,0]
    resolution : float, default=0.35
        The compactness of the spiral layout returned.
        Lower values result in more compressed spiral layouts.
    equidistant : bool, default=False
        If True, nodes will be positioned equidistant from each other
        by decreasing angle further from center.
        If False, nodes will be positioned at equal angles
        from each other by increasing separation further from center.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node
    """
    if center is None:
        center = [0, 0]

    if H.num_nodes == 0:
        pos = {}
        return pos
    elif H.num_nodes == 1:
        pos = {list(H.nodes)[0]: center}
        return pos

    pos = []
    if equidistant:
        chord = 1
        step = 0.5
        theta = resolution
        theta += chord / (step * theta)
        for _ in range(len(H)):
            r = step * theta
            theta += chord / r
            pos.append([np.cos(theta) * r + center[0], np.sin(theta) * r + center[1]])
    else:
        dist = np.arange(len(H), dtype=float)
        angle = resolution * dist
        pos = np.transpose(dist * np.array([np.cos(angle), np.sin(angle)]))

    pos = dict(zip(list(H.nodes), pos))

    return pos


def barycenter_kamada_kawai_layout(H, return_phantom_graph=False, **kwargs):
    """Position nodes using Kamada-Kawai path-length cost-function
    using an augmented version of the the graph projection
    of the hypergraph (or simplicial complex), where phantom nodes
    (barycenters) are created for each edge composed by more than two nodes.
    If a simplicial complex is provided the results will be based on the
    hypergraph constructed from its maximal simplices.

    Parameters
    ----------
    H : xgi Hypergraph or SimplicialComplex
        A position will be assigned to every node in H.
    return_phantom_graph: bool (default=False)
        If True the function returns also the augmented version of the
        the graph projection of the hypergraph (or simplicial complex).
    kwargs :
        Optional arguments for the NetworkX spring_layout() function.
        See https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node
    """
    if isinstance(H, SimplicialComplex):
        H = convert.from_max_simplices(H)

    G = _augmented_projection(H)

    # Creating a dictionary for the position of the nodes with the standard spring layout
    pos_with_phantom_nodes = nx.kamada_kawai_layout(G, **kwargs)

    # Retaining only the positions of the real nodes
    pos = {k: pos_with_phantom_nodes[k] for k in list(H.nodes)}

    if return_phantom_graph:
        return pos, G
    else:
        return pos
