xgi.classes.simplicialcomplex.SimplicialComplex
===============================================

.. currentmodule:: xgi.classes.simplicialcomplex

.. autoclass:: SimplicialComplex
   :show-inheritance:
   :members:

   
   .. rubric:: Attributes

   .. autosummary::
      
      ~SimplicialComplex.edges
      ~SimplicialComplex.nodes
      ~SimplicialComplex.num_edges
      ~SimplicialComplex.num_nodes
   

   .. rubric:: Methods that modify the structure

   .. autosummary::
      :nosignatures:

      ~SimplicialComplex.add_simplex
      ~SimplicialComplex.add_simplices_from
      ~SimplicialComplex.add_weighted_simplices_from
      ~SimplicialComplex.remove_simplex_id
      ~SimplicialComplex.remove_simplex_ids_from
      ~SimplicialComplex.close

   .. rubric:: Methods that query nodes and edges

   .. autosummary::
      :nosignatures:

      ~SimplicialComplex.has_simplex


   .. rubric:: Inherited methods that cannot be used

   .. autosummary::
      :nosignatures:
      
      ~SimplicialComplex.add_edge
      ~SimplicialComplex.add_edges_from
      ~SimplicialComplex.add_weighted_edges_from
      ~SimplicialComplex.remove_edge
      ~SimplicialComplex.remove_edges_from
      