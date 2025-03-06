"""
===================================
Simple hypergraph as multilayer
===================================

Draw simple hypergraph as multilayer
"""

import matplotlib.pyplot as plt

import xgi

hyperedges = [[1, 2, 3], [3, 4, 5], [3, 6], [6, 7, 8, 9], [1, 4, 10, 11, 12], [1, 4]]
H = xgi.Hypergraph(hyperedges)


ax3 = plt.axes(projection="3d")  # requires a 3d axis
xgi.draw_multilayer(H, ax=ax3)

plt.show()
