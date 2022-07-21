"""
**********
Matplotlib
**********

Draw hypergraphs with matplotlib.
"""

from itertools import combinations
from collections.abc import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

from .. import convert
from ..classes import Hypergraph, SimplicialComplex, max_edge_order
from ..exception import XGIError
from .layout import barycenter_spring_layout

__all__ = [
    "draw",
]


def draw(
    H,
    pos=None,
    cmap=None,
    ax=None,
    edge_lc="black",
    edge_lw=1.5,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=0.03,
):
    """Draw hypergraph or simplicial complex.

    Parameters
    ----
    H : Hypergraph or SimplicialComplex.

    pos : dict (default=None)
        If passed, this dictionary of positions d:(x,y) is used for placing the 0-simplices.
        If None (default), use the `barycenter_spring_layout` to compute the positions.

    cmap : `matplotlib.colors.ListedColormap`, default: `matplotlib.cm.Paired`
        The qualitative colormap used to distinguish edges of different order.
        If a continuous `matplotlib.colors.LinearSegmentedColormap` is given, it is discretized first.

    ax : matplotlib.pyplot.axes (default=None)

    edge_lc : color (str, dict, or iterable, default='black')
    Color of the edges (dyadic links and borders of the hyperedges).  If str, use the
    same color for all edges.  If a dict, must contain (edge_id: color_str) pairs.  If
    iterable, assume the colors are specified in the same order as the edges are found
    in H.edges.

    edge_lw :  float (default=1.5)
    Line width of edges of order 1 (dyadic links).

    node_fc : color (str, dict, or iterable, default='white')
    Color of the nodes.  If str, use the same color for all nodes.  If a dict, must
    contain (node_id: color_str) pairs.  If other iterable, assume the colors are
    specified in the same order as the nodes are found in H.nodes.

    node_ec : color (dict or str, default='black')
    Color of node borders.  If str, use the same color for all nodes.  If a dict, must
    contain (node_id: color_str) pairs.  If other iterable, assume the colors are
    specified in the same order as the nodes are found in H.nodes.

    node_lw : float (default=1.0)
    Line width of the node borders.

    node_size : float (default=0.03)
    Size of the nodes.

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph()
    >>> H.add_edges_from([[1,2,3],[3,4],[4,5,6,7],[7,8,9,10,11]])
    >>> xgi.draw(H, pos=xgi.barycenter_spring_layout(H))

    """

    if pos is None:
        pos = barycenter_spring_layout(H)

    # Note Iterable covers lists, tuples, ranges, generators, np.ndarrays, etc
    if not isinstance(node_fc, dict):
        if isinstance(node_fc, str):
            node_fc = {n: node_fc for n in H.nodes}
        elif isinstance(node_fc, Iterable):
            node_fc = {n: node_fc[idx] for idx, n in enumerate(H.nodes)}
        else:
            raise TypeError(
                f"node_fc must be dict, str, or iterable, received {type(node_fc)}"
            )

    if not isinstance(node_ec, dict):
        if isinstance(node_ec, str):
            node_ec = {n: node_ec for n in H.nodes}
        elif isinstance(node_ec, Iterable):
            node_ec = {n: node_ec[idx] for idx, n in enumerate(H.nodes)}
        else:
            raise TypeError(
                f"node_ec must be dict, str, or iterable, received {type(node_ec)}"
            )

    if not isinstance(edge_lc, dict):
        if isinstance(edge_lc, str):
            edge_lc = {n: edge_lc for n in H.edges}
        elif isinstance(edge_lc, Iterable):
            edge_lc = {n: edge_lc[idx] for idx, n in enumerate(H.edges)}
        else:
            raise TypeError(
                f"edge_lc must be dict, str, or iterable, received {type(edge_lc)}"
            )

    def CCW_sort(p):
        """
        Sort the input 2D points counterclockwise.
        """
        p = np.array(p)
        mean = np.mean(p, axis=0)
        d = p - mean
        s = np.arctan2(d[:, 0], d[:, 1])
        return p[np.argsort(s), :]

    # Defining colors, one for each dimension
    d_max = max_edge_order(H)
    if cmap is None:
        cmap = cm.Paired
        colors = [cmap(i) for i in range(0, d_max + 1)]
    else:
        if type(cmap) == ListedColormap:
            # The colormap is already discrete
            colors = [cmap(i) for i in range(0, d_max + 1)]
        elif type(cmap) == LinearSegmentedColormap:
            # I need to discretize the given colormap
            color_range = np.linspace(0.1, 0.9, d_max)
            colors = [cmap(i) for i in color_range]

    if ax is None:
        ax = plt.gca()
    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    if isinstance(H, Hypergraph):
        # Looping over the hyperedges of different order (reversed) -- nodes will be plotted separately
        for d in reversed(range(1, d_max + 1)):
            if d == 1:
                # Drawing the edges
                for idx, he in H.edges.filterby("order", d).members(dtype=dict).items():
                    he = list(he)
                    x_coords = [pos[he[0]][0], pos[he[1]][0]]
                    y_coords = [pos[he[0]][1], pos[he[1]][1]]
                    line = plt.Line2D(
                        x_coords, y_coords, color=edge_lc[idx], lw=edge_lw
                    )
                    ax.add_line(line)

            else:
                # Hyperedges of order d (d=1: links, etc.)
                for idx, he in H.edges.filterby("order", d).members(dtype=dict).items():
                    # Filling the polygon
                    coordinates = [[pos[n][0], pos[n][1]] for n in he]
                    # Sorting the points counterclockwise (needed to have the correct filling)
                    sorted_coordinates = CCW_sort(coordinates)
                    obj = plt.Polygon(
                        sorted_coordinates,
                        edgecolor=edge_lc[idx],
                        facecolor=colors[d - 1],
                        alpha=0.4,
                        lw=0.5,
                    )
                    ax.add_patch(obj)
    elif isinstance(H, SimplicialComplex):
        # I will only plot the maximal simplices, so I convert the SC to H
        H_ = convert.from_simplicial_complex_to_hypergraph(H)

        # Looping over the hyperedges of different order (reversed) -- nodes will be plotted separately
        for d in reversed(range(1, d_max + 1)):
            if d == 1:
                # Drawing the edges
                for idx, he in (
                    H_.edges.filterby("order", d).members(dtype=dict).items()
                ):
                    he = list(he)
                    x_coords = [pos[he[0]][0], pos[he[1]][0]]
                    y_coords = [pos[he[0]][1], pos[he[1]][1]]
                    line = plt.Line2D(
                        x_coords, y_coords, color=edge_lc[idx], lw=edge_lw
                    )
                    ax.add_line(line)
            else:
                # Hyperedges of order d (d=1: links, etc.)
                for idx, he in (
                    H_.edges.filterby("order", d).members(dtype=dict).items()
                ):
                    # Filling the polygon
                    coordinates = [[pos[n][0], pos[n][1]] for n in he]
                    # Sorting the points counterclockwise (needed to have the correct filling)
                    sorted_coordinates = CCW_sort(coordinates)
                    obj = plt.Polygon(
                        sorted_coordinates,
                        edgecolor=edge_lc[idx],
                        facecolor=colors[d - 1],
                        alpha=0.4,
                        lw=0.5,
                    )
                    ax.add_patch(obj)
                    # Drawing the all the edges within
                    for i, j in combinations(sorted_coordinates, 2):
                        x_coords = [i[0], j[0]]
                        y_coords = [i[1], j[1]]
                        line = plt.Line2D(
                            x_coords, y_coords, color=edge_lc[idx], lw=edge_lw
                        )
                        ax.add_line(line)
    else:
        raise XGIError("The input must be a SimplicialComplex or Hypergraph")

    # Drawing the nodes
    for i in list(H.nodes):
        (x, y) = pos[i]
        circ = plt.Circle(
            [x, y],
            radius=node_size,
            lw=node_lw,
            zorder=d_max + 1,
            ec=node_ec[i],
            fc=node_fc[i],
        )
        ax.add_patch(circ)
