********
XGI-DATA
********

XGI-DATA is a repository of openly available hypergraph datasets in JSON format with corresponding documentation of network statistics, limitations of the data, and methods of collection. They are hosted in the `XGI Community <https://zenodo.org/communities/xgi>`_ on Zenodo. This is loosely inspired by `Datasheets for Datasets <https://arxiv.org/abs/1803.09010>`_ by Gebru et al.

Loading datasets
----------------

Loading a dataset using XGI is as simple as the following two lines:

.. code-block:: python

   import xgi
   H = xgi.load_xgi_data("<dataset_name>")

XGI-DATA uses an HTTP request to load the hypergraph dataset. See the `load_xgi_data() documentation  <api/readwrite/xgi.readwrite.xgi_data.html>`_ for a complete description of the function.

The directed hypergraph datasets from the Biochemical, Genetic and Genomic (BIGG) database can also be loaded with:


.. code-block:: python

   import xgi
   H = xgi.load_bigg_data("<dataset_name>")  


See the `load_bigg_data() documentation <api/readwrite/xgi.readwrite.bigg_data.html>`_ for a complete description of the function.

Dataset format
--------------

The xgi-data format for higher-order datasets is a JSON data structure with the following structure:

* :code:`hypergraph-data`: This tag accesses the attributes of the entire hypergraph dataset such as the authors or dataset name.

* :code:`node-data`: This tag accesses the nodes of the hypergraph and their associated properties as a dictionary where the keys are node IDs and the corresponding values are dictionaries. If a node doesn't have any properties, the associated dictionary is empty.

  * :code:`name`: This tag accesses the node's name if there is one that is different from the ID specified in the hyperedges.
  * Other tags are user-specified based on the particular attributes provided by the dataset.

* :code:`edge-data`: This tag accesses the hyperedges of the hypergraph and their associated attributes.

  * :code:`name`: This tag accesses the edge's name if one is provided.
  * :code:`timestamp`: This is the tag specifying the time associated with the hyperedge if it is given. All times are stored in ISO8601 standard.
  * Other tags are user-specified based on the particular attributes provided by the dataset.

* :code:`edge-dict`: This tag accesses the edge IDs and the corresponding nodes which participate in that hyperedge.


Network Statistics
------------------

.. raw:: html

   <script type="text/javascript">
      display_table()
   </script>

   <p>More details on individual datasets are available at the <a href="https://github.com/xgi-org/xgi-data">XGI-DATA page</a>.</p>

   <p>In this table, |V| denotes the number of nodes, |E| denotes the number of edges, |E<sup>*</sup>| denotes the number of unique edges, and s<sub>max</sub> denotes the maximum edge size.</p>