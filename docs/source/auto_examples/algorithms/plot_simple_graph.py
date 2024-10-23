"""
=================
Simple hypergraph
=================

Draw simple hypergraph with manual layout.
"""

import matplotlib.pyplot as plt
import xgi

hyperedges = [[1, 2, 3], [3, 4], [4, 5, 6, 7]]
H = xgi.Hypergraph(hyperedges)


pos = xgi.barycenter_spring_layout(H, seed=1)
xgi.draw(H, pos=pos)

plt.show()