---
name: xgi
description: Use this skill when reading, writing, or modifying Python code that uses the XGI library (higher-order networks, hypergraphs, simplicial complexes). It covers XGI basics, the stats interface (XGI's most-missed feature), idiomatic patterns, and the common mistakes that AI agents make. Activate it whenever `import xgi` appears or is about to appear, or when the user asks about hypergraphs, simplicial complexes, or directed hypergraphs.
version: 0.1.0
---

# XGI skill for AI coding agents

XGI is a Python library for higher-order networks. The most common failure
mode of AI agents working with XGI is using only its container classes
(treating it like NetworkX) and missing the stats, generators, algorithms,
drawing, and I/O that make XGI worth using.

If you are about to write XGI code, read this whole file. It is short.

## When this skill does NOT apply

- Code that imports `networkx`, `igraph`, `graph-tool`, or `hypergraphx`
  (the unrelated competing library — distinct from XGI; APIs differ
  substantially).
- Generic Python / numpy / scipy / matplotlib code that doesn't touch XGI.

---

## Basics

Three core classes:

```python
import xgi

H  = xgi.Hypergraph([[1, 2, 3], [2, 3, 4]])    # undirected, multiedges allowed
DH = xgi.DiHypergraph([([1, 2], [3, 4])])      # directed; edges are (tail, head) tuples
SC = xgi.SimplicialComplex([[1, 2, 3]])        # closure property enforced
```

Other ways to build:

```python
xgi.Hypergraph({"e1": [1, 2, 3]})              # from dict-of-edges
xgi.load_xgi_data("congress-bills")            # from xgi-data repository
xgi.random_hypergraph(50, [0.1, 0.01], seed=1) # from a generator
xgi.read_hif(path)                             # from HIF JSON
```

Inspecting:

```python
H.num_nodes, H.num_edges
H.nodes, H.edges                # NodeView, EdgeView
H.edges.members(0)              # {1, 2, 3} — the nodes in edge 0
H.nodes.memberships(node_id)    # {edge_id, ...} — edges containing the node
list(H.nodes), list(H.edges)    # iterate IDs
```

Important: `H.edges[0]` does NOT give you the members. It gives you the
edge's attribute dict. See "Gotchas" below.

## Where each capability lives

| If you need... | Look in... | Online reference |
|---|---|---|
| Per-node / per-edge quantities and filtering | `H.nodes.<stat>`, `H.edges.<stat>` (see "Stats" below) | [stats](https://xgi.readthedocs.io/en/stable/api/stats.html) · [cheat sheet](https://xgi.readthedocs.io/en/stable/stats_cheatsheet.html) |
| Centralities, clustering, connectivity, simpliciality | `xgi.algorithms` | [algorithms](https://xgi.readthedocs.io/en/stable/api/algorithms.html) |
| Random / structured hypergraph generators | `xgi.generators` | [generators](https://xgi.readthedocs.io/en/stable/api/generators.html) |
| Drawing with matplotlib | `xgi.draw`, `xgi.drawing.*` | [drawing](https://xgi.readthedocs.io/en/stable/api/drawing.html) |
| Read/write HIF and other formats | `xgi.read_hif`, `xgi.write_hif`, `xgi.readwrite.*` | [readwrite](https://xgi.readthedocs.io/en/stable/api/readwrite.html) |
| Conversions and projections | `xgi.to_*`, `xgi.from_*` | [convert](https://xgi.readthedocs.io/en/stable/api/convert.html) |
| Matrix representations | `xgi.adjacency_matrix`, `xgi.laplacian`, etc. | [linalg](https://xgi.readthedocs.io/en/stable/api/linalg.html) |
| Loading datasets from xgi-data | `xgi.load_xgi_data(name)` | [xgi-data](https://xgi.readthedocs.io/en/stable/xgi-data.html) |

For the full API surface, browse the [online docs](https://xgi.readthedocs.io/en/stable/api_reference.html)
or introspect at runtime (`dir(xgi)`, `help(xgi.foo)`, `xgi.foo?` in IPython).

---

## The stats interface

The stats interface is the highest-value and most-missed surface in XGI. If
you are treating XGI like NetworkX, this is the section that fixes that.

### What stats are

A stat is a mapping from each node (or edge) to a value. Examples: degree,
clustering coefficient, eigenvector centrality, an arbitrary attribute, or a
user-defined function.

Access them through the view, not the hypergraph:

```python
H.nodes.degree            # NodeStat object
H.edges.size              # EdgeStat object
H.nodes.attrs("color")    # NodeStat over an attribute
```

A `NodeStat` / `EdgeStat` is callable (to parametrize) and exposes many
output methods. It does *not* hold computed values until you ask.

### Output formats

```python
H.nodes.degree.asdict()    # {id: value}
H.nodes.degree.aslist()    # [value, ...] in id order
H.nodes.degree.asnumpy()   # numpy ndarray
H.nodes.degree.aspandas()  # pandas Series
H.nodes.degree[node_id]    # single value
```

### Summary statistics

```python
H.nodes.degree.max()
H.nodes.degree.min()
H.nodes.degree.mean()
H.nodes.degree.median()
H.nodes.degree.mode()
H.nodes.degree.std()
H.nodes.degree.var()
H.nodes.degree.sum()
H.nodes.degree.argmax()         # id of the max
H.nodes.degree.argmin()
H.nodes.degree.argsort(reverse=True)
H.nodes.degree.unique(return_counts=True)
H.nodes.degree.moment(order=2, center=True)
H.nodes.degree.ashist(bins=10, density=False)   # pandas DataFrame
```

### Parametrized stats

Some stats accept arguments. Call to parametrize:

```python
H.nodes.degree(order=2)              # count only order-2 edges
H.nodes.degree(weight="w")           # weighted by edge attribute "w"
H.edges.order(degree=3)              # restrict to member-nodes of degree 3
```

Calling does NOT execute the computation. You still need `.asdict()` to
materialize values:

```python
H.nodes.degree(order=2).asdict()
```

### Filtering nodes or edges by a stat

```python
H.nodes.filterby("degree", 5)                       # degree == 5
H.nodes.filterby("degree", 5, mode="gt")            # > 5
H.nodes.filterby("degree", (2, 5), mode="between")  # 2 <= deg <= 5
H.edges.filterby("size", 4, mode="leq")             # size <= 4
```

Modes: `eq` (default), `neq`, `lt`, `gt`, `leq`, `geq`, `between`.

For arbitrary node attributes:

```python
H.nodes.filterby_attr("color", "red")
H.nodes.filterby_attr("age", 18, mode="geq")
```

### Multiple stats at once

```python
H.nodes.multi(["degree", "clustering_coefficient"]).aspandas()
```

Returns a DataFrame with one column per stat.

### Custom stats via decorator

```python
@xgi.nodestat_func
def my_stat(net, bunch):
    return {n: net.degree(n) ** 2 for n in bunch}

H.nodes.my_stat.asdict()                          # works
H.nodes.my_stat.max()                             # works
H.nodes.filterby("my_stat", 100, mode="gt")       # works
```

Same pattern with `edgestat_func`, `dinodestat_func`, `diedgestat_func`.

### Stats in drawing

Pass a stat object directly to `xgi.draw`; the library handles colormap
scaling automatically:

```python
xgi.draw(H, node_fc=H.nodes.degree, node_size=H.nodes.clustering_coefficient)
```

Do not precompute `.asdict()` for this.

### Discovering what stats exist

```python
[s for s in dir(H.nodes) if not s.startswith("_")]
[s for s in dir(H.edges) if not s.startswith("_")]
```

For the full reference of built-in stats and their algorithms, see the
[stats reference](https://xgi.readthedocs.io/en/stable/api/stats.html) and
the [stats cheat sheet](https://xgi.readthedocs.io/en/stable/stats_cheatsheet.html).

---

## Gotchas

Things that look like they should work but don't, or work differently than
you'd assume from NetworkX-like libraries.

### `H.edges[idx]` returns attributes, not members

```python
H = xgi.Hypergraph([[1, 2, 3], [3, 4]])
H.edges[0]              # {}   — empty attribute dict (NOT the members!)
H.edges.members(0)      # {1, 2, 3}   — the actual members of edge 0
```

Same applies to `H.nodes[n]`: it returns the node's attribute dict, not the
edges that node belongs to. For that, use `H.nodes.memberships(n)`.

### Stats live on the view, not the hypergraph

```python
H.degree              # function (proxy through __getattr__)
H.degree()            # dict, equivalent to H.nodes.degree.asdict()
H.degree(node)        # int — that node's degree
H.nodes.degree        # NodeStat object — the *idiomatic* form
H.nodes.degree.asdict()  # dict (most common)
H.nodes.degree[node]  # int — single node, via __getitem__
```

**Prefer `H.nodes.<stat>` and `H.edges.<stat>`** over the `H.<stat>()`
proxy. The proxy exists for convenience; the view-based form gives you the
full stats API for free.

### Only actual stats can flow through the proxy

The `H.<name>` proxy raises `AttributeError` for view methods that aren't
stats. So `H.filterby(...)`, `H.neighbors(...)`, `H.memberships(...)`,
`H.isolates(...)` etc. will not work. Always go through the view:
`H.nodes.filterby(...)`, `H.nodes.neighbors(...)`, etc.

### Output container types differ across view methods

| API | No-arg returns | With-id returns |
|---|---|---|
| `H.edges.members(e=None)` | **list** | set |
| `H.edges.members(e=None, dtype=dict)` | dict | dict |
| `H.nodes.memberships(n=None)` | dict | set |
| `H.nodes.neighbors(id)` | n/a (id required) | set |

Note `members()` defaults to a list, `memberships()` defaults to a dict.
If you want a uniform dict from members, pass `dtype=dict`.

### Random number generators

`seed` accepts `int`, `numpy.random.Generator`, or `None`:

- Same `int` reused across calls → identical outputs.
- Same `Generator` reused across calls → **different** outputs (state
  advances).
- Two fresh `np.random.default_rng(seed)` instances with the same seed →
  identical outputs.
- `seed=42` vs `seed=np.random.default_rng(42)` → **different** outputs
  (the conversion paths are unrelated).

This matches sklearn/scipy. See xgi's Randomness docs for more.

### Drawing: positions stored as a `pos` node attribute

```python
pos = xgi.barycenter_spring_layout(H, seed=1)
xgi.draw(H, pos=pos)                              # standard pattern

# If pos is stored as a node attribute:
H.set_node_attributes(pos, name="pos")
xgi.draw(H, pos=H.nodes.pos.asdict())             # via the pos stat accessor
```

### Deprecated I/O

```python
xgi.read_hif(path)            # use this
xgi.write_hif(H, path)        # use this
# xgi.readwrite.json.read_json — internal-only, do not call directly
```

### Class-specific differences

- `Hypergraph` allows multiedges and empty edges.
- `SimplicialComplex` enforces the closure property (subfaces auto-added)
  and disallows multi-simplices. It does NOT have `add_edge` /
  `remove_edge`; use `add_simplex` / `remove_simplex_id` etc. Calling the
  wrong method raises `XGIError` with a hint.
- `DiHypergraph` edges are `(tail, head)` pairs (ordered tuples or lists,
  NOT sets). Passing a set raises `TypeError`.

### Construction shortcuts (cross-class)

```python
xgi.Hypergraph(other_hypergraph)      # copy
xgi.Hypergraph(di_hypergraph)         # DiHypergraph -> Hypergraph (union of tail+head)
xgi.Hypergraph(simplicial_complex)    # SC -> Hypergraph
```

### Exception types

- `xgi.XGIError` — hypergraph-state violation (frozen network, duplicate
  IDs, etc.)
- `TypeError` — wrong argument type
- `ValueError` — right type, invalid value
- `xgi.IDNotFound` — looking up a node/edge id that doesn't exist
  (subclasses both `XGIError` and `KeyError`)

Don't catch `XGIError` to filter "any XGI-related problem"; many failures
now raise plain `TypeError` or `ValueError`.

---

## Idiomatic patterns

### Build → compute → visualize

```python
import xgi
import matplotlib.pyplot as plt

# Build
H = xgi.random_hypergraph(50, [0.1, 0.01], seed=1)

# Compute
print("Mean degree:", H.nodes.degree.mean())
print("Top-5 nodes by degree:", H.nodes.degree.argsort()[-5:][::-1])
top_nodes = H.nodes.filterby("degree", 10, mode="geq")

# Visualize, encoding stats directly
pos = xgi.barycenter_spring_layout(H, seed=1)
xgi.draw(H, pos=pos, node_fc=H.nodes.degree, node_size=H.nodes.degree)
plt.show()
```

### Storing and reusing layouts

```python
pos = xgi.barycenter_spring_layout(H, seed=1)
H.set_node_attributes(pos, name="pos")

# Later, retrieve through the pos stat accessor
xgi.draw(H, pos=H.nodes.pos.asdict())
```

Generators like `xgi.ring_lattice(..., with_positions=True)` store `pos`
automatically.

### Conversions

```python
xgi.to_hypergraph(data)            # universal: list, dict, DataFrame, matrix, ...
xgi.to_dihypergraph(data)
xgi.to_simplicial_complex(data)

# Pairwise projections
G = xgi.to_graph(H)                # networkx Graph (clique projection)
LG = xgi.to_line_graph(H)
B = xgi.to_bipartite_graph(H)

# I/O
xgi.write_hif(H, "out.hif")
H = xgi.read_hif("out.hif")
```

### Reproducibility with a single Generator

```python
import numpy as np
rng = np.random.default_rng(42)

H = xgi.random_hypergraph(50, [0.1, 0.01], seed=rng)
pos = xgi.barycenter_spring_layout(H, seed=rng)
# The whole pipeline is reproducible from one seed integer.
```

Remember: `Generator` state advances between calls (see Gotchas).

### Algorithms (top-level functions, take a hypergraph)

```python
xgi.is_connected(H)
xgi.connected_components(H)
xgi.largest_connected_hypergraph(H)
xgi.clustering_coefficient(H)        # also as H.nodes.clustering_coefficient
xgi.katz_centrality(H)               # also as H.nodes.katz_centrality
xgi.h_eigenvector_centrality(H)
xgi.simplicial_fraction(H)
xgi.shortest_path_length(H)
```

Most algorithms with per-node output also have a stat-interface mirror, so
they show up in `dir(H.nodes)` and tab completion. Prefer the stat
interface when you want filtering / aggregation / multi-stat composition;
prefer the top-level function when you just want the values.

### Linear algebra

```python
A = xgi.adjacency_matrix(H)
B = xgi.incidence_matrix(H)
L = xgi.laplacian(H)
W = xgi.clique_motif_matrix(H)
```

All accept `index=True` to also return id-to-index mappings.

### Inspecting and cleaning a hypergraph

```python
H.num_nodes, H.num_edges
H.cleanup(isolates=False, singletons=False, empties=False, multiedges=False,
          connected=True, relabel=True)
H.copy()
H == other_H
```

`cleanup()` defaults remove isolates, singletons, empties, and multiedges;
keep the largest connected component; and relabel to sequential integers.
Pass `True` for any flag to keep that thing.
