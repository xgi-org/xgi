********
XGI-DATA
********

XGI-DATA is a repository of openly available hypergraph datasets in JSON format with corresponding documentation of network statistics, limitations of the data, and methods of collection. They are hosted in the `XGI Community <https://zenodo.org/communities/xgi>`_ on Zenodo. This is loosely inspired by `Datasheets for Datasets <https://arxiv.org/abs/1803.09010>`_ by Gebru et al.

Dataset format
--------------

The xgi-data format for higher-order datasets is a JSON data structure with the following structure:

* "hypergraph-data": This tag accesses the attributes of the entire hypergraph dataset such as the authors or dataset name.

* "node-data": This tag accesses the nodes of the hypergraph and their associated properties as a dictionary where the keys are node IDs and the corresponding values are dictionaries. If a node doesn't have any properties, the associated dictionary is empty.

  * "name": This tag accesses the node's name if there is one that is different from the ID specified in the hyperedges.
  * Other tags are user-specified based on the particular attributes provided by the dataset.

* "edge-data": This tag accesses the hyperedges of the hypergraph and their associated attributes.

  * "name": This tag accesses the edge's name if one is provided.
  * "timestamp": This is the tag specifying the time associated with the hyperedge if it is given. All times are stored in ISO8601 standard.
  * Other tags are user-specified based on the particular attributes provided by the dataset.

* "edge-dict": This tag accesses the edge IDs and the corresponding nodes which participate in that hyperedge.

Loading datasets
----------------

Loading a dataset using XGI is as simple as the following two lines:

.. code-block:: python

   import xgi
   H = xgi.load_xgi_data("<dataset_name>")

XGI-DATA uses an HTTP request to load the hypergraph dataset.


Network Statistics
------------------

.. raw:: html

   <style>
   
   </style>
   
   <script type="text/javascript">
      display_table()
   </script>

   <p>More details on individual datasets are available at the <a href="https://github.com/xgi-org/xgi-data">XGI-DATA page</a>.</p>