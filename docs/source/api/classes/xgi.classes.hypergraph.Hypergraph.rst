xgi.classes.hypergraph.Hypergraph
=================================

.. currentmodule:: xgi.classes.hypergraph

.. autoclass:: Hypergraph
   :show-inheritance:
   :members:


   .. rubric:: Attributes

   .. autosummary::

      ~Hypergraph.edges
      ~Hypergraph.nodes
      ~Hypergraph.num_edges
      ~Hypergraph.num_nodes


   .. rubric:: Methods that modify the structure

   .. autosummary::
      :nosignatures:

      ~Hypergraph.add_node
      ~Hypergraph.add_edge
      ~Hypergraph.add_nodes_from
      ~Hypergraph.add_edges_from
      ~Hypergraph.add_node_to_edge
      ~Hypergraph.add_weighted_edges_from
      ~Hypergraph.update
      ~Hypergraph.remove_node
      ~Hypergraph.remove_edge
      ~Hypergraph.remove_nodes_from
      ~Hypergraph.remove_nodes_from
      ~Hypergraph.remove_edges_from
      ~Hypergraph.remove_node_from_edge
      ~Hypergraph.remove_isolates
      ~Hypergraph.remove_singleton_edges
      ~Hypergraph.clear
      ~Hypergraph.clear_edges


   .. rubric:: Methods that return other hypergraphs

   .. autosummary::
      :nosignatures:

      ~Hypergraph.copy
      ~Hypergraph.dual


   .. rubric:: Methods that query nodes and edges

   .. autosummary::
      :nosignatures:

      ~Hypergraph.isolates
      ~Hypergraph.duplicate_edges
      ~Hypergraph.has_edge
      ~Hypergraph.singleton_edges
