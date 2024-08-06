import pytest

import xgi
from xgi.exception import IDNotFound, XGIError


def test_num_edges_order(edgelist2):
    H = xgi.Hypergraph(edgelist2)

    assert xgi.num_edges_order(H, 0) == 0
    assert xgi.num_edges_order(H, 1) == 2
    assert xgi.num_edges_order(H, 2) == 1
    assert xgi.num_edges_order(H) == 3


def test_max_edge_order(edgelist1, edgelist4, edgelist5):
    H0 = xgi.empty_hypergraph()
    H1 = xgi.empty_hypergraph()
    H1.add_nodes_from(range(5))
    H2 = xgi.Hypergraph(edgelist1)
    H3 = xgi.Hypergraph(edgelist4)
    H4 = xgi.Hypergraph(edgelist5)

    assert xgi.max_edge_order(H0) is None
    assert xgi.max_edge_order(H1) == 0
    assert xgi.max_edge_order(H2) == 2
    assert xgi.max_edge_order(H3) == 3
    assert xgi.max_edge_order(H4) == 3


def test_is_possible_order(edgelist1):
    H1 = xgi.Hypergraph(edgelist1)

    assert xgi.is_possible_order(H1, -1) is False
    assert xgi.is_possible_order(H1, 0) is True
    assert xgi.is_possible_order(H1, 1) is True
    assert xgi.is_possible_order(H1, 2) is True
    assert xgi.is_possible_order(H1, 3) is False


def test_is_uniform(edgelist1, edgelist6, edgelist7):
    H0 = xgi.Hypergraph(edgelist1)
    H1 = xgi.Hypergraph(edgelist6)
    H2 = xgi.Hypergraph(edgelist7)
    H3 = xgi.empty_hypergraph()

    assert xgi.is_uniform(H0) is False
    assert xgi.is_uniform(H1) == 2
    assert xgi.is_uniform(H2) == 2
    assert xgi.is_uniform(H3) is False


def test_edge_neighborhood(edgelist3):
    H = xgi.Hypergraph(edgelist3)
    assert H.nodes.neighbors(3) == {1, 2, 4}
    assert xgi.edge_neighborhood(H, 3) == [{1, 2}, {4}]
    assert xgi.edge_neighborhood(H, 3, include_self=True) == [{1, 2, 3}, {3, 4}]
    with pytest.raises(IDNotFound):
        xgi.edge_neighborhood(H, 7)


def test_degree_counts(edgelist1, edgelist2, edgelist3):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)

    assert xgi.degree_counts(H1) == [0, 7, 1]
    assert xgi.degree_counts(H2) == [0, 5, 1]
    assert xgi.degree_counts(H3) == [0, 4, 2]

    assert xgi.degree_counts(H1, order=2) == [2, 6]


def test_degree_histogram(edgelist1, edgelist2, edgelist3):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist3)

    assert xgi.degree_histogram(H1) == ([1, 2], [7, 1])
    assert xgi.degree_histogram(H2) == ([1, 2], [5, 1])
    assert xgi.degree_histogram(H3) == ([1, 2], [4, 2])


def test_unique_edge_sizes(edgelist1, edgelist2, edgelist4, edgelist5):
    H1 = xgi.Hypergraph(edgelist1)
    H2 = xgi.Hypergraph(edgelist2)
    H3 = xgi.Hypergraph(edgelist4)
    H4 = xgi.Hypergraph(edgelist5)

    assert xgi.unique_edge_sizes(H1) == [1, 2, 3]
    assert xgi.unique_edge_sizes(H2) == [2, 3]
    assert xgi.unique_edge_sizes(H3) == [3, 4]
    assert xgi.unique_edge_sizes(H4) == [1, 2, 3, 4]

    # ensure python int and not numpy int
    # see https://github.com/xgi-org/xgi/issues/566

    assert isinstance(xgi.unique_edge_sizes(H1)[0], int)


def test_density_no_nodes():
    H = xgi.Hypergraph()
    with pytest.raises(XGIError):
        xgi.density(H)
    with pytest.raises(XGIError):
        xgi.density(H, order=3)
    with pytest.raises(XGIError):
        xgi.density(H, max_order=7)
    with pytest.raises(XGIError):
        xgi.density(H, ignore_singletons=True)
    with pytest.raises(XGIError):
        xgi.density(H, order=2, ignore_singletons=True)
    with pytest.raises(XGIError):
        xgi.density(H, max_order=2, ignore_singletons=True)


def test_density_no_edges():
    tol = 1e-10
    H = xgi.Hypergraph()
    H.add_node(0)
    assert xgi.density(H) < tol
    assert xgi.density(H, order=3) < tol
    assert xgi.density(H, max_order=7) < tol
    assert xgi.density(H, ignore_singletons=True) < tol
    assert xgi.density(H, order=2, ignore_singletons=True) < tol
    assert xgi.density(H, max_order=2, ignore_singletons=True) < tol


def test_density_one_node():
    tol = 1e-10
    H = xgi.Hypergraph([[0]])  # one node, one singleton edge
    assert abs(xgi.density(H) - 1) < tol
    assert xgi.density(H, ignore_singletons=True) < tol

    H = xgi.Hypergraph()
    H.add_node(0)  # one node, no edges
    assert xgi.density(H) < tol
    assert xgi.density(H, order=2) < tol
    assert xgi.density(H, max_order=13) < tol
    assert xgi.density(H, ignore_singletons=True) < tol


def test_density_two_nodes():
    tol = 1e-10

    H = xgi.Hypergraph()  # two nodes, no edges
    H.add_nodes_from([0, 1])
    assert xgi.density(H) < tol
    assert xgi.density(H, order=3) < tol
    assert xgi.density(H, max_order=6) < tol
    assert xgi.density(H, ignore_singletons=True) < tol

    H = xgi.Hypergraph()  # two nodes, one singleton edge
    H.add_nodes_from([0, 1])
    H.add_edge([0])
    assert abs(xgi.density(H) - 1 / 3) < tol
    assert abs(xgi.density(H, order=0) - 1 / 2) < tol
    assert xgi.density(H, order=1) < tol
    assert xgi.density(H, ignore_singletons=True) < tol

    H = xgi.Hypergraph()  # two nodes, one 2-edge
    H.add_nodes_from([0, 1])
    H.add_edge([0, 1])
    assert abs(xgi.density(H) - 1 / 3) < tol
    assert xgi.density(H, order=0) < tol
    assert abs(xgi.density(H, order=1) - 1) < tol
    assert abs(xgi.density(H, order=1, ignore_singletons=True) - 1) < tol

    H = xgi.Hypergraph()  # two nodes, one singleton and one 2-edge
    H.add_nodes_from([0, 1])
    H.add_edges_from(([0], [0, 1]))
    assert abs(xgi.density(H) - 2 / 3) < tol
    assert abs(xgi.density(H, order=0) - 1 / 2) < tol
    assert abs(xgi.density(H, order=0, ignore_singletons=True)) < tol
    assert abs(xgi.density(H, order=1) - 1) < tol
    assert abs(xgi.density(H, order=1, ignore_singletons=True) - 1) < tol
    assert abs(xgi.density(H, max_order=0) - 1 / 2) < tol
    assert abs(xgi.density(H, max_order=0, ignore_singletons=True)) < tol
    assert abs(xgi.density(H, max_order=1) - 2 / 3) < tol
    assert abs(xgi.density(H, max_order=1, ignore_singletons=True) - 1) < tol

    H = xgi.Hypergraph()  # two nodes, all possible edges
    H.add_nodes_from([0, 1])
    H.add_edges_from(([0], [1], [0, 1]))
    assert abs(xgi.density(H) - 1) < tol
    assert abs(xgi.density(H, order=0) - 1) < tol
    assert abs(xgi.density(H, order=0, ignore_singletons=True)) < tol
    assert abs(xgi.density(H, order=1) - 1) < tol
    assert abs(xgi.density(H, order=1, ignore_singletons=True) - 1) < tol
    assert abs(xgi.density(H, max_order=0) - 1) < tol
    assert abs(xgi.density(H, max_order=0, ignore_singletons=True)) < tol
    assert abs(xgi.density(H, max_order=1) - 1) < tol
    assert abs(xgi.density(H, max_order=1, ignore_singletons=True) - 1) < tol


def test_density_max_order(edgelist5):
    # max_order cannot be larger than the number of nodes
    H = xgi.Hypergraph([(0, 1)])
    with pytest.raises(ValueError):
        xgi.density(H, max_order=2)
    with pytest.raises(ValueError):
        xgi.density(H, max_order=3)

    H = xgi.Hypergraph(edgelist5)
    with pytest.raises(ValueError):
        xgi.density(H, max_order=10)
    with pytest.raises(ValueError):
        xgi.density(H, max_order=11)


def test_density_order(edgelist5):
    # order cannot be larger than the number of nodes
    H = xgi.Hypergraph([(0, 1)])
    with pytest.raises(ValueError):
        xgi.density(H, order=2)
    with pytest.raises(ValueError):
        xgi.density(H, order=3)

    H = xgi.Hypergraph(edgelist5)
    with pytest.raises(ValueError):
        xgi.density(H, order=10)
    with pytest.raises(ValueError):
        xgi.density(H, order=11)


def test_density(edgelist1):
    tol = 1e-10

    H = xgi.Hypergraph(edgelist1)
    assert abs(xgi.density(H) - 0.01568627450980392) < tol
    assert abs(xgi.density(H, ignore_singletons=True) - 0.012145748987854251) < tol

    assert abs(xgi.density(H, order=0) - 0.125) < tol
    assert abs(xgi.density(H, order=0, ignore_singletons=True)) < tol
    assert abs(xgi.density(H, order=1) - 0.03571428571428571) < tol
    assert abs(xgi.density(H, order=1, ignore_singletons=True) - 0.0357142857142) < tol
    assert abs(xgi.density(H, order=2) - 0.03571428571428571) < tol
    for i in range(3, 8):
        assert abs(xgi.density(H, order=i) - 0.0) < tol
        assert abs(xgi.density(H, order=i, ignore_singletons=True) - 0.0) < tol
    with pytest.raises(ValueError):
        xgi.density(H, order=8)  # order cannot be larger than number of nodes
    with pytest.raises(ValueError):
        xgi.density(H, order=8, ignore_singletons=True)

    assert abs(xgi.density(H, max_order=0) - 0.125) < tol
    assert abs(xgi.density(H, max_order=1) - 0.05555555555555555) < tol
    assert abs(xgi.density(H, max_order=2) - 0.043478260869565216) < tol
    assert abs(xgi.density(H, max_order=3) - 0.024691358024691357) < tol
    assert abs(xgi.density(H, max_order=4) - 0.01834862385321101) < tol
    assert abs(xgi.density(H, max_order=5) - 0.016260162601626018) < tol
    assert abs(xgi.density(H, max_order=6) - 0.015748031496062992) < tol
    assert abs(xgi.density(H, max_order=7) - 0.01568627450980392) < tol
    with pytest.raises(ValueError):
        xgi.density(H, max_order=8)  # max_order cannot be larger than number of nodes

    def dens_ignore_sing(m):
        return xgi.density(H, max_order=m, ignore_singletons=True)

    assert abs(dens_ignore_sing(0) - 0.0) < tol
    assert abs(dens_ignore_sing(1) - 0.03571428571428571) < tol
    assert abs(dens_ignore_sing(2) - 0.03571428571428571) < tol
    assert abs(dens_ignore_sing(3) - 0.01948051948051948) < tol
    assert abs(dens_ignore_sing(4) - 0.014285714285714285) < tol
    assert abs(dens_ignore_sing(5) - 0.012605042016806723) < tol
    assert abs(dens_ignore_sing(6) - 0.012195121951219513) < tol
    assert abs(dens_ignore_sing(7) - 0.012145748987854251) < tol
    with pytest.raises(ValueError):
        xgi.density(H, max_order=8, ignore_singletons=True)


def test_incidence_density_no_nodes():
    H = xgi.Hypergraph()
    with pytest.raises(XGIError):
        xgi.incidence_density(H)
    with pytest.raises(XGIError):
        xgi.incidence_density(H, order=3)
    with pytest.raises(XGIError):
        xgi.incidence_density(H, max_order=7)
    with pytest.raises(XGIError):
        xgi.incidence_density(H, ignore_singletons=True)
    with pytest.raises(XGIError):
        xgi.incidence_density(H, order=2, ignore_singletons=True)
    with pytest.raises(XGIError):
        xgi.incidence_density(H, max_order=2, ignore_singletons=True)


def test_incidence_density_no_edges():
    tol = 1e-10
    H = xgi.Hypergraph()
    H.add_node(0)
    assert xgi.incidence_density(H) < tol
    assert xgi.incidence_density(H, order=3) < tol
    assert xgi.incidence_density(H, max_order=7) < tol
    assert xgi.incidence_density(H, ignore_singletons=True) < tol
    assert xgi.incidence_density(H, order=2, ignore_singletons=True) < tol
    assert xgi.incidence_density(H, max_order=2, ignore_singletons=True) < tol


def test_incidence_density_one_node():
    tol = 1e-10
    H = xgi.Hypergraph([[0]])  # one node, one singleton edge
    assert abs(xgi.incidence_density(H) - 1) < tol
    assert xgi.incidence_density(H, ignore_singletons=True) < tol

    H = xgi.Hypergraph()
    H.add_node(0)  # one node, no edges
    assert xgi.incidence_density(H) < tol
    assert xgi.incidence_density(H, order=2) < tol
    assert xgi.incidence_density(H, max_order=13) < tol
    assert xgi.incidence_density(H, ignore_singletons=True) < tol


def test_incidence_density_two_nodes():
    tol = 1e-10

    H = xgi.Hypergraph()  # two nodes, no edges
    H.add_nodes_from([0, 1])
    assert xgi.incidence_density(H) < tol
    assert xgi.incidence_density(H, order=3) < tol
    assert xgi.incidence_density(H, max_order=6) < tol
    assert xgi.incidence_density(H, ignore_singletons=True) < tol

    H = xgi.Hypergraph()  # two nodes, one singleton edge
    H.add_nodes_from([0, 1])
    H.add_edge([0])
    assert abs(xgi.incidence_density(H) - 1 / 2) < tol
    assert abs(xgi.incidence_density(H, order=0) - 1 / 2) < tol
    assert xgi.incidence_density(H, order=1) < tol
    assert xgi.incidence_density(H, ignore_singletons=True) < tol

    H = xgi.Hypergraph()  # two nodes, one 2-edge
    H.add_nodes_from([0, 1])
    H.add_edge([0, 1])
    assert abs(xgi.incidence_density(H) - 1) < tol
    assert xgi.incidence_density(H, order=0) < tol
    assert abs(xgi.incidence_density(H, order=1) - 1) < tol
    assert abs(xgi.incidence_density(H, order=1, ignore_singletons=True) - 1) < tol

    H = xgi.Hypergraph()  # two nodes, one singleton and one 2-edge
    H.add_nodes_from([0, 1])
    H.add_edges_from(([0], [0, 1]))
    assert abs(xgi.incidence_density(H) - 3 / 4) < tol
    assert abs(xgi.incidence_density(H, order=0) - 1 / 2) < tol
    assert abs(xgi.incidence_density(H, order=0, ignore_singletons=True)) < tol
    assert abs(xgi.incidence_density(H, order=1) - 1) < tol
    assert abs(xgi.incidence_density(H, order=1, ignore_singletons=True) - 1) < tol
    assert abs(xgi.incidence_density(H, max_order=0) - 1 / 2) < tol
    assert abs(xgi.incidence_density(H, max_order=0, ignore_singletons=True)) < tol
    assert abs(xgi.incidence_density(H, max_order=1) - 3 / 4) < tol
    assert abs(xgi.incidence_density(H, max_order=1, ignore_singletons=True) - 1) < tol

    H = xgi.Hypergraph()  # two nodes, all possible edges
    H.add_nodes_from([0, 1])
    H.add_edges_from(([0], [1], [0, 1]))
    assert abs(xgi.incidence_density(H) - 2 / 3) < tol
    assert abs(xgi.incidence_density(H, order=0) - 1 / 2) < tol
    assert abs(xgi.incidence_density(H, order=0, ignore_singletons=True)) < tol
    assert abs(xgi.incidence_density(H, order=1) - 1) < tol
    assert abs(xgi.incidence_density(H, order=1, ignore_singletons=True) - 1) < tol
    assert abs(xgi.incidence_density(H, max_order=0) - 1 / 2) < tol
    assert abs(xgi.incidence_density(H, max_order=0, ignore_singletons=True)) < tol
    assert abs(xgi.incidence_density(H, max_order=1) - 2 / 3) < tol
    assert abs(xgi.incidence_density(H, max_order=1, ignore_singletons=True) - 1) < tol


def test_incidence_density_max_order(edgelist5):
    # max_order cannot be larger than the number of nodes
    H = xgi.Hypergraph([(0, 1)])
    with pytest.raises(ValueError):
        xgi.incidence_density(H, max_order=2)
    with pytest.raises(ValueError):
        xgi.incidence_density(H, max_order=3)

    H = xgi.Hypergraph(edgelist5)
    with pytest.raises(ValueError):
        xgi.incidence_density(H, max_order=10)
    with pytest.raises(ValueError):
        xgi.incidence_density(H, max_order=11)


def test_incidence_density_order(edgelist5):
    # order cannot be larger than the number of nodes
    H = xgi.Hypergraph([(0, 1)])
    with pytest.raises(ValueError):
        xgi.incidence_density(H, order=2)
    with pytest.raises(ValueError):
        xgi.incidence_density(H, order=3)

    H = xgi.Hypergraph(edgelist5)
    with pytest.raises(ValueError):
        xgi.incidence_density(H, order=10)
    with pytest.raises(ValueError):
        xgi.incidence_density(H, order=11)


def test_incidence_density(edgelist1):
    tol = 1e-10

    H = xgi.Hypergraph(edgelist1)
    assert abs(xgi.incidence_density(H) - 0.28125) < tol
    assert abs(xgi.incidence_density(H, ignore_singletons=True) - 1 / 3) < tol
    assert abs(xgi.incidence_density(H, order=0) - 0.125) < tol
    assert abs(xgi.incidence_density(H, order=0, ignore_singletons=True)) < tol
    assert abs(xgi.incidence_density(H, order=1) - 0.25) < tol
    assert abs(xgi.incidence_density(H, order=1, ignore_singletons=True) - 0.25) < tol
    assert abs(xgi.incidence_density(H, order=2) - 0.375) < tol
    for i in range(3, 8):
        assert abs(xgi.incidence_density(H, order=i)) < tol
        assert abs(xgi.incidence_density(H, order=i, ignore_singletons=True)) < tol
    with pytest.raises(ValueError):
        xgi.incidence_density(H, order=8)  # order cannot be larger than number of nodes
    with pytest.raises(ValueError):
        xgi.incidence_density(H, order=8, ignore_singletons=True)

    assert abs(xgi.incidence_density(H, max_order=0) - 0.125) < tol
    assert abs(xgi.incidence_density(H, max_order=1) - 0.1875) < tol
    assert abs(xgi.incidence_density(H, max_order=2) - 0.28125) < tol
    assert abs(xgi.incidence_density(H, max_order=3) - 0.28125) < tol
    assert abs(xgi.incidence_density(H, max_order=4) - 0.28125) < tol
    assert abs(xgi.incidence_density(H, max_order=5) - 0.28125) < tol
    assert abs(xgi.incidence_density(H, max_order=6) - 0.28125) < tol
    assert abs(xgi.incidence_density(H, max_order=7) - 0.28125) < tol
    with pytest.raises(ValueError):
        xgi.incidence_density(
            H, max_order=8
        )  # max_order cannot be larger than number of nodes

    def dens_ignore_sing(m):
        return xgi.incidence_density(H, max_order=m, ignore_singletons=True)

    assert abs(dens_ignore_sing(0) - 0.0) < tol
    assert abs(dens_ignore_sing(1) - 0.25) < tol
    assert abs(dens_ignore_sing(2) - 1 / 3) < tol
    assert abs(dens_ignore_sing(3) - 1 / 3) < tol
    assert abs(dens_ignore_sing(4) - 1 / 3) < tol
    assert abs(dens_ignore_sing(5) - 1 / 3) < tol
    assert abs(dens_ignore_sing(6) - 1 / 3) < tol
    assert abs(dens_ignore_sing(7) - 1 / 3) < tol
    with pytest.raises(ValueError):
        xgi.incidence_density(H, max_order=8, ignore_singletons=True)
