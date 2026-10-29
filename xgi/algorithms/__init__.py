"""Algorithms for analyzing hypergraphs.

This module collects functions that compute global or local properties of a hypergraph.
All functions take a :class:`~xgi.core.hypergraph.Hypergraph` (or
:class:`~xgi.core.simplicialcomplex.SimplicialComplex`) as their first argument.

Connectivity
    :func:`is_connected`, :func:`connected_components`,
    :func:`largest_connected_component`, :func:`number_connected_components`,
    :func:`node_connected_component`, :func:`largest_connected_hypergraph`

Centrality
    :func:`clique_eigenvector_centrality`, :func:`h_eigenvector_centrality`,
    :func:`z_eigenvector_centrality`, :func:`node_edge_centrality`,
    :func:`line_vector_centrality`, :func:`katz_centrality`,
    :func:`uniform_h_eigenvector_centrality`

Clustering
    :func:`clustering_coefficient`, :func:`local_clustering_coefficient`,
    :func:`two_node_clustering_coefficient`

Assortativity
    :func:`dynamical_assortativity`, :func:`degree_assortativity`

Shortest paths
    :func:`single_source_shortest_path_length`, :func:`shortest_path_length`

Simpliciality
    :func:`edit_simpliciality`, :func:`simplicial_edit_distance`,
    :func:`face_edit_simpliciality`, :func:`mean_face_edit_distance`,
    :func:`simplicial_fraction`

Structural properties
    :func:`equal`, :func:`num_edges_order`, :func:`max_edge_order`,
    :func:`is_uniform`, :func:`is_possible_order`, :func:`edge_neighborhood`,
    :func:`degree_counts`, :func:`degree_histogram`, :func:`unique_edge_sizes`,
    :func:`density`, :func:`incidence_density`

Many of these quantities are also available as per-node or per-edge statistics via
the :mod:`~xgi.stats` framework (e.g., ``H.nodes.degree``,
``H.nodes.clustering_coefficient``).
"""

from . import (
    assortativity,
    centrality,
    clustering,
    connected,
    properties,
    shortest_path,
    simpliciality,
)
from .assortativity import *
from .centrality import *
from .clustering import *
from .connected import *
from .properties import *
from .shortest_path import *
from .simpliciality import *

__all__ = [
    "dynamical_assortativity",
    "degree_assortativity",
    "clique_eigenvector_centrality",
    "h_eigenvector_centrality",
    "z_eigenvector_centrality",
    "node_edge_centrality",
    "line_vector_centrality",
    "katz_centrality",
    "uniform_h_eigenvector_centrality",
    "clustering_coefficient",
    "local_clustering_coefficient",
    "two_node_clustering_coefficient",
    "is_connected",
    "connected_components",
    "largest_connected_component",
    "number_connected_components",
    "node_connected_component",
    "largest_connected_hypergraph",
    "equal",
    "num_edges_order",
    "max_edge_order",
    "is_uniform",
    "is_possible_order",
    "edge_neighborhood",
    "degree_counts",
    "degree_histogram",
    "unique_edge_sizes",
    "density",
    "incidence_density",
    "single_source_shortest_path_length",
    "shortest_path_length",
    "edit_simpliciality",
    "simplicial_edit_distance",
    "face_edit_simpliciality",
    "mean_face_edit_distance",
    "simplicial_fraction",
]
