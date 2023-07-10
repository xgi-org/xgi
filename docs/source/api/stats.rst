#############
stats package
#############

.. automodule:: xgi.stats

.. admonition:: Available statistics
   
   The available statistics are:

   ---------------
   Hypergraphs and simplicial complexes
   ---------------

   .. rubric:: Statistics of nodes

   .. autosummary::
      :nosignatures:
      
      ~xgi.stats.nodestats.average_neighbor_degree
      ~xgi.stats.nodestats.clique_eigenvector_centrality
      ~xgi.stats.nodestats.clustering_coefficient
      ~xgi.stats.nodestats.degree
      ~xgi.stats.nodestats.eigenvector_centrality
      ~xgi.stats.nodestats.local_clustering_coefficient
      ~xgi.stats.nodestats.node_edge_centrality
      ~xgi.stats.nodestats.two_nodes_clustering_coefficient

   .. rubric:: Statistics of edges

   .. autosummary::
      :nosignatures:

      ~xgi.stats.edgestats.order
      ~xgi.stats.edgestats.size
      ~xgi.stats.edgestats.node_edge_centrality

   .. rubric:: Corresponding modules

   .. autosummary::
      :toctree: stats

      ~xgi.stats.nodestats
      ~xgi.stats.edgestats

   .. rubric:: Corresponding classes

   .. autosummary::
      :toctree: stats
      :nosignatures:

      ~xgi.stats.NodeStat
      ~xgi.stats.EdgeStat
      ~xgi.stats.DiNodeStat
      ~xgi.stats.DiEdgeStat
      ~xgi.stats.MultiNodeStat
      ~xgi.stats.MultiEdgeStat
      ~xgi.stats.MultiDiNodeStat
      ~xgi.stats.MultiDiEdgeStat

   ---------------
   Directed hypergraphs
   ---------------
   

   .. rubric:: Statistics of nodes in directed hypergraphs

   .. autosummary::
      :nosignatures:

      ~xgi.stats.dinodestats.degree
      ~xgi.stats.dinodestats.in_degree
      ~xgi.stats.dinodestats.out_degree

   .. rubric:: Statistics of edges in directed hypergraphs

   .. autosummary::
      :nosignatures:

      ~xgi.stats.diedgestats.order
      ~xgi.stats.diedgestats.size
      ~xgi.stats.diedgestats.head_order
      ~xgi.stats.diedgestats.head_size
      ~xgi.stats.diedgestats.tail_order
      ~xgi.stats.diedgestats.tail_size

.. rubric:: Modules

.. autosummary::
   :toctree: stats

   ~xgi.stats.nodestats
   ~xgi.stats.edgestats
   ~xgi.stats.dinodestats
   ~xgi.stats.diedgestats


.. rubric:: Classes

.. autosummary::
   :toctree: stats
   :nosignatures:

   ~xgi.stats.NodeStat
   ~xgi.stats.EdgeStat
   ~xgi.stats.DiNodeStat
   ~xgi.stats.DiEdgeStat
   ~xgi.stats.MultiNodeStat
   ~xgi.stats.MultiEdgeStat
   ~xgi.stats.MultiDiNodeStat
   ~xgi.stats.MultiDiEdgeStat


.. rubric:: Decorators

.. autosummary::
   :toctree: stats
   :nosignatures:

   ~xgi.stats.nodestat_func
   ~xgi.stats.edgestat_func
   ~xgi.stats.dinodestat_func
   ~xgi.stats.diedgestat_func
