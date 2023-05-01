"""Draw hypergraphs and simplicial complexes with matplotlib."""

from collections.abc import Iterable
from inspect import signature
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from scipy.spatial import ConvexHull

from .. import convert
from ..classes import Hypergraph, SimplicialComplex, max_edge_order
from ..exception import XGIError
from ..stats import EdgeStat, NodeStat
from .layout import barycenter_spring_layout

__all__ = [
    "draw",
    "draw_nodes",
    "draw_hyperedges",
    "draw_simplices",
    "draw_node_labels",
    "draw_hyperedge_labels",
    "draw_hypergraph_hull",
]


def draw(
    H,
    pos=None,
    ax=None,
    dyad_color="black",
    dyad_lw=1.5,
    edge_fc=None,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=15,
    max_order=None,
    node_labels=False,
    hyperedge_labels=False,
    **kwargs,
):
    """Draw hypergraph or simplicial complex.

    Parameters
    ----
    H : Hypergraph or SimplicialComplex.
        Hypergraph to draw
    pos : dict, optional
        If passed, this dictionary of positions node_id:(x,y) is used for placing the
        0-simplices.  If None (default), use the `barycenter_spring_layout` to compute
        the positions.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
    dyad_color : str, dict, iterable, or EdgeStat, optional
        Color of the dyadic links.  If str, use the same color for all edges. If a dict,
        must contain (edge_id: color_str) pairs.  If iterable, assume the colors are
        specified in the same order as the edges are found in H.edges. If EdgeStat, use
        a colormap (specified with dyad_color_cmap) associated to it. By default,
        "black".
    dyad_lw : int, float, dict, iterable, or EdgeStat, optional
        Line width of edges of order 1 (dyadic links).  If int or float, use the same
        width for all edges.  If a dict, must contain (edge_id: width) pairs.  If
        iterable, assume the widths are specified in the same order as the edges are
        found in H.edges. If EdgeStat, use a monotonic linear interpolation defined
        between min_dyad_lw and max_dyad_lw. By default, 1.5.
    edge_fc : str, dict, iterable, or EdgeStat, optional
        Color of the hyperedges.  If str, use the same color for all nodes.  If a dict,
        must contain (edge_id: color_str) pairs.  If other iterable, assume the colors
        are specified in the same order as the hyperedges are found in H.edges. If
        EdgeStat, use the colormap specified with edge_fc_cmap. If None (default), use
        the H.edges.size.
    node_fc : str, dict, iterable, or NodeStat, optional
        Color of the nodes.  If str, use the same color for all nodes.  If a dict, must
        contain (node_id: color_str) pairs.  If other iterable, assume the colors are
        specified in the same order as the nodes are found in H.nodes. If NodeStat, use
        the colormap specified with node_fc_cmap. By default, "white".
    node_ec : str, dict, iterable, or NodeStat, optional
        Color of node borders.  If str, use the same color for all nodes.  If a dict,
        must contain (node_id: color_str) pairs.  If other iterable, assume the colors
        are specified in the same order as the nodes are found in H.nodes. If NodeStat,
        use the colormap specified with node_ec_cmap. By default, "black".
    node_lw : int, float, dict, iterable, or NodeStat, optional
        Line width of the node borders in pixels.  If int or float, use the same width
        for all node borders.  If a dict, must contain (node_id: width) pairs.  If
        iterable, assume the widths are specified in the same order as the nodes are
        found in H.nodes. If NodeStat, use a monotonic linear interpolation defined
        between min_node_lw and max_node_lw. By default, 1.
    node_size : int, float, dict, iterable, or NodeStat, optional
        Radius of the nodes in pixels.  If int or float, use the same radius for all
        nodes.  If a dict, must contain (node_id: radius) pairs.  If iterable, assume
        the radiuses are specified in the same order as the nodes are found in
        H.nodes. If NodeStat, use a monotonic linear interpolation defined between
        min_node_size and max_node_size. By default, 15.
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
    node_labels : bool or dict, optional
        If True, draw ids on the nodes. If a dict, must contain (node_id: label) pairs.
        By default, False.
    hyperedge_labels : bool or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  By default, False.
    **kwargs : optional args
        Alternate default values. Values that can be overwritten are the following:
        * min_node_size
        * max_node_size
        * min_node_lw
        * max_node_lw
        * min_dyad_lw
        * max_dyad_lw
        * node_fc_cmap
        * node_ec_cmap
        * dyad_color_cmap
        * edge_fc_cmap

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph()
    >>> H.add_edges_from([[1,2,3],[3,4],[4,5,6,7],[7,8,9,10,11]])
    >>> ax = xgi.draw(H, pos=xgi.barycenter_spring_layout(H))

    See Also
    --------
    draw_nodes
    draw_hyperedges
    draw_simplices
    draw_node_labels
    draw_hyperedge_labels

    """
    settings = {
        "min_node_size": 10.0,
        "max_node_size": 30.0,
        "min_dyad_lw": 2.0,
        "max_dyad_lw": 10.0,
        "min_node_lw": 1.0,
        "max_node_lw": 5.0,
        "node_fc_cmap": cm.Reds,
        "node_ec_cmap": cm.Greys,
        "edge_fc_cmap": cm.Blues,
        "dyad_color_cmap": cm.Greys,
    }

    settings.update(kwargs)

    if edge_fc is None:
        edge_fc = H.edges.size

    if pos is None:
        pos = barycenter_spring_layout(H)

    if ax is None:
        ax = plt.gca()

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    if not max_order:
        max_order = max_edge_order(H)

    if isinstance(H, SimplicialComplex):
        draw_simplices(
            H,
            pos,
            ax,
            dyad_color,
            dyad_lw,
            edge_fc,
            max_order,
            settings,
            hyperedge_labels,
            **kwargs,
        )
    elif isinstance(H, Hypergraph):
        draw_hyperedges(
            H,
            pos,
            ax,
            dyad_color,
            dyad_lw,
            edge_fc,
            max_order,
            settings,
            hyperedge_labels,
            **kwargs,
        )
    else:
        raise XGIError("The input must be a SimplicialComplex or Hypergraph")

    draw_nodes(
        H,
        pos,
        ax,
        node_fc,
        node_ec,
        node_lw,
        node_size,
        max_order,
        settings,
        node_labels,
        **kwargs,
    )

    # compute axis limits
    _update_lims(pos, ax)

    return ax


def draw_nodes(
    H,
    pos=None,
    ax=None,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=15,
    zorder=None,
    settings=None,
    node_labels=False,
    **kwargs,
):
    """Draw the nodes of a hypergraph

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex
        Higher-order network to plot.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
    pos : dict, optional
        If passed, this dictionary of positions node_id:(x,y) is used for placing the
        0-simplices.  If None (default), use the `barycenter_spring_layout` to compute
        the positions.
    node_fc : str, dict, iterable, or NodeStat, optional
        Color of the nodes.  If str, use the same color for all nodes.  If a dict, must
        contain (node_id: color_str) pairs.  If other iterable, assume the colors are
        specified in the same order as the nodes are found in H.nodes. If NodeStat, use
        the colormap specified with node_fc_cmap. By default, "white".
    node_ec : str, dict, iterable, or NodeStat, optional
        Color of node borders.  If str, use the same color for all nodes.  If a dict,
        must contain (node_id: color_str) pairs.  If other iterable, assume the colors
        are specified in the same order as the nodes are found in H.nodes. If NodeStat,
        use the colormap specified with node_ec_cmap. By default, "black".
    node_lw : int, float, dict, iterable, or EdgeStat, optional
        Line width of the node borders in pixels.  If int or float, use the same width
        for all node borders.  If a dict, must contain (node_id: width) pairs.  If
        iterable, assume the widths are specified in the same order as the nodes are
        found in H.nodes. If NodeStat, use a monotonic linear interpolation defined
        between min_node_lw and max_node_lw. By default, 1.
    node_size : int, float, dict, iterable, or NodeStat, optional
        Radius of the nodes in pixels.  If int or float, use the same radius for all
        nodes.  If a dict, must contain (node_id: radius) pairs.  If iterable, assume
        the radiuses are specified in the same order as the nodes are found in
        H.nodes. If NodeStat, use a monotonic linear interpolation defined between
        min_node_size and max_node_size. By default, 15.
    zorder : int
        The layer on which to draw the nodes.
    node_labels : bool or dict
        If True, draw ids on the nodes. If a dict, must contain (node_id: label) pairs.
    settings : dict
        Default parameters. Keys that may be useful to override default settings:
        * min_node_size
        * max_node_size
        * min_node_lw
        * max_node_lw
        * node_fc_cmap
        * node_ec_cmap
    kwargs : optional keywords
        See `draw_node_labels` for a description of optional keywords.

    See Also
    --------
    draw
    draw_hyperedges
    draw_simplices
    draw_node_labels
    draw_hyperedge_labels

    """

    if settings is None:
        settings = {
            "min_node_size": 10.0,
            "max_node_size": 30.0,
            "min_node_lw": 1.0,
            "max_node_lw": 5.0,
            "node_fc_cmap": cm.Reds,
            "node_ec_cmap": cm.Greys,
        }

    settings.update(kwargs)

    if pos is None:
        pos = barycenter_spring_layout(H)

    if ax is None:
        ax = plt.gca()

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    # Note Iterable covers lists, tuples, ranges, generators, np.ndarrays, etc
    node_fc = _color_arg_to_dict(node_fc, H.nodes, settings["node_fc_cmap"])
    node_ec = _color_arg_to_dict(node_ec, H.nodes, settings["node_ec_cmap"])
    node_lw = _scalar_arg_to_dict(
        node_lw,
        H.nodes,
        settings["min_node_lw"],
        settings["max_node_lw"],
    )
    node_size = _scalar_arg_to_dict(
        node_size, H.nodes, settings["min_node_size"], settings["max_node_size"]
    )

    (x, y, s, c, ec, lw,) = zip(
        *[
            (
                pos[i][0],
                pos[i][1],
                node_size[i] ** 2,
                node_fc[i],
                node_ec[i],
                node_lw[i],
            )
            for i in H.nodes
        ]
    )
    ax.scatter(x=x, y=y, s=s, c=c, edgecolors=ec, linewidths=lw, zorder=zorder)

    if node_labels:
        # Get all valid keywords by inspecting the signatures of draw_node_labels
        valid_label_kwds = signature(draw_node_labels).parameters.keys()
        # Remove the arguments of this function (draw_networkx)
        valid_label_kwds = valid_label_kwds - {"H", "pos", "ax", "node_labels"}
        if any([k not in valid_label_kwds for k in kwargs]):
            invalid_args = ", ".join([k for k in kwargs if k not in valid_label_kwds])
            raise ValueError(f"Received invalid argument(s): {invalid_args}")
        label_kwds = {k: v for k, v in kwargs.items() if k in valid_label_kwds}
        draw_node_labels(H, pos, node_labels, ax_nodes=ax, **label_kwds)

    # compute axis limits
    _update_lims(pos, ax)

    return ax


def draw_hyperedges(
    H,
    pos=None,
    ax=None,
    dyad_color="black",
    dyad_lw=1.5,
    edge_fc=None,
    max_order=None,
    settings=None,
    hyperedge_labels=False,
    **kwargs,
):
    """Draw hyperedges.

    Parameters
    ----------
    H : Hypergraph
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
    pos : dict, optional
        If passed, this dictionary of positions node_id:(x,y) is used for placing the
        0-simplices.  If None (default), use the `barycenter_spring_layout` to compute
        the positions.
    dyad_color : str, dict, iterable, or EdgeStat, optional
        Color of the dyadic links.  If str, use the same color for all edges. If a dict,
        must contain (edge_id: color_str) pairs.  If iterable, assume the colors are
        specified in the same order as the edges are found in H.edges. If EdgeStat, use
        a colormap (specified with dyad_color_cmap) associated to it. By default,
        "black".
    dyad_lw : int, float, dict, iterable, or EdgeStat, optional
        Line width of edges of order 1 (dyadic links).  If int or float, use the same
        width for all edges.  If a dict, must contain (edge_id: width) pairs.  If
        iterable, assume the widths are specified in the same order as the edges are
        found in H.edges. If EdgeStat, use a monotonic linear interpolation defined
        between min_dyad_lw and max_dyad_lw. By default, 1.5.
    edge_fc : str, dict, iterable, or EdgeStat, optional
        Color of the hyperedges.  If str, use the same color for all nodes.  If a dict,
        must contain (edge_id: color_str) pairs.  If other iterable, assume the colors
        are specified in the same order as the hyperedges are found in H.edges. If
        EdgeStat, use the colormap specified with edge_fc_cmap. If None (default), color
        by edge size.
    max_order : int, optional
        Maximum of hyperedges to plot. By default, None.
    hyperedge_labels : bool or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  By default, None.
    settings : dict
        Default parameters. Keys that may be useful to override default settings:
        * min_dyad_lw
        * max_dyad_lw
        * dyad_color_cmap
        * edge_fc_cmap
    kwargs : optional keywords
        See `draw_hyperedge_labels` for a description of optional keywords.

    Raises
    ------
    XGIError
        If a SimplicialComplex is passed.

    See Also
    --------
    draw
    draw_nodes
    draw_simplices
    draw_node_labels
    draw_hyperedge_labels

    """

    if pos is None:
        pos = barycenter_spring_layout(H)

    if ax is None:
        ax = plt.gca()

    if max_order is None:
        max_order = max_edge_order(H)

    if edge_fc is None:
        edge_fc = H.edges.size

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    if settings is None:
        settings = {
            "min_dyad_lw": 2.0,
            "max_dyad_lw": 10.0,
            "edge_fc_cmap": cm.Blues,
            "dyad_color_cmap": cm.Greys,
        }

    settings.update(kwargs)

    dyad_color = _color_arg_to_dict(dyad_color, H.edges, settings["dyad_color_cmap"])
    dyad_lw = _scalar_arg_to_dict(
        dyad_lw, H.edges, settings["min_dyad_lw"], settings["max_dyad_lw"]
    )

    edge_fc = _color_arg_to_dict(edge_fc, H.edges, settings["edge_fc_cmap"])

    # Looping over the hyperedges of different order (reversed) -- nodes will be plotted
    # separately
    for id, he in H.edges.members(dtype=dict).items():
        d = len(he) - 1
        if d > max_order:
            continue
        if d == 1:
            # Drawing the edges
            he = list(he)
            x_coords = [pos[he[0]][0], pos[he[1]][0]]
            y_coords = [pos[he[0]][1], pos[he[1]][1]]
            line = plt.Line2D(
                x_coords,
                y_coords,
                color=dyad_color[id],
                lw=dyad_lw[id],
                zorder=max_order - 1,
            )
            ax.add_line(line)
        else:
            # Hyperedges of order d (d=2: triangles, etc.)
            # Filling the polygon
            coordinates = [[pos[n][0], pos[n][1]] for n in he]
            # Sorting the points counterclockwise (needed to have the correct filling)
            sorted_coordinates = _CCW_sort(coordinates)
            obj = plt.Polygon(
                sorted_coordinates,
                facecolor=edge_fc[id],
                alpha=0.4,
                zorder=max_order - d,
            )
            ax.add_patch(obj)

    if hyperedge_labels:
        # Get all valid keywords by inspecting the signatures of draw_node_labels
        valid_label_kwds = signature(draw_hyperedge_labels).parameters.keys()
        # Remove the arguments of this function (draw_networkx)
        valid_label_kwds = valid_label_kwds - {"H", "pos", "ax", "hyperedge_labels"}
        if any([k not in valid_label_kwds for k in kwargs]):
            invalid_args = ", ".join([k for k in kwargs if k not in valid_label_kwds])
            raise ValueError(f"Received invalid argument(s): {invalid_args}")
        label_kwds = {k: v for k, v in kwargs.items() if k in valid_label_kwds}
        draw_hyperedge_labels(H, pos, hyperedge_labels, ax_edges=ax, **label_kwds)

    # compute axis limits
    _update_lims(pos, ax)

    return ax


def draw_simplices(
    SC,
    pos=None,
    ax=None,
    dyad_color="black",
    dyad_lw=1.5,
    edge_fc=None,
    max_order=None,
    settings=None,
    hyperedge_labels=False,
    **kwargs,
):
    """Draw maximal simplices and pairwise faces.

    Parameters
    ----------
    SC : SimplicialComplex
        Simplicial complex to draw
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
    pos : dict, optional
        If passed, this dictionary of positions node_id:(x,y) is used for placing the
        0-simplices.  If None (default), use the `barycenter_spring_layout` to compute
        the positions.
    dyad_color : str, dict, iterable, or EdgeStat, optional
        Color of the dyadic links.  If str, use the same color for all edges. If a dict,
        must contain (edge_id: color_str) pairs.  If iterable, assume the colors are
        specified in the same order as the edges are found in H.edges. If EdgeStat, use
        a colormap (specified with dyad_color_cmap) associated to it. By default,
        "black".
    dyad_lw : int, float, dict, iterable, or EdgeStat, optional
        Line width of edges of order 1 (dyadic links).  If int or float, use the same
        width for all edges.  If a dict, must contain (edge_id: width) pairs.  If
        iterable, assume the widths are specified in the same order as the edges are
        found in H.edges. If EdgeStat, use a monotonic linear interpolation defined
        between min_dyad_lw and max_dyad_lw. By default, 1.5.
    edge_fc : str, dict, iterable, or EdgeStat, optional
        Color of the hyperedges.  If str, use the same color for all nodes.  If a dict,
        must contain (edge_id: color_str) pairs.  If other iterable, assume the colors
        are specified in the same order as the hyperedges are found in H.edges. If
        EdgeStat, use the colormap specified with edge_fc_cmap. If None (default), color
        by simplex size.
    max_order : int, optional
        Maximum of hyperedges to plot. By default, None.
    hyperedge_labels : bool or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  Note, we plot only the maximal simplices so if you pass a dict be
        careful to match its keys with the new edge ids in the converted
        SimplicialComplex. These may differ from the edge ids in the given SC. By
        default, False.
    settings : dict
        Default parameters. Keys that may be useful to override default settings:
        * min_dyad_lw
        * max_dyad_lw
        * dyad_color_cmap
        * edge_fc_cmap
    kwargs : optional keywords
        See `draw_hyperedge_labels` for a description of optional keywords.


    Raises
    ------
    XGIError
        If a Hypergraph is passed.

    See Also
    --------
    draw
    draw_nodes
    draw_hyperedges
    draw_node_labels
    draw_hyperedge_labels

    """

    if max_order:
        max_edges = SC.edges.filterby("order", max_order, "leq").members()
        SC = SimplicialComplex(max_edges)  # SC without simplices larger than max_order

    # Plot only the maximal simplices, thus let's convert the SC to H
    H_ = convert.from_max_simplices(SC)

    if not max_order:
        max_order = max_edge_order(H_)

    if pos is None:
        pos = barycenter_spring_layout(H_)

    if ax is None:
        ax = plt.gca()

    if edge_fc is None:
        edge_fc = H_.edges.size

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    if settings is None:
        settings = {
            "min_dyad_lw": 2.0,
            "max_dyad_lw": 10.0,
            "edge_fc_cmap": cm.Blues,
            "dyad_color_cmap": cm.Greys,
        }

    settings.update(kwargs)

    dyad_color = _color_arg_to_dict(dyad_color, H_.edges, settings["dyad_color_cmap"])
    dyad_lw = _scalar_arg_to_dict(
        dyad_lw,
        H_.edges,
        settings["min_dyad_lw"],
        settings["max_dyad_lw"],
    )

    edge_fc = _color_arg_to_dict(edge_fc, H_.edges, settings["edge_fc_cmap"])

    # Looping over the hyperedges of different order (reversed) -- nodes will be plotted
    # separately
    for id, he in H_.edges.members(dtype=dict).items():
        d = len(he) - 1

        if d == 1:
            # Drawing the edges
            he = list(he)
            x_coords = [pos[he[0]][0], pos[he[1]][0]]
            y_coords = [pos[he[0]][1], pos[he[1]][1]]

            line = plt.Line2D(
                x_coords,
                y_coords,
                color=dyad_color[id],
                lw=dyad_lw[id],
                zorder=max_order - 1,
            )
            ax.add_line(line)
        else:
            # Hyperedges of order d (d=2: triangles, etc.)
            # Filling the polygon
            coordinates = [[pos[n][0], pos[n][1]] for n in he]
            # Sorting the points counterclockwise (needed to have the correct filling)
            sorted_coordinates = _CCW_sort(coordinates)
            obj = plt.Polygon(
                sorted_coordinates,
                facecolor=edge_fc[id],
                alpha=0.4,
                zorder=max_order - d,
            )
            ax.add_patch(obj)
            # Drawing all the edges within
            for i, j in combinations(sorted_coordinates, 2):
                x_coords = [i[0], j[0]]
                y_coords = [i[1], j[1]]
                line = plt.Line2D(
                    x_coords,
                    y_coords,
                    color=dyad_color[id],
                    lw=dyad_lw[id],
                    zorder=max_order - 1,
                )
                ax.add_line(line)

    if hyperedge_labels:
        # Get all valid keywords by inspecting the signatures of draw_node_labels
        valid_label_kwds = signature(draw_hyperedge_labels).parameters.keys()
        # Remove the arguments of this function (draw_networkx)
        valid_label_kwds = valid_label_kwds - {"H", "pos", "ax", "hyperedge_labels"}
        if any([k not in valid_label_kwds for k in kwargs]):
            invalid_args = ", ".join([k for k in kwargs if k not in valid_label_kwds])
            raise ValueError(f"Received invalid argument(s): {invalid_args}")
        label_kwds = {k: v for k, v in kwargs.items() if k in valid_label_kwds}
        draw_hyperedge_labels(H_, pos, hyperedge_labels, ax_edges=ax, **label_kwds)

    # compute axis limits
    _update_lims(pos, ax)

    return ax


def _scalar_arg_to_dict(arg, ids, min_val, max_val):
    """Map different types of arguments for drawing style to a dict with scalar values.

    Parameters
    ----------
    arg : int, float, dict, iterable, or NodeStat/EdgeStat
        Attributes for drawing parameter.
    ids : NodeView or EdgeView
        This is the node or edge IDs that attributes get mapped to.
    min_val : int or float
        The minimum value of the drawing parameter.
    max_val : int or float
        The maximum value of the drawing parameter.

    Returns
    -------
    dict
        An ID: attribute dictionary.

    Raises
    ------
    TypeError
        If a int, float, list, dict, or NodeStat/EdgeStat is not passed.
    """
    if isinstance(arg, str):
        raise TypeError(
            "Argument must be int, float, dict, iterable, "
            f"or NodeStat/EdgeStat. Received {type(arg)}"
        )
    elif isinstance(arg, dict):
        return {id: arg[id] for id in arg if id in ids}
    elif type(arg) in [int, float]:
        return {id: arg for id in ids}
    elif isinstance(arg, NodeStat) or isinstance(arg, EdgeStat):
        vals = np.interp(arg.asnumpy(), [arg.min(), arg.max()], [min_val, max_val])
        return dict(zip(ids, vals))
    elif isinstance(arg, Iterable):
        return {id: arg[idx] for idx, id in enumerate(ids)}
    else:
        raise TypeError(
            "Argument must be int, float, dict, iterable, "
            f"or NodeStat/EdgeStat. Received {type(arg)}"
        )


def _color_arg_to_dict(arg, ids, cmap):
    """Map different types of arguments for drawing style to a dict with color values.

    Parameters
    ----------
    arg : str, dict, iterable, or NodeStat/EdgeStat
        Attributes for drawing parameter.
    ids : NodeView or EdgeView
        This is the node or edge IDs that attributes get mapped to.
    cmap : ListedColormap or LinearSegmentedColormap
        colormap to use for NodeStat/EdgeStat.

    Returns
    -------
    dict
        An ID: attribute dictionary.

    Raises
    ------
    TypeError
        If a string, dict, iterable, or NodeStat/EdgeStat is not passed.
    """
    if isinstance(arg, dict):
        return {id: arg[id] for id in arg if id in ids}
    elif isinstance(arg, str):
        return {id: arg for id in ids}
    elif isinstance(arg, (NodeStat, EdgeStat)):
        if isinstance(cmap, ListedColormap):
            vals = np.interp(arg.asnumpy(), [arg.min(), arg.max()], [0, cmap.N])
        elif isinstance(cmap, LinearSegmentedColormap):
            vals = np.interp(arg.asnumpy(), [arg.min(), arg.max()], [0.1, 0.9])
        else:
            raise XGIError("Invalid colormap!")

        return {id: np.array(cmap(vals[i])).reshape(1, -1) for i, id in enumerate(ids)}
    elif isinstance(arg, Iterable):
        return {id: arg[idx] for idx, id in enumerate(ids)}
    else:
        raise TypeError(
            "Argument must be str, dict, iterable, or "
            f"NodeStat/EdgeStat. Received {type(arg)}"
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


def draw_node_labels(
    H,
    pos,
    node_labels=False,
    font_size_nodes=10,
    font_color_nodes="black",
    font_family_nodes="sans-serif",
    font_weight_nodes="normal",
    alpha_nodes=None,
    bbox_nodes=None,
    horizontalalignment_nodes="center",
    verticalalignment_nodes="center",
    ax_nodes=None,
    clip_on_nodes=True,
):
    """Draw node labels on the hypergraph or simplicial complex.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex.
    pos : dict
        Dictionary of positions node_id:(x,y).
    node_labels : bool or dict, optional
        If True, draw ids on the nodes. If a dict, must contain (node_id: label) pairs.
        By default, False.
    font_size_nodes : int, optional
        Font size for text labels, by default 10.
    font_color_nodes : str, optional
        Font color string, by default "black".
    font_family_nodes : str, optional
        Font family, by default "sans-serif".
    font_weight_nodes : str (default='normal')
        Font weight.
    alpha_nodes : float, optional
        The text transparency, by default None.
    bbox_nodes : Matplotlib bbox, optional
        Specify text box properties (e.g. shape, color etc.) for node labels.
        When it is None (default), use Matplotlib's ax.text default
    horizontalalignment_nodes : str, optional
        Horizontal alignment {'center', 'right', 'left'}.
        By default, "center".
    verticalalignment_nodes : str, optional
        Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}.
        By default, "center".
    ax_nodes : matplotlib.pyplot.axes, optional
        Draw the graph in the specified Matplotlib axes.
        By default, None.
    clip_on_nodes : bool, optional
        Turn on clipping of node labels at axis boundaries.
        By default, True.

    Returns
    -------
    dict
        `dict` of labels keyed by node id.

    See Also
    --------
    draw
    draw_nodes
    draw_hyperedges
    draw_simplices
    draw_hyperedge_labels
    """
    if ax_nodes is None:
        ax = plt.gca()
    else:
        ax = ax_nodes

    if node_labels is True:
        node_labels = {id: id for id in H.nodes}

    # Plot the labels in the last layer
    zorder = max_edge_order(H) + 1

    text_items = {}
    for idx, label in node_labels.items():
        (x, y) = pos[idx]

        if not isinstance(label, str):
            label = str(label)

        t = ax.text(
            x,
            y,
            label,
            size=font_size_nodes,
            color=font_color_nodes,
            family=font_family_nodes,
            weight=font_weight_nodes,
            alpha=alpha_nodes,
            horizontalalignment=horizontalalignment_nodes,
            verticalalignment=verticalalignment_nodes,
            transform=ax.transData,
            bbox=bbox_nodes,
            clip_on=clip_on_nodes,
            zorder=zorder,
        )
        text_items[idx] = t

    return text_items


def draw_hyperedge_labels(
    H,
    pos,
    hyperedge_labels=False,
    font_size_edges=10,
    font_color_edges="black",
    font_family_edges="sans-serif",
    font_weight_edges="normal",
    alpha_edges=None,
    bbox_edges=None,
    horizontalalignment_edges="center",
    verticalalignment_edges="center",
    ax_edges=None,
    rotate_edges=False,
    clip_on_edges=True,
):
    """Draw hyperedge labels on the hypegraph or simplicial complex.

    Parameters
    ----------
    H : Hypergraph.
    pos : dict
        Dictionary of positions node_id:(x,y).
    hyperedge_labels : bool or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  By default, False.
    font_size_edges : int, optional
        Font size for text labels, by default 10.
    font_color_edges : str, optional
        Font color string, by default "black".
    font_family_edges : str (default='sans-serif')
        Font family.
    font_weight_edges : str (default='normal')
        Font weight.
    alpha_edges : float, optional
        The text transparency, by default None.
    bbox_edges : Matplotlib bbox, optional
        Specify text box properties (e.g. shape, color etc.) for edge labels.
        By default, {boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0)}
    horizontalalignment_edges : str, optional
        Horizontal alignment {'center', 'right', 'left'}.
        By default, "center".
    verticalalignment_edges: str, optional
        Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}.
        By default, "center".
    ax_edges : matplotlib.pyplot.axes, optional
        Draw the graph in the specified Matplotlib axes. By default, None.
    rotate_edges : bool, optional
        Rotate edge labels for dyadic links to lie parallel to edges, by default False.
    clip_on_edges: bool, optional
        Turn on clipping of hyperedge labels at axis boundaries, by default True.

    Returns
    -------
    dict
        `dict` of labels keyed by hyperedge id.

    See Also
    --------
    draw
    draw_nodes
    draw_hyperedges
    draw_simplices
    draw_node_labels

    """
    if ax_edges is None:
        ax = plt.gca()
    else:
        ax = ax_edges

    if hyperedge_labels is True:
        hyperedge_labels = {id: id for id in H.edges}

    text_items = {}
    for id, label in hyperedge_labels.items():
        he = H.edges.members(id)
        coordinates = [[pos[n][0], pos[n][1]] for n in he]
        x, y = np.mean(coordinates, axis=0)

        if len(he) == 2:
            # Rotate edge labels for dyadic links to lie parallel to edges
            if rotate_edges:
                x_diff, y_diff = np.subtract(coordinates[1], coordinates[0])
                angle = np.arctan2(y_diff, x_diff) / (2.0 * np.pi) * 360
                # Make label orientation "right-side-up"
                if angle > 90:
                    angle -= 180
                if angle < -90:
                    angle += 180
                # Transform data coordinate angle to screen coordinate angle
                xy = np.array((x, y))
                trans_angle = ax.transData.transform_angles(
                    np.array((angle,)), xy.reshape((1, 2))
                )[0]
            else:
                trans_angle = 0.0
        else:
            trans_angle = 0.0

        # Use default box of white with white border
        if bbox_edges is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        else:
            bbox = bbox_edges

        if not isinstance(label, str):
            label = str(label)

        t = ax.text(
            x,
            y,
            label,
            size=font_size_edges,
            color=font_color_edges,
            family=font_family_edges,
            weight=font_weight_edges,
            alpha=alpha_edges,
            horizontalalignment=horizontalalignment_edges,
            verticalalignment=verticalalignment_edges,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            clip_on=clip_on_edges,
        )
        text_items[id] = t

    return text_items


def _update_lims(pos, ax):
    """Update Axis limits based on node positions"""

    # compute axis limits
    pos_arr = np.asarray([[x, y] for n, (x, y) in pos.items()])

    maxx, maxy = np.max(pos_arr, axis=0)
    minx, miny = np.min(pos_arr, axis=0)
    w = maxx - minx
    h = maxy - miny

    # update view after drawing
    padx, pady = 0.05 * w, 0.05 * h
    corners = (minx - padx, miny - pady), (maxx + padx, maxy + pady)
    ax.update_datalim(corners)
    ax.autoscale_view()


def _draw_hull(node_pos, ax, edges_ec, facecolor, alpha, zorder, radius):
    """Draw a convex hull encompassing the nodes in node_pos

    Parameters
    ----------
    node_pos : np.array
        nx2 dimensional array containing positions of the nodes
    ax : matplotlib.pyplot.axes
    edges_ec : str
        Color of the border of the convex hull
    facecolor : str
        Filling color of the convex hull
    alpha : float
        Transparency of the convex hull
    radius : float
        Radius of the convex hull in the vicinity of the nodes.

    Returns
    -------
    ax : matplotlib.pyplot.axes

    """

    thetas = np.linspace(0, 2 * np.pi, num=100, endpoint=False)
    offsets = radius * np.array([np.cos(thetas), np.sin(thetas)]).T
    points = np.vstack([p + offsets for p in node_pos])
    points = np.vstack([node_pos, points])

    hull = ConvexHull(points)

    for simplex in hull.simplices:
        ax.plot(points[simplex, 0], points[simplex, 1], color=edges_ec, zorder=zorder)
    ax.fill(
        points[hull.vertices, 0],
        points[hull.vertices, 1],
        color=facecolor,
        alpha=alpha,
        zorder=zorder,
    )

    return ax


def draw_hypergraph_hull(
    H,
    pos=None,
    ax=None,
    dyad_color="black",
    edge_fc=None,
    edge_ec=None,
    node_fc="tab:blue",
    node_ec="black",
    node_lw=1,
    node_size=7,
    max_order=None,
    node_labels=False,
    hyperedge_labels=False,
    radius=0.05,
    **kwargs,
):
    """Draw hypergraphs displaying the hyperedges of order k>1 as convex hulls


    Parameters
    ----------
    H : Hypergraph
    pos : dict, optional
        If passed, this dictionary of positions node_id:(x,y) is used for placing the
        nodes.  If None (default), use the `barycenter_spring_layout` to compute the
        positions.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
    dyad_color : str, dict, iterable, or EdgeStat, optional
        Color of the dyadic links.  If str, use the same color for all edges. If a dict,
        must contain (edge_id: color_str) pairs.  If iterable, assume the colors are
        specified in the same order as the edges are found in H.edges. If EdgeStat, use
        a colormap (specified with dyad_color_cmap) associated to it. By default,
        "black".
    edge_fc : str, dict, iterable, or EdgeStat, optional
        Color of the hyperedges of order k>1.  If str, use the same color for all
        hyperedges of order k>1.  If a dict, must contain (edge_id: color_str) pairs.
        If other iterable, assume the colors are specified in the same order as the
        hyperedges are found in H.edges. If EdgeStat, use the colormap specified with
        edge_fc_cmap. If None (default), use the H.edges.size.
    edge_ec : str, dict, iterable, or EdgeStat, optional
        Color of the borders of the hyperdges of order k>1.  If str, use the same color
        for all edges. If a dict, must contain (edge_id: color_str) pairs.  If iterable,
        assume the colors are specified in the same order as the edges are found in
        H.edges. If EdgeStat, use a colormap (specified with edge_ec_cmap) associated to
        it. If None (default), use the H.edges.size.
    node_fc : node_fc : str, dict, iterable, or NodeStat, optional
        Color of the nodes.  If str, use the same color for all nodes.  If a dict, must
        contain (node_id: color_str) pairs.  If other iterable, assume the colors are
        specified in the same order as the nodes are found in H.nodes. If NodeStat, use
        the colormap specified with node_fc_cmap. By default, "tab:blue".
    node_ec : str, dict, iterable, or NodeStat, optional
        Color of node borders.  If str, use the same color for all nodes.  If a dict,
        must contain (node_id: color_str) pairs.  If other iterable, assume the colors
        are specified in the same order as the nodes are found in H.nodes. If NodeStat,
        use the colormap specified with node_ec_cmap. By default, "black".
    node_lw : int, float, dict, iterable, or EdgeStat, optional
        Line width of the node borders in pixels.  If int or float, use the same width
        for all node borders.  If a dict, must contain (node_id: width) pairs.  If
        iterable, assume the widths are specified in the same order as the nodes are
        found in H.nodes. If NodeStat, use a monotonic linear interpolation defined
        between min_node_lw and max_node_lw. By default, 1.
    node_size : int, float, dict, iterable, or NodeStat, optional
        Radius of the nodes in pixels.  If int or float, use the same radius for all
        nodes.  If a dict, must contain (node_id: radius) pairs.  If iterable, assume
        the radiuses are specified in the same order as the nodes are found in
        H.nodes. If NodeStat, use a monotonic linear interpolation defined between
        min_node_size and max_node_size. By default, 7.
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
    node_labels : bool, or dict, optional
        If True, draw ids on the nodes. If a dict, must contain (node_id: label) pairs.
        By default, False
    hyperedge_labels : bool, or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  By default, False.
    radius : float, optional
        Radius of the convex hull in the vicinity of the nodes, by default 0.05.
    **kwargs : optional args
        Alternate default values. Values that can be overwritten are the following:
        * min_node_size
        * max_node_size
        * min_node_lw
        * max_node_lw
        * node_fc_cmap
        * node_ec_cmap
        * dyad_color_cmap
        * edge_fc_cmap
        * edge_ec_cmap
        * alpha

    Returns
    -------
    ax : matplotlib.pyplot.axes

    See Also
    --------
    draw

    """

    settings = {
        "min_node_size": 5.0,
        "max_node_size": 30.0,
        "min_node_lw": 1.0,
        "max_node_lw": 5.0,
        "node_fc_cmap": cm.Reds,
        "node_ec_cmap": cm.Greys,
        "dyad_color_cmap": cm.Greys,
        "edge_fc_cmap": cm.Blues,
        "edge_ec_cmap": cm.Greys,
        "alpha": 0.4,
    }

    alpha = settings["alpha"]

    if edge_fc is None:
        edge_fc = H.edges.size

    edge_fc = _color_arg_to_dict(edge_fc, H.edges, settings["edge_fc_cmap"])

    if edge_ec is None:
        edge_ec = H.edges.size

    edge_ec = _color_arg_to_dict(edge_ec, H.edges, settings["edge_ec_cmap"])

    settings.update(kwargs)

    if pos is None:
        pos = barycenter_spring_layout(H)

    if ax is None:
        ax = plt.gca()

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    if not max_order:
        max_order = max_edge_order(H)

    dyad_color = _color_arg_to_dict(dyad_color, H.edges, settings["dyad_color_cmap"])

    for id, he in H._edge.items():
        d = len(he) - 1
        if d > max_order:
            continue
        if d == 1:
            # Drawing the edges
            he = list(he)
            x_coords = [pos[he[0]][0], pos[he[1]][0]]
            y_coords = [pos[he[0]][1], pos[he[1]][1]]
            line = plt.Line2D(
                x_coords,
                y_coords,
                color=dyad_color[id],
                zorder=max_order - 1,
                alpha=1,
            )
            ax.add_line(line)

        else:
            coordinates = [[pos[n][0], pos[n][1]] for n in he]
            _draw_hull(
                node_pos=np.array(coordinates),
                ax=ax,
                edges_ec=edge_ec[id],
                facecolor=edge_fc[id],
                alpha=alpha,
                zorder=max_order - d,
                radius=radius,
            )

    if hyperedge_labels:
        # Get all valid keywords by inspecting the signatures of draw_node_labels
        valid_label_kwds = signature(draw_hyperedge_labels).parameters.keys()
        # Remove the arguments of this function (draw_networkx)
        valid_label_kwds = valid_label_kwds - {"H", "pos", "ax", "hyperedge_labels"}
        if any([k not in valid_label_kwds for k in kwargs]):
            invalid_args = ", ".join([k for k in kwargs if k not in valid_label_kwds])
            raise ValueError(f"Received invalid argument(s): {invalid_args}")
        label_kwds = {k: v for k, v in kwargs.items() if k in valid_label_kwds}
        draw_hyperedge_labels(H, pos, hyperedge_labels, ax_edges=ax, **label_kwds)

    draw_nodes(
        H,
        pos,
        ax,
        node_fc,
        node_ec,
        node_lw,
        node_size,
        max_order,
        settings,
        node_labels,
        **kwargs,
    )

    # compute axis limits
    _update_lims(pos, ax)

    return ax
