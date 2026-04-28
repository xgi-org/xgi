"""
=============================
Clique eigenvector centrality
=============================

Compute and visualize the clique eigenvector centrality.
"""

import matplotlib.pyplot as plt

import xgi


# generate hypergraph
n = 20
ps = [0.15, 0.01]
H = xgi.random_hypergraph(n, ps, seed=1)

# visualize hypergraph and centrality
pos = xgi.barycenter_spring_layout(H, seed=1)
ax, collections = xgi.draw(H, pos=pos, node_fc=H.nodes.clique_eigenvector_centrality)

node_col, _, edge_col = collections
plt.colorbar(node_col, label="Clique eigenvector centrality")

plt.show()