import numpy as np

import xgi
from xgi.drawing.draw import _CCW_sort, _draw_arg_to_arr, _interp_draw_arg


def test_CCW_sort():
    coords = [[0.919, 0.145], [0.037, 0.537], [0.402, 0.56]]
    sorted_coords = _CCW_sort(coords)
    assert np.all(
        sorted_coords == np.array([[0.037, 0.537], [0.402, 0.56], [0.919, 0.145]])
    )

    coords = [[0.037, 0.537], [0.402, 0.56], [0.791, 0.91], [0.0, 0.868]]
    sorted_coords = _CCW_sort(coords)
    assert np.all(
        sorted_coords
        == np.array([[0.037, 0.537], [0.0, 0.868], [0.791, 0.91], [0.402, 0.56]])
    )


def test_draw_arg_to_arr(edgelist4):

    H = xgi.Hypergraph(edgelist4)

    # arg stat
    arg = H.nodes.degree
    degree = _draw_arg_to_arr(arg)
    assert np.all(degree == np.array([1, 2, 3, 2, 2]))

    # arg dict
    arg_dict = {1: 1, 2: 2, 3: 3, 4: 2, 5: 2}
    degree = _draw_arg_to_arr(arg_dict)
    assert np.all(degree == np.array([1, 2, 3, 2, 2]))


def test_interp_draw_arg(edgelist4):

    arg = np.linspace(0, 10, num=10)
    out = _interp_draw_arg(arg, 1, 9)
    assert np.allclose(out, np.linspace(1, 9, num=10))

    arg = np.linspace(0, 10, num=10)
    out = _interp_draw_arg(arg, 0, 9)
    assert np.allclose(out, np.linspace(0, 9, num=10))

    arg = np.linspace(0, 10, num=10)
    out = _interp_draw_arg(arg, 1, 11)
    assert np.allclose(out, np.linspace(1, 11, num=10))
