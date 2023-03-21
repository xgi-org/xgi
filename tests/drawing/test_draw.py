import numpy as np
import pytest
from matplotlib import cm

import xgi
from xgi.drawing.draw import _CCW_sort, _color_arg_to_dict, _scalar_arg_to_dict
from xgi.exception import XGIError


def test_draw():
    assert 0 == 0


def test_draw_nodes():
    assert 0 == 0


def test_draw_hyperedges():
    assert 0 == 0


def test_draw_simplices():
    assert 0 == 0


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


def test_color_arg_to_dict(edgelist4):
    ids = [1, 2, 3]

    arg = "black"
    d = _color_arg_to_dict(arg, ids, None)
    assert d == {1: "black", 2: "black", 3: "black"}

    with pytest.raises(TypeError):
        arg = 0.3
        d = _color_arg_to_dict(arg, ids, None)

    with pytest.raises(TypeError):
        arg = 1
        d = _color_arg_to_dict(arg, ids, None)

    arg = ["black", "blue", "red"]
    d = _color_arg_to_dict(arg, ids, None)
    assert d == {1: "black", 2: "blue", 3: "red"}

    arg = np.array(["black", "blue", "red"])
    d = _color_arg_to_dict(arg, ids, None)
    assert d == {1: "black", 2: "blue", 3: "red"}

    H = xgi.Hypergraph(edgelist4)
    arg = H.nodes.degree
    d = _color_arg_to_dict(arg, ids, cm.Reds)
    assert np.allclose(d[1], np.array([[0.99692426, 0.89619377, 0.84890427, 1.0]]))
    assert np.allclose(d[2], np.array([[0.98357555, 0.41279508, 0.28835063, 1.0]]))
    assert np.allclose(d[3], np.array([[0.59461745, 0.0461361, 0.07558631, 1.0]]))


def test_draw_node_labels():
    assert 0 == 0


def test_draw_hyperedge_labels():
    assert 0 == 0
