xgi.core.hypergraph.Hypergraph
==============================

.. currentmodule:: xgi.core.hypergraph

.. autoclass:: Hypergraph
   :show-inheritance:
   :members:


   .. rubric:: Attributes

   .. autosummary::

      ~Hypergraph.edges
      ~Hypergraph.nodes
      ~Hypergraph.num_edges
      ~Hypergraph.num_nodes
      ~Hypergraph.is_frozen


   .. rubric:: Methods that modify the structure

   .. autosummary::
      :nosignatures:

      ~Hypergraph.add_node
      ~Hypergraph.add_edge
      ~Hypergraph.add_nodes_from
      ~Hypergraph.add_edges_from
      ~Hypergraph.add_node_to_edge
      ~Hypergraph.add_weighted_edges_from
      ~Hypergraph.set_node_attributes
      ~Hypergraph.set_edge_attributes
      ~Hypergraph.update
      ~Hypergraph.remove_node
      ~Hypergraph.remove_edge
      ~Hypergraph.remove_nodes_from
      ~Hypergraph.remove_edges_from
      ~Hypergraph.remove_node_from_edge
      ~Hypergraph.clear
      ~Hypergraph.clear_edges
      ~Hypergraph.merge_duplicate_edges
      ~Hypergraph.cleanup
      ~Hypergraph.freeze
      ~Hypergraph.double_edge_swap
      ~Hypergraph.random_edge_shuffle


   .. rubric:: Methods that return other hypergraphs

   .. autosummary::
      :nosignatures:

      ~Hypergraph.copy
      ~Hypergraph.dual