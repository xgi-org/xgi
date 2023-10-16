import matplotlib.pyplot as plt
import numpy as np
import pytest
import seaborn as sb

import xgi
from xgi.exception import XGIError


def test_draw(edgelist8):
    H = xgi.Hypergraph(edgelist8)

    fig, ax = plt.subplots()
    ax, collections = xgi.draw(H, ax=ax)

    (node_collection, dyad_collection, edge_collection) = collections

    # number of elements
    assert len(ax.lines) == 0
    assert len(ax.patches) == 0
    offsets = node_collection.get_offsets()
    assert offsets.shape[0] == H.num_nodes  # nodes
    assert len(ax.collections) == 3
    assert len(dyad_collection.get_paths()) == 3  # dyads
    assert len(edge_collection.get_paths()) == 6  # other hyperedges

    # zorder
    for line in ax.lines:  # dyads
        assert line.get_zorder() == 3
    for patch, z in zip(ax.patches, [2, 2, 0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z
    assert node_collection.get_zorder() == 4  # nodes

    plt.close()

    # simplicial complex 
    S = xgi.SimplicialComplex(edgelist8)

    fig, ax = plt.subplots()
    ax, collections = xgi.draw(S, ax=ax)
    (node_collection, dyad_collection, edge_collection) = collections

    # number of elements
    assert len(ax.lines) == 0 
    assert len(ax.patches) == 0 
    offsets = node_collection.get_offsets()
    assert offsets.shape[0] == S.num_nodes  # nodes
    assert len(ax.collections) == 3 

    assert len(dyad_collection.get_paths()) == 16  # dyads
    assert len(edge_collection.get_paths()) == 3  # other hyperedges

    # zorder
    for line in ax.lines:  # dyads
        assert line.get_zorder() == 3
    for patch, z in zip(ax.patches, [0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z

    plt.close()


def test_draw_nodes(edgelist8):

    H = xgi.Hypergraph(edgelist8)

    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(H, ax=ax)
    fig2, ax2 = plt.subplots()
    ax2, node_collection2 = xgi.draw_nodes(
        H,
        ax=ax2,
        node_fc="r",
        node_ec="b",
        node_lw=2,
        node_size=20,
        zorder=10,
        node_shape="v",
    )

    # number of elements
    assert len(ax.lines) == 0  # dyads
    assert len(ax.patches) == 0  # hyperedges
    offsets = node_collection.get_offsets()
    assert offsets.shape[0] == H.num_nodes  # nodes

    # node_fc
    assert np.all(
        node_collection.get_facecolor() == np.array([[1.0, 1.0, 1.0, 1.0]])
    )  # white
    assert np.all(
        node_collection2.get_facecolor() == np.array([[1.0, 0.0, 0.0, 1.0]])
    )  # blue

    # node_ec
    assert np.all(
        node_collection.get_edgecolor() == np.array([[0.0, 0.0, 0.0, 1.0]])
    )  # black
    assert np.all(
        node_collection2.get_edgecolor() == np.array([[0.0, 0.0, 1.0, 1.0]])
    )  # red

    # node_lw
    assert np.all(node_collection.get_linewidth() == np.array([1]))
    assert np.all(node_collection2.get_linewidth() == np.array([2]))

    # node_size
    assert np.all(node_collection.get_sizes() == np.array([15**2]))
    assert np.all(node_collection2.get_sizes() == np.array([20**2]))

    # zorder
    assert node_collection.get_zorder() == 0
    assert node_collection2.get_zorder() == 10

    # negative node_lw or node_size
    with pytest.raises(ValueError):
        ax3, node_collection3 = xgi.draw_nodes(H, node_size=-1)
        plt.close()
    with pytest.raises(ValueError):
        ax3, node_collection3 = xgi.draw_nodes(H, node_lw=-1)
        plt.close()

    plt.close("all")


def test_draw_nodes_fc_cmap(edgelist8):

    H = xgi.Hypergraph(edgelist8)

    # unused default when single color
    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(H, ax=ax, node_fc="r")
    assert node_collection.get_cmap() == plt.cm.viridis
    plt.close()

    # default cmap
    fig, ax = plt.subplots()
    colors = [11, 12, 14, 16, 17, 19, 21]
    ax, node_collection = xgi.draw_nodes(H, ax=ax, node_fc=colors)
    assert node_collection.get_cmap() == plt.cm.Reds
    plt.close()

    # set cmap
    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(
        H, ax=ax, node_fc=colors, node_fc_cmap="Greens"
    )
    assert node_collection.get_cmap() == plt.cm.Greens
    assert (min(colors), max(colors)) == node_collection.get_clim()
    plt.close()

    # vmin/vmax
    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(H, ax=ax, node_fc=colors, vmin=14, vmax=19)
    assert (14, 19) == node_collection.get_clim()
    plt.close()


def test_draw_nodes_interp(edgelist8):

    H = xgi.Hypergraph(edgelist8)
    arg = H.nodes.degree
    deg_arr = np.array([6, 5, 4, 4, 3, 2, 2])
    assert np.all(arg.aslist() == deg_arr)

    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(H, ax=ax, node_size=1, node_lw=10)
    assert np.all(node_collection.get_sizes() == np.array([1]))
    assert np.all(node_collection.get_linewidth() == np.array([10]))
    plt.close()

    # rescaling does not affect scalars
    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(
        H, ax=ax, node_size=1, node_lw=10, rescale_sizes=True
    )
    assert np.all(node_collection.get_sizes() == np.array([1]))
    assert np.all(node_collection.get_linewidth() == np.array([10]))
    plt.close()

    # not rescaling IDStat
    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(
        H, ax=ax, node_size=arg, node_lw=arg, rescale_sizes=False
    )
    assert np.all(node_collection.get_sizes() == deg_arr**2)
    assert np.all(node_collection.get_linewidth() == deg_arr)
    plt.close()

    # rescaling IDStat
    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(
        H, ax=ax, node_size=arg, node_lw=arg, rescale_sizes=True
    )
    assert min(node_collection.get_sizes()) == 5**2
    assert max(node_collection.get_sizes()) == 30**2
    assert min(node_collection.get_linewidth()) == 0
    assert max(node_collection.get_linewidth()) == 5
    plt.close()

    # rescaling IDStat with manual values
    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(
        H,
        ax=ax,
        node_size=arg,
        node_lw=arg,
        rescale_sizes=True,
        **{"min_node_size": 1, "max_node_size": 20, "min_node_lw": 1, "max_node_lw": 10}
    )
    assert min(node_collection.get_sizes()) == 1**2
    assert max(node_collection.get_sizes()) == 20**2
    assert min(node_collection.get_linewidth()) == 1
    assert max(node_collection.get_linewidth()) == 10
    plt.close()

    # rescaling ndarray
    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_nodes(
        H, ax=ax, node_size=arg, node_lw=deg_arr, rescale_sizes=True
    )
    assert min(node_collection.get_sizes()) == 5**2
    assert max(node_collection.get_sizes()) == 30**2
    assert min(node_collection.get_linewidth()) == 0
    assert max(node_collection.get_linewidth()) == 5
    plt.close()


def test_draw_hyperedges(edgelist8):
    H = xgi.Hypergraph(edgelist8)

    fig, ax = plt.subplots()
    ax, collections = xgi.draw_hyperedges(H, ax=ax)
    (dyad_collection, edge_collection) = collections
    fig2, ax2 = plt.subplots()
    ax2, collections2 = xgi.draw_hyperedges(H, ax=ax2, dyad_color="r",  edge_fc="r", dyad_lw=3, dyad_style="--")
    (dyad_collection2, edge_collection2) = collections2

    # number of elements
    assert len(ax.lines) == 0
    assert len(ax.patches) == 0
    assert len(ax.collections) == 2
    assert len(dyad_collection.get_paths()) == 3  # dyads
    assert len(edge_collection.get_paths()) == 6  # other hyperedges

    # zorder
    for line in ax.lines:  # dyads
        assert line.get_zorder() == 3
    for patch, z in zip(ax.patches, [2, 2, 0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z

    # dyad_style
    dyad_collection.get_linestyle() == [(0.0, None)]
    dyad_collection2.get_linestyle() == [(0.0, [5.550000000000001, 2.4000000000000004])]

    # dyad_fc
    assert np.all(
        dyad_collection.get_color() == np.array([[0, 0, 0, 1]])
    )  # black
    assert np.all(
        dyad_collection2.get_color() == np.array([[1, 0, 0, 1]])
    )  # black

    # edge_fc
    assert np.all(
        edge_collection.get_facecolor()[:, -1] == np.array([0.4, 0.4, 0.4, 0.4, 0.4, 0.4])
    )
    assert np.all(
        edge_collection2.get_facecolor() == np.array([[1., 0., 0., 0.4]])
    )

    # edge_lw
    assert np.all(dyad_collection.get_linewidth() == np.array([1.5]))
    assert np.all(dyad_collection2.get_linewidth() == np.array([3]))
    assert np.all(edge_collection.get_linewidth() == np.array([1.]))

    # negative node_lw or node_size
    with pytest.raises(ValueError):
        ax, collections = xgi.draw_hyperedges(H, ax=ax, dyad_lw=-1)
        (dyad_collection, edge_collection) = collections
        plt.close()


    plt.close("all")


def test_draw_hyperedges_fc_cmap(edgelist8):

    H = xgi.Hypergraph(edgelist8)

    # default cmap
    fig, ax = plt.subplots()
    ax, collections = xgi.draw_hyperedges(H, ax=ax)
    (dyad_collection, edge_collection) = collections
    assert dyad_collection.get_cmap() == plt.cm.Greys
    assert edge_collection.get_cmap() == sb.color_palette("crest_r", as_cmap=True)
    plt.close()

    # set cmap
    fig, ax = plt.subplots()
    dyad_colors = [1, 3, 5]
    ax, collections = xgi.draw_hyperedges(H, ax=ax, dyad_color=dyad_colors, dyad_color_cmap="Greens", edge_fc_cmap="Blues")
    (dyad_collection, edge_collection) = collections
    assert dyad_collection.get_cmap() == plt.cm.Greens
    assert edge_collection.get_cmap() == plt.cm.Blues

    plt.colorbar(dyad_collection)
    plt.colorbar(edge_collection)

    assert (min(dyad_colors), max(dyad_colors)) == dyad_collection.get_clim()
    assert (3, 5) == edge_collection.get_clim()
    plt.close()

    # vmin/vmax
    fig, ax = plt.subplots()
    ax, collections = xgi.draw_hyperedges(H, ax=ax, dyad_color=dyad_colors, dyad_vmin=5, dyad_vmax=6, edge_vmin=14, edge_vmax=19)
    (dyad_collection, edge_collection) = collections
    plt.colorbar(dyad_collection)
    plt.colorbar(edge_collection)
    assert (14, 19) == edge_collection.get_clim()
    assert (5, 6) == dyad_collection.get_clim()

    plt.close()


def test_draw_simplices(edgelist8):
    with pytest.raises(XGIError):
        H = xgi.Hypergraph(edgelist8)
        ax = xgi.draw_simplices(H)
        plt.close()

    S = xgi.SimplicialComplex(edgelist8)

    fig, ax = plt.subplots()
    ax, collections = xgi.draw_simplices(S, ax=ax)
    (dyad_collection, edge_collection) = collections

    # number of elements
    assert len(ax.lines) == 0 
    assert len(ax.patches) == 0 
    assert len(ax.collections) == 2 

    assert len(dyad_collection.get_paths()) == 16  # dyads
    assert len(edge_collection.get_paths()) == 3  # other hyperedges

    # zorder
    for line in ax.lines:  # dyads
        assert line.get_zorder() == 3
    for patch, z in zip(ax.patches, [0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z

    plt.close()


def test_draw_hypergraph_hull(edgelist8):

    H = xgi.Hypergraph(edgelist8)

    fig, ax = plt.subplots()
    ax, node_collection = xgi.draw_hypergraph_hull(H, ax=ax)

    # number of elements
    assert len(ax.patches) == len(H.edges.filterby("size", 2, mode="gt"))  # hyperedges
    offsets = node_collection.get_offsets()
    assert offsets.shape[0] == H.num_nodes  # nodes

    # zorder
    for patch, z in zip(ax.patches, [2, 2, 0, 2, 2]):  # hyperedges
        assert patch.get_zorder() == z
    assert node_collection.get_zorder() == 4  # nodes

    plt.close()


def test_correct_number_of_collections_draw_multilayer(edgelist8):
    # hypergraph
    H = xgi.Hypergraph(edgelist8)

    ax1 = xgi.draw_multilayer(H)
    sizes = xgi.unique_edge_sizes(H)
    num_planes = max(sizes) - min(sizes) + 1
    num_node_collections = max(sizes) - min(sizes) + 1
    num_edge_collections = H.num_edges
    num_thru_lines_collections = 1

    assert (
        num_planes
        + num_node_collections
        + num_edge_collections
        + num_thru_lines_collections
        == len(ax1.collections)
    )
    plt.close()

    # max_order parameter
    max_order = 2
    ax2 = xgi.draw_multilayer(H, max_order=max_order)
    sizes = [2, 3]
    num_planes = max(sizes) - min(sizes) + 1
    num_node_collections = max(sizes) - min(sizes) + 1
    num_edge_collections = len(H.edges.filterby("size", [2, 3], "between"))
    num_thru_lines_collections = 1

    assert (
        num_planes
        + num_node_collections
        + num_edge_collections
        + num_thru_lines_collections
        == len(ax2.collections)
    )
    plt.close()

    # conn_lines parameter
    ax3 = xgi.draw_multilayer(H, conn_lines=False)
    sizes = xgi.unique_edge_sizes(H)
    num_planes = max(sizes) - min(sizes) + 1
    num_node_collections = max(sizes) - min(sizes) + 1
    num_edge_collections = H.num_edges
    assert num_planes + num_node_collections + num_edge_collections == len(
        ax3.collections
    )
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
    sizes = xgi.unique_edge_sizes(H)
    num_planes = max(sizes) - min(sizes) + 1
    num_node_collections = max(sizes) - min(sizes) + 1
    num_edge_collections = H.num_edges
    num_thru_lines_collections = 1

    assert (
        num_planes
        + num_node_collections
        + num_edge_collections
        + num_thru_lines_collections
        == len(ax4.collections)
    )
    plt.close()


def test_draw_dihypergraph(diedgelist2, edgelist8):
    DH = xgi.DiHypergraph(diedgelist2)

    fig, ax1 = plt.subplots()
    ax1 = xgi.draw_dihypergraph(DH, ax=ax1)

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
    fig, ax2 = plt.subplots()
    ax2 = xgi.draw_dihypergraph(DH, edge_marker_toggle=False, ax=ax2)
    assert len(ax2.collections) == 1

    plt.close()

    # test XGI ERROR raise
    with pytest.raises(XGIError):
        H = xgi.Hypergraph(edgelist8)
        fig, ax3 = plt.subplots()
        ax3 = xgi.draw_dihypergraph(H, ax=ax3)
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

    fig, ax4 = plt.subplots()
    ax4 = xgi.draw_dihypergraph(DH1, ax=ax4)
    assert len(ax4.lines) == 3
    assert len(ax4.patches) == 4
    assert len(ax4.collections) == DH1.num_edges + 1 - len(
        DH1.edges.filterby("size", 1)
    )
