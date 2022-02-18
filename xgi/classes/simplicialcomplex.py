"""Base class for undirected simplicial complexes.

The SimplicialComplex class allows any hashable object as a node
and can associate key/value attribute pairs with each undirected edge and node.

Multiedges and self-loops are allowed.
"""
from copy import deepcopy
from itertools import combinations

import xgi
import xgi.convert as convert
from xgi.classes import Hypergraph
from xgi.classes.reportviews import (DegreeView, EdgeSizeView, EdgeView,
                                     NodeView)
from xgi.exception import XGIError
from xgi.utils import XGICounter

__all__ = ["SimplicialComplex"]

class SimplicialComplex(Hypergraph) :
	"""A class to represent undirected simplicial complexes."""

	def is_simplicial_complex(self) :
        """Returns True if all subfaces of each edge exist
        
        Goes through all edges, from larger to smaller and stops at first missing subface found.
        """
        
        # check that all nodes in hyperedges are in nodes
        nodes_to_have = sorted({node for edge in self.edges for node in edge})
        if not set(nodes_to_have).issubset(self.nodes) :
            print("Some of the nodes members of edges are not in H.nodes.")
            return False
        else : # check that all subfaces of each edge exist
            edges = self.edges
            for edge in edges[::-1] : # loop over edges, from larger to smaller 
        
                size = len(edge) 
                if size>=3 : # because we already checked nodes 
                    for face in combinations(edge, size-1) : # check if all subfaces are present

                        face = tuple(sorted(face))
                        if face not in edges : 
                            print(f"{face} not in Hypergraph (first found)")
                            return False
            
            else : 
                return True 

    def add_edge(self, edge, **attr):
    	"""Add an edge to the simplicial complex, and all its subfaces that do
    	not exist yet. The universal ID is automatically assigned to the edge(s).

        Edge attributes can be specified with keywords or by directly
        accessing the edge's attribute dictionary. See examples below.

        Parameters
        ----------
        edge : an container or iterable of hashables
            A list of node ids
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edges_from : add a collection of edges

        Notes
        -----
        Currently cannot add empty edges.
        """

        super().add_edge(edge, **attr)
        # add all subfaces
        size = len(edge)
        faces = []
        for n in range(size, 3, -1):
        	for face in combinations(edge, n-1):
        		faces.append(face)
		super().add_edges_from(faces)

    def add_edges_from(self, ebunch_to_add, **attr):
        """Add all the edges in ebunch_to_add.

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the container will be added to the
            graph. Each edge must be given as as a container of nodes
            or a container with the last entry as a dictionary.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edge : add a single edge
        add_weighted_edges_from : convenient way to add weighted edges

        Notes
        -----
        Adding the same edge twice will create a multi-edge. Currently
        cannot add empty edges; the method skips over them.
        """

        super().add_edges_from(ebunch_to_add, **attr)
        # add subfaces 
        faces = []
        for edge in ebunch_to_add:
        	size = len(edge)
    		for n in range(size, 3, -1):
    			for face in combinations(edge, n-1):
    				faces.append(face)
		super().add_edges_from(faces)

	def add_weighted_edges_from(self, ebunch_to_add, weight="weight", **attr):
        """Add weighted edges in `ebunch_to_add` with specified weight attr

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the list or container will be added
            to the graph. The edges must be given as containers.
        weight : string, optional (default= 'weight')
            The attribute name for the edge weights to be added.
        attr : keyword arguments, optional (default= no attributes)
            Edge attributes to add/update for all edges.

        See Also
        --------
        add_edge : add a single edge
        add_edges_from : add multiple edges

        Notes
        -----
        Adding the same edge twice creates a multiedge.
        """

        super().add_weighted_edges_from(ebunch_to_add, weight="weight", **attr)
        # add subfaces 
        faces = []
        for edge in ebunch_to_add:
        	size = len(edge)
    		for n in range(size, 3, -1):
    			for face in combinations(edge, n-1):
    				faces.append(face)
		super().add_edges_from(faces)
