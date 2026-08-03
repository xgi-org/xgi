Dynamics on higher-order networks
=================================

XGI does not itself provide solvers for dynamical processes on higher-order
networks. The scope was minimal (a few Kuramoto helpers) and the value was
low compared to keeping the core library tight. Instead, we recommend using
one of the maintained companion packages below, all of which either build on
XGI directly or interoperate with it via standard formats.

Contagion / spreading
---------------------

`hypercontagion <https://github.com/nwlandry/hypercontagion>`_
   SIR, SIS, and other epidemic models on hypergraphs. Interoperates with
   XGI hypergraph objects.

Synchronization (Kuramoto, oscillators)
---------------------------------------

`hypersynchronization <https://github.com/maximelucas/hypersynchronization>`_
   Kuramoto-type synchronization models on hypergraphs, including the
   two-body / three-body coupling explored in
   `Adhikari, Restrepo, and Skardal (2023) <https://doi.org/10.48550/arXiv.2208.00909>`_.

`simplicial-kuramoto <https://github.com/arnaudon/simplicial-kuramoto>`_
   Simplicial Kuramoto model on oriented simplicial complexes, from
   `Millán, Torres, and Bianconi (2020) <https://doi.org/10.1103/PhysRevLett.124.218301>`_
   and the Hodge-Sakaguchi framework of
   `Arnaudon, Peach, Petri, and Expert (2022) <https://doi.org/10.1038/s42005-022-00963-7>`_.

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
