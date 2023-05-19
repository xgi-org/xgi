import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib import cm

import xgi
from xgi.drawing.draw import _CCW_sort, _color_arg_to_dict, _scalar_arg_to_dict
from xgi.exception import XGIError


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


def test_draw(edgelist8):
    H = xgi.Hypergraph(edgelist8)

    ax = xgi.draw(H)

    # number of elements
    assert len(ax.lines) == len(H.edges.filterby("size", 2))  # dyads
    assert len(ax.patches) == len(H.edges.filterby("size", 2, mode="gt"))  # hyperedges
    assert len(ax.collections[0].get_sizes()) == H.num_nodes  # nodes

    # zorder
    for line in ax.lines:  # dyads
        assert line.get_zorder() == 3
    for patch, z in zip(ax.patches, [2, 2, 0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z
    assert ax.collections[0].get_zorder() == 4  # nodes

    plt.close()


def test_draw_nodes(edgelist8):
    H = xgi.Hypergraph(edgelist8)

    ax = xgi.draw_nodes(H)

    # number of elements
    assert len(ax.lines) == 0  # dyads
    assert len(ax.patches) == 0  # hyperedges
    assert len(ax.collections[0].get_sizes()) == H.num_nodes  # nodes

    # zorder
    assert ax.collections[0].get_zorder() == 0  # nodes

    plt.close()


def test_draw_hyperedges(edgelist8):
    H = xgi.Hypergraph(edgelist8)

    ax = xgi.draw_hyperedges(H)

    # number of elements
    assert len(ax.lines) == len(H.edges.filterby("size", 2))  # dyads
    assert len(ax.patches) == len(H.edges.filterby("size", 2, mode="gt"))  # hyperedges
    assert len(ax.collections) == 0  # nodes

    # zorder
    for line in ax.lines:  # dyads
        assert line.get_zorder() == 3
    for patch, z in zip(ax.patches, [2, 2, 0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z

    plt.close()


def test_draw_simplices(edgelist8):
    with pytest.raises(XGIError):
        H = xgi.Hypergraph(edgelist8)
        ax = xgi.draw_simplices(H)
        plt.close()

    S = xgi.SimplicialComplex(edgelist8)
    ax = xgi.draw_simplices(S)

    # number of elements
    assert len(ax.lines) == 18  # dyads
    assert len(ax.patches) == 3  # hyperedges
    assert len(ax.collections) == 0  # nodes

    # zorder
    for line in ax.lines:  # dyads
        assert line.get_zorder() == 3
    for patch, z in zip(ax.patches, [0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z

    plt.close()


def test_draw_hypergraph_hull(edgelist8):

    H = xgi.Hypergraph(edgelist8)

    ax = xgi.draw_hypergraph_hull(H)

    # number of elements
    assert len(ax.patches) == len(H.edges.filterby("size", 2, mode="gt"))  # hyperedges
    assert len(ax.collections[0].get_sizes()) == H.num_nodes  # nodes

    # zorder
    for patch, z in zip(ax.patches, [2, 2, 0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z
    assert ax.collections[0].get_zorder() == 4  # nodes

    plt.close()


def test_draw_multilayer(edgelist8):
    # hypergraph
    H = xgi.Hypergraph(edgelist8)
    ax1 = xgi.draw_multilayer(H)
    assert xgi.max_edge_order(H) * 4 - 1 == len(ax1.collections)
    plt.close()

    # max_order parameter
    max_order = 2
    ax2 = xgi.draw_multilayer(H, max_order=max_order)
    assert max_order * 4 - 1 == len(ax2.collections)
    plt.close()

    # conn_lines parameter
    ax3 = xgi.draw_multilayer(H, conn_lines=False)
    assert xgi.max_edge_order(H) * 3 == len(ax3.collections)
    plt.close()

    # custom parameters
    pos = xgi.circular_layout(H)
    ax4 = xgi.draw_multilayer(
        H,
        pos=pos,
        node_fc="red",
        node_ec="blue",
        node_size=10,
        palette="rainbow",
        conn_lines_style="dashed",
        width=8,
        height=6,
        h_angle=30,
        v_angle=15,
        sep=2,
    )
    assert xgi.max_edge_order(H) * 4 - 1 == len(ax4.collections)
    plt.close()
