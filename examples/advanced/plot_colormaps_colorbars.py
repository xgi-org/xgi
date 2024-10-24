"""
========================
Colormaps and colorbars
========================

Set colormaps and show colorbars.
"""

import matplotlib.pyplot as plt

import xgi

hyperedges = [[1, 2, 3], [3, 4, 5], [3, 6], [6, 7, 8, 9], [1, 4, 10, 11, 12], [1, 4]]
H = xgi.Hypergraph(hyperedges)


pos = xgi.barycenter_spring_layout(H, seed=1)

fig, ax = plt.subplots(figsize=(6, 2.5))

ax, collections = xgi.draw(
    H,
    pos=pos,
    node_fc=H.nodes.degree,
    edge_fc=H.edges.size,
    edge_fc_cmap="viridis",
    node_fc_cmap="mako_r",
)

node_col, _, edge_col = collections

plt.colorbar(node_col, label="Node degree")
plt.colorbar(edge_col, label="Edge size")

plt.show()
