"""
**********
Matplotlib
**********

Draw hypergraphs with matplotlib.
"""

from collections.abc import Iterable
from itertools import combinations

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
    edge_fc=None,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=10,
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
    Line width of the node borders in pixels.

    node_size : float (default=0.03)
    Radius of the nodes in pixels

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph()
    >>> H.add_edges_from([[1,2,3],[3,4],[4,5,6,7],[7,8,9,10,11]])
    >>> xgi.draw(H, pos=xgi.barycenter_spring_layout(H))

    """

    if pos is None:
        pos = barycenter_spring_layout(H)

    if ax is None:
        ax = plt.gca()
    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    d_max = max_edge_order(H)

    if isinstance(H, Hypergraph):
        draw_xgi_hyperedges(ax, H, pos, edge_lc, edge_lw, edge_fc, d_max)

    elif isinstance(H, SimplicialComplex):
        draw_xgi_complexes(ax, H, pos, edge_lc, edge_lw, edge_fc, d_max)
    else:
        raise XGIError("The input must be a SimplicialComplex or Hypergraph")

    draw_xgi_nodes(ax, H, pos, node_fc, node_ec, node_lw, node_size, d_max)


def draw_xgi_nodes(ax, H, pos, node_fc, node_ec, node_lw, node_size, zorder):
    # Note Iterable covers lists, tuples, ranges, generators, np.ndarrays, etc
    node_fc = _arg_to_dict(node_fc, H.nodes)
    node_ec = _arg_to_dict(node_ec, H.nodes)
    node_lw = _arg_to_dict(node_lw, H.nodes)
    node_size = _arg_to_dict(node_size, H.nodes)

    for i in H.nodes:
        (x, y) = pos[i]
        ax.scatter(
            x,
            y,
            s=node_size[i] ** 2,
            c=node_fc[i],
            edgecolors=node_ec[i],
            linewidths=node_lw[i],
            zorder=zorder,
        )


def draw_xgi_hyperedges(ax, H, pos, edge_lc, edge_lw, edge_fc, d_max):
    edge_lc = _arg_to_dict(edge_lc, H.edges)
    edge_lw = _arg_to_dict(edge_lw, H.edges)

    edge_fc = _color_edges(edge_fc, H)
    # Looping over the hyperedges of different order (reversed) -- nodes will be plotted separately

    for id, he in H.edges.members(dtype=dict).items():
        d = len(he) - 1
        if d == 1:
            # Drawing the edges
            he = list(he)
            x_coords = [pos[he[0]][0], pos[he[1]][0]]
            y_coords = [pos[he[0]][1], pos[he[1]][1]]
            line = plt.Line2D(
                x_coords, y_coords, color=edge_lc[id], lw=edge_lw[id], zorder=d_max - 1
            )
            ax.add_line(line)

        else:
            # Hyperedges of order d (d=1: links, etc.)
            # Filling the polygon
            coordinates = [[pos[n][0], pos[n][1]] for n in he]
            # Sorting the points counterclockwise (needed to have the correct filling)
            sorted_coordinates = _CCW_sort(coordinates)
            obj = plt.Polygon(
                sorted_coordinates,
                edgecolor=edge_lc[id],
                facecolor=edge_fc[id],
                alpha=0.4,
                lw=0.5,
                zorder=d_max - d,
            )
            ax.add_patch(obj)


def draw_xgi_complexes(ax, H, pos, edge_lc, edge_lw, edge_fc, d_max):
    # I will only plot the maximal simplices, so I convert the SC to H
    H_ = convert.from_simplicial_complex_to_hypergraph(H)

    edge_lc = _arg_to_dict(edge_lc, H.edges)
    edge_fc = _color_edges(edge_fc, H.edges)
    # Looping over the hyperedges of different order (reversed) -- nodes will be plotted separately
    for id, he in H_.edges.members(dtype=dict).items():
        d = len(he) - 1
        if d == 1:
            # Drawing the edges
            he = list(he)
            x_coords = [pos[he[0]][0], pos[he[1]][0]]
            y_coords = [pos[he[0]][1], pos[he[1]][1]]
            line = plt.Line2D(x_coords, y_coords, color=edge_lc[id], lw=edge_lw)
            ax.add_line(line)
        else:
            # Hyperedges of order d (d=1: links, etc.)
            # Filling the polygon
            coordinates = [[pos[n][0], pos[n][1]] for n in he]
            # Sorting the points counterclockwise (needed to have the correct filling)
            sorted_coordinates = _CCW_sort(coordinates)
            obj = plt.Polygon(
                sorted_coordinates,
                edgecolor=edge_lc[id],
                facecolor=edge_fc[id],
                alpha=0.4,
                lw=0.5,
            )
            ax.add_patch(obj)
            # Drawing the all the edges within
            for i, j in combinations(sorted_coordinates, 2):
                x_coords = [i[0], j[0]]
                y_coords = [i[1], j[1]]
                line = plt.Line2D(x_coords, y_coords, color=edge_lc[id], lw=edge_lw[id])
                ax.add_line(line)


def _arg_to_dict(arg, ids):
    """Map different types of arguments for drawing style to a dict.

    Parameters
    ----------
    arg : str, dict, or iterable
        attributes for drawing parameter
    ids : NodeView or EdgeView
        This is the node or edge IDs that attributes get mapped to.

    Returns
    -------
    dict
        an ID: attribute dictionary

    Raises
    ------
    TypeError
        if a string, list, or dict is not passed
    """
    if isinstance(arg, dict):
        return {id: arg[id] for id in arg if id in ids}
    if type(arg) in [int, float, str]:
        return {id: arg for id in ids}
    elif isinstance(arg, Iterable):
        return {id: arg[idx] for idx, id in enumerate(ids)}
    else:
        raise TypeError(
            f"argument must be dict, str, or iterable, received {type(arg)}"
        )


def _color_edges(colors, H):
    """Map different types of arguments for drawing style to a dict.

    Parameters
    ----------
    colors : str, dict, cmap, or iterable
        attributes for drawing parameter
    ids : NodeView or EdgeView
        This is the node or edge IDs that attributes get mapped to.

    Returns
    -------
    dict
        an ID: attribute dictionary

    Raises
    ------
    TypeError
        if a string, list, or dict is not passed
    """
    # Defining colors, one for each dimension
    d_max = max_edge_order(H)
    if colors is None:
        colors = cm.Paired

    if type(colors) == ListedColormap:
        # The colormap is already discrete
        c = [colors(i) for i in range(d_max)]
        order = H.edges.order.asdict()
        return {e: c[order[e] - 1] for e in H.edges}
    elif type(colors) == LinearSegmentedColormap:
        # I need to discretize the given colormap
        color_range = np.linspace(0.1, 0.9, d_max)
        c = [colors(i) for i in color_range]
        order = H.edges.order.asdict()
        return {e: c[order[e] - 1] for e in H.edges}
    else:
        return _arg_to_dict(colors, H.edges)


def _CCW_sort(p):
    """
    Sort the input 2D points counterclockwise.
    """
    p = np.array(p)
    mean = np.mean(p, axis=0)
    d = p - mean
    s = np.arctan2(d[:, 0], d[:, 1])
    return p[np.argsort(s), :]
