xgi.drawing.draw
================

.. currentmodule:: xgi.drawing.draw

.. automodule:: xgi.drawing.draw
   
   .. rubric:: Functions

.. note::
   
   **Node Label Sizing**: The :func:`draw` function does not currently support 
   customizing the size of node labels. Node labels are drawn with default sizing.
   
   If you need to customize node label properties (including size), you can draw 
   the hypergraph elements separately using :func:`draw_nodes` and then use 
   :func:`draw_node_labels` with custom matplotlib text properties. Alternatively, 
   you can use matplotlib's text manipulation functions directly on the drawn labels.

   
   .. autofunction:: draw
   .. autofunction:: draw_bipartite
   .. autofunction:: draw_multilayer
   .. autofunction:: draw_nodes
   .. autofunction:: draw_hyperedges
   .. autofunction:: draw_undirected_dyads
   .. autofunction:: draw_directed_dyads
   .. autofunction:: draw_simplices
   .. autofunction:: draw_node_labels
   .. autofunction:: draw_hyperedge_labels
