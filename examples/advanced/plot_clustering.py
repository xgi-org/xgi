"""
=================
Show communities
=================

Draw hypergraph with communities.
"""

import matplotlib.pyplot as plt

import xgi

# generate clustered hypergraph
H1 = xgi.uniform_HPPM(100, 2, 3, 0.9, seed=0)
H2 = xgi.uniform_HPPM(100, 3, 2, 0.9, seed=0)
H = H1 << H2
H.cleanup()

# compute communities
node_labels = xgi.spectral_clustering(H, k=2, max_iter=100, seed=0)
H.set_node_attributes(node_labels, "group")

# draw hypergraph
pos = xgi.pca_transform(xgi.pairwise_spring_layout(H, seed=0))
xgi.draw(H, pos=pos, node_fc=H.nodes.attrs("group"))

plt.show()
