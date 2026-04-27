"""
=======================
Ring latting hypergraph
=======================

Generate a ring-lattice hypergraph
"""

import matplotlib.pyplot as plt

import xgi

# specify parameters
n = 10 # number of nodes
s = 3 # size of hyperedges
k = 4 # number of edges of which a node is a part.

# generate hypergraph
H = xgi.ring_lattice(n, s, k, 0) 

# draw hypergraph
pos = xgi.circular_layout(H)
xgi.draw(H, pos=pos)

plt.show()
