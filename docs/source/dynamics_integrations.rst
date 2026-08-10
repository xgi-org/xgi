:orphan:

Dynamics on higher-order networks
=================================

XGI does not itself provide solvers for dynamical processes on higher-order
networks. Instead, we recommend using one of the maintained companion
packages below, all of which either build on XGI directly or interoperate
with it via standard formats.

Contagion / spreading
---------------------

`hypercontagion <https://github.com/nwlandry/hypercontagion>`_
   SIR, SIS, and other epidemic models.

Synchronization (Kuramoto, oscillators)
---------------------------------------

`hypersynchronization <https://github.com/maximelucas/hypersynchronization>`_
   Kuramoto-type synchronization dynamics on hypergraphs, where oscillators
   are associated with nodes. See
   `Skardal and Skardal (2019) <https://doi.org/10.1103/PhysRevLett.122.248301>`_
   for an example model, or
   `Battiston et al. (2026) <https://doi.org/10.1038/s42254-025-00916-3>`_
   for a review.

`simplicial-kuramoto <https://github.com/arnaudon/simplicial-kuramoto>`_
   Simplicial Kuramoto dynamics on simplicial complexes, where oscillators
   are associated with simplices rather than just nodes. See
   `Millán, Torres, and Bianconi (2020) <https://doi.org/10.1103/PhysRevLett.124.218301>`_
   and
   `Arnaudon, Peach, Petri, and Expert (2022) <https://doi.org/10.1038/s42005-022-00963-7>`_
   for example models, and
   `Nurisso et al. (2024) <https://doi.org/10.1016/j.chaos.2024.115198>`_
   for a review.

Contributing
------------

If you maintain a dynamics package that works well with XGI and you'd like
it listed here, open an issue or a pull request adding it to this page.

Historical note
---------------

Earlier versions of XGI (up to 0.10.x) exposed a ``xgi.dynamics`` submodule
containing four functions: ``simulate_kuramoto``,
``compute_kuramoto_order_parameter``, ``simulate_simplicial_kuramoto``, and
``compute_simplicial_order_parameter``. These were removed in v1.0 in
favor of the companion packages listed above.
