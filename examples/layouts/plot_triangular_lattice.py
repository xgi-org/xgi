"""
=======================
Show triangular lattice
=======================

Draw triangular lattice.
"""

import matplotlib.pyplot as plt
import networkx as nx

import xgi

# generate lattice
m, n = 10, 20 # lattice dimensions
p = 0.5 # probability to promote 3-clique to 2-simplex

G = nx.triangular_lattice_graph(m, n, with_positions=True)

pos = nx.get_node_attributes(G, "pos")
mapping = {i: list(G.nodes)[i] for i in range(0, len(list(G.nodes)))}
inv_mapping = {v: k for k, v in mapping.items()}

G_aux = nx.relabel_nodes(G, inv_mapping)
S = xgi.flag_complex_d2(G_aux, p2=p) 

# draw lattice
pos = {inv_mapping[k]: v for k, v in pos.items()}
xgi.draw(S, pos=pos)

plt.show()