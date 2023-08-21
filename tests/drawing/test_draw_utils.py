import numpy as np
import pytest
from matplotlib import cm

import xgi
from xgi.drawing.draw import (
    _CCW_sort,
    _color_arg_to_dict,
    _interp_draw_arg,
    _scalar_arg_to_dict,
    _draw_arg_to_arr,
)


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


def test_scalar_arg_to_dict(edgelist4):
    ids = [1, 2, 3]
    min_val = 1
    max_val = 5

    arg = 1
    d = _scalar_arg_to_dict(arg, ids, min_val, max_val)
    assert d == {1: 1, 2: 1, 3: 1}

    arg = 0.3
    d = _scalar_arg_to_dict(arg, ids, min_val, max_val)
    assert d == {1: 0.3, 2: 0.3, 3: 0.3}

    arg = [0.2, 3, 4]
    d = _scalar_arg_to_dict(arg, ids, min_val, max_val)
    assert d == {1: 0.2, 2: 3, 3: 4}

    arg = np.array([0.2, 3, 4])
    d = _scalar_arg_to_dict(arg, ids, min_val, max_val)
    assert d == {1: 0.2, 2: 3, 3: 4}

    arg = {1: 0.2, 2: 3, 3: 4}
    d = _scalar_arg_to_dict(arg, ids, min_val, max_val)
    assert d == {1: 0.2, 2: 3, 3: 4}

    H = xgi.Hypergraph(edgelist4)
    arg = H.nodes.degree
    d = _scalar_arg_to_dict(arg, ids, min_val, max_val)
    assert d == {1: 1.0, 2: 3.0, 3: 5.0}

    with pytest.raises(TypeError):
        arg = "2"
        d = _scalar_arg_to_dict(arg, ids, min_val, max_val)

    with pytest.raises(TypeError):
        arg = (1, 2, 3)
        d = _scalar_arg_to_dict(arg, ids, min_val, max_val)


def test_color_arg_to_dict(edgelist4):
    ids = [1, 2, 3]

    # single values
    arg1 = "black"
    arg2 = (0.1, 0.2, 0.3)
    arg3 = (0.1, 0.2, 0.3, 0.5)

    # test iterables of colors
    arg4 = [(0.1, 0.2, 0.3), (0.1, 0.2, 0.4), (0.1, 0.2, 0.5)]
    arg5 = ["blue", "black", "red"]
    arg6 = np.array(["blue", "black", "red"])
    arg7 = {0: (0.1, 0.2, 0.3), 1: (0.1, 0.2, 0.4), 2: (0.1, 0.2, 0.5)}
    arg8 = {0: "blue", 1: "black", 2: "red"}

    # test iterables of values
    arg9 = [0, 0.1, 0.2]
    arg10 = {1: 0, 2: 0.1, 3: 0.2}
    arg11 = np.array([0, 0.1, 0.2])

    # test single values
    d = _color_arg_to_dict(arg1, ids, None)
    assert d == {1: "black", 2: "black", 3: "black"}

    d = _color_arg_to_dict(arg2, ids, None)
    assert d == {1: (0.1, 0.2, 0.3), 2: (0.1, 0.2, 0.3), 3: (0.1, 0.2, 0.3)}

    d = _color_arg_to_dict(arg3, ids, None)
    for i in d:
        assert np.allclose(d[i], np.array([0.1, 0.2, 0.3, 0.5]))

    # Test iterables of colors
    d = _color_arg_to_dict(arg4, ids, None)
    assert d == {1: (0.1, 0.2, 0.3), 2: (0.1, 0.2, 0.4), 3: (0.1, 0.2, 0.5)}

    d = _color_arg_to_dict(arg5, ids, None)
    assert d == {1: "blue", 2: "black", 3: "red"}

    d = _color_arg_to_dict(arg6, ids, None)
    assert d == {1: "blue", 2: "black", 3: "red"}

    d = _color_arg_to_dict(arg7, ids, None)
    assert d == {1: (0.1, 0.2, 0.4), 2: (0.1, 0.2, 0.5)}

    d = _color_arg_to_dict(arg8, ids, None)
    assert d == {1: "black", 2: "red"}

    # Test iterables of values
    cdict = {
        1: np.array([[0.89173395, 0.93510188, 0.97539408, 1.0]]),
        2: np.array([[0.41708574, 0.68063053, 0.83823145, 1.0]]),
        3: np.array([[0.03137255, 0.28973472, 0.57031911, 1.0]]),
    }
    d = _color_arg_to_dict(arg9, ids, cm.Blues)
    for i in d:
        assert np.allclose(d[i], cdict[i])

    d = _color_arg_to_dict(arg10, ids, cm.Blues)
    for i in d:
        assert np.allclose(d[i], cdict[i])

    d = _color_arg_to_dict(arg11, ids, cm.Blues)
    for i in d:
        assert np.allclose(d[i], cdict[i])

    H = xgi.Hypergraph(edgelist4)
    arg = H.nodes.degree
    d = _color_arg_to_dict(arg, ids, cm.Reds)
    assert np.allclose(d[1], np.array([[0.99692426, 0.89619377, 0.84890427, 1.0]]))
    assert np.allclose(d[2], np.array([[0.98357555, 0.41279508, 0.28835063, 1.0]]))
    assert np.allclose(d[3], np.array([[0.59461745, 0.0461361, 0.07558631, 1.0]]))

    # Test bad calls
    with pytest.raises(TypeError):
        arg = 0.3
        d = _color_arg_to_dict(arg, ids, None)

    with pytest.raises(TypeError):
        arg = 1
        d = _color_arg_to_dict(arg, ids, None)
