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

XGI-DATA uses an HTTP request to load the hypergraph dataset.


Network Statistics
------------------

.. raw:: html

   <style>
   
   </style>
   
   <script type="text/javascript">
      display_table()
   </script>

   <p>More details on individual datasets are available at the <a href="https://github.com/xgi-org/xgi-data">XGI-DATA page</a>