"""
=========================
Random simplicial complex
=========================

Generate a random hypergraph.
"""

import matplotlib.pyplot as plt

import xgi

# specify parameters
seed = 1  # fix random number generation
n = 20  # number of nodes
ps = [0.15, 0.01]  # wiring probabilities

# generate hypergraph
H = xgi.random_simplicial_complex(n, ps, seed=seed)

# draw hypergraph
pos = xgi.barycenter_spring_layout(H, seed=seed)
xgi.draw(H, pos=pos)

plt.show()
