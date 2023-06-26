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


def test_correct_number_of_collections_draw_multilayer(edgelist8):
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


def test_draw_dihypergraph(diedgelist2, edgelist8):
    DH = xgi.DiHypergraph(diedgelist2)
    ax1 = xgi.draw_dihypergraph(DH)

    # number of elements
    assert len(ax1.lines) == 7  # number of source nodes
    assert len(ax1.patches) == 4  # number of target nodes
    assert len(ax1.collections) == DH.num_edges + 1 - len(
        DH.edges.filterby("size", 1)
    )  # hyperedges markers + nodes

    # zorder
    for line, z in zip(ax1.lines, [1, 1, 1, 1, 0, 0, 0]):  # lines for source nodes
        assert line.get_zorder() == z
    for patch, z in zip(ax1.patches, [1, 1, 0, 0]):  # arrows for target nodes
        assert patch.get_zorder() == z
    for collection in ax1.collections:
        assert collection.get_zorder() == 3  # nodes and hyperedges markers

    plt.close()

    # test toggle for edges
    ax2 = xgi.draw_dihypergraph(DH, edge_marker_toggle=False)
    assert len(ax2.collections) == 1

    plt.close()

    # test XGI ERROR raise
    with pytest.raises(XGIError):
        H = xgi.Hypergraph(edgelist8)
        ax3 = xgi.draw_dihypergraph(H)
        plt.close()


def test_draw_dihypergraph_with_str_labels_and_isolated_nodes():
    DH1 = xgi.DiHypergraph()
    DH1.add_edges_from(
        [
            [{"one"}, {"two", "three"}],
            [{"two", "three"}, {"four", "five"}],
            [{"six"}, {}],
        ]
    )
    ax4 = xgi.draw_dihypergraph(DH1)
    assert len(ax4.lines) == 3
    assert len(ax4.patches) == 4
    assert len(ax4.collections) == DH1.num_edges + 1 - len(
        DH1.edges.filterby("size", 1)
    )
