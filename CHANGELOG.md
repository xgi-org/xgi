# Changelog

## v0.4.3
* `Hypergraph.has_edge` is now `IDView.lookup`, `Hypergraph.duplicate_edges` is now `IDView.duplicates`, and `utilities.convert_labels_to_integer` is now `function.convert_labels_to_integer` ([#150](https://github.com/ComplexGroupInteractions/xgi/pull/150)).
* Added some unit tests for the convert module, the function module, and the classic generators module. Fixed for minor bugs encountered while writing tests and added documentation to Read The Docs for the drawing module. ([#153](https://github.com/ComplexGroupInteractions/xgi/pull/153))
* Fixed a bug in `remove_node_from_edge()` ([#154](https://github.com/ComplexGroupInteractions/xgi/pull/154)).
* Implemented computation of moments for NodeStat and EdgeStat ([#155](https://github.com/ComplexGroupInteractions/xgi/pull/155)).
* Implemented weak and strong node removal as per issue [#167](https://github.com/ComplexGroupInteractions/xgi/issues/76) ([#156](https://github.com/ComplexGroupInteractions/xgi/pull/156)).
* Added a dynamics module and created a Kuramoto model synchronization function ([#159](https://github.com/ComplexGroupInteractions/xgi/pull/159)).
* Added a cleanup method that removes artifacts specified by the user: multi-edges, singletons, isolates. It also can convert all labels to consecutive integers ([#161](https://github.com/ComplexGroupInteractions/xgi/pull/161)).
* Modified the `duplicates()` method to not include the first instance of the node/edge in the list of duplicates ([#161](https://github.com/ComplexGroupInteractions/xgi/pull/161)).
* Converted all instances of edges to sets from lists in response to issue [#158](https://github.com/ComplexGroupInteractions/xgi/issues/158) ([#162](https://github.com/ComplexGroupInteractions/xgi/pull/162)).
* Added lambda function default arguments for $f$, $g$, $\varphi$, $\psi$ as defined by Tudisco and Higham. Default behavior is identical as before. Fixes [#132](https://github.com/ComplexGroupInteractions/xgi/issues/132) ([#165](https://github.com/ComplexGroupInteractions/xgi/pull/165)).
* Added `sum()` as a stats method ([#168](https://github.com/ComplexGroupInteractions/xgi/pull/168)).
* Added a benchmarking suite for the core hypergraph data structure using airspeed velocity ([#170](https://github.com/ComplexGroupInteractions/xgi/pull/170)).
* Fixed issue [#171](https://github.com/ComplexGroupInteractions/xgi/issues/171) ([#172](https://github.com/ComplexGroupInteractions/xgi/pull/172))

Contributors: @nwlandry, @leotrs, and @saad1282

## v0.4.2
* Keyword arguments are now consistent in the `draw()` function ([#148](https://github.com/ComplexGroupInteractions/xgi/pull/148)).
* Notebooks are now formatted with black and the requirements have been updated to reflect this ([#148](https://github.com/ComplexGroupInteractions/xgi/pull/148)).

Contributors: @nwlandry

## v0.4.1
* Added the ability to color nodes and edges in `xgi.draw()` by value, iterable, or NodeStat/EdgeStat ([#139](https://github.com/ComplexGroupInteractions/xgi/pull/139), [#142](https://github.com/ComplexGroupInteractions/xgi/pull/142), and [#143](https://github.com/ComplexGroupInteractions/xgi/pull/143)).
* Fixed the distortion of the node aspect ratio with different figure sizes in [Issue #137](https://github.com/ComplexGroupInteractions/xgi/issues/137).
* Moved the `isolates()` and `singletons()` method from the `Hypergraph` class to the `NodeView` and `EdgeView` classes respectively ([#146](https://github.com/ComplexGroupInteractions/xgi/pull/146)).
* Fixed `Hypergraph.copy()` to not use the `subhypergraph` method ([#145](https://github.com/ComplexGroupInteractions/xgi/pull/145)).
* `filterby()` now accepts `NodeStat` and `EdgeStat` objects instead of just strings ([#144](https://github.com/ComplexGroupInteractions/xgi/pull/144)).
* Removed edit-mode install to run the Github Actions test suite ([#136](https://github.com/ComplexGroupInteractions/xgi/pull/136)).
* Added unit tests ([#147](https://github.com/ComplexGroupInteractions/xgi/pull/147)).

Contributors: @nwlandry, @leotrs, and @maximelucas

## v0.4
* Added the `stats` package which implements `NodeStat`, `EdgeStat` and related functionality. This package now handles computation of edge size and degree ([#120](https://github.com/ComplexGroupInteractions/xgi/pull/120)).
* Removed the `EdgeSizeView` and `DegreeView` classes ([#120](https://github.com/ComplexGroupInteractions/xgi/pull/120)).
* Changed all imports to be relative in the `xgi` package ([#121](https://github.com/ComplexGroupInteractions/xgi/pull/121)).
* Added an assortativity module ([#122](https://github.com/ComplexGroupInteractions/xgi/pull/122)).
* Improved the performance of accessing edge members ([#124](https://github.com/ComplexGroupInteractions/xgi/pull/124)).
* Added more operations for node and edge attributes besides "eq" ([#125](https://github.com/ComplexGroupInteractions/xgi/pull/125)).
* Added a function to convert all node and edge labels to integers and store the old labels as properties ([#127](https://github.com/ComplexGroupInteractions/xgi/pull/127)).
* * Renamed the `egonet` method to `edge_neighborhood ([#129](https://github.com/ComplexGroupInteractions/xgi/pull/129)).
* Moved the `neighbors` method in the `Hypergraph` class to the `IDView` class so that node and edge neighbors are now supported (PR #129).
* Added a centrality module and added these methods to `nodestats.py` and `edgestats.py` ([#130](https://github.com/ComplexGroupInteractions/xgi/pull/130)).
* Moved the `load_xgi_data` method to the `readwrite` module ([#130](https://github.com/ComplexGroupInteractions/xgi/pull/130)).
* Added a generator for sunflower hypergraphs ([#130](https://github.com/ComplexGroupInteractions/xgi/pull/130)).
* Added a Jupyter notebook as a quickstart guide ([#131](https://github.com/ComplexGroupInteractions/xgi/pull/131) and [#134](https://github.com/ComplexGroupInteractions/xgi/pull/134)).
* Fixed a bug in the `barycenter_spring_layout` and `weighted_barycenter_spring_layout` methods to handle non-integer node IDs ([#133](https://github.com/ComplexGroupInteractions/xgi/pull/133)).
* Added an isort configuration file so it no longer sorts the `__init__.py` files ([#134](https://github.com/ComplexGroupInteractions/xgi/pull/134)).

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
