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

# Generative Models

The `generators` module provides functionality to generate common models of hypergraphs, both non-uniform and uniform.

```{code-cell} ipython3
import xgi
import numpy as np
import random
```

### Uniform configuration model

```{code-cell} ipython3
n = 1000
m = 3
k = {i: random.randint(10, 30) for i in range(n)}
H = xgi.uniform_hypergraph_configuration_model(k, m)
```

### Erdős–Rényi model

```{code-cell} ipython3
n = 1000
ps = [0.01, 0.001]
H = xgi.random_hypergraph(n, ps)
```

### Non-uniform configuration model

```{code-cell} ipython3
n = 1000
k1 = {i : random.randint(10, 30) for i in range(n)}
k2 = {i : sorted(k1.values())[i] for i in range(n)}
H = xgi.chung_lu_hypergraph(k1, k2)
```

### Non-uniform DCSBM hypergraph

```{code-cell} ipython3
n = 1000
k1 = {i : random.randint(1, 100) for i in range(n)}
k2 = {i : sorted(k1.values())[i] for i in range(n)}
g1 = {i : random.choice([0, 1]) for i in range(n)}
g2 = {i : random.choice([0, 1]) for i in range(n)}
omega = np.array([[100, 10], [10, 100]])
H = xgi.dcsbm_hypergraph(k1, k2, g1, g2, omega)
```
