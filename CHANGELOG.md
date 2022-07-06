# Changelog

## v0.4
* Added the `stats` package which implements `NodeStat`, `EdgeStat` and related functionality. This package now handles computation of edge size and degree (PR #120).
* Removed the `EdgeSizeView` and `DegreeView` classes (PR #120).
* Changed all imports to be relative in the `xgi` package (PR #121).
* Added an assortativity module (PR #122).
* Improved the performance of accessing edge members (PR #124).
* Added more operations for node and edge attributes besides "eq" (PR #125).
* Added a function to convert all node and edge labels to integers and store the old labels as properties (PR #127).
* * Renamed the `egonet` method to `edge_neighborhood (PR #129).
* Moved the `neighbors` method in the `Hypergraph` class to the `IDView` class so that node and edge neighbors are now supported (PR #129).
* Added a centrality module and added these methods to `nodestats.py` and `edgestats.py` (PR #130).
* Moved the `load_xgi_data` method to the `readwrite` module (PR #130).
* Added a generator for sunflower hypergraphs (PR #130).
* Added a Jupyter notebook as a quickstart guide (PRs #131, #134).
* Fixed a bug in the `barycenter_spring_layout` and `weighted_barycenter_spring_layout` methods to handle non-integer node IDs (PR #133).
* Added an isort configuration file so it no longer sorts the `__init__.py` files (PR #134).

Contributors: @leotrs, @nwlandry, and @iaciac

## v0.3.1
* Refactored the subhypergraph methods
* Moved functions not related to the core Hypergraph data structure to functions.py
* Removed unnecessary duplicated functions (`n_bunch_iter`, `get_edge_data`, and `has_node`)
* Refactored the `members()` method as well as the `NodeView` and `EdgeView` classes for significant speedup.
* Github Actions now tests the docstrings and tutorial notebooks
* The `add_edges_from` method now supports different input formats.
* Fixed various bugs in the generative models module.
* A method for double edge swaps is now implemented.

Contributors: @leotrs and @nwlandry

## v0.3
* Added the ability to convert to and from a NetworkX bipartite graph.
* Removed the `shape` property from `Hypergraph` and renamed the `number_of_nodes()` and `number_of_edges()` methods to the `num_nodes` and `num_edges` properties, respectively.
* Added random seed decorator as in NetworkX.
* Added a `SimplicialComplex` class.
* Added order and weighted arguments to the `incidence_matrix` and `adjacency_matrix functions`.
* Added an `intersection_profile` function.
* Added a `laplacian` function with argument `order` and a `multiorder_laplacian` function.
* Fix: Return an empty array rather than a 1x1 zero array when appropriate.
* Fix: Ensured that the incidence matrix is always has dimensions num_nodes x num_edges.
* Added 2 generators of random (maximal) simplicial complexes, and toy star-clique generator
* Extensively rewrote the documentation, updating the content and format on Read The Docs.
* Added an egonet function to get the edges neighboring a specified node.
* Added functions to visualize hypergraphs and simplicial complexes.
* Added the ability to get nodes and edges of given degrees/sizes respectively.
* Extended the `members()` function to be able to get different data types and to either get a single edge or all edges.
* Added the `load_xgi_data` function to load datasets from the xgi-data repository.
* Added two additional tutorials: a tutorial on visualizing higher-order networks and a case study replicating a recent paper.
* Changed the API of `degree_histogram` and added `degree_counts` based on #23.
* Refactored the `IDDegreeView` class and changed the API. Added the ability to specify `order` and the datatype.
* Added an abstract class `IDDict` to handle data validation.

Contributors: @iaciac, @leotrs, @lordgrilo, @maximelucas, @nwlandry, and @tlarock

## v0.2
* `H[attr]` now accesses hypergraph attributes
* `H.nodes[id]` now accesses attributes, not bipartite neighbors
* Removed the`__call__()` functionality from `H.nodes` and `H.edges`
* `H.nodes.memberships(id)` and `H.edges.members(id)` now access the bipartite neighbors
* Created base classes for the Node/Edge Views and Degree/Edge Size Views to inherit from.
* Removed the NodeDataView and EdgeDataView.
* Updated the list of developers
* `__getitem__()` in the NodeView and EdgeView are now in a try-except block for greater efficiency.
* Removed the name attribute and fixed methods and tests to match.
* Fixed the `erdos_renyi_hypergraph()`, `chung_lu_hypergraph()`, and `dcsbm_hypergraph()` methods such that the number of nodes will always match the number the user specifies, even if the resulting hypergraph is disconnected.
* Changed the construction method from reading in a Pandas DataFrame to using the `add_node_to_edge()` method for a 2x speedup.
* Added some basic unit tests for the generative models.
* Added the dual keyword for the read_bipartite_edgelist() method.
* Added small functions to the Hypergraph class
* Added generator of random hypergraph
* Added functions for finding and removing isolates
* Refactored the `has_edge()` method in the Hypergraph class.

Contributors: @leotrs, @maximelucas, and @nwlandry
