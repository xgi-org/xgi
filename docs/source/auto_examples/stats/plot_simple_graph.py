"""
============
Simple graph
============

Draw simple graph with manual layout.
"""

import matplotlib.pyplot as plt
import xgi

hyperedges = [[1, 2, 3], [3, 4], [4, 5, 6, 7]]
H = xgi.Hypergraph(hyperedges)

xgi.draw(H, hull=True)

print("test")

plt.show()