"""
=============================
Node edge centrality
=============================

Compute and visualize the node edge centrality.
"""

import matplotlib.pyplot as plt

import xgi

# generate hypergraph
n = 20
ps = [0.15, 0.01]
H = xgi.fast_random_hypergraph(n, ps, seed=20)

# visualize hypergraph and centrality
pos = xgi.barycenter_spring_layout(H, seed=1)
ax, collections = xgi.draw(H, pos=pos, edge_fc=H.edges.node_edge_centrality)

node_col, _, edge_col = collections

plt.colorbar(edge_col, label="Node edge centrality")

plt.show()
