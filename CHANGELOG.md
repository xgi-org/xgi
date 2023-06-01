# Changelog


## latest

* Added Katz-centrality algorithm (`katz_centrality`) [#366](https://github.com/xgi-org/xgi/issues/366) (@acombretrenouard).

## v0.6

* Added new drawing layouts (`circular_layout`, `spiral_layout`, and `barycenter_kamada_kawai_layout`) [#360](https://github.com/xgi-org/xgi/pull/360) (@thomasrobiglio).

## v0.5.8
* Formatted the codebase with ruff [#346](https://github.com/xgi-org/xgi/pull/346) (@leotrs).
* Improved the performance of `flag_complex` and `random_flag_complex` [#355](https://github.com/xgi-org/xgi/pull/355) (@maximelucas).
* Moved the `IDDict` class to utilities and removed unnecessary arguments in the `IDView` constructor [#353](https://github.com/xgi-org/xgi/pull/353) (@nwlandry).
* Up-versioned sphinx to v6.xxx and up-versioned sphinx-rtd-theme to >= 1.2 to be compatible with Sphinx v6.xxx. Updated the contribution guide and the GH, PyPI, and RTD landing pages [#350](https://github.com/xgi-org/xgi/pull/350) (@nwlandry).
* Fixed a bug in the double edge swap method [#349](https://github.com/xgi-org/xgi/pull/349) (@nwlandry)
* Updated the convert module methods to be able to return a hypergraph, addressing Issue [#327](https://github.com/xgi-org/xgi/issues/327). Now the conversion from a simplicial complex to a hypergraph only includes maximal faces [#345](https://github.com/xgi-org/xgi/pull/345) (@thomasrobiglio)
* Place a ceiling on IPython so that it is Python 3.8 compatible [#344](https://github.com/xgi-org/xgi/pull/344) (@nwlandry).
* Started fixing the cross references in the "See Also" section in the function/class docstrings [#343](https://github.com/xgi-org/xgi/pull/343) (@nwlandry).
* Feature: added complete_hypergraph [#337](https://github.com/xgi-org/xgi/pull/337) (@maximelucas).
* Updated the quickstart notebook [#338](https://github.com/xgi-org/xgi/pull/338) (@nwlandry).
* Added `strict` keyword to the `maximal()` method [#332](https://github.com/xgi-org/xgi/pull/332) (@nwlandry).
* Feature: added trivial hypergraph [#335](https://github.com/xgi-org/xgi/pull/335) (@maximelucas).

## v0.5.7
* Changed the organization name to `xgi-org` and removed `codecov` from the test requirements file [#334](https://github.com/xgi-org/xgi/pull/334) (@nwlandry).
* Fix: improved the `degree_counts` documentation [#329](https://github.com/xgi-org/xgi/pull/329) (@maximelucas).
* Added the `maximal()` method to EdgeView, removed the `maximal_simplices()` method, and removed a bug from the `duplicates()` method [#324](https://github.com/xgi-org/xgi/pull/324) (@nwlandry).
* Fix: documented max_order in `add_simplices_from()` [#328](https://github.com/xgi-org/xgi/pull/328) (@maximelucas).
* Restructured folder for the generators and linalg modules [#321](https://github.com/xgi-org/xgi/pull/321) (@maximelucas).
* Added 3 clustering coefficient definitions to the `algorithms` module as well as to NodeStats [#316](https://github.com/xgi-org/xgi/pull/316) (@nwlandry).
* Added the ability to choose whether to output the index-to-ID mappings from `to_bipartite_graph()` method. Fixes #322 [#323](https://github.com/xgi-org/xgi/pull/323) (@leotrs).
* Added the ability to draw hypergraphs with hyperedges as convex hulls [#320](https://github.com/xgi-org/xgi/pull/320) (@thomasrobiglio).


## v0.5.6
* Renamed `convert_to_line_graph()` to `to_line_graph()`, added an `s` parameter to the function, and added corresponding unit tests [#318](https://github.com/xgi-org/xgi/pull/318) (@nwlandry).
* Made the sparse warning in the `adjacency_matrix()` function more intelligible [#315](https://github.com/xgi-org/xgi/pull/315) (@nwlandry).
* Added a function for the normalized hypergraph laplacian [#314](https://github.com/xgi-org/xgi/pull/314) (@nwlandry).
* Added tests for draw functions [#312](https://github.com/xgi-org/xgi/pull/312) (@maximelucas).
* Updated the centrality functions so they more gracefully handle empty and disconnected hypergraphs [#313](https://github.com/xgi-org/xgi/pull/313) (@nwlandry).
* Added `keep_isolates` argument to the subhypergraph function [#308](https://github.com/xgi-org/xgi/pull/308) (@maximelucas).
* Fix: raise error for assortativity of empty hypergraph [#307](https://github.com/xgi-org/xgi/pull/307) (@maximelucas).
* Minor: renamed to from_max_simplices [#306](https://github.com/xgi-org/xgi/pull/306) (@maximelucas).

## v0.5.5
* Refactored `incidence_matrix()` for ~4x speedup, made output consistent for empty matrices, added tests, and refactored `multiorder_laplacian()` so all internal variables are sparse if sparse=True. Fixes [#301](https://github.com/xgi-org/xgi/issues/301) [#303](https://github.com/xgi-org/xgi/pull/303) (@maximelucas).
* Renamed plotting functions, `xgi_pylab` module, and node/hyperedge/simplex plotting functions. All drawing functions now return axes. Added `pca_transform()` to rotate the node positions relative to the principal axes [#300](https://github.com/xgi-org/xgi/pull/300) (@nwlandry).
* Changed the Github actions to test all notebooks in the tutorial folder [#299](https://github.com/xgi-org/xgi/pull/299) (@nwlandry).
* Added the `convert_to_line_graph()` function and the `vector_centrality()` function, which uses it [#290](https://github.com/xgi-org/xgi/pull/290) (@goznalo-git).
* Fixed the quickstart notebook by updating the synchronization [#294](https://github.com/xgi-org/xgi/pull/294) (@nwlandry).
* Added more tests for the layout functions [#296](https://github.com/xgi-org/xgi/pull/296) (@maximelucas).
* Added basic tests for layout functions [#293](https://github.com/xgi-org/xgi/pull/293) (@maximelucas).
* Added tests for generators [#291](https://github.com/xgi-org/xgi/pull/291) (@maximelucas).
* Added the ability to specify sparsity in the matrix functions in the linalg module [#284](https://github.com/xgi-org/xgi/pull/284) (@nwlandry).
* Added the `uniform_HSBM()` and `uniform_HPPM` generative models [#286](https://github.com/xgi-org/xgi/pull/286) (@nwlandry).
* Up-versioned requirements to fix [#287](https://github.com/xgi-org/xgi/issues/287) and make compatible with NetworkX [#288](https://github.com/xgi-org/xgi/pull/288) (@nwlandry).
* Added code coverage with `codecov` and displayed coverage on main page [#285](https://github.com/xgi-org/xgi/pull/285) (@nwlandry).
* Fixed a bug in the `add_edge()` method [#289](https://github.com/xgi-org/xgi/pull/289) (@nwlandry).
* Added examples of sorting matrices by node/edge IDs to the documentation [#282](https://github.com/xgi-org/xgi/pull/282) (@nwlandry).
* Added the ability in `draw()` to plot any node positions by rescaling the plot area [#279](https://github.com/xgi-org/xgi/pull/279) (@maximelucas).


## v0.5.4
* Fixed issue #270 [#271](https://github.com/xgi-org/xgi/pull/271) (@nwlandry).
* Fixed the centralities so that they are positive and 1-normalized [#274](https://github.com/xgi-org/xgi/pull/274) (@nwlandry).


## v0.5.3
* Added support for NetworkX 3.0, removed support for Python 3.7, and changed all scipy sparse matrices to scipy sparse arrays [#268](https://github.com/xgi-org/xgi/pull/268) (@nwlandry).
* Added the ability to display the list of available datasets in xgi-data with `load_xgi_data()` [#266](https://github.com/xgi-org/xgi/pull/266) (@nwlandry).


## v0.5.2
* Added the `find_triangles()` and `flag_complex_d2()` functions. The `flag_complex_d2()` function is much faster than `flag_complex()` for simplicial complexes of max order 2. Also refactored `random_flag_complex_d2()` to use `flag_complex_d2()` [#263](https://github.com/xgi-org/xgi/pull/263) (@maximelucas).
* add the `items()` method so NodeStats and EdgeStats are even more dict-like [#233](https://github.com/xgi-org/xgi/pull/233) (@leotrs).
* Added the ability to cache the output of `load_xgi_data()` and added more interpretable errors when the http request fails [#261](https://github.com/xgi-org/xgi/pull/261) (@nwlandry).
* Deleted the data folder [#260](https://github.com/xgi-org/xgi/pull/260) (@nwlandry).
* Split the simulation of the Kuramoto model and its order parameter into two functions [#257](https://github.com/xgi-org/xgi/pull/257) (@maximelucas).
* Added the ability to write/read xgi-data datasets to/from a file, and pointed the `load_xgi_data()` function to the new xgi-data collection in Gitlab [#254](https://github.com/xgi-org/xgi/pull/254) (@acuschwarze).
* remove singletons from random generators [#256](https://github.com/xgi-org/xgi/pull/256) (@maximelucas).
* Remove references to the disGene dataset in the data folder [#253](https://github.com/xgi-org/xgi/pull/253) (@nwlandry).
* Updated the new release process [#249](https://github.com/xgi-org/xgi/pull/249) (@nwlandry).


## v0.5.1
* `draw()` now correctly plots simplicial complexes with the `max_order` keyword [#248](https://github.com/xgi-org/xgi/pull/248) (@maximelucas).
* Changed the `add_simplex` method to be non recursive [#247](https://github.com/xgi-org/xgi/pull/247) (@maximelucas).
* Added tests for the SimplicialComplex class [#245](https://github.com/xgi-org/xgi/pull/245) (@maximelucas).
* Made all draw functions available from xgi [#246](https://github.com/xgi-org/xgi/pull/246) (@maximelucas).
* Added an indent to make hypergraph json files more readable [#242](https://github.com/xgi-org/xgi/pull/242) (@maximelucas).
* Improved the efficiency of the uid update function [#239](https://github.com/xgi-org/xgi/pull/239) (@nwlandry).
* Added the ability to display the node and hyperedge labels in `draw()` [#234](https://github.com/xgi-org/xgi/pull/234) (@mcontisc).
* Fixed the uid counter initialisation [#225](https://github.com/xgi-org/xgi/pull/225) (@maximelucas).
* Added the ability to pickle hypergraphs [#229](https://github.com/xgi-org/xgi/pull/229) (@nwlandry).
* Made `random_hypergraph()` and `random_simplicialcomplex()` faster [#213](https://github.com/xgi-org/xgi/pull/213) (@maximelucas).
* Fixed a bug in `dynamical_assortativity()` [#230](https://github.com/xgi-org/xgi/pull/230) (@nwlandry).
* Removed all random decorators [#227](https://github.com/xgi-org/xgi/pull/227) (@nwlandry).
* Modified `unique_edge_sizes()` so that the list of sizes is now sorted [#226](https://github.com/xgi-org/xgi/pull/226) (@nwlandry).
* Added the `merge_duplicate_edges()` function to merge multi-edges [#210](https://github.com/xgi-org/xgi/pull/210) (@nwlandry).
* Partial speed-up of `draw` function [#211](https://github.com/xgi-org/xgi/pull/211) (@iaciac).
* Added a simplicial synchronization function [#212](https://github.com/xgi-org/xgi/pull/212) (@Marconurisso).
* Sped up the `add_simplices_from()` method [#223](https://github.com/xgi-org/xgi/pull/223) (@maximelucas).
* Updated the `add_simplices_from()` method to match `add_hyperedges_from()` [#220](https://github.com/xgi-org/xgi/pull/220) (@maximelucas).


## v0.5.0
* Fixed [#214](https://github.com/xgi-org/xgi/issues/214), added a `powerset()` function, added a `subfaces()` function, and added examples of these functions ([#209](https://github.com/xgi-org/xgi/pull/209)).
* Refactored the NodeStats and EdgeStats classes to be more efficient ([#209](https://github.com/xgi-org/xgi/pull/209)).
* Implemented set operations for NodeView and EdgeView ([#208](https://github.com/xgi-org/xgi/pull/208)).
* Addressed [#180](https://github.com/xgi-org/xgi/issues/180) with  `density()` and `incidence_density()` functions ([#204](https://github.com/xgi-org/xgi/pull/204) and [#207](https://github.com/xgi-org/xgi/pull/207)).
* Added the `<<` operator to "add" two hypergraphs together ([#203](https://github.com/xgi-org/xgi/pull/203)).
* Improved the documentation ([#202](https://github.com/xgi-org/xgi/pull/202)).
* Added Python 3.11 to the test suite ([#201](https://github.com/xgi-org/xgi/pull/201)).
* Added an option to fill only some cliques with probabilities `ps` to `xgi.flag_complex()` ([#200](https://github.com/xgi-org/xgi/pull/200)).
* Fixed Issue [#198](https://github.com/xgi-org/xgi/issues/198) ([#199](https://github.com/xgi-org/xgi/pull/199)).
* Refactored `load_xgi_data()` to call `dict_to_hypergraph()` and fixed a bug in `dict_to_hypergraph()` ([#193](https://github.com/xgi-org/xgi/pull/193)).
* Added `num_edges_order()` to get the number of edges of a given order and added an `order` parameter to the `degree_counts()` function ([#192](https://github.com/xgi-org/xgi/pull/192)).
* Fixed [#182](https://github.com/xgi-org/xgi/issues/182) and [#186](https://github.com/xgi-org/xgi/issues/186) by adding a `max_order` argument to `draw()` and `load_xgi_data()` ([#173](https://github.com/xgi-org/xgi/pull/173)) . 
* Made `draw()` faster by refactoring `_color_arg_to_dict()` and `_scalar_arg_to_dict()` ([#173](https://github.com/xgi-org/xgi/pull/173)).

Contributors: @leotrs, @maximelucas, and @nwlandry


## v0.4.3
* `Hypergraph.has_edge` is now `IDView.lookup`, `Hypergraph.duplicate_edges` is now `IDView.duplicates`, and `utilities.convert_labels_to_integer` is now `function.convert_labels_to_integer` ([#150](https://github.com/xgi-org/xgi/pull/150)).
* Added some unit tests for the convert module, the function module, and the classic generators module. Fixed for minor bugs encountered while writing tests and added documentation to Read The Docs for the drawing module. ([#153](https://github.com/xgi-org/xgi/pull/153))
* Fixed a bug in `remove_node_from_edge()` ([#154](https://github.com/xgi-org/xgi/pull/154)).
* Implemented computation of moments for NodeStat and EdgeStat ([#155](https://github.com/xgi-org/xgi/pull/155)).
* Implemented weak and strong node removal as per issue [#167](https://github.com/xgi-org/xgi/issues/76) ([#156](https://github.com/xgi-org/xgi/pull/156)).
* Added a dynamics module and created a Kuramoto model synchronization function ([#159](https://github.com/xgi-org/xgi/pull/159)).
* Added a cleanup method that removes artifacts specified by the user: multi-edges, singletons, isolates. It also can convert all labels to consecutive integers ([#161](https://github.com/xgi-org/xgi/pull/161)).
* Modified the `duplicates()` method to not include the first instance of the node/edge in the list of duplicates ([#161](https://github.com/xgi-org/xgi/pull/161)).
* Converted all instances of edges to sets from lists in response to issue [#158](https://github.com/xgi-org/xgi/issues/158) ([#162](https://github.com/xgi-org/xgi/pull/162)).
* Added lambda function default arguments for $f$, $g$, $\varphi$, $\psi$ as defined by Tudisco and Higham. Default behavior is identical as before. Fixes [#132](https://github.com/xgi-org/xgi/issues/132) ([#165](https://github.com/xgi-org/xgi/pull/165)).
* Added `sum()` as a stats method ([#168](https://github.com/xgi-org/xgi/pull/168)).
* Added a benchmarking suite for the core hypergraph data structure using airspeed velocity ([#170](https://github.com/xgi-org/xgi/pull/170)).
* Fixed issue [#171](https://github.com/xgi-org/xgi/issues/171) ([#172](https://github.com/xgi-org/xgi/pull/172))

Contributors: @nwlandry, @leotrs, and @saad1282


## v0.4.2
* Keyword arguments are now consistent in the `draw()` function ([#148](https://github.com/xgi-org/xgi/pull/148)).
* Notebooks are now formatted with black and the requirements have been updated to reflect this ([#148](https://github.com/xgi-org/xgi/pull/148)).

Contributors: @nwlandry


## v0.4.1
* Added the ability to color nodes and edges in `xgi.draw()` by value, iterable, or NodeStat/EdgeStat ([#139](https://github.com/xgi-org/xgi/pull/139), [#142](https://github.com/xgi-org/xgi/pull/142), and [#143](https://github.com/xgi-org/xgi/pull/143)).
* Fixed the distortion of the node aspect ratio with different figure sizes in [Issue #137](https://github.com/xgi-org/xgi/issues/137).
* Moved the `isolates()` and `singletons()` method from the `Hypergraph` class to the `NodeView` and `EdgeView` classes respectively ([#146](https://github.com/xgi-org/xgi/pull/146)).
* Fixed `Hypergraph.copy()` to not use the `subhypergraph` method ([#145](https://github.com/xgi-org/xgi/pull/145)).
* `filterby()` now accepts `NodeStat` and `EdgeStat` objects instead of just strings ([#144](https://github.com/xgi-org/xgi/pull/144)).
* Removed edit-mode install to run the Github Actions test suite ([#136](https://github.com/xgi-org/xgi/pull/136)).
* Added unit tests ([#147](https://github.com/xgi-org/xgi/pull/147)).

Contributors: @nwlandry, @leotrs, and @maximelucas


## v0.4
* Added the `stats` package which implements `NodeStat`, `EdgeStat` and related functionality. This package now handles computation of edge size and degree ([#120](https://github.com/xgi-org/xgi/pull/120)).
* Removed the `EdgeSizeView` and `DegreeView` classes ([#120](https://github.com/xgi-org/xgi/pull/120)).
* Changed all imports to be relative in the `xgi` package ([#121](https://github.com/xgi-org/xgi/pull/121)).
* Added an assortativity module ([#122](https://github.com/xgi-org/xgi/pull/122)).
* Improved the performance of accessing edge members ([#124](https://github.com/xgi-org/xgi/pull/124)).
* Added more operations for node and edge attributes besides "eq" ([#125](https://github.com/xgi-org/xgi/pull/125)).
* Added a function to convert all node and edge labels to integers and store the old labels as properties ([#127](https://github.com/xgi-org/xgi/pull/127)).
* * Renamed the `egonet` method to `edge_neighborhood ([#129](https://github.com/xgi-org/xgi/pull/129)).
* Moved the `neighbors` method in the `Hypergraph` class to the `IDView` class so that node and edge neighbors are now supported (PR #129).
* Added a centrality module and added these methods to `nodestats.py` and `edgestats.py` ([#130](https://github.com/xgi-org/xgi/pull/130)).
* Moved the `load_xgi_data` method to the `readwrite` module ([#130](https://github.com/xgi-org/xgi/pull/130)).
* Added a generator for sunflower hypergraphs ([#130](https://github.com/xgi-org/xgi/pull/130)).
* Added a Jupyter notebook as a quickstart guide ([#131](https://github.com/xgi-org/xgi/pull/131) and [#134](https://github.com/xgi-org/xgi/pull/134)).
* Fixed a bug in the `barycenter_spring_layout` and `weighted_barycenter_spring_layout` methods to handle non-integer node IDs ([#133](https://github.com/xgi-org/xgi/pull/133)).
* Added an isort configuration file so it no longer sorts the `__init__.py` files ([#134](https://github.com/xgi-org/xgi/pull/134)).

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
