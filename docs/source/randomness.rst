Randomness and reproducibility
==============================

Most stochastic functions in XGI accept a ``seed`` argument so that results can
be made reproducible. This page documents what to pass and what to expect.

Accepted types for ``seed``
---------------------------

XGI accepts three kinds of values:

- ``None`` (default): a fresh, non-deterministic random state is used.
- ``int``: a deterministic seed. Each call seeded with the same integer
  produces identical output.
- ``numpy.random.Generator``: the modern NumPy random API. The ``Generator``
  carries state and advances it as randomness is consumed.

This mirrors the conventions used by NumPy, SciPy, and scikit-learn.

Semantics
---------

The four cases worth pinning down explicitly:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Pattern
     - Result
   * - Same ``int`` seed reused across calls
     - Identical outputs
   * - Single ``Generator`` reused across calls
     - **Different** outputs (state advances)
   * - Two fresh ``np.random.default_rng(seed)`` instances with the same ``seed``
     - Identical outputs
   * - ``seed=42`` vs ``seed=np.random.default_rng(42)``
     - **Different** outputs (the conversion paths are unrelated)

The last case sometimes surprises users: passing ``42`` and passing a
``Generator`` constructed *from* ``42`` are not equivalent. The Generator has
its own internal state derived from the seed via a SeedSequence, and reading
from it produces a different first integer than ``42`` itself.

Examples
--------

Reusing a single ``Generator`` — state advances:

.. code-block:: python

    import xgi
    import numpy as np

    H = xgi.random_hypergraph(20, [0.15, 0.01], seed=42)
    rng = np.random.default_rng(42)

    pos_a = xgi.barycenter_spring_layout(H, seed=rng)
    pos_b = xgi.barycenter_spring_layout(H, seed=rng)
    # pos_a != pos_b — rng advanced between calls

Fresh ``Generator`` from the same seed — identical outputs:

.. code-block:: python

    pos_a = xgi.barycenter_spring_layout(H, seed=np.random.default_rng(42))
    pos_b = xgi.barycenter_spring_layout(H, seed=np.random.default_rng(42))
    # pos_a == pos_b

Same ``int`` seed reused — identical outputs:

.. code-block:: python

    pos_a = xgi.barycenter_spring_layout(H, seed=42)
    pos_b = xgi.barycenter_spring_layout(H, seed=42)
    # pos_a == pos_b

Why use a ``Generator``
-----------------------

Passing a single ``Generator`` to several calls is useful when you want each
call to draw from a different part of the same random stream. This is the
recommended pattern for any pipeline that performs multiple stochastic steps:
the whole pipeline becomes reproducible from a single integer seed, but each
step still gets independent randomness.

.. code-block:: python

    rng = np.random.default_rng(42)
    H = xgi.random_hypergraph(20, [0.15, 0.01], seed=rng)
    pos = xgi.barycenter_spring_layout(H, seed=rng)
    swapped = xgi.node_swap(H, 1, 2)  # purely deterministic, no seed needed
    # everything above is reproducible by re-running with the same starting seed

NumPy reference
---------------

For deeper background on NumPy's modern random API, see the upstream
documentation:

- `NumPy: Random sampling <https://numpy.org/doc/stable/reference/random/index.html>`_
- `NumPy: Generator <https://numpy.org/doc/stable/reference/random/generator.html>`_
- `NumPy: SeedSequence <https://numpy.org/doc/stable/reference/random/bit_generators/generated/numpy.random.SeedSequence.html>`_
