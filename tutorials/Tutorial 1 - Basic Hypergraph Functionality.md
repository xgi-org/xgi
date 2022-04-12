---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: Python 3.9.7 64-bit (conda)
  name: python3
---

# Tutorial 1 - Loading hypergraphs and basic functionality

+++

This tutorial will give a brief introduction to using the XGI library to construct hypergraphs and perform basic operations on them.

```{code-cell} ipython3
import xgi
import random
import pandas as pd
import numpy as np
```

## Loading hypergraphs from different formats

We handle loading hypergraphs in many different formats, but the hypergraph constructor takes five main data formats:
* A Hypergraph object
* A hyperedge list
* A hyperedge dictionary
* A 2-column pandas dataframe specifying (node, edge) bipartite edges
* An incidence matrix (A Numpy or Scipy matrix)

```{code-cell} ipython3
n = 1000
m = 1000

min_edge_size = 2
max_edge_size = 25

# hyperedge list
hyperedge_list = [random.sample(range(n), random.choice(range(min_edge_size,max_edge_size+1))) for i in range(m)]

# hyperedge dict
hyperedge_dict = {i : random.sample(range(n), random.choice(range(min_edge_size,max_edge_size+1))) for i in range(m)}

# pandas dataframe
fname = "../data/disGene.txt"
df = pd.read_csv(fname, delimiter=" ", header=None)

# incidence matrix
incidence_matrix = np.random.randint(0, high=2, size=(n, m), dtype=int)
```

### Loading a hyperedge list

When a user gives a hyperedge list, the system automatically creates system edge IDs.

```{code-cell} ipython3
H = xgi.Hypergraph(hyperedge_list)
print(f"The hypergraph has {H.num_nodes} nodes and {H.num_edges} edges")
```

### Loading a hyperedge dictionary

When a user gives a hyperedge dictionary, the system uses the edge IDs specified in the dictionary.

```{code-cell} ipython3
H = xgi.Hypergraph(hyperedge_dict)
print(f"The hypergraph has {H.num_nodes} nodes and {H.num_edges} edges")
```

### Loading an incidence matrix

When a user gives an incidence matrix, the system transforms the non-zero entries into lists of rows and columns specifying a bipartite edge list.

```{code-cell} ipython3
H = xgi.Hypergraph(incidence_matrix)
print(f"The hypergraph has {H.num_nodes} nodes and {H.num_edges} edges")
```

### Loading a Pandas dataframe
When a user gives a Pandas dataframe, the system automatically imports the first two columns as lists of node and edge indices specifying a bipartite edge list.

```{code-cell} ipython3
H = xgi.Hypergraph(df)
print(f"The hypergraph has {H.num_nodes} nodes and {H.num_edges} edges")
```

## Simple functions

The Hypergraph class can do simple things like
* output an incidence matrix
* output the adjacency matrix for s-connectedness
* output the dual of the hypergraph
* find if the hypergraph is connected

+++

### Output relevant matrices

```{code-cell} ipython3
# The incidence matrix
I = xgi.incidence_matrix(H, sparse=True)
# The adjacency matrix
A = xgi.adjacency_matrix(H)
# The clique motif matrix
W = xgi.clique_motif_matrix(H)
```

### Forming the dual

```{code-cell} ipython3
D = H.dual()
```

### Testing whether the hypergraph is connected

```{code-cell} ipython3
n = 1000
m = 100

min_edge_size = 2
max_edge_size = 10

# hyperedge list
hyperedge_list = [random.sample(range(n), random.choice(range(min_edge_size,max_edge_size+1))) for i in range(m)]
H = xgi.Hypergraph(hyperedge_list)
```

```{code-cell} ipython3
is_connected = xgi.is_connected(H)
if is_connected:
    print(f"H is connected")
else:
    print(f"H is not connected")

print(f"The sizes of the connected components are:")
print([len(component) for component in xgi.connected_components(H)])

node = 0
print(f"The size of the component containing node {node} is {len(xgi.node_connected_component(H, node))}")
```

### Constructing subhypergraphs

A subhypergraph can be induced by a node subset, an edge subset, or an arbitrary combination of both. These examples are presented below.

```{code-cell} ipython3
# A subhypergraph induced on nodes
node_subhypergraph = H.subhypergraph(list(range(100)))
# A subhypergraph induced on edges
edge_subhypergraph = H.edge_subhypergraph(list(range(100)))
# A subhypergraph induced on both nodes and edges
arbitrary_subhypergraph = H.arbitrary_subhypergraph(list(range(100)),list(range(100)))
```

## Converting to other formats

Below are examples showing how to convert a hypergraph to a hyperedge list, a hyperedge dict, or an incidence matrix.

```{code-cell} ipython3
# Convert to a hyperedge list
h_list = xgi.to_hyperedge_list(H)
# Convert to a hyperedge dict
h_dict = xgi.to_hyperedge_dict(H)
# Convert to an incidence matrix
h_I = xgi.to_incidence_matrix(H)
```

```{code-cell} ipython3

```
