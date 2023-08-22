"""Draw hypergraphs and simplicial complexes with matplotlib."""

from inspect import signature
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.patches import FancyArrow
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
from networkx import spring_layout
from scipy.spatial import ConvexHull

from .. import convert
from ..algorithms import max_edge_order, unique_edge_sizes
from ..core import DiHypergraph, Hypergraph, SimplicialComplex
from ..exception import XGIError
from .draw_utils import (
    _CCW_sort,
    _color_arg_to_dict,
    _draw_arg_to_arr,
    _draw_init,
    _interp_draw_arg,
    _scalar_arg_to_dict,
    _update_lims,
)
from .layout import _augmented_projection, barycenter_spring_layout

__all__ = [
    "draw",
    "draw_nodes",
    "draw_hyperedges",
    "draw_simplices",
    "draw_node_labels",
    "draw_hyperedge_labels",
    "draw_hypergraph_hull",
    "draw_multilayer",
    "draw_dihypergraph",
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
    node_shape="o",
    max_order=None,
    node_labels=False,
    hyperedge_labels=False,
    aspect="equal",
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
    node_shape :  string, optional
        The shape of the node. Specification is as matplotlib.scatter
        marker. Default is "o".
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
    node_labels : bool or dict, optional
        If True, draw ids on the nodes. If a dict, must contain (node_id: label) pairs.
        By default, False.
    hyperedge_labels : bool or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  By default, False.
    aspect : {"auto", "equal"} or float, optional
        Set the aspect ratio of the axes scaling, i.e. y/x-scale. `aspect` is passed
        directly to matplotlib's `ax.set_aspect()`. Default is `equal`. See full
        Set the aspect ratio of the axes scaling, i.e. y/x-scale. `aspect` is passed
        directly to matplotlib's `ax.set_aspect()`. Default is `equal`. See full
        description at
        https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_aspect.html
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
        "min_node_size": 5,
        "max_node_size": 30,
        "min_dyad_lw": 2.0,
        "max_dyad_lw": 10.0,
        "min_node_lw": 0,
        "max_node_lw": 5,
        "node_fc_cmap": cm.Reds,
        "node_ec_cmap": cm.Greys,
        "edge_fc_cmap": cm.Blues,
        "dyad_color_cmap": cm.Greys,
    }

    settings.update(kwargs)

    if edge_fc is None:
        edge_fc = H.edges.size

    ax, pos = _draw_init(H, ax, pos)

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

    ax, node_collection = draw_nodes(
        H=H,
        pos=pos,
        ax=ax,
        node_fc=node_fc,
        node_ec=node_ec,
        node_lw=node_lw,
        node_size=node_size,
        node_shape=node_shape,
        zorder=max_order,
        params=settings,
        node_labels=node_labels,
        **kwargs,
    )

    # compute axis limits
    _update_lims(pos, ax)

    ax.set_aspect(aspect, "datalim")

    return ax, node_collection


def draw_nodes(
    H,
    pos=None,
    ax=None,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=15,
    node_shape="o",
    node_fc_cmap="Reds",
    vmin=None,
    vmax=None,
    zorder=None,
    params=dict(),
    node_labels=False,
    rescale_sizes=True,
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
    node_fc : str, iterable, or NodeStat, optional
        Color of the nodes.  If str, use the same color for all nodes. If other iterable,
        or NodeStat, assume the colors are specified in the same order as the nodes are
        found in H.nodes. By default, "white".
    node_ec : color or sequence of colors, optional
        Color of node borders. If color, use the same color for all nodes. If sequence
        of colors, assume the colors are specified in the same order as the nodes are
        found in H.nodes. By default, "black".
    node_lw : int, float, iterable, or NodeStat, optional
        Line width of the node borders in pixels.  If int or float, use the same width
        for all node borders.  If iterable or NodeStat, assume the widths are specified
        in the same order as the nodes are found in H.nodes. Values are clipped below
        and above by min_node_lw and max_node_lw, respectively. By default, 1.
    node_size : int, float, iterable, or NodeStat, optional
        Radius of the nodes in pixels.  If int or float, use the same radius for all
        nodes. If iterable or NodeStat, assume the radiuses are specified in the same
        order as the nodes are found in H.nodes. Values are clipped below
        and above by min_node_size and max_node_size, respectively. By default, 15.
    node_shape :  string, optional
        The shape of the node. Specification is as matplotlib.scatter
        marker. Default is "o".
    node_fc_cmap : colormap
        Colormap for mapping node colors. By default, "Reds". Ignored, if `node_fc` is
        a str (single color).
    vmin : float or None
        Minimum for the node_fc_cmap scaling. By default, None.
    vmax : float or None
        Maximum for the node_fc_cmap scaling. By default, None.
    zorder : int
        The layer on which to draw the nodes.
    node_labels : bool or dict
        If True, draw ids on the nodes. If a dict, must contain (node_id: label) pairs.
    rescale_sizes: bool, optional
        If True, linearly interpolate `node_size` and `node_lw` between min/max values
        (5/30 for size, 0/5 for lw) that can be changed in the other argument `params`.
        If `node_size` (`node_lw`) is a single value, `interpolate_sizes` is ignored
        for it. By default, True.
    params : dict
        Default parameters used if `interpolate_sizes` is True.
        Keys to override default settings:
        * "min_node_size" (default: 5)
        * "max_node_size" (default: 30)
        * "min_node_lw" (default: 0)
        * "max_node_lw" (default: 5)
    kwargs : optional keywords
        See `draw_node_labels` for a description of optional keywords.

    Returns
    -------
    ax : matplotlib Axes
        Axes plotted on
    node_collection : matplotlib PathCollection
        Collection containing the nodes

    See Also
    --------
    draw
    draw_hyperedges
    draw_simplices
    draw_node_labels
    draw_hyperedge_labels

    Notes
    -----

    * If nodes are colored with a cmap, the `node_collection` returned
    can be used to easily plot a colorbar corresponding to the node
    colors. Simply do `plt.colorbar(node_collection)`.

    * Nodes with nonfinite `node_fc` (i.e. `inf`, `-inf` or `nan` are drawn
    with the bad colormap color (see `plotnonfinitebool` in `plt.scatter` and
    Colormap.set_bad from Matplotlib).

    """

    settings = {
        "min_node_size": 5,
        "max_node_size": 30,
        "min_node_lw": 0,
        "max_node_lw": 5,
    }

    settings.update(params)
    settings.update(kwargs)

    # avoid matplotlib scatter UserWarning "Parameters 'cmap' will be ignored"
    if isinstance(node_fc, str):
        node_fc_cmap = None

    ax, pos = _draw_init(H, ax, pos)

    # convert pos to format convenient for scatter
    try:
        xy = np.asarray([pos[v] for v in H.nodes])
    except KeyError as err:
        raise XGIError(f"Node {err} has no position.") from err

    # convert all formats to ndarray
    node_size = _draw_arg_to_arr(node_size)
    node_fc = _draw_arg_to_arr(node_fc)
    node_lw = _draw_arg_to_arr(node_lw)

    # check validity of input values
    if np.any(node_size < 0):
        raise ValueError("node_size cannot contain negative values.")
    if np.any(node_lw < 0):
        raise ValueError("node_lw cannot contain negative values.")

    # interpolate if needed
    if rescale_sizes and isinstance(node_size, np.ndarray):
        node_size = _interp_draw_arg(
            node_size, settings["min_node_size"], settings["max_node_size"]
        )
    if rescale_sizes and isinstance(node_lw, np.ndarray):
        node_lw = _interp_draw_arg(
            node_lw, settings["min_node_lw"], settings["max_node_lw"]
        )

    node_size = node_size**2

    # plot
    node_collection = ax.scatter(
        x=xy[:, 0],
        y=xy[:, 1],
        s=node_size,
        marker=node_shape,
        c=node_fc,
        cmap=node_fc_cmap,
        vmin=vmin,
        vmax=vmax,
        edgecolors=node_ec,
        linewidths=node_lw,
        zorder=zorder,
        plotnonfinite=True,  # plot points with nonfinite color
    )

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

    return ax, node_collection


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

    ax, pos = _draw_init(H, ax, pos)

    if max_order is None:
        max_order = max_edge_order(H)

    if edge_fc is None:
        edge_fc = H.edges.size

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

    ax, pos = _draw_init(H_, ax, pos)

    if edge_fc is None:
        edge_fc = H_.edges.size

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
    node_shape="o",
    max_order=None,
    node_labels=False,
    hyperedge_labels=False,
    radius=0.05,
    aspect="equal",
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
    node_shape :  string, optional
        The shape of the node. Specification is as matplotlib.scatter
        marker. Default is "o".
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
    aspect : {"auto", "equal"} or float, optional
        Set the aspect ratio of the axes scaling, i.e. y/x-scale. `aspect` is passed
        directly to matplotlib's `ax.set_aspect()`. Default is `equal`. See full
        description at
        https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_aspect.html
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

    ax, pos = _draw_init(H, ax, pos)

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

    ax, node_collection = draw_nodes(
        H=H,
        pos=pos,
        ax=ax,
        node_fc=node_fc,
        node_ec=node_ec,
        node_lw=node_lw,
        node_size=node_size,
        node_shape=node_shape,
        zorder=max_order,
        params=settings,
        node_labels=node_labels,
        **kwargs,
    )

    # compute axis limits
    _update_lims(pos, ax)

    ax.set_aspect(aspect, "datalim")

    return ax, node_collection


def draw_multilayer(
    H,
    pos=None,
    ax=None,
    dyad_color="black",
    dyad_lw=0.5,
    edge_fc=None,
    node_fc="white",
    node_ec="black",
    node_lw=0.5,
    node_size=5,
    plane_color="grey",
    max_order=None,
    conn_lines=True,
    conn_lines_style="dotted",
    width=5,
    height=5,
    h_angle=10,
    v_angle=20,
    sep=1,
    **kwargs,
):
    """Draw a hypergraph or simplicial complex visualized in 3D
    showing hyperedges/simplices of different orders on superimposed layers.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex.
        Higher-order network to plot.
    pos : dict or None, optional
        The positions of the nodes in the multilayer network.
        If None, a default layout will be computed using
        xgi.barycenter_spring_layout(). Default is None.
    ax : matplotlib Axes3DSubplot or None, optional
        The subplot to draw the visualization on.
        If None, a new subplot will be created. Default is None.
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
        between min_dyad_lw and max_dyad_lw. By default, 0.5.
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
        min_node_size and max_node_size. By default, 5.
    plane_color : color (str or tuple) or iterable (dict, list, or numpy array), optional
        Color of each plane. If a dict, must contain (edge size: color) pairs.
        By default, "grey".
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
    conn_lines : bool, optional
        Whether to draw connections between layers. Default is True.
    conn_lines_style : str, optional
        The linestyle of the connections between layers. Default is 'dotted'.
    width : float, optional
        The width of the figure in inches. Default is 5.
    height : float, optional
        The height of the figure in inches. Default is 5.
    h_angle : float, optional
        The rotation angle around the horizontal axis in degrees. Default is 10.
    v_angle : float, optional
        The rotation angle around the vertical axis in degrees. Default is 0.
    sep : float, optional
        The separation between layers. Default is 1.
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

    Returns
    -------
    ax : matplotlib Axes3DSubplot
        The subplot with the multilayer network visualization.
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
        "plane_color_cmap": cm.Greys,
    }

    settings.update(kwargs)

    if edge_fc is None:
        edge_fc = H.edges.size

    if pos is None:
        pos = barycenter_spring_layout(H)

    if ax is None:
        _, ax = plt.subplots(
            1, 1, figsize=(width, height), dpi=600, subplot_kw={"projection": "3d"}
        )

    s = unique_edge_sizes(H)
    if max_order is None:
        max_order = max(s) - 1
    else:
        max_order = min(max_order, max(s) - 1)
    min_order = min(s) - 1

    xs, ys = zip(*pos.values())

    dyad_color = _color_arg_to_dict(dyad_color, H.edges, settings["dyad_color_cmap"])
    dyad_lw = _scalar_arg_to_dict(
        dyad_lw, H.edges, settings["min_dyad_lw"], settings["max_dyad_lw"]
    )

    edge_fc = _color_arg_to_dict(edge_fc, H.edges, settings["edge_fc_cmap"])

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

    plane_color = _color_arg_to_dict(
        plane_color,
        [i for i in range(min_order, max_order + 1)],
        settings["plane_color_cmap"],
    )

    for id, he in H.edges.members(dtype=dict).items():
        d = len(he) - 1
        zs = d * sep

        # dyads
        if d > max_order:
            continue

        if d == 1:
            he = list(he)
            x1 = [pos[he[0]][0], pos[he[0]][1], zs]
            x2 = [pos[he[1]][0], pos[he[1]][1], zs]
            l = Line3DCollection(
                [(x1, x2)],
                color=dyad_color[id],
                linewidth=dyad_lw[id],
            )
            ax.add_collection3d(l)
        # higher-orders
        else:
            poly = []
            vertices = np.array([[pos[i][0], pos[i][1], zs] for i in he])
            vertices = _CCW_sort(vertices)
            poly.append(vertices)
            poly = Poly3DCollection(
                poly,
                zorder=d - 1,
                color=edge_fc[id],
                alpha=0.5,
                edgecolor=None,
            )
            ax.add_collection3d(poly)

    # now draw by order
    # draw lines connecting points on the different planes
    if conn_lines:
        lines3d_between = [
            (list(pos[i]) + [min_order * sep], list(pos[i]) + [max_order * sep])
            for i in H.nodes
        ]
        between_lines = Line3DCollection(
            lines3d_between,
            zorder=d,
            color=".5",
            alpha=0.4,
            linestyle=conn_lines_style,
            linewidth=1,
        )
        ax.add_collection3d(between_lines)

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
    for d in range(min_order, max_order + 1):
        # draw nodes
        z = [sep * d] * H.num_nodes
        ax.scatter(
            x,
            y,
            z,
            s=s,
            c=c,
            edgecolors=ec,
            linewidths=lw,
            zorder=max_order + 1,
            alpha=1,
        )

        # draw surfaces corresponding to the different orders
        xdiff = np.max(xs) - np.min(xs)
        ydiff = np.max(ys) - np.min(ys)
        ymin = np.min(ys) - ydiff * 0.1
        ymax = np.max(ys) + ydiff * 0.1
        xmin = np.min(xs) - xdiff * 0.1 * (width / height)
        xmax = np.max(xs) + xdiff * 0.1 * (width / height)
        xx, yy = np.meshgrid([xmin, xmax], [ymin, ymax])
        zz = np.zeros(xx.shape) + d * sep
        ax.plot_surface(
            xx,
            yy,
            zz,
            color=plane_color[d],
            alpha=0.1,
            zorder=d,
        )

    ax.view_init(h_angle, v_angle)
    ax.set_ylim(np.min(ys) - ydiff * 0.1, np.max(ys) + ydiff * 0.1)
    ax.set_xlim(np.min(xs) - xdiff * 0.1, np.max(xs) + xdiff * 0.1)
    ax.set_axis_off()

    return ax


def draw_dihypergraph(
    DH,
    ax=None,
    lines_fc=None,
    lines_lw=1.5,
    line_head_width=0.05,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=15,
    edge_marker_toggle=True,
    edge_marker_fc=None,
    edge_marker_ec=None,
    edge_marker="s",
    edge_marker_lw=1,
    edge_marker_size=15,
    max_order=None,
    node_labels=False,
    hyperedge_labels=False,
    settings=None,
    **kwargs,
):
    """Draw a directed hypergraph

    Parameters
    ----------
    DH : DirectedHypergraph
        The directed hypergraph to draw.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
    lines_fc : str, dict, iterable, optional
        Color of the hyperedges (lines). If str, use the same color for all hyperedges.
        If a dict, must contain (hyperedge_id: color_str) pairs. If other iterable,
        assume the colors are specified in the same order as the hyperedges are found
        in DH.edges. If None (default), use the size of the hyperedges.
    lines_lw : int, float, dict, iterable, optional
        Line width of the hyperedges (lines). If int or float, use the same width for
        all hyperedges. If a dict, must contain (hyperedge_id: width) pairs. If other
        iterable, assume the widths are specified in the same order as the hyperedges
        are found in DH.edges. By default, 1.5.
    line_head_width : float, optional
        Length of arrows' heads. By default, 0.05
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
    edge_marker_toggle: bool, optional
        If True then marker representing the hyperedges are drawn. By default True.
    edge_marker_fc: str, dict, iterable, optional
        Filling color of the hyperedges (markers). If str, use the same color for all hyperedges.
        If a dict, must contain (hyperedge_id: color_str) pairs. If other iterable,
        assume the colors are specified in the same order as the hyperedges are found
        in DH.edges. If None (default), use the size of the hyperedges.
    edge_marker_ec: str, dict, iterable, optional
        Edge color of the hyperedges (markers). If str, use the same color for all hyperedges.
        If a dict, must contain (hyperedge_id: color_str) pairs. If other iterable,
        assume the colors are specified in the same order as the hyperedges are found
        in DH.edges. If None (default), use the size of the hyperedges.
    edge_marker: str, optional
        Marker used for the hyperedges. By default 's' (square marker).
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
        * node_fc_cmap
        * node_ec_cmap
        * min_lines_lw
        * max_lines_lw
        * lines_fc_cmap
        * edge_fc_cmap
        * edge_marker_fc_cmap
        * edge_marker_ec_cmap

    Returns
    -------
    ax : matplotlib.pyplot.axes

    Raises
    ------
    XGIError
        If something different than a DiHypergraph is passed.

    See Also
    --------
    draw
    draw_nodes
    draw_node_labels

    """
    if not isinstance(DH, DiHypergraph):
        raise XGIError("The input must be a DiHypergraph")

    if settings is None:
        settings = {
            "min_node_size": 10.0,
            "max_node_size": 30.0,
            "min_node_lw": 1.0,
            "max_node_lw": 5.0,
            "node_fc_cmap": cm.Reds,
            "node_ec_cmap": cm.Greys,
            "min_lines_lw": 2.0,
            "max_lines_lw": 10.0,
            "lines_fc_cmap": cm.Blues,
            "edge_marker_fc_cmap": cm.Blues,
            "edge_marker_ec_cmap": cm.Greys,
        }

    settings.update(kwargs)

    if ax is None:
        ax = plt.gca()

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    # convert to hypergraph in order to use the augmented projection function
    H_conv = convert.convert_to_hypergraph(DH)

    if not max_order:
        max_order = max_edge_order(H_conv)

    lines_lw = _scalar_arg_to_dict(
        lines_lw, H_conv.edges, settings["min_lines_lw"], settings["max_lines_lw"]
    )

    if lines_fc is None:
        lines_fc = H_conv.edges.size

    lines_fc = _color_arg_to_dict(lines_fc, H_conv.edges, settings["lines_fc_cmap"])

    if edge_marker_fc is None:
        edge_marker_fc = H_conv.edges.size

    edge_marker_fc = _color_arg_to_dict(
        edge_marker_fc, H_conv.edges, settings["edge_marker_fc_cmap"]
    )

    if edge_marker_ec is None:
        edge_marker_ec = H_conv.edges.size

    edge_marker_ec = _color_arg_to_dict(
        edge_marker_ec, H_conv.edges, settings["edge_marker_ec_cmap"]
    )

    node_size = _scalar_arg_to_dict(
        node_size, H_conv.nodes, settings["min_node_size"], settings["max_node_size"]
    )

    G_aug = _augmented_projection(H_conv)
    for dyad in H_conv.edges.filterby("size", 2).members():
        try:
            index = max(n for n in G_aug.nodes if isinstance(n, int)) + 1
        except ValueError:
            # The list of node-labels has no integers, so I start from 0
            index = 0
        G_aug.add_edges_from([[list(dyad)[0], index], [list(dyad)[1], index]])

    phantom_nodes = [n for n in list(G_aug.nodes) if n not in list(H_conv.nodes)]
    pos = spring_layout(G_aug)

    for id, he in DH.edges.members(dtype=dict).items():
        d = len(he) - 1
        if d > 0:
            # identify the center of the edge in the augemented projection
            center = [n for n in phantom_nodes if set(G_aug.neighbors(n)) == he][0]
            x_center, y_center = pos[center]
            for node in DH.edges.dimembers(id)[0]:
                x_coords = [pos[node][0], x_center]
                y_coords = [pos[node][1], y_center]
                line = plt.Line2D(
                    x_coords,
                    y_coords,
                    color=lines_fc[id],
                    lw=lines_lw[id],
                    zorder=max_order - d,
                )
                ax.add_line(line)
            for node in DH.edges.dimembers(id)[1]:
                dx, dy = pos[node][0] - x_center, pos[node][1] - y_center
                # the following to avoid the point of the arrow overlapping the node
                distance = np.hypot(dx, dy)
                direction_vector = np.array([dx, dy]) / distance
                shortened_distance = (
                    distance - node_size[node] * 0.003
                )  # Calculate the shortened length
                dx = direction_vector[0] * shortened_distance
                dy = direction_vector[1] * shortened_distance
                arrow = FancyArrow(
                    x_center,
                    y_center,
                    dx,
                    dy,
                    color=lines_fc[id],
                    width=lines_lw[id] * 0.001,
                    length_includes_head=True,
                    head_width=line_head_width,
                    zorder=max_order - d,
                )
                ax.add_patch(arrow)
            if edge_marker_toggle:
                ax.scatter(
                    x=x_center,
                    y=y_center,
                    marker=edge_marker,
                    s=edge_marker_size**2,
                    c=edge_marker_fc[id],
                    edgecolors=edge_marker_ec[id],
                    linewidths=edge_marker_lw,
                    zorder=max_order,
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
        if "font_size_edges" not in label_kwds:
            label_kwds["font_size_edges"] = 6
        draw_hyperedge_labels(H_conv, pos, hyperedge_labels, ax_edges=ax, **label_kwds)

    draw_nodes(
        H=H_conv,
        pos=pos,
        ax=ax,
        node_fc=node_fc,
        node_ec=node_ec,
        node_lw=node_lw,
        node_size=node_size,
        zorder=max_order,
        params=settings,
        node_labels=node_labels,
        **kwargs,
    )

    # compute axis limits
    _update_lims(pos, ax)

    return ax
