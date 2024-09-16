**************
API Reference
**************

This page gives an overview of all public XGI objects, functions and methods. All classes and functions are exposed in xgi.* namespace are public

XGI is organized into the following subpackages:

* ``xgi.algorithms``: Function to compute classic algorightms on higher-order networks
* ``xgi.convert``:  Functions to convert between different representations of the data
* ``xgi.core``: Classes for the core datastructures and views
* ``xgi.drawing``:  Functions for plotting
* ``xgi.dynamics``: Functions to simulate given dynamical processes
* ``xgi.generators``: Functions to generate higher-order networks from models
* ``xgi.linalg``: Functions to compute matrix and tensors representations
* ``xgi.readwrite``:  Functions to load and store higher-order networks in standard formats
* ``xgi.stats``:  Functions to compute node and edge statistics in a single interface
* ``xgi.utils``: Small utility functions


.. note::

   .. only:: stable_version

      This page describes release |version| of XGI. Find out more about this release and previous releases in the `release notes <https://github.com/xgi-org/xgi/releases>`_.
      
   .. only:: dev_version
      
      This page describes the latest XGI development with features that may not be released yet. To see officially released features, visit the `API reference <https://xgi.readthedocs.io/en/stable/api_reference.html>`_ for the most recent stable version.

.. toctree::
   :maxdepth: 2

   Algorithms <api/algorithms.rst>
   Convert <api/convert.rst>
   Core functionality <api/core.rst>
   Drawing <api/drawing.rst>
   Dynamics <api/dynamics.rst>
   Generators <api/generators.rst>
   Linear Algebra <api/linalg.rst>
   I/O <api/readwrite.rst>
   Stats for nodes and edges <api/stats.rst>
   Utilities <api/utils.rst>
