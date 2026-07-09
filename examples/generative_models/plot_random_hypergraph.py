"""
=======================
Random hypergraph
=======================

Generate a random hypergraph.
"""

import matplotlib.pyplot as plt

import xgi

# specify parameters
n = 20  # number of nodes
ps = [0.15, 0.01]  # wiring probabilities

# generate hypergraph
H = xgi.random_hypergraph(n, ps, seed=1)

# draw hypergraph
pos = xgi.barycenter_spring_layout(H, seed=1)
xgi.draw(H, pos=pos)

plt.show()
