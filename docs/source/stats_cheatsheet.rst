Stats Cheat Sheet
=================

Quick reference for XGI's statistics interface.  For a full tutorial, see
:doc:`api/tutorials/focus_6`.

Accessing stats
---------------

Stats are accessed through the ``nodes`` and ``edges`` views:

.. code-block:: python

   import xgi
   H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])

   H.nodes.degree            # NodeStat object
   H.edges.order              # EdgeStat object

Output formats
--------------

Every stat object supports the same output methods:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Method
     - Returns
   * - ``.asdict()``
     - ``{id: value, ...}``
   * - ``.aslist()``
     - ``[value, ...]``
   * - ``.asnumpy()``
     - NumPy array
   * - ``.aspandas()``
     - Pandas Series

Summary statistics
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Description
   * - ``.max()``, ``.min()``
     - Maximum / minimum value
   * - ``.mean()``, ``.median()``, ``.mode()``
     - Central tendency
   * - ``.std()``, ``.var()``
     - Spread
   * - ``.sum()``
     - Total
   * - ``.moment(order, center)``
     - Statistical moments
   * - ``.argmax()``, ``.argmin()``
     - ID of the max / min
   * - ``.argsort(reverse)``
     - IDs sorted by value
   * - ``.unique(return_counts)``
     - Unique values
   * - ``.ashist(bins, density)``
     - Histogram as DataFrame

Available node statistics
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Stat
     - Example
   * - ``degree``
     - ``H.nodes.degree``
   * - ``average_neighbor_degree``
     - ``H.nodes.average_neighbor_degree``
   * - ``clustering_coefficient``
     - ``H.nodes.clustering_coefficient``
   * - ``local_clustering_coefficient``
     - ``H.nodes.local_clustering_coefficient``
   * - ``two_node_clustering_coefficient``
     - ``H.nodes.two_node_clustering_coefficient``
   * - ``clique_eigenvector_centrality``
     - ``H.nodes.clique_eigenvector_centrality``
   * - ``h_eigenvector_centrality``
     - ``H.nodes.h_eigenvector_centrality``
   * - ``z_eigenvector_centrality``
     - ``H.nodes.z_eigenvector_centrality``
   * - ``node_edge_centrality``
     - ``H.nodes.node_edge_centrality``
   * - ``katz_centrality``
     - ``H.nodes.katz_centrality``
   * - ``attrs``
     - ``H.nodes.attrs('color')``

Available edge statistics
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Stat
     - Example
   * - ``order``
     - ``H.edges.order``
   * - ``size``
     - ``H.edges.size``
   * - ``node_edge_centrality``
     - ``H.edges.node_edge_centrality``
   * - ``attrs``
     - ``H.edges.attrs('weight')``

Directed hypergraph statistics
------------------------------

**Nodes:** ``degree``, ``in_degree``, ``out_degree``

**Edges:** ``order``, ``size``, ``head_order``, ``head_size``, ``tail_order``, ``tail_size``

Passing arguments
-----------------

Some stats accept arguments. Call the stat to pass them:

.. code-block:: python

   H.nodes.degree              # all orders
   H.nodes.degree(order=2)     # only order-2 edges
   H.edges.order(degree=3)     # only nodes with degree 3

Filtering
---------

Filter nodes or edges by any statistic:

.. code-block:: python

   H.nodes.filterby('degree', 2)                      # degree == 2
   H.nodes.filterby('degree', 2, mode='gt')           # degree > 2
   H.nodes.filterby('degree', (2, 5), mode='between') # 2 <= degree <= 5
   H.edges.filterby('order', 1, mode='leq')           # order <= 1

Available modes: ``eq``, ``neq``, ``lt``, ``gt``, ``leq``, ``geq``, ``between``.

Filter by attributes:

.. code-block:: python

   H.nodes.filterby_attr('color', 'red')
   H.nodes.filterby_attr('age', 18, mode='geq')

Multiple statistics
-------------------

Combine multiple stats into a single DataFrame:

.. code-block:: python

   H.nodes.multi(['degree', 'clustering_coefficient']).aspandas()

Custom statistics
-----------------

Define your own stats with decorators:

.. code-block:: python

   @xgi.nodestat_func
   def my_stat(net, bunch):
       return {n: net.degree(n) ** 2 for n in bunch}

   H.nodes.my_stat.asdict()  # works like any built-in stat

Using stats with visualization
------------------------------

Pass stat objects directly to drawing functions:

.. code-block:: python

   xgi.draw(H, node_fc=H.nodes.degree, node_size=H.nodes.degree)
   xgi.draw(H, edge_fc=H.edges.order)
