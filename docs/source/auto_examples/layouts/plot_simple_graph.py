"""
=================
Circular 
=================

Draw simple hypergraph with circular layout.
"""

import matplotlib.pyplot as plt

import xgi

hyperedges = [[1, 2, 3], [3, 4, 5], [3, 6], [6, 7, 8, 9], [1, 4, 10, 11, 12], [1, 4]]
H = xgi.Hypergraph(hyperedges)


pos = xgi.circular_layout(H)
xgi.draw(H, pos=pos)

plt.show()
