"""
=======================
Chung-Lu hypergraph
=======================

Generate a Chung-Lu hypergraph
"""

import matplotlib.pyplot as plt
import numpy as np

import xgi

# fix random seed for reproducibility
seed = 42
rng = np.random.default_rng(seed)

# specify parameters
n = 20  # number of nodes
k1 = {i: int(rng.integers(1, 101)) for i in range(n)}  # degree distribution
k2 = {i: sorted(k1.values())[i] for i in range(n)}  # degree distribution

# generate hypergraph
H = xgi.chung_lu_hypergraph(k1, k2, seed=rng)

# draw hypergraph
pos = xgi.barycenter_spring_layout(H, seed=seed)
xgi.draw(H, pos=pos, alpha=0.3)

plt.show()
