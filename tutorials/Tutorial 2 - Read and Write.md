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

## Importing and exporting hypergraph data

When working with empirical hypergraph data, the following file formats representing hypergraphs are commonly seen in practice:
* A hyperedge list, where each line represents a hyperedge
* A bipartite edge list where each line contains two entries: a node ID and an edge ID
* An incidence matrix

The `readwrite` module provides functionality to import and export these file formats.

```{code-cell} ipython3
import xgi
import random
```

### Example hypergraph

```{code-cell} ipython3
n = 10
m = 10

min_edge_size = 2
max_edge_size = 10

# hyperedge list
hyperedge_list = [random.sample(range(n), random.choice(range(min_edge_size,max_edge_size+1))) for i in range(m)]
H = xgi.Hypergraph(hyperedge_list)
```

### JSON

These functions import and export the hypergraph to a standardized JSON format.

```{code-cell} ipython3
# Write the example hypergraph to a JSON file
xgi.write_hypergraph_json(H,"hypergraph_json.json")
# Load the file just written and store it in a new hypergraph
H_json = xgi.read_hypergraph_json("hypergraph_json.json")
```

### Edge List

These functions import and export the hypergraph as an edge list, with user specified delimiters.

```{code-cell} ipython3
# Write the hypergraph to a file as a hyperedge list
xgi.write_edgelist(H, "hyperedge_list.csv", delimiter=",")
# Read the file just written as a new hypergraph
H_el = xgi.read_edgelist("hyperedge_list.csv", delimiter=",", nodetype=int)
```

### Weighted Edge List

These functions import and export the hypergraph as a weighted edge list, with user specified delimiters.

```{code-cell} ipython3
# add weights to the hypergraph
weights = dict()
for edge in H.edges:
    weights[edge] = {"weight" : random.random()}

xgi.set_edge_attributes(H, weights)
```

```{code-cell} ipython3
# Write the hypergraph as a weighted edge list (uses the "weight" attribute by default)
xgi.write_weighted_edgelist(H, "weighted_hyperedge_list.csv", delimiter=",")
# Read the file just written as a new hypergraph
H_wel = xgi.read_weighted_edgelist("weighted_hyperedge_list.csv", delimiter=",", nodetype=int)
```

### Bipartite Edge List

These functions import and export the hypergraph as a bipartite edge list with user-specified delimiters.

```{code-cell} ipython3
# Write the hypergraph as a bipartite edge list
xgi.write_bipartite_edgelist(H, "bipartite_edge_list.csv", delimiter=",")
# Read the file just written as a new hypergraph
H_bel = xgi.read_bipartite_edgelist("bipartite_edge_list.csv", delimiter=",", nodetype=int)
```
