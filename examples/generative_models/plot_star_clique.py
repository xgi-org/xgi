"""
=========================
Star-clique
=========================

Generate a star-clique hypergaph.
"""

import matplotlib.pyplot as plt

import xgi

# specify parameters
n_star = 6 # number of legs of the star
n_clique = 7 # number of nodes in the clique
d_max = 2 # maximum order up to which to promote cliques to hyperedges

# generate hypergraph
H = xgi.star_clique(6, 7, 2)

# draw hypergraph
pos = xgi.barycenter_spring_layout(H, seed=1)
xgi.draw(H, pos=pos)

plt.show()
