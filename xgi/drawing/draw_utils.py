"""Draw hypergraphs and simplicial complexes with matplotlib."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import is_color_like, to_rgba_array

from ..stats import EdgeStat, IDStat, NodeStat
from .layout import barycenter_spring_layout


def _draw_init(H, ax, pos):
    """Initializes the axis and node positions

    Parameters
    ----------
    H : Hypergraph
        The hypergraph to draw
    ax : Matplotlib axis
        The axis on which to plot
    pos : dict of lists
        The output of the layout functions.
        If None, uses the barycenter spring layout.

    Returns
    -------
    ax, pos
        ax: axis updated with the XGI format
        pos: dict of lists with the node positions
    """

    if pos is None:
        pos = barycenter_spring_layout(H)

    if ax is None:
        ax = plt.gca()

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis("off")

    return ax, pos


def _update_lims(pos, ax):
    """Update Axis limits based on node positions

    Parameters
    ----------
    pos : dict of lists
        The output of the layout functions.
    ax : Matplotlib axis
        The axis on which to plot

    Returns
    -------
    None

    """

    # compute axis limits
    pos_arr = np.asarray([[x, y] for _, (x, y) in pos.items()])

    maxx, maxy = np.max(pos_arr, axis=0)
    minx, miny = np.min(pos_arr, axis=0)
    w = maxx - minx
    h = maxy - miny

    # update view after drawing
    padx, pady = 0.05 * w, 0.05 * h
    corners = (minx - padx, miny - pady), (maxx + padx, maxy + pady)
    ax.update_datalim(corners)
    ax.autoscale_view()


def _parse_color_arg(colors, ids, id_kind="edges"):
    """
    Parse and process color arguments for plotting.

    This function is needed to handle the input formats not naturally
    handled by matploltib's Collections: IDStat, dict, and arrays of
    floats. All those numerical formats are converted to arrays of floats.

    Parameters:
    -----------
    colors : color or list of colors or array-like or dict or IDStat
        The color(s) to use. The accepted formats are the same as
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
    ids : array-like or None
        The IDs of the elements being plotted.
    id_kind : str, optional
        The kind of element IDs, "edges" (default) or "nodes".

    Returns:
    --------
    colors : single color or ndarray
        Processed color values for plotting.
    colors_to_map : bool
        True if the colors need to be mapped and need special handling. This
        is used in draw_hyperedges to deal with Collections.

    Raises:
    -------
    TypeError
        If color argument is inappropriate for the provided id_kind.
    ValueError
        If color argument has an invalid format or length.

    Notes:
    ------
    This function processes the color argument to ensure compatibility with
    PatchCollection's facecolor/array and checks for correct input format and length.
    """

    if id_kind == "edges" and isinstance(colors, NodeStat):
        raise TypeError("The color argument for edges cannot be a NodeStat")
    elif id_kind == "nodes" and isinstance(colors, EdgeStat):
        raise TypeError("The color argument for nodes cannot be an EdgeStat")

    xsize = len(ids)

    # convert all dict-like input formats to an array
    if isinstance(colors, IDStat):
        colors = colors.asdict()
    if isinstance(colors, dict):
        if ids is not None:  # filter if needed
            colors = {key: val for key, val in colors.items() if key in ids}
        values = list(colors.values())
        colors = np.array(values)

    # see if input format needs to be mapped to colors (if numeric)
    try:  # see if the input format is compatible with PatchCollection's facecolor
        colors = to_rgba_array(colors)
        colors_to_map = False
    except:
        try:  # in case of array of floats (can be fed to PatchCollection with some care)
            colors = np.asanyarray(colors, dtype=float)
            colors_to_map = True
        except:
            raise ValueError("Invalid input format for colors.")

    if not is_color_like(colors) and len(colors) != xsize:
        raise ValueError(
            f"The input color argument must be a single color or its length must match the number of plotted elements ({xsize})."
        )

    return colors, colors_to_map


def _draw_arg_to_arr(arg):
    """Convert drawing arguments to a matplotlib-compliant format.

    IDStat, dict, and list are converted to ndarray.
    Scalar values are untouched.

    Parameters
    ----------
    arg: int, float, dict, iterable, or NodeStat/EdgeStat
        Attributes for drawing parameter. Scalars are ignored.

    Returns
    -------
    arg : ndarray
        Drawing argument in matplotlib-compliant form (scalar or array)
    """
    if isinstance(arg, IDStat):
        arg = arg.asnumpy()
    elif isinstance(arg, dict):
        values = list(arg.values())
        arg = np.array(values)
    elif isinstance(arg, list):
        arg = np.array(arg)

    return arg


def _interp_draw_arg(arg, min_val, max_val):
    """Linearly interpolate drawing arguments between min/max values

    Parameters
    ----------
    arg: arr-like
        Attributes for drawing parameter.

    Returns
    -------
    vals : ndarray
        Drawing argument interpolated
    """

    vals = np.interp(arg, [min(arg), max(arg)], [min_val, max_val])

    return vals


def _CCW_sort(p):
    """
    Sort the input 2D points counterclockwise.
    """
    p = np.array(p)
    mean = np.mean(p, axis=0)
    d = p - mean
    s = np.arctan2(d[:, 0], d[:, 1])
    return p[np.argsort(s), :]
