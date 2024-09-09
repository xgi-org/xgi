"""Draw hypergraphs and simplicial complexes with matplotlib."""

from inspect import signature
from itertools import chain

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb  # This cannot be removed because it is used for cmap "crest"
from matplotlib import cm
from matplotlib.colors import is_color_like
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.art3d import (
    Line3DCollection,
    LineCollection,
    PatchCollection,
    Poly3DCollection,
)
from scipy.spatial import ConvexHull

chaini = chain.from_iterable

from .. import convert
from ..algorithms import max_edge_order, unique_edge_sizes
from ..convert import to_bipartite_edgelist
from ..core import DiHypergraph, Hypergraph, SimplicialComplex
from ..exception import XGIError
from ..utils import subfaces
from .draw_utils import (
    _CCW_sort,
    _draw_arg_to_arr,
    _draw_init,
    _interp_draw_arg,
    _parse_color_arg,
    _update_lims,
)
from .layout import barycenter_spring_layout, bipartite_spring_layout

__all__ = [
    "draw",
    "draw_nodes",
    "draw_hyperedges",
    "draw_simplices",
    "draw_node_labels",
    "draw_hyperedge_labels",
    "draw_multilayer",
    "draw_bipartite",
    "draw_undirected_dyads",
    "draw_directed_dyads",
]


def draw(
    H,
    pos=None,
    ax=None,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=7,
    node_shape="o",
    node_fc_cmap="Reds",
    vmin=None,
    vmax=None,
    max_order=None,
    dyad_color="black",
    dyad_lw=1.5,
    dyad_style="solid",
    dyad_color_cmap="Greys",
    dyad_vmin=None,
    dyad_vmax=None,
    edge_fc=None,
    edge_fc_cmap="crest_r",
    edge_vmin=None,
    edge_vmax=None,
    edge_ec=None,
    alpha=0.4,
    hull=False,
    radius=0.05,
    node_labels=False,
    hyperedge_labels=False,
    rescale_sizes=True,
    aspect="equal",
    **kwargs,
):
    """Draw hypergraph or simplicial complex.

    Parameters
    ----------
    H : Hypergraph or SimplicialComplex.
        Hypergraph to draw
    pos : dict, optional
        If passed, this dictionary of positions node_id:(x,y) is used for placing the
        0-simplices.  If None (default), use the `barycenter_spring_layout` to compute
        the positions.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
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
    node_fc_cmap : colormap
        Colormap for mapping node colors. By default, "Reds". Ignored, if `node_fc` is
        a str (single color).
    vmin : float or None
        Minimum for the node_fc_cmap scaling. By default, None.
    vmax : float or None
        Maximum for the node_fc_cmap scaling. By default, None.
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
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
    dyad_style : str or list of strings, optional
        Line style of the dyads, e.g. ‘-’, ‘–’, ‘-.’, ‘:’ or words like ‘solid’ or ‘dashed’.
        See matplotlib's documentation for all accepted values. By default, "solid".
    dyad_color_cmap: matplotlib colormap
        Colormap used to map the dyad colors. By default, "Greys".
    dyad_vmin, dyad_vmax : float, optional
        Minimum and maximum for dyad colormap scaling. By default, None.
    edge_fc : color or list of colors or array-like or dict or EdgeStat, optional
        Color of the hyperedges.  The accepted formats are the same as
        matplotlib's scatter, with the addition of dict and IDStat.
        Those with colors:

        * single color as a string
        * single color as 3- or 4-tuple
        * list of colors of length len(ids)
        * dict of colors containing the `ids` as keys

        Those with numerical values (will be mapped to colors):

        * array of floats
        * dict of floats containing the `ids` as keys
        * IDStat containing the `ids` as keys

        If None (default), color by edge size.
    edge_fc_cmap: matplotlib colormap
        Colormap used to map the edge colors. By default, "cres_r".
    edge_vmin, edge_vmax : float, optional
        Minimum and maximum for edge colormap scaling. By default, None.
    edge_ec : color or list of colors or array-like or dict or EdgeStat, optional
        Color of the hyperedges.  The accepted formats are the same as
        matplotlib's scatter, with the addition of dict and IDStat.
        Formats with colors:

        * single color as a string
        * single color as 3- or 4-tuple
        * list of colors of length len(ids)
        * dict of colors containing the `ids` as keys

        Formats with numerical values (will be mapped to colors):

        * array of floats
        * dict of floats containing the `ids` as keys
        * IDStat containing the `ids` as keys

        If None (default), color by edge size.
        Numerical formats will be mapped to colors using edge_vmin, edge_vmax,
        and edge_fc_cmap.
    alpha : float, optional
        The edge transparency. By default, 0.4.
    hull : bool, optional
        Wether to draw hyperedes as convex hulls. By default, False.
    radius: float, optional
        Radius margin around the nodes when drawing convex hulls. Ignored if
        `hull is False`. Default is 0.05.
    node_labels : bool or dict, optional
        If True, draw ids on the nodes. If a dict, must contain (node_id: label) pairs.
        By default, False. The default node_size (7) is too small to display the default
        labels well. The user may need to set it to a size of a least 15.
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
    rescale_sizes: bool, optional
        If True, linearly interpolate `node_size`, `node_lw` and `dyad_lw`
        between min/max values that can be changed in the other argument `params`.
        If those are single values, `interpolate_sizes` is ignored
        for it. By default, True.
    **kwargs : optional args
        Alternate default values. Values that can be overwritten are the following:

        * "min_node_size" (default: 5)
        * "max_node_size" (default: 30)
        * "min_node_lw" (default: 0)
        * "max_node_lw" (default: 5)
        * "min_dyad_lw" (default: 1)
        * "max_dyad_lw" (default: 10)

    Returns
    -------
    ax : matplotlib Axes
        Axes plotted on
    collections : a tuple of 3 collections:

        * node_collection : matplotlib PathCollection
            Collection containing the nodes
        * dyad_collection : matplotlib LineCollection
            Collection containing the dyads
        * edge_collection : matplotlib PathCollection
            Collection containing the edges

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
        "min_dyad_lw": 1,
        "max_dyad_lw": 10,
        "min_node_lw": 0,
        "max_node_lw": 5,
    }

    settings.update(kwargs)

    ax, pos = _draw_init(H, ax, pos)

    if not max_order:
        max_order = max_edge_order(H)

    if isinstance(H, SimplicialComplex):
        ax, (dyad_collection, edge_collection) = draw_simplices(
            SC=H,
            pos=pos,
            ax=ax,
            dyad_color=dyad_color,
            dyad_lw=dyad_lw,
            dyad_style=dyad_style,
            dyad_color_cmap=dyad_color_cmap,
            dyad_vmin=dyad_vmin,
            dyad_vmax=dyad_vmax,
            alpha=alpha,
            edge_fc=edge_fc,
            edge_fc_cmap=edge_fc_cmap,
            edge_vmin=edge_vmin,
            edge_vmax=edge_vmax,
            edge_ec=edge_ec,
            max_order=max_order,
            hyperedge_labels=hyperedge_labels,
            rescale_sizes=rescale_sizes,
            **kwargs,
        )

    elif isinstance(H, Hypergraph):

        ax, (dyad_collection, edge_collection) = draw_hyperedges(
            H=H,
            pos=pos,
            ax=ax,
            dyad_color=dyad_color,
            dyad_lw=dyad_lw,
            dyad_style=dyad_style,
            dyad_color_cmap=dyad_color_cmap,
            dyad_vmin=dyad_vmin,
            dyad_vmax=dyad_vmax,
            alpha=alpha,
            edge_fc=edge_fc,
            edge_fc_cmap=edge_fc_cmap,
            edge_vmin=edge_vmin,
            edge_vmax=edge_vmax,
            edge_ec=edge_ec,
            max_order=max_order,
            hyperedge_labels=hyperedge_labels,
            hull=hull,
            radius=radius,
            rescale_sizes=rescale_sizes,
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
        node_fc_cmap=node_fc_cmap,
        vmin=vmin,
        vmax=vmax,
        zorder=max_order,
        params=settings,
        node_labels=node_labels,
        rescale_sizes=rescale_sizes,
        **kwargs,
    )

    # compute axis limits
    _update_lims(pos, ax)

    ax.set_aspect(aspect, "datalim")

    return ax, (node_collection, dyad_collection, edge_collection)


def draw_nodes(
    H,
    pos=None,
    ax=None,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=7,
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
    pos : dict, optional
        If passed, this dictionary of positions node_id:(x,y) is used for placing the
        0-simplices.  If None (default), use the `barycenter_spring_layout` to compute
        the positions.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
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
        The default node_size (7) is too small to display the default labels well.
        The user may need to set it to a size of a least 15.
    rescale_sizes: bool, optional
        If True, linearly interpolate `node_size` and `node_lw` between min/max values
        (5/30 for size, 0/5 for lw) that can be changed in the other argument `params`.
        If `node_size` (`node_lw`) is a single value, `interpolate_sizes` is ignored
        for it. By default, True.
    params : dict
        Default parameters used if `rescale_sizes` is True.
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
    If nodes are colored with a cmap, the `node_collection` returned
    can be used to easily plot a colorbar corresponding to the node
    colors. Simply do `plt.colorbar(node_collection)`.

    Nodes with nonfinite `node_fc` (i.e. `inf`, `-inf` or `nan` are drawn
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

    # avoid matplotlib scatter UserWarning "Parameters 'cmap' will be ignored"
    if isinstance(node_fc, str) or (
        isinstance(node_fc, np.ndarray) and is_color_like(node_fc[0])
    ):
        node_fc_cmap = None

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

    node_size = np.array(node_size) ** 2

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
    dyad_style="solid",
    dyad_color_cmap="Greys",
    dyad_vmin=None,
    dyad_vmax=None,
    edge_fc=None,
    edge_fc_cmap="crest_r",
    edge_vmin=None,
    edge_vmax=None,
    edge_ec=None,
    alpha=0.4,
    max_order=None,
    params=dict(),
    hyperedge_labels=False,
    hull=False,
    radius=0.05,
    rescale_sizes=True,
    **kwargs,
):
    """Draw hyperedges.

    Parameters
    ----------
    H : Hypergraph
        Hypergraph to plot
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
    dyad_style : str or list of strings, optional
        Line style of the dyads, e.g. ‘-’, ‘–’, ‘-.’, ‘:’ or words like ‘solid’ or ‘dashed’.
        See matplotlib's documentation for all accepted values. By default, "solid".
    dyad_color_cmap: matplotlib colormap
        Colormap used to map the dyad colors. By default, "Greys".
    dyad_vmin, dyad_vmax : float, optional
        Minimum and maximum for dyad colormap scaling. By default, None.
    edge_fc : color or list of colors or array-like or dict or EdgeStat, optional
        Color of the hyperedges.  The accepted formats are the same as
        matplotlib's scatter, with the addition of dict and IDStat.
        Formats with colors:

        * single color as a string
        * single color as 3- or 4-tuple
        * list of colors of length len(ids)
        * dict of colors containing the `ids` as keys

        Formats with numerical values (will be mapped to colors):
        * array of floats
        * dict of floats containing the `ids` as keys
        * IDStat containing the `ids` as keys

        If None (default), color by edge size.
    edge_fc_cmap: matplotlib colormap
        Colormap used to map the edge colors. By default, "crest_r".
    edge_vmin, edge_vmax : float, optional
        Minimum and maximum for edge colormap scaling. By default, None.
    edge_ec : color or list of colors or array-like or dict or EdgeStat, optional
        Color of the hyperedges.  The accepted formats are the same as
        matplotlib's scatter, with the addition of dict and IDStat.
        Formats with colors:

        * single color as a string
        * single color as 3- or 4-tuple
        * list of colors of length len(ids)
        * dict of colors containing the `ids` as keys

        Formats with numerical values (will be mapped to colors):

        * array of floats
        * dict of floats containing the `ids` as keys
        * IDStat containing the `ids` as keys

        If None (default), color by edge size.
        Numerical formats will be mapped to colors using edge_vmin, edge_vmax,
        and edge_fc_cmap.
    alpha : float, optional
        The edge transparency. By default, 0.4.
    max_order : int, optional
        Maximum of hyperedges to plot. By default, None.
    hyperedge_labels : bool or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  By default, None.
    hull : bool, optional
        Wether to draw hyperedes as convex hulls. By default, False.
    radius: float, optional
        Radius margin around the nodes when drawing convex hulls. Ignored if
        `hull is False`. Default is 0.05.
    rescale_sizes: bool, optional
        If True, linearly interpolate `dyad_lw` and between min/max values
        (1/10) that can be changed in the other argument `params`.
        If `dyad_lw` is a single value, `interpolate_sizes` is ignored
        for it. By default, True.
    params : dict
        Default parameters. Keys that may be useful to override default settings:

        * "min_dyad_lw" (default: 1)
        * "max_dyad_lw" (default: 10)

    kwargs : optional keywords
        See `draw_hyperedge_labels` for a description of optional keywords.

    Returns
    -------
    ax : matplotlib Axes
        Axes plotted on
    collections : a tuple of 2 collections:

        * dyad_collection : matplotlib LineCollection
            Collection containing the dyads
        * edge_collection : matplotlib PathCollection
            Collection containing the edges

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

    settings = {
        "min_dyad_lw": 1,
        "max_dyad_lw": 10,
    }

    settings.update(params)
    settings.update(kwargs)

    ax, pos = _draw_init(H, ax, pos)

    # filter edge sizes
    if max_order is None:
        max_order = max_edge_order(H)
    dyads = H.edges.filterby("order", 1)
    edges = H.edges.filterby("order", (2, max_order), "between")

    if edge_fc is None:  # color is proportional to size
        edge_fc = edges.size
    if edge_ec is None:  # color is proportional to size
        edge_ec = edges.size

    # convert all formats to ndarray
    dyad_lw = _draw_arg_to_arr(dyad_lw)

    # parse colors
    dyad_color, dyad_c_to_map = _parse_color_arg(dyad_color, list(dyads))
    edge_fc, edge_c_to_map = _parse_color_arg(edge_fc, list(edges))
    edge_ec, edge_ec_to_map = _parse_color_arg(edge_ec, list(edges))
    # edge_c_to_map and dyad_c_to_map are True if the colors
    # are input as numeric values that need to be mapped to colors

    # check validity of input values
    if np.any(dyad_lw < 0):
        raise ValueError("dyad_lw cannot contain negative values.")

    # interpolate if needed
    if rescale_sizes and isinstance(dyad_lw, np.ndarray):
        dyad_lw = _interp_draw_arg(
            dyad_lw, settings["min_dyad_lw"], settings["max_dyad_lw"]
        )

    # convert dyad pos to format convenient for scatter
    dyad_pos = np.asarray([(pos[list(e)[0]], pos[list(e)[1]]) for e in dyads.members()])

    # plot dyads
    if dyad_c_to_map:
        dyad_c_arr = dyad_color
        dyad_colors = None
    else:
        dyad_c_arr = None
        dyad_colors = dyad_color

    dyad_collection = LineCollection(
        dyad_pos,
        colors=dyad_colors,
        array=dyad_c_arr,  # colors if to be mapped, ie arr of floats
        linewidths=dyad_lw,
        antialiaseds=(1,),
        linestyle=dyad_style,
        cmap=dyad_color_cmap,
        zorder=max_order - 1,
    )

    # dyad_collection.set_cmap(dyad_color_cmap)
    if dyad_c_to_map:
        dyad_collection.set_clim(dyad_vmin, dyad_vmax)
    # dyad_collection.set_zorder(max_order - 1)  # edges go behind nodes
    ax.add_collection(dyad_collection)

    # reorder to plot larger hyperedges first
    ids_sorted = np.argsort(edges.size.aslist())[::-1]

    # plot other hyperedges

    # prepare colors for PatchCollection format
    if edge_c_to_map:
        edge_fc_arr = edge_fc[ids_sorted]
        edge_fc_colors = None
    else:
        edge_fc_arr = None
        edge_fc_colors = edge_fc[ids_sorted] if len(edge_fc) > 1 else edge_fc

    edge_ec = edge_ec[ids_sorted] if len(edge_ec) > 1 else edge_ec  # reorder

    if edge_ec_to_map:  # edgecolors need to be manually mapped

        # create scalarmappable to map floats to colors
        # we use the same vmin, vmax, and cmap as for edge_fc
        norm = mpl.colors.Normalize(vmin=edge_vmin, vmax=edge_vmax)
        sm_edgecolors = cm.ScalarMappable(norm=norm, cmap=edge_fc_cmap)

        edge_ec = sm_edgecolors.to_rgba(edge_ec)  # map to colors

    patches = []
    for he in np.array(edges.members())[ids_sorted]:
        d = len(he) - 1
        he = list(he)
        coordinates = [[pos[n][0], pos[n][1]] for n in he]
        # Sorting the points counterclockwise (needed to have the correct filling)
        sorted_coordinates = _CCW_sort(coordinates)
        if hull:
            # add points in circle with radius around each node
            thetas = np.linspace(0, 2 * np.pi, num=100, endpoint=False)
            offsets = radius * np.array([np.cos(thetas), np.sin(thetas)]).T
            points = np.vstack([p + offsets for p in sorted_coordinates])
            points = np.vstack([sorted_coordinates, points])

            hull = ConvexHull(points)
            pts = points[hull.vertices]

            patch = plt.Polygon(pts, capstyle="round")

        else:
            patch = plt.Polygon(sorted_coordinates)
        patches.append(patch)

    edge_collection = PatchCollection(
        patches,
        facecolors=edge_fc_colors,
        array=edge_fc_arr,  # will be mapped by PatchCollection
        cmap=edge_fc_cmap,
        edgecolors=edge_ec,
        alpha=alpha,
        zorder=max_order - 2,  # below dyads
    )
    # edge_collection.set_cmap(edge_fc_cmap)
    if edge_c_to_map:
        edge_collection.set_clim(edge_vmin, edge_vmax)
    ax.add_collection(edge_collection)

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

    return ax, (dyad_collection, edge_collection)


def draw_simplices(
    SC,
    pos=None,
    ax=None,
    dyad_color="black",
    dyad_lw=1.5,
    dyad_style="solid",
    dyad_color_cmap="Greys",
    dyad_vmin=None,
    dyad_vmax=None,
    edge_fc=None,
    edge_fc_cmap="crest_r",
    edge_vmin=None,
    edge_vmax=None,
    alpha=0.4,
    max_order=None,
    params=dict(),
    hyperedge_labels=False,
    rescale_sizes=True,
    **kwargs,
):
    """Draw maximal simplices and pairwise faces.

    Parameters
    ----------
    SC : SimplicialComplex
        Simplicial complex to draw
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
    dyad_style : str or list of strings, optional
        Line style of the dyads, e.g. ‘-’, ‘–’, ‘-.’, ‘:’ or words like ‘solid’ or ‘dashed’.
        See matplotlib's documentation for all accepted values. By default, "solid".
    dyad_color_cmap: matplotlib colormap
        Colormap used to map the dyad colors. By default, "Greys".
    dyad_vmin, dyad_vmax : float, optional
        Minimum and maximum for dyad colormap scaling. By default, None.
    edge_fc : color or list of colors or array-like or dict or EdgeStat, optional
        Color of the hyperedges.  The accepted formats are the same as
        matplotlib's scatter, with the addition of dict and IDStat.
        Those with colors:

        * single color as a string
        * single color as 3- or 4-tuple
        * list of colors of length len(ids)
        * dict of colors containing the `ids` as keys

        Those with numerical values (will be mapped to colors):

        * array of floats
        * dict of floats containing the `ids` as keys
        * IDStat containing the `ids` as keys

        If None (default), color by edge size.
    edge_fc_cmap: matplotlib colormap
        Colormap used to map the edge colors. By default, "crest_r".
    edge_vmin, edge_vmax : float, optional
        Minimum and maximum for edge colormap scaling. By default, None.
    alpha : float, optional
        The edge transparency. By default, 0.4.
    max_order : int, optional
        Maximum of hyperedges to plot. By default, None.
    hyperedge_labels : bool or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  By default, None.
    rescale_sizes: bool, optional
        If True, linearly interpolate `dyad_lw` and between min/max values
        (1/10) that can be changed in the other argument `params`.
        If `dyad_lw` is a single value, `interpolate_sizes` is ignored
        for it. By default, True.
    params : dict
        Default parameters. Keys that may be useful to override default settings:

        * "min_dyad_lw" (default: 1)
        * "max_dyad_lw" (default: 10)

    kwargs : optional keywords
        See `draw_hyperedge_labels` for a description of optional keywords.

    Returns
    -------
    ax
    collections : a tuple of 2 collections:

        * dyad_collection : matplotlib LineCollection
            Collection containing the dyads
        * edge_collection : matplotlib PathCollection
            Collection containing the edges

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

    # add the projected pairwise interactions
    dyads = subfaces(H_.edges.members(), order=1)
    H_.add_edges_from(dyads)
    H_.cleanup(
        multiedges=False,
        isolates=True,
        connected=False,
        relabel=False,
        in_place=True,
        singletons=True,
    )  # remove multi-dyads

    if not max_order:
        max_order = max_edge_order(H_)

    ax, (dyad_collection, edge_collection) = draw_hyperedges(
        H_,
        pos=pos,
        ax=ax,
        dyad_color=dyad_color,
        dyad_lw=dyad_lw,
        dyad_style=dyad_style,
        dyad_color_cmap=dyad_color_cmap,
        dyad_vmin=dyad_vmin,
        dyad_vmax=dyad_vmax,
        edge_fc=edge_fc,
        edge_fc_cmap=edge_fc_cmap,
        edge_vmin=edge_vmin,
        edge_vmax=edge_vmax,
        alpha=alpha,
        max_order=max_order,
        params=params,
        hyperedge_labels=hyperedge_labels,
        rescale_sizes=rescale_sizes,
        **kwargs,
    )

    return ax, (dyad_collection, edge_collection)


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
    zorder=None,
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
    zorder : int, optional
        The vertical order on which to draw the labels. By default, None,
        in which case it is plotted above the last plotted object.

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
    if zorder is None:
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


def draw_multilayer(
    H,
    pos=None,
    ax=None,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=5,
    node_shape="o",
    node_fc_cmap="Reds",
    vmin=None,
    vmax=None,
    dyad_color="grey",
    dyad_lw=1.5,
    dyad_style="solid",
    edge_fc=None,
    edge_fc_cmap="crest_r",
    edge_vmin=None,
    edge_vmax=None,
    alpha=0.4,
    layer_color="grey",
    layer_cmap="crest_r",
    max_order=None,
    conn_lines=True,
    conn_lines_style="dotted",
    h_angle=10,
    v_angle=20,
    sep=0.4,
    rescale_sizes=True,
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
        and above by min_node_size and max_node_size, respectively. By default, 5.
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
    dyad_color : color or list of colors
        Color of the dyadic links.  If str, use the same color for all edges. If iterable,
        assume the colors are specified in the same order as the edges are found in H.edges.
        By default, "black".
    dyad_lw : int, float, dict, iterable, or EdgeStat, optional
        Line width of edges of order 1 (dyadic links).  If int or float, use the same
        width for all edges.  If a dict, must contain (edge_id: width) pairs.  If
        iterable, assume the widths are specified in the same order as the edges are
        found in H.edges. If EdgeStat, use a monotonic linear interpolation defined
        between min_dyad_lw and max_dyad_lw. By default, 1.5.
    dyad_style : str or list of strings, optional
        Line style of the dyads, e.g. ‘-’, ‘–’, ‘-.’, ‘:’ or words like ‘solid’ or ‘dashed’.
        See matplotlib's documentation for all accepted values. By default, "solid".
    edge_fc : color or list of colors or array-like or dict or EdgeStat, optional
        Color of the hyperedges.  The accepted formats are the same as
        matplotlib's scatter, with the addition of dict and IDStat.
        Those with colors:

        * single color as a string
        * single color as 3- or 4-tuple
        * list of colors of length len(ids)
        * dict of colors containing the `ids` as keys

        Those with numerical values (will be mapped to colors):

        * array of floats
        * dict of floats containing the `ids` as keys
        * IDStat containing the `ids` as keys

        If None (default), color by edge size.
    edge_fc_cmap: matplotlib colormap, optional
        Colormap used to map the edge colors. By default, "crest_r".
    edge_vmin, edge_vmax : float, optional
        Minimum and maximum for edge colormap scaling. By default, None.
    alpha : float, optional
        The edge transparency. By default, 0.4.
    layer_color : color or list of colors, optional
        Color of layers. By default, "grey".
    layer_cmap : colormap, optional
        Colormap to use in case of numerical values in layer_color. Ignored if layer_color
        does not contain numerical values to be mapped. By default, "crest_r", but ignored.
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
    conn_lines : bool, optional
        Whether to draw connections between layers. Default is True.
    conn_lines_style : str, optional
        The linestyle of the connections between layers. Default is 'dotted'.
    h_angle : float, optional
        The rotation angle around the horizontal axis in degrees. Default is 10.
    v_angle : float, optional
        The rotation angle around the vertical axis in degrees. Default is 0.
    sep : float, optional
        The separation between layers. Default is 0.4.
    **kwargs : optional args
        Alternate default values. Values that can be overwritten are the following:

        * "min_node_size" (default: 10)
        * "max_node_size" (default: 30)
        * "min_node_lw" (default: 2)
        * "max_node_lw" (default: 10)
        * "min_dyad_lw" (default: 1)
        * "max_dyad_lw" (default: 5)

    Returns
    -------
    ax : matplotlib Axes3DSubplot
        The subplot with the multilayer network visualization.
    collections : a tuple of 2 collections:

        * node_collection : matplotlib PathCollection
            Collection containing the nodes one the top layer
        * edge_collection : matplotlib PathCollection
            Collection containing the edges of size > 2
    """
    settings = {
        "min_node_size": 10,
        "max_node_size": 30,
        "min_dyad_lw": 2,
        "max_dyad_lw": 10,
        "min_node_lw": 1,
        "max_node_lw": 5,
    }

    settings.update(kwargs)

    if ax is None:
        _, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if pos is None:
        pos = barycenter_spring_layout(H)

    s = unique_edge_sizes(H)
    if max_order is None:
        max_order = max(s) - 1
    else:
        max_order = min(max_order, max(s) - 1)
    min_order = min(s) - 1

    orders = list(range(min_order, max_order + 1))

    xs, ys = zip(*pos.values())

    dyads = H.edges.filterby("order", 1)
    edges = H.edges.filterby("order", (2, max_order), "between")

    if edge_fc is None:  # color is proportional to size
        edge_fc = edges.size

    # convert pos to format convenient for scatter
    try:
        xy = np.asarray([pos[v] for v in H.nodes])
    except KeyError as err:
        raise XGIError(f"Node {err} has no position.") from err

    # convert all formats to ndarray
    node_size = _draw_arg_to_arr(node_size)
    node_fc = _draw_arg_to_arr(node_fc)
    node_lw = _draw_arg_to_arr(node_lw)
    dyad_lw = _draw_arg_to_arr(dyad_lw)
    layer_color = _draw_arg_to_arr(layer_color)

    # avoid matplotlib scatter UserWarning "Parameters 'cmap' will be ignored"
    if isinstance(node_fc, str) or (
        isinstance(node_fc, np.ndarray) and is_color_like(node_fc[0])
    ):
        node_fc_cmap = None

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
    if rescale_sizes and isinstance(dyad_lw, np.ndarray):
        dyad_lw = _interp_draw_arg(
            dyad_lw, settings["min_dyad_lw"], settings["max_dyad_lw"]
        )

    # check validity of input values
    if np.any(dyad_lw < 0):
        raise ValueError("dyad_lw cannot contain negative values.")

    # parse colors
    dyad_color, dyad_c_to_map = _parse_color_arg(dyad_color, list(dyads))
    edge_fc, edge_c_to_map = _parse_color_arg(edge_fc, list(edges))
    layer_color, layer_c_to_map = _parse_color_arg(layer_color, orders)

    node_size = np.array(node_size) ** 2

    # compute ax limits
    xdiff = np.max(xs) - np.min(xs)
    ydiff = np.max(ys) - np.min(ys)
    ymin = np.min(ys) - ydiff * 0.1
    ymax = np.max(ys) + ydiff * 0.1
    xmin = np.min(xs) - xdiff * 0.1  # * (width / height)
    xmax = np.max(xs) + xdiff * 0.1  # * (width / height)
    xx, yy = np.meshgrid([xmin, xmax], [ymin, ymax])

    # plot layers
    for jj, d in enumerate(orders):

        z = [sep * d] * H.num_nodes

        # draw surfaces corresponding to the different orders
        zz = np.zeros(xx.shape) + d * sep

        if layer_c_to_map:
            layer_c = None
        else:
            layer_c = layer_color[jj] if len(layer_color) > 1 else layer_color
            layer_cmap = None

        ax.plot_surface(
            xx,
            yy,
            zz,
            color=layer_c,
            cmap=layer_cmap,
            vmin=min_order * sep,
            vmax=max_order * sep,
            alpha=0.1,
            zorder=0,
        )

    # convert dyad pos to format convenient for scatter
    dyad_pos = [
        (np.append(pos[list(e)[0]], sep), np.append(pos[list(e)[1]], sep))
        for e in dyads.members()
    ]

    # plot dyads
    if dyad_c_to_map:
        raise ValueError(
            "dyad_color needs to be a color or list of colors, not numerical values."
        )

    dyad_collection = Line3DCollection(
        dyad_pos,
        colors=dyad_color,
        linewidths=dyad_lw,
        antialiaseds=(1,),
        linestyle=dyad_style,
        zorder=1,  # above layer
    )

    ax.add_collection3d(dyad_collection)

    # reorder to plot larger hyperedges first
    ids_sorted = np.argsort(edges.size.aslist())[::-1]

    # plot other hyperedges
    if edge_c_to_map:
        edge_fc_arr = edge_fc[ids_sorted]
        edge_fc_colors = None
    else:
        edge_fc_arr = None
        edge_fc_colors = edge_fc[ids_sorted] if len(edge_fc) > 1 else edge_fc

    patches = []
    zs = []
    for he in np.array(edges.members())[ids_sorted]:
        d = len(he) - 1
        zs.append(d * sep)
        he = list(he)
        coordinates = [[pos[n][0], pos[n][1], d * sep] for n in he]
        # Sorting the points counterclockwise (needed to have the correct filling)
        sorted_coordinates = _CCW_sort(coordinates)
        patches.append(sorted_coordinates)

    edge_collection = Poly3DCollection(
        patches,
        facecolors=edge_fc_colors,
        array=edge_fc_arr,
        cmap=edge_fc_cmap,
        alpha=alpha,
        zorder=max_order - 2,  # below dyads
    )
    edge_collection.set_cmap(edge_fc_cmap)
    if edge_c_to_map:
        edge_collection.set_clim(edge_vmin, edge_vmax)
    ax.add_collection3d(edge_collection)

    # draw inter-layer links between nodes
    if conn_lines:
        lines3d_between = [
            (list(pos[i]) + [min_order * sep], list(pos[i]) + [max_order * sep])
            for i in H.nodes
        ]
        between_lines = Line3DCollection(
            lines3d_between,
            zorder=5,
            color=".5",
            alpha=0.4,
            linestyle=conn_lines_style,
            linewidth=1,
        )
        ax.add_collection3d(between_lines)

    # draw nodes (last)
    for d in orders:

        z = [sep * d] * H.num_nodes

        node_collection = ax.scatter(
            xs=xy[:, 0],
            ys=xy[:, 1],
            zs=z,
            s=node_size,
            marker=node_shape,
            c=node_fc,
            cmap=node_fc_cmap,
            vmin=vmin,
            vmax=vmax,
            edgecolors=node_ec,
            linewidths=node_lw,
            zorder=max_order + 1,
            plotnonfinite=True,  # plot points with nonfinite color
            alpha=1,
        )

    ax.view_init(h_angle, v_angle)
    ax.set_ylim(np.min(ys) - ydiff * 0.1, np.max(ys) + ydiff * 0.1)
    ax.set_xlim(np.min(xs) - xdiff * 0.1, np.max(xs) + xdiff * 0.1)
    ax.set_axis_off()
    ax.set_aspect("equal")

    return ax, (node_collection, edge_collection)


def draw_bipartite(
    H,
    pos=None,
    ax=None,
    node_fc="white",
    node_ec="black",
    node_lw=1,
    node_size=7,
    node_shape="o",
    node_fc_cmap="Reds",
    edge_marker_fc=None,
    edge_marker_ec="black",
    edge_marker_lw=1,
    edge_marker_size=7,
    edge_marker_shape="s",
    edge_marker_fc_cmap="crest_r",
    max_order=None,
    dyad_color=None,
    dyad_lw=1,
    dyad_style="solid",
    dyad_color_cmap="crest_r",
    node_labels=None,
    hyperedge_labels=None,
    arrowsize=10,
    arrowstyle="->",
    connectionstyle="arc3",
    rescale_sizes=True,
    aspect="equal",
    **kwargs,
):
    """Draw a hypergraph as a bipartite network.

    Parameters
    ----------
    H : Hypergraph or DiHypergraph
        The hypergraph to draw.
    pos : tuple of two dicts, optional
        The tuple should contain a (1) dictionary of positions node_id:(x,y) for
        placing node markers, and (2) a dictionary of positions edge_id:(x,y) for
        placing the edge markers.  If None (default), use the `bipartite_spring_layout`
        to compute the positions.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
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
        min_node_size and max_node_size. By default, 7.
    node_shape : str, optional
        Marker used for the nodes. By default 'o' (circle marker).
    node_fc_cmap : colormap
        Colormap for mapping node colors. By default, "Reds". Ignored, if `node_fc` is
        a str (single color).
    edge_marker_fc: str, dict, iterable, optional
        Filling color of the hyperedges (markers). If str, use the same color for all hyperedges.
        If a dict, must contain (hyperedge_id: color_str) pairs. If other iterable,
        assume the colors are specified in the same order as the hyperedges are found
        in H.edges. If None, colors markers by edge size. By default, None.
    edge_marker_ec: str, dict, iterable, optional
        Edge color of the hyperedges (markers). If str, use the same color for all hyperedges.
        If a dict, must contain (hyperedge_id: color_str) pairs. If other iterable,
        assume the colors are specified in the same order as the hyperedges are found
        in H.edges. By default, "black".
    edge_marker_lw : int, float, dict, iterable, or EdgeStat, optional
        Line width of the edge marker borders in pixels.  If int or float, use the same width
        for all edge marker borders.  If a dict, must contain (edge_id: width) pairs.  If
        iterable, assume the widths are specified in the same order as the nodes are
        found in H.edges. If EdgeStat, use a monotonic linear interpolation defined
        between min_edge_marker_lw and max_edge_marker_lw. By default, 1.
    edge_marker_size : int, float, dict, iterable, or EdgeStat, optional
        Radius of the edge markers in pixels.  If int or float, use the same radius for all
        edge markers.  If a dict, must contain (edge_id: radius) pairs.  If iterable, assume
        the radii are specified in the same order as the edges are found in
        H.edges. If EdgeStat, use a monotonic linear interpolation defined between
        min_edge_marker_size and max_edge_marker_size. By default, 7.
    edge_marker_shape: str, optional
        Marker used for the hyperedges. By default 's' (square marker). If "", no marker is
        displayed.
    edge_marker_fc_cmap : colormap
        Colormap for mapping edge marker colors. By default, "Blues".
        Ignored, if `edge_marker_fc` is a str (single color) or an iterable of colors.
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
    dyad_color : str, dict, iterable, optional
        Color of the bipartite edges. If str, use the same color for all edges.
        If a dict, must contain (hyperedge_id: color_str) pairs. If other iterable,
        assume the colors are specified in the same order as the hyperedges are found
        in H.edges. By default, "black".
    dyad_lw : int, float, dict, iterable, optional
        Line width of the bipartite edges. If int or float, use the same width for
        all hyperedges. If a dict, must contain (hyperedge_id: width) pairs. If other
        iterable, assume the widths are specified in the same order as the hyperedges
        are found in H.edges. By default, 1.
    dyad_style : str or list of strings, optional
        Line style of the dyads, e.g. ‘-’, ‘–’, ‘-.’, ‘:’ or words like ‘solid’ or ‘dashed’.
        See matplotlib's documentation for all accepted values. By default, "solid".
    dyad_color_cmap : colormap
        Colormap for mapping bipartite edge colors. By default, "Greys".
        Ignored, if `dyad_color` is a str (single color) or an iterable of colors.
    node_labels : bool or dict, optional
        If True, draw ids on the nodes. If a dict, must contain (node_id: label) pairs.
        By default, False.
    hyperedge_labels : bool or dict, optional
        If True, draw ids on the hyperedges. If a dict, must contain (edge_id: label)
        pairs.  By default, False.
    arrowsize : int (default=10)
        Size of the arrow head's length and width. See `matplotlib.patches.FancyArrowPatch`
        for attribute `mutation_scale` for more info. Only used if the higher-order network
        is a `DiHypergraph`.
    arrowstyle : str, optional
        By default: '->'. See `matplotlib.patches.ArrowStyle` for more options.
        Only used if the higher-order network is a `DiHypergraph`.
    connectionstyle : string (default="arc3")
        Pass the connectionstyle parameter to create curved arc of rounding
        radius rad. For example, connectionstyle='arc3,rad=0.2'.
        See `matplotlib.patches.ConnectionStyle` and
        `matplotlib.patches.FancyArrowPatch` for more info.
        Only used if the higher-order network is a `DiHypergraph`.
    rescale_sizes: bool, optional
        If True, linearly interpolate `node_size` and between min/max values
        that can be changed in the other argument `params`.
        If `node_size` is a single value, this is ignored. By default, True.
    aspect : {"auto", "equal"} or float, optional
        Set the aspect ratio of the axes scaling, i.e. y/x-scale. `aspect` is passed
        directly to matplotlib's `ax.set_aspect()`. Default is `equal`. See full
        description at
        https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_aspect.html
    **kwargs : optional args
        Alternate default values. Values that can be overwritten are the following:

        * min_node_size (default: 5)
        * max_node_size (default: 30)
        * min_node_lw (default: 0)
        * max_node_lw (default: 5)
        * min_edge_marker_size (default: 5)
        * max_edge_marker_size (default: 30)
        * min_edge_marker_lw (default: 0)
        * max_edge_marker_lw (default: 5)
        * min_dyad_lw (default: 1)
        * max_dyad_lw (default: 10)
        * min_source_margin (default: 0)
        * min_target_margin (default: 0)


    Returns
    -------
    ax : matplotlib.pyplot.axes
        The axes corresponding the visualization
    collections : a tuple of 3 collections

        * node_collection : matplotlib PathCollection
            Collection containing the nodes
        * edge_marker_collection : matplotlib PathCollection
            Collection containing the edge markers
        * dyad_collection : matplotlib LineCollection if undirected, list of FancyArrowPatches if not
            Collection containing the edges

    Raises
    ------
    XGIError
        If the network is not a Hypergraph, SimplicialComplex or a DiHypergraph.

    See Also
    --------
    draw
    draw_multilayer
    """

    is_directed = False
    if isinstance(H, DiHypergraph):
        from ..convert import to_hypergraph

        DH = H.copy()
        H = to_hypergraph(DH)
        is_directed = True

    if not isinstance(H, Hypergraph):
        raise XGIError("The input must be a Hypergraph")

    settings = {
        "min_node_lw": 0,
        "max_node_lw": 5,
        "min_node_size": 5,
        "max_node_size": 30,
        "min_edge_marker_lw": 0,
        "max_edge_marker_lw": 5,
        "min_edge_marker_size": 0,
        "max_edge_marker_size": 5,
        "min_dyad_lw": 1,
        "max_dyad_lw": 10,
        "min_source_margin": 0,
        "min_target_margin": 0,
    }

    settings.update(kwargs)

    node_settings = {
        "min_node_lw": settings["min_node_lw"],
        "max_node_lw": settings["max_node_lw"],
        "min_node_size": settings["min_node_size"],
        "max_node_size": settings["max_node_size"],
    }

    edge_marker_settings = {
        "min_node_lw": settings["min_edge_marker_lw"],
        "max_node_lw": settings["max_edge_marker_lw"],
        "min_node_size": settings["min_edge_marker_size"],
        "max_node_size": settings["max_edge_marker_size"],
    }

    if not pos:
        pos = bipartite_spring_layout(H)
    elif not (isinstance(pos[0], dict) and isinstance(pos[1], dict)):
        raise XGIError("Position must be a 2-tuple of dictionaries!")

    node_pos, edge_pos = pos

    if ax is None:
        ax = plt.gca()

    if not max_order:
        max_order = max_edge_order(H)

    D = H.dual()
    if edge_marker_fc is None:
        edge_marker_fc = D.nodes.degree

    ax, node_collection = draw_nodes(
        H=H,
        pos=node_pos,
        ax=ax,
        node_fc=node_fc,
        node_ec=node_ec,
        node_lw=node_lw,
        node_size=node_size,
        node_shape=node_shape,
        node_fc_cmap=node_fc_cmap,
        zorder=2,
        params=node_settings,
        node_labels=node_labels,
        rescale_sizes=rescale_sizes,
        **kwargs,
    )

    ax, edge_marker_collection = draw_nodes(
        H=D,
        pos=edge_pos,
        ax=ax,
        node_fc=edge_marker_fc,
        node_ec=edge_marker_ec,
        node_lw=edge_marker_lw,
        node_size=edge_marker_size,
        node_shape=edge_marker_shape,
        node_fc_cmap=edge_marker_fc_cmap,
        zorder=1,
        params=edge_marker_settings,
        node_labels=hyperedge_labels,
        rescale_sizes=rescale_sizes,
        **kwargs,
    )

    if is_directed:
        ax = draw_directed_dyads(
            DH,
            pos=pos,
            ax=ax,
            max_order=max_order,
            dyad_color=dyad_color,
            dyad_lw=dyad_lw,
            dyad_style=dyad_style,
            dyad_color_cmap=dyad_color_cmap,
            rescale_sizes=rescale_sizes,
            arrowsize=arrowsize,
            arrowstyle=arrowstyle,
            connectionstyle=connectionstyle,
            node_size=node_size,
            node_shape=node_shape,
            edge_marker_size=edge_marker_size,
            edge_marker_shape=edge_marker_shape,
            **kwargs,
        )
    else:
        ax, dyad_collection = draw_undirected_dyads(
            H,
            pos=pos,
            ax=ax,
            max_order=max_order,
            dyad_color=dyad_color,
            dyad_lw=dyad_lw,
            dyad_style=dyad_style,
            dyad_color_cmap=dyad_color_cmap,
            rescale_sizes=rescale_sizes,
            **kwargs,
        )

    pos = {}
    for i, n in enumerate(node_pos):
        pos[i] = node_pos[n]
    n = H.num_nodes
    for i, e in enumerate(edge_pos):
        pos[i + n] = edge_pos[e]

    # compute axis limits
    _update_lims(pos, ax)

    ax.set_aspect(aspect, "datalim")

    if is_directed:
        return ax, (node_collection, edge_marker_collection)
    else:
        return ax, (node_collection, edge_marker_collection, dyad_collection)


def draw_undirected_dyads(
    H,
    pos=None,
    ax=None,
    max_order=None,
    dyad_color=None,
    dyad_lw=1,
    dyad_style="solid",
    dyad_color_cmap="crest_r",
    rescale_sizes=True,
    **kwargs,
):
    """Draw the bipartite edges of an undirected hypergraph.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph to draw.
    pos : tuple of two dicts, optional
        The tuple should contains a (1) dictionary of positions node_id:(x,y) for
        placing node markers, and (2) a dictionary of positions edge_id:(x,y) for
        placing the edge markers.  If None (default), use the `bipartite_spring_layout`
        to compute the positions.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
    dyad_color : str, dict, iterable, optional
        Color of the bipartite edges. If str, use the same color for all edges.
        If a dict, must contain (hyperedge_id: color_str) pairs. If other iterable,
        assume the colors are specified in the same order as the hyperedges are found
        in H.edges. By default, "black".
    dyad_lw : int, float, dict, iterable, optional
        Line width of the bipartite edges. If int or float, use the same width for
        all hyperedges. If a dict, must contain (hyperedge_id: width) pairs. If other
        iterable, assume the widths are specified in the same order as the hyperedges
        are found in H.edges. By default, 1.
    dyad_style : str or list of strings, optional
        Line style of the dyads, e.g. ‘-’, ‘–’, ‘-.’, ‘:’ or words like ‘solid’ or ‘dashed’.
        See matplotlib's documentation for all accepted values. By default, "solid".
    dyad_color_cmap : colormap
        Colormap for mapping bipartite edge colors. By default, "Greys".
        Ignored, if `dyad_color` is a str (single color) or an iterable of colors.
    rescale_sizes: bool, optional
        If True, linearly interpolate `node_size` and between min/max values
        that can be changed in the other argument `params`.
        If `node_size` is a single value, this is ignored. By default, True.
    **kwargs : optional args
        Alternate default values. Values that can be overwritten are the following:

        * min_dyad_lw (default: 1)
        * max_dyad_lw (default: 10)

    Returns
    -------
    ax : matplotlib.pyplot.axes
        The axes corresponding the visualization
    * dyad_collection : matplotlib LineCollection
        of bipartite edges

    Raises
    ------
    XGIError
        If DiHypergraph is passed.

    See Also
    --------
    draw_bipartite
    draw_directed_dyads

    """
    settings = {
        "min_dyad_lw": 1,
        "max_dyad_lw": 10,
    }
    settings.update(kwargs)

    if not isinstance(H, Hypergraph):
        raise XGIError("The input must be a Hypergraph")

    if not pos:
        pos = bipartite_spring_layout(H)

    if ax is None:
        ax = plt.gca()

    if dyad_color is None:  # color is proportional to size
        dyad_color = H.edges.size

    if not max_order:
        edge_ids = list(H.edges)
        max_order = max_edge_order(H)
    else:
        edge_ids = list(H.edges.filterby("order", max_order, "leq"))

    node_pos, edge_pos = pos

    dyads = to_bipartite_edgelist(H)
    dyad_pos = np.asarray(
        [(node_pos[e[0]], edge_pos[e[1]]) for e in dyads if e[1] in edge_ids]
    )

    dyad_lw = _draw_arg_to_arr(dyad_lw)

    if rescale_sizes and isinstance(dyad_lw, np.ndarray):
        dyad_lw = _interp_draw_arg(
            dyad_lw, settings["min_dyad_lw"], settings["max_dyad_lw"]
        )

    # parse colors
    dyad_color, dyads_c_to_map = _parse_color_arg(dyad_color, H.edges)

    # The following two list comprehensions map colors assigned to a hyperedge to
    # all of the bipartite edges, so that users need not specify colors for every
    # node-edge incidence.
    if isinstance(dyad_lw, np.ndarray):
        dyad_lw = np.array(
            list(
                chaini([lw] * int(s) for s, lw in zip(H.edges.size.aslist(), dyad_lw)),
                dtype=float,
            )
        )

    if isinstance(dyad_color, np.ndarray):
        dyad_color = np.array(
            list(
                chaini(
                    [dc] * int(s) for s, dc in zip(H.edges.size.aslist(), dyad_color)
                ),
            )
        )

    # convert numbers to colors for FancyArrowPatch
    if dyads_c_to_map:
        norm = mpl.colors.Normalize()
        m = cm.ScalarMappable(norm=norm, cmap=dyad_color_cmap)
        dyad_color = m.to_rgba(dyad_color)

    # check validity of input values
    if np.any(dyad_lw < 0):
        raise ValueError("dyad_lw cannot contain negative values.")

    # interpolate if needed
    if rescale_sizes and isinstance(dyad_lw, np.ndarray):
        dyad_lw = _interp_draw_arg(
            dyad_lw, settings["min_dyad_lw"], settings["max_dyad_lw"]
        )

    dyad_collection = LineCollection(
        dyad_pos,
        colors=dyad_color,
        linewidths=dyad_lw,
        antialiaseds=(1,),
        linestyle=dyad_style,
        cmap=dyad_color_cmap,
        zorder=0,
    )

    ax.add_collection(dyad_collection)
    return ax, dyad_collection


def draw_directed_dyads(
    H,
    pos=None,
    ax=None,
    max_order=None,
    dyad_color=None,
    dyad_lw=1,
    dyad_style="solid",
    dyad_color_cmap="crest_r",
    arrowsize=10,
    arrowstyle="->",
    connectionstyle="arc3",
    node_size=5,
    node_shape="o",
    edge_marker_size=5,
    edge_marker_shape="s",
    rescale_sizes=True,
    **kwargs,
):
    """Draw the bipartite edges of a directed hypergraph.

    Parameters
    ----------
    H : DiHypergraph
        The hypergraph to draw.
    pos : tuple of two dicts, optional
        The tuple should contains a (1) dictionary of positions node_id:(x,y) for
        placing node markers, and (2) a dictionary of positions edge_id:(x,y) for
        placing the edge markers.  If None (default), use the `bipartite_spring_layout`
        to compute the positions.
    ax : matplotlib.pyplot.axes, optional
        Axis to draw on. If None (default), get the current axes.
    max_order : int, optional
        Maximum of hyperedges to plot. If None (default), plots all orders.
    dyad_color : str, dict, iterable, optional
        Color of the bipartite edges. If str, use the same color for all edges.
        If a dict, must contain (hyperedge_id: color_str) pairs. If other iterable,
        assume the colors are specified in the same order as the hyperedges are found
        in H.edges. By default, "black".
    dyad_lw : int, float, dict, iterable, optional
        Line width of the bipartite edges. If int or float, use the same width for
        all hyperedges. If a dict, must contain (hyperedge_id: width) pairs. If other
        iterable, assume the widths are specified in the same order as the hyperedges
        are found in H.edges. By default, 1.
    dyad_style : str or list of strings, optional
        Line style of the dyads, e.g. ‘-’, ‘–’, ‘-.’, ‘:’ or words like ‘solid’ or ‘dashed’.
        See matplotlib's documentation for all accepted values. By default, "solid".
    dyad_color_cmap : colormap
        Colormap for mapping bipartite edge colors. By default, "Greys".
        Ignored, if `dyad_color` is a str (single color) or an iterable of colors.
    arrowsize : int (default=10)
        Size of the arrow head's length and width. See `matplotlib.patches.FancyArrowPatch`
        for attribute `mutation_scale` for more info. Only used if the higher-order network
        is a `DiHypergraph`.
    arrowstyle : str, optional
        By default: '->'. See `matplotlib.patches.ArrowStyle` for more options.
        Only used if the higher-order network is a `DiHypergraph`.
    connectionstyle : string (default="arc3")
        Pass the connectionstyle parameter to create curved arc of rounding
        radius rad. For example, connectionstyle='arc3,rad=0.2'.
        See `matplotlib.patches.ConnectionStyle` and
        `matplotlib.patches.FancyArrowPatch` for more info.
        Only used if the higher-order network is a `DiHypergraph`.
    rescale_sizes: bool, optional
        If True, linearly interpolate `node_size` and between min/max values
        that can be changed in the other argument `params`.
        If `node_size` is a single value, this is ignored. By default, True.
    node_size : int, float, dict, iterable, or NodeStat, optional
        Radius of the nodes in pixels.  If int or float, use the same radius for all
        nodes.  If a dict, must contain (node_id: radius) pairs.  If iterable, assume
        the radiuses are specified in the same order as the nodes are found in
        H.nodes. If NodeStat, use a monotonic linear interpolation defined between
        min_node_size and max_node_size. Used for arrow spacing. By default, 7.
    node_shape : str, optional
        Marker used for the nodes. Used for arrow spacing. By default 'o' (circle marker).
    edge_marker_size : int, float, dict, iterable, or EdgeStat, optional
        Radius of the edge markers in pixels.  If int or float, use the same radius for all
        edge markers.  If a dict, must contain (edge_id: radius) pairs.  If iterable, assume
        the radii are specified in the same order as the edges are found in
        H.edges. If EdgeStat, use a monotonic linear interpolation defined between
        min_edge_marker_size and max_edge_marker_size. Used for arrow spacing. By default, 7.
    edge_marker_shape: str, optional
        Marker used for the hyperedges. If "", no marker is
        displayed. Used for arrow spacing. By default 's' (square marker).
    **kwargs : optional args
        Alternate default values. Values that can be overwritten are the following:

        * min_dyad_lw (default: 1)
        * max_dyad_lw (default: 10)

    Returns
    -------
    ax : matplotlib.pyplot.axes
        The axes corresponding the visualization
    dyad_collection : list of FancyArrowPatches
        representing directed bipartite edges

    Raises
    ------
    XGIError
        If something different than a DiHypergraph is passed.

    See Also
    --------
    draw_bipartite
    draw_directed_dyads

    """
    settings = {
        "min_dyad_lw": 1,
        "max_dyad_lw": 10,
        "min_source_margin": 0,
        "min_target_margin": 0,
    }
    settings.update(kwargs)

    if not isinstance(H, DiHypergraph):
        raise XGIError("Input must be a DiHypergraph")

    if not pos:
        from ..convert import to_hypergraph

        pos = bipartite_spring_layout(to_hypergraph(H))

    if ax is None:
        ax = plt.gca()

    if dyad_color is None:  # color is proportional to size
        dyad_color = H.edges.size

    if not max_order:
        edge_ids = list(H.edges)
        max_order = H.edges.order.max()
    else:
        edge_ids = list(H.edges.filterby("order", max_order, "leq"))

    dyad_lw = _draw_arg_to_arr(dyad_lw)
    node_size = _draw_arg_to_arr(node_size)
    edge_marker_size = _draw_arg_to_arr(edge_marker_size)

    if rescale_sizes and isinstance(dyad_lw, np.ndarray):
        dyad_lw = _interp_draw_arg(
            dyad_lw, settings["min_dyad_lw"], settings["max_dyad_lw"]
        )

    # parse colors
    dyad_color, dyads_c_to_map = _parse_color_arg(dyad_color, H.edges)

    # convert numbers to colors for FancyArrowPatch
    if dyads_c_to_map:
        norm = mpl.colors.Normalize()
        m = cm.ScalarMappable(norm=norm, cmap=dyad_color_cmap)
        dyad_color = m.to_rgba(dyad_color)

    # check validity of input values
    if np.any(dyad_lw < 0):
        raise ValueError("dyad_lw cannot contain negative values.")

    # interpolate if needed
    if rescale_sizes and isinstance(dyad_lw, np.ndarray):
        dyad_lw = _interp_draw_arg(
            dyad_lw, settings["min_dyad_lw"], settings["max_dyad_lw"]
        )

    node_pos, edge_pos = pos

    """Helper functions"""

    def _arrow_shrink(
        source="node", target="edge", node_size=None, edge_marker_size=None
    ):
        """Compute the shrink factor for the arrows based on node sizes."""

        def to_marker_edge(marker_size, marker):
            # from networkx
            # https://networkx.org/documentation/stable/_modules/networkx/drawing/nx_pylab.html#draw_networkx_edges
            if marker in "s^>v<d":  # `large` markers need extra space
                return marker_size / 1.6
            else:
                return marker_size / 2

        shrink_source = to_marker_edge(
            node_size, node_shape
        )  # space from source to tail
        shrink_target = to_marker_edge(
            edge_marker_size, edge_marker_shape
        )  # space from  head to target

        if shrink_source < settings["min_source_margin"]:
            shrink_source = settings["min_source_margin"]

        if shrink_target < settings["min_target_margin"]:
            shrink_target = settings["min_target_margin"]

        if source == "node" and target == "edge":
            return shrink_source, shrink_target
        elif source == "edge" and target == "node":
            return shrink_target, shrink_source
        else:
            raise ValueError("Wrong input arguments.")

    # We are using single patches rather than a PatchCollection of arrows
    # because Matplotlib has an old bug: FancyArrowPatch has incompatibilities
    # with PatchCollection (https://github.com/matplotlib/matplotlib/issues/2341)
    # We are thus following the approach used by NetworkX
    # https://github.com/networkx/networkx/pull/2760
    edges = H.edges
    nodes = H.nodes
    edge_to_idx = dict(zip(edges, range(len(edges))))
    node_to_idx = dict(zip(nodes, range(len(nodes))))

    patches = []
    for e, (tail, head) in edges.dimembers(dtype=dict).items():
        if e in edge_ids:
            if isinstance(dyad_lw, np.ndarray):  # many node sizes
                dlw = dyad_lw[edge_to_idx[n]]
            else:
                dlw = dyad_lw

            if dyads_c_to_map:
                d_color = dyad_color[edge_to_idx[e]]
            else:
                d_color = dyad_color

            if isinstance(edge_marker_size, np.ndarray):  # many node sizes
                ems = edge_marker_size[edge_to_idx[e]]
            else:
                ems = edge_marker_size

            for n in tail:  # lines going towards the center

                xy_source = node_pos[n]
                xy_target = edge_pos[e]

                if isinstance(node_size, np.ndarray):  # many node sizes
                    ns = node_size[node_to_idx[n]]
                else:
                    ns = node_size

                shrink_source, shrink_target = _arrow_shrink(
                    source="node",
                    target="edge",
                    node_size=ns,
                    edge_marker_size=ems,
                )

                patch = FancyArrowPatch(
                    xy_source,
                    xy_target,
                    arrowstyle=arrowstyle,
                    shrinkA=shrink_source,
                    shrinkB=shrink_target,
                    mutation_scale=arrowsize,
                    linewidth=dlw,
                    linestyle=dyad_style,
                    zorder=0,
                    color=d_color,
                    connectionstyle=connectionstyle,
                )  # arrows go behind nodes

                patches.append(patch)
                ax.add_patch(patch)

            for n in head:  # lines going out from the center
                xy_source = edge_pos[e]
                xy_target = node_pos[n]

                if isinstance(node_size, np.ndarray):  # many node sizes
                    ns = node_size[node_to_idx[n]]
                else:
                    ns = node_size

                shrink_source, shrink_target = _arrow_shrink(
                    source="edge",
                    target="node",
                    node_size=ns,
                    edge_marker_size=ems,
                )

                patch = FancyArrowPatch(
                    xy_source,
                    xy_target,
                    arrowstyle=arrowstyle,
                    shrinkA=shrink_source,
                    shrinkB=shrink_target,
                    mutation_scale=arrowsize,
                    linewidth=dlw,
                    linestyle=dyad_style,
                    zorder=0,
                    color=d_color,
                    connectionstyle=connectionstyle,
                )  # arrows go behind nodes

                patches.append(patch)
                ax.add_patch(patch)
    return ax
