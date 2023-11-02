#############
stats package
#############

.. automodule:: xgi.stats

.. admonition:: Available statistics
   
   .. rubric:: Hypergraphs and simplicial complexes

   *Statistics of nodes*

   .. autosummary::
      :nosignatures:
      
      ~xgi.stats.nodestats.average_neighbor_degree
      ~xgi.stats.nodestats.clique_eigenvector_centrality
      ~xgi.stats.nodestats.clustering_coefficient
      ~xgi.stats.nodestats.degree
      ~xgi.stats.nodestats.h_eigenvector_centrality
      ~xgi.stats.nodestats.local_clustering_coefficient
      ~xgi.stats.nodestats.node_edge_centrality
      ~xgi.stats.nodestats.two_node_clustering_coefficient

   *Statistics of edges*

   .. autosummary::
      :nosignatures:

      ~xgi.stats.edgestats.order
      ~xgi.stats.edgestats.size
      ~xgi.stats.edgestats.node_edge_centrality

   *Corresponding decorators*

   .. autosummary::
      :toctree: stats
      :nosignatures:

      ~xgi.stats.nodestat_func
      ~xgi.stats.edgestat_func

   *Corresponding modules*

   .. autosummary::
      :toctree: stats

      ~xgi.stats.nodestats
      ~xgi.stats.edgestats

   *Corresponding classes*

   .. autosummary::
      :toctree: stats
      :nosignatures:

      ~xgi.stats.NodeStat
      ~xgi.stats.EdgeStat
      ~xgi.stats.MultiNodeStat
      ~xgi.stats.MultiEdgeStat

   .. rubric:: Directed hypergraphs
   

   *Statistics of nodes*

   .. autosummary::
      :nosignatures:

      ~xgi.stats.dinodestats.degree
      ~xgi.stats.dinodestats.in_degree
      ~xgi.stats.dinodestats.out_degree

   *Statistics of edges*

   .. autosummary::
      :nosignatures:

      ~xgi.stats.diedgestats.order
      ~xgi.stats.diedgestats.size
      ~xgi.stats.diedgestats.head_order
      ~xgi.stats.diedgestats.head_size
      ~xgi.stats.diedgestats.tail_order
      ~xgi.stats.diedgestats.tail_size

   *Corresponding decorators*

   .. autosummary::
      :toctree: stats
      :nosignatures:

      ~xgi.stats.dinodestat_func
      ~xgi.stats.diedgestat_func

   *Corresponding modules*

   .. autosummary::
      :toctree: stats

      ~xgi.stats.dinodestats
      ~xgi.stats.diedgestats


   *Corresponding classes*

   .. autosummary::
      :toctree: stats
      :nosignatures:

      ~xgi.stats.DiNodeStat
      ~xgi.stats.DiEdgeStat
      ~xgi.stats.MultiDiNodeStat
      ~xgi.stats.MultiDiEdgeStat
