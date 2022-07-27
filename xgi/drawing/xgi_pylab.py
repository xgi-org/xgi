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
from ..stats import EdgeStat, NodeStat
from .layout import barycenter_spring_layout

__all__ = [
    "draw",
]


def draw(
    H,
    pos=None,
    ax=None,
    link_color="black",
    link_width=1.5,
    edge_facecolor=None,
    node_facecolor="white",
    node_edgecolor="black",
    node_edgewidth=1,
    node_size=10,
    **kwargs,
):
    """Draw hypergraph or simplicial complex.

    Parameters
    ----
    H : Hypergraph or SimplicialComplex.

    pos : dict (default=None)
        If passed, this dictionary of positions d:(x,y) is used for placing the 0-simplices.
        If None (default), use the `barycenter_spring_layout` to compute the positions.

    ax : matplotlib.pyplot.axes (default=None)

    link_color : color (str, dict, or iterable, default='black')
        Color of the dyadic links.  If str, use the
        same color for all edges.  If a dict, must contain (edge_id: color_str) pairs.  If
        iterable, assume the colors are specified in the same order as the edges are found
        in H.edges.

    link_width :  float (default=1.5)
        Line width of edges of order 1 (dyadic links).

    edge_facecolor : str, 4-tuple, ListedColormap, LinearSegmentedColormap, or dict of 4-tuples or strings
        Color of hyperedges

    node_facecolor : color (str, dict, or iterable, default='white')
        Color of the nodes.  If str, use the same color for all nodes.  If a dict, must
        contain (node_id: color_str) pairs.  If other iterable, assume the colors are
        specified in the same order as the nodes are found in H.nodes.

    node_edgecolor : color (dict or str, default='black')
        Color of node borders.  If str, use the same color for all nodes.  If a dict, must
        contain (node_id: color_str) pairs.  If other iterable, assume the colors are
        specified in the same order as the nodes are found in H.nodes.

    node_edgewidth : float (default=1.0)
        Line width of the node borders in pixels.

    node_size : float (default=0.03)
        Radius of the nodes in pixels

    **kwargs : optional args
        alternate default values. Values that can be overwritten are the following:
        * min_node_size
        * max_node_size
        * min_link_width
        * max_link_width
        * min_node_edgewidth
        * max_node_edgewidth
        * node_facecolor_cmap
        * node_lc_cmap
        * edge_facecolor_cmap
        * link_color_cmap

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph()
    >>> H.add_edges_from([[1,2,3],[3,4],[4,5,6,7],[7,8,9,10,11]])
    >>> xgi.draw(H, pos=xgi.barycenter_spring_layout(H))

    """
    settings = {
        "min_node_size": 10,
        "max_node_size": 30,
        "min_link_width": 2,
        "max_link_width": 10,
        "min_node_edgewidth": 1,
        "max_node_edgewidth": 5,
        "node_facecolor_cmap": cm.Reds,
        "node_lc_cmap": cm.Greys,
        "edge_facecolor_cmap": cm.Blues,
        "link_color_cmap": cm.Greys,
    }

    settings.update(kwargs)

    if edge_facecolor is None:
        edge_facecolor = H.edges.size

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

    if isinstance(H, SimplicialComplex):
        draw_xgi_simplices(H, pos, ax, link_color, link_width, edge_facecolor, settings)
    elif isinstance(H, Hypergraph):
        draw_xgi_hyperedges(
            H, pos, ax, link_color, link_width, edge_facecolor, d_max, settings
        )
    else:
        raise XGIError("The input must be a SimplicialComplex or Hypergraph")

    draw_xgi_nodes(
        H,
        pos,
        ax,
        node_facecolor,
        node_edgecolor,
        node_edgewidth,
        node_size,
        d_max,
        settings,
    )


def draw_xgi_nodes(
    H,
    pos,
    ax,
    node_facecolor,
    node_edgecolor,
    node_edgewidth,
    node_size,
    zorder,
    settings,
):
    """Draw the nodes of a hypergraph

    Parameters
    ----------
    ax : axis handle
        Plot axes on which to draw the visualization
    H : Hypergraph or SimplicialComplex
        Higher-order network to plot
    pos : dict of lists
        The x, y position of every node
    node_facecolor : str, 4-tuple, or dict of strings or 4-tuples
        The color of the nodes
    node_edgecolor : str, 4-tuple, or dict of strings or 4-tuples
        The outline color of the nodes
    node_edgewidth : int, float, or dict of ints or floats
        The line weight of the outline of the nodes
    node_size : int, float, or dict of ints or floats
        The node radius
    zorder : int
        The layer on which to draw the nodes
    settings : dict
        Default parameters. Keys that may be useful to override default settings:
        * node_facecolor_cmap
        * node_lc_cmap
        * min_node_edgewidth
        * max_node_edgewidth
        * min_node_size
        * max_node_size
    """
    # Note Iterable covers lists, tuples, ranges, generators, np.ndarrays, etc
    node_facecolor = _color_arg_to_dict(
        node_facecolor, H.nodes, settings["node_facecolor_cmap"]
    )
    node_edgecolor = _color_arg_to_dict(
        node_edgecolor, H.nodes, settings["node_lc_cmap"]
    )
    node_edgewidth = _scalar_arg_to_dict(
        node_edgewidth,
        H.nodes,
        settings["min_node_edgewidth"],
        settings["max_node_edgewidth"],
    )
    node_size = _scalar_arg_to_dict(
        node_size, H.nodes, settings["min_node_size"], settings["max_node_size"]
    )

    for i in H.nodes:
        (x, y) = pos[i]
        ax.scatter(
            x,
            y,
            s=node_size[i] ** 2,
            c=node_facecolor[i],
            edgecolors=node_edgecolor[i],
            linewidths=node_edgewidth[i],
            zorder=zorder,
        )


def draw_xgi_hyperedges(
    H, pos, ax, link_color, link_width, edge_facecolor, d_max, settings
):
    """Draw hyperedges.

    Parameters
    ----------
    ax : axis handle
        Figure axes to plot onto
    H : Hypergraph
        A hypergraph
    pos : dict of lists
        x,y position of every node
    link_color : str, 4-tuple, or dict of 4-tuples or strings
        The color of the pairwise edges
    link_width : int, float, or dict
        Pairwise edge widths
    edge_facecolor : str, 4-tuple, ListedColormap, LinearSegmentedColormap, or dict of 4-tuples or strings
        Color of hyperedges
    settings : dict
        Default parameters. Keys that may be useful to override default settings:
        * link_color_cmap
        * min_link_width
        * max_link_width
        * edge_facecolor_cmap

    Raises
    ------
    XGIError
        If a SimplicialComplex is passed.
    """
    link_color = _color_arg_to_dict(link_color, H.edges, settings["link_color_cmap"])
    link_width = _scalar_arg_to_dict(
        link_width, H.edges, settings["min_link_width"], settings["max_link_width"]
    )

    edge_facecolor = _color_arg_to_dict(
        edge_facecolor, H.edges, settings["edge_facecolor_cmap"]
    )
    # Looping over the hyperedges of different order (reversed) -- nodes will be plotted separately

    for id, he in H.edges.members(dtype=dict).items():
        d = len(he) - 1
        if d == 1:
            # Drawing the edges
            he = list(he)
            x_coords = [pos[he[0]][0], pos[he[1]][0]]
            y_coords = [pos[he[0]][1], pos[he[1]][1]]
            line = plt.Line2D(
                x_coords,
                y_coords,
                color=link_color[id],
                lw=link_width[id],
                zorder=d_max - 1,
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
                facecolor=edge_facecolor[id],
                alpha=0.4,
                lw=0.5,
                zorder=d_max - d,
            )
            ax.add_patch(obj)


def draw_xgi_simplices(SC, pos, ax, link_color, link_width, edge_facecolor, settings):
    """Draw maximal simplices and pairwise faces.

    Parameters
    ----------
    ax : axis handle
        Figure axes to plot onto
    SC : SimplicialComplex
        A simpicial complex
    pos : dict of lists
        x,y position of every node
    link_color : str, 4-tuple, or dict of 4-tuples or strings
        The color of the pairwise edges
    link_width : int, float, or dict
        Pairwise edge widths
    edge_facecolor : str, 4-tuple, ListedColormap, LinearSegmentedColormap, or dict of 4-tuples or strings
        Color of simplices
    settings : dict
        Default parameters. Keys that may be useful to override default settings:
        * link_color_cmap
        * min_link_width
        * max_link_width
        * edge_facecolor_cmap

    Raises
    ------
    XGIError
        If a SimplicialComplex is passed.
    """
    # I will only plot the maximal simplices, so I convert the SC to H
    H_ = convert.from_simplicial_complex_to_hypergraph(SC)

    link_color = _color_arg_to_dict(link_color, H_.edges, settings["link_color_cmap"])
    link_width = _scalar_arg_to_dict(
        link_width,
        H_.edges,
        settings["min_link_width"],
        settings["max_link_width"],
    )

    edge_facecolor = _color_arg_to_dict(
        edge_facecolor, H_.edges, settings["edge_facecolor_cmap"]
    )
    # Looping over the hyperedges of different order (reversed) -- nodes will be plotted separately
    for id, he in H_.edges.members(dtype=dict).items():
        d = len(he) - 1
        if d == 1:
            # Drawing the edges
            he = list(he)
            x_coords = [pos[he[0]][0], pos[he[1]][0]]
            y_coords = [pos[he[0]][1], pos[he[1]][1]]

            line = plt.Line2D(
                x_coords, y_coords, color=link_color[id], lw=link_width[id]
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
                facecolor=edge_facecolor[id],
                alpha=0.4,
                lw=0.5,
            )
            ax.add_patch(obj)
            # Drawing the all the edges within
            for i, j in combinations(sorted_coordinates, 2):
                x_coords = [i[0], j[0]]
                y_coords = [i[1], j[1]]
                line = plt.Line2D(
                    x_coords, y_coords, color=link_color[id], lw=link_width[id]
                )
                ax.add_line(line)


def _scalar_arg_to_dict(arg, ids, min_val, max_val):
    """Map different types of arguments for drawing style to a dict with scalar values.

    Parameters
    ----------
    arg : int, float, dict, iterable, or NodeStat/EdgeStat
        Attributes for drawing parameter
    ids : NodeView or EdgeView
        This is the node or edge IDs that attributes get mapped to.
    min_val : int or float
        The minimum value of the drawing parameter
    max_val : int or float
        The maximum value of the drawing parameter

    Returns
    -------
    dict
        An ID: attribute dictionary

    Raises
    ------
    TypeError
        If a int, float, list, dict, or NodeStat/EdgeStat is not passed
    """
    if isinstance(arg, dict):
        return {id: arg[id] for id in arg if id in ids}
    elif type(arg) in [int, float]:
        return {id: arg for id in ids}
    elif isinstance(arg, NodeStat) or isinstance(arg, EdgeStat):
        f = lambda val: np.interp(val, [arg.min(), arg.max()], [min_val, max_val])
        s = arg.asdict()
        return {id: f(s[id]) for id in ids}
    elif isinstance(arg, Iterable):
        return {id: arg[idx] for idx, id in enumerate(ids)}
    else:
        raise TypeError(
            f"argument must be dict, str, or iterable, received {type(arg)}"
        )


def _color_arg_to_dict(arg, ids, cmap):
    """Map different types of arguments for drawing style to a dict with color values.

    Parameters
    ----------
    arg : str, dict, iterable, or NodeStat/EdgeStat
        Attributes for drawing parameter
    ids : NodeView or EdgeView
        This is the node or edge IDs that attributes get mapped to.
    cmap : ListedColormap or LinearSegmentedColormap
        colormap to use for NodeStat/EdgeStat

    Returns
    -------
    dict
        An ID: attribute dictionary

    Raises
    ------
    TypeError
        If a string, tuple, list, or dict is not passed
    """
    if isinstance(arg, dict):
        return {id: arg[id] for id in arg if id in ids}
    elif type(arg) in [tuple, str]:
        return {id: arg for id in ids}
    elif isinstance(arg, NodeStat) or isinstance(arg, EdgeStat):
        if isinstance(cmap, ListedColormap):
            f = lambda val: np.interp(val, [arg.min(), arg.max()], [0, cmap.N])
        elif isinstance(cmap, LinearSegmentedColormap):
            f = lambda val: np.interp(val, [arg.min(), arg.max()], [0.1, 0.9])
        else:
            raise XGIError("Invalid colormap!")
        s = arg.asdict()
        return {id: np.array(cmap(f(s[id]))).reshape(1, -1) for id in ids}
    elif isinstance(arg, Iterable):
        return {id: arg[idx] for idx, id in enumerate(ids)}
    else:
        raise TypeError(
            f"argument must be dict, str, or iterable, received {type(arg)}"
        )


def _CCW_sort(p):
    """
    Sort the input 2D points counterclockwise.
    """
    p = np.array(p)
    mean = np.mean(p, axis=0)
    d = p - mean
    s = np.arctan2(d[:, 0], d[:, 1])
    return p[np.argsort(s), :]
