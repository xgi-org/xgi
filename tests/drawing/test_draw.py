import matplotlib.pyplot as plt
import pytest

import xgi
from xgi.exception import XGIError


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
