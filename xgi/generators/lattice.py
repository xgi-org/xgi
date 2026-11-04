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

    A d-uniform hypergraph on n nodes arranged on a ring. Each node i originates
    k//2 edges, made of i and d-1 consecutive nodes going clockwise:
    ``[i, s+l, ..., s+l+d-2]`` for ``s = i+1, ..., i+k//2`` (modulo n).

    Parameters
    ----------
    n : int
        Number of nodes
    d : int
        Edge size
    k : int
        Twice the number of edges originating at each node. Should be a multiple
        of 2. Each node is then part of k*d/2 edges on average (k for d=2).
    l : int
        Offset of the d-1 consecutive nodes from the originating node: the block
        starts l nodes after the nearest possible position. With l=0, the first
        edge of node i is ``[i, i+1, ..., i+d-1]``.
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
