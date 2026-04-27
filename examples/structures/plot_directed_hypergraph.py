"""
=======================
Directed hypegraph
=======================

Draw a directed hypergraph.
"""

import matplotlib.pyplot as plt
import networkx as nx

import xgi

# generate from a list
DH = xgi.DiHypergraph([[{1, 2}, {5, 6}], [{4}, {1, 3}]])

xgi.draw_bipartite(DH)

plt.show()
