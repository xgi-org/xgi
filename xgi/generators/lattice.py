"""Generators for some lattice hypergraphs.

All the functions in this module return a Hypergraph class (i.e. a simple, undirected
hypergraph).

"""

from math import cos, pi, sin
from warnings import warn

__all__ = [
    "ring_lattice",
]


def ring_lattice(n, d, k, l, with_positions=False):
    """A ring lattice hypergraph.

    A d-uniform hypergraph on n nodes where each node is part of k edges and the
    overlap between consecutive edges is d-l.

    Parameters
    ----------
    n : int
        Number of nodes
    d : int
        Edge size
    k : int
        Number of edges of which a node is a part. Should be a multiple of 2.
    l : int
        Overlap between edges
    with_positions : bool, optional
        If True, store each node's coordinates on a unit circle as the ``"pos"`` node
        attribute. By default, False. Useful for plotting:
        ``xgi.draw(H, pos=H.nodes.pos.asdict())``.

    Returns
    -------
    Hypergraph
        The generated hypergraph

    Raises
    ------
    ValueError
        If k is negative.

    Notes
    -----
    ring_lattice(n, 2, k, 0) is a ring lattice graph where each node has k//2 edges on
    either side.

    """
    from ..core import Hypergraph

    if k < 0:
        raise ValueError("Invalid k value!")

    if k < 2:
        warn("This creates a completely disconnected hypergraph!")

    if k % 2 != 0:
        warn("k is not divisible by 2")

    edges = [
        [node] + [(start + l + i) % n for i in range(d - 1)]
        for node in range(n)
        for start in range(node + 1, node + k // 2 + 1)
    ]
    H = Hypergraph(edges)
    H.add_nodes_from(range(n))
    if with_positions:
        pos = {i: (cos(2 * pi * i / n), sin(2 * pi * i / n)) for i in range(n)}
        H.set_node_attributes(pos, name="pos")
    return H
