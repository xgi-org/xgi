"""Draw hypergraphs and simplicial complexes with matplotlib."""

from collections.abc import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from numpy import ndarray

from ..exception import XGIError
from ..stats import IDStat
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
        Drawing argument in matplotlib-comliant form (scalar or array)
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


def _scalar_arg_to_dict(scalar_arg, ids, min_val, max_val):
    """Map different types of arguments for drawing style to a dict with scalar values.

    Parameters
    ----------
    scalar_arg : int, float, dict, iterable, or NodeStat/EdgeStat
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
        An ID: scalar dictionary.

    Raises
    ------
    TypeError
        If a int, float, list, dict, or NodeStat/EdgeStat is not passed.
    """
    if isinstance(scalar_arg, str):
        raise TypeError(
            "Argument must be int, float, dict, iterable, "
            f"or NodeStat/EdgeStat. Received {type(scalar_arg)}"
        )

    # Single argument
    if isinstance(scalar_arg, (int, float)):
        return {id: scalar_arg for id in ids}

    # IDStat
    if isinstance(scalar_arg, IDStat):
        vals = np.interp(
            scalar_arg.asnumpy(),
            [scalar_arg.min(), scalar_arg.max()],
            [min_val, max_val],
        )
        return dict(zip(ids, vals))

    # Iterables of floats or ints
    if isinstance(scalar_arg, Iterable):
        if isinstance(scalar_arg, dict):
            try:
                return {id: float(scalar_arg[id]) for id in scalar_arg if id in ids}
            except ValueError as e:
                raise TypeError(
                    "The input dict must have values that can be cast to floats."
                )

        elif isinstance(scalar_arg, (list, ndarray)):
            try:
                return {id: float(scalar_arg[idx]) for idx, id in enumerate(ids)}
            except ValueError as e:
                raise TypeError(
                    "The input list or array must have values that can be cast to floats."
                )
        else:
            raise TypeError(
                "Argument must be an dict, list, or numpy array of floats or ints."
            )

    raise TypeError(
        "Argument must be int, float, dict, iterable, "
        f"or NodeStat/EdgeStat. Received {type(scalar_arg)}"
    )


def _color_arg_to_dict(color_arg, ids, cmap):
    """Map different types of arguments for drawing style to a dict with color values.

    Parameters
    ----------
    color_arg : Several formats are accepted:

        Single color values

        * str
        * 3- or 4-tuple

        Iterable of colors (each color specified as above)

        * numpy array
        * list
        * dict {id: color} pairs

        Iterable of numerical values (floats or ints)

        * list
        * dict
        * numpy array

        Stats

        * NodeStat
        * EdgeStat

        Attributes for drawing parameter.
    ids : NodeView or EdgeView
        This is the node or edge IDs that attributes get mapped to.
    cmap : ListedColormap or LinearSegmentedColormap
        colormap to use for NodeStat/EdgeStat.

    Returns
    -------
    dict
        An ID: color dictionary.

    Raises
    ------
    TypeError
        If a string, dict, iterable, or NodeStat/EdgeStat is not passed.

    Notes
    -----
    For the iterable of values, we do not accept tuples,
    because there is the potential for ambiguity.
    """

    # single argument. Must be a string or a tuple of floats
    if isinstance(color_arg, str) or (
        isinstance(color_arg, tuple) and isinstance(color_arg[0], float)
    ):
        return {id: color_arg for id in ids}

    # Iterables of colors. The values of these iterables must strings or tuples. As of now,
    # there is not a check to verify that the tuples contain floats.
    if isinstance(color_arg, Iterable):
        if isinstance(color_arg, dict) and isinstance(
            next(iter(color_arg.values())), (str, tuple, ndarray)
        ):
            return {id: color_arg[id] for id in color_arg if id in ids}
        if isinstance(color_arg, (list, ndarray)) and isinstance(
            color_arg[0], (str, tuple, ndarray)
        ):
            return {id: color_arg[idx] for idx, id in enumerate(ids)}

    # Stats or iterable of values
    if isinstance(color_arg, (Iterable, IDStat)):
        # set max and min of interpolation based on color map
        if isinstance(cmap, ListedColormap):
            minval = 0
            maxval = cmap.N
        elif isinstance(cmap, LinearSegmentedColormap):
            minval = 0.1
            maxval = 0.9
        else:
            raise XGIError("Invalid colormap!")

        # handle the case of IDStat vs iterables
        if isinstance(color_arg, IDStat):
            vals = np.interp(
                color_arg.asnumpy(),
                [color_arg.min(), color_arg.max()],
                [minval, maxval],
            )
            return {
                id: np.array(cmap(vals[i])).reshape(1, -1) for i, id in enumerate(ids)
            }

        elif isinstance(color_arg, Iterable):
            if isinstance(color_arg, dict) and isinstance(
                next(iter(color_arg.values())), (int, float)
            ):
                v = list(color_arg.values())
                vals = np.interp(v, [np.min(v), np.max(v)], [minval, maxval])
                # because we have ids, we can't just assume that the keys of arg correspond to
                # the ids.
                return {
                    id: np.array(cmap(v)).reshape(1, -1)
                    for v, id in zip(vals, color_arg.keys())
                    if id in ids
                }

            if isinstance(color_arg, (list, ndarray)) and isinstance(
                color_arg[0], (int, float)
            ):
                vals = np.interp(
                    color_arg, [np.min(color_arg), np.max(color_arg)], [minval, maxval]
                )
                return {
                    id: np.array(cmap(vals[i])).reshape(1, -1)
                    for i, id in enumerate(ids)
                }
            else:
                raise TypeError(
                    "Argument must be an dict, list, or numpy array of floats."
                )

    raise TypeError(
        "Argument must be str, dict, iterable, or "
        f"NodeStat/EdgeStat. Received {type(color_arg)}"
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
