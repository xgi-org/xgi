"""Base class for undirected simplicial complexes.

The SimplicialComplex class allows any hashable object as a node
and can associate key/value attribute pairs with each undirected simplex and node.

Multi-simplices are not allowed.
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

    # def is_simplicial_complex(self) :
    #     """Returns True if all subfaces of each edge exist
        
    #     Goes through all simplices, from larger to smaller and stops at first missing subface found.
    #     """
        
    #     # check that all nodes in simplices are in nodes
    #     nodes_to_have = sorted({node for edge in self.edges for node in edge})
    #     if not set(nodes_to_have).issubset(self.nodes) :
    #         print("Some of the nodes members of edges are not in H.nodes.")
    #         return False
    #     else : # check that all subfaces of each edge exist
    #         edges = self.edges
    #         for edge in edges[::-1] : # loop over edges, from larger to smaller 
        
    #             size = len(edge) 
    #             if size>=3 : # because we already checked nodes 
    #                 for face in combinations(edge, size-1) : # check if all subfaces are present

    #                     face = tuple(sorted(face))
    #                     if face not in edges : 
    #                         print(f"{face} not in SimplicialComplex (first found)")
    #                         return False
            
    #         else : 
    #             return True 
    
    def __str__(self):
        """Returns a short summary of the simplicial complex.

        Returns
        -------
        string
            SimplicialComplex information

        Examples
        --------
        >>> import xgi
        >>> H = xgi.SimplicialComplex(name="foo")
        >>> str(H)
        "SimplicialComplex named 'foo' with 0 nodes and 0 edges"

        """
        try:
            return f"{type(self).__name__} named {self['name']} with {self.number_of_nodes()} nodes and {self.number_of_edges()} simplices"
        except:
            return f"Unnamed {type(self).__name__} with {self.number_of_nodes()} nodes and {self.number_of_edges()} simplices"

    def add_edge(self, edge, **attr):
        raise XGIError("Cannot add_edge to SimplicialComplex, use add_simplex instead")

    def add_edges_from(self, edges, **attr):
        raise XGIError("Cannot add_edges_from to SimplicialComplex, use add_simplices_from instead")

    def add_weighted_edges_from(self, ebunch_to_add, weight="weight", **attr):
        raise XGIError("Cannot add_weighted_edges_from to SimplicialComplex, use add_weighted_simplices_from instead")

    def remove_edge(self, id):
        raise XGIError("Cannot remove_edge to SimplicialComplex, use remove_simplex instead")

    def remove_edges_from(self, ebunch)::
        raise XGIError("Cannot remove_edges_from to SimplicialComplex, use remove_simplices_from instead")

    def add_simplex(self, simplex, **attr):
        """Add a simplex to the simplicial complex, and all its subfaces that do
        not exist yet. The universal ID is automatically assigned to the simplex(s).

        Simplex attributes can be specified with keywords or by directly
        accessing the simplex's attribute dictionary. The attributes do not propagate
        to the subfaces. See examples below.

        Parameters
        ----------
        simplex : an container or iterable of hashables
            A list of node ids
        attr : keyword arguments, optional
            Simplex data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_simplices_from : add a collection of simplexs

        Notes
        -----
        Currently cannot add empty edges.
        """

        if not self.has_simplex(simplex) :

            # add simplex and its nodes
            if simplex:
                uid = self._edge_uid()
            else:
                raise XGIError("Cannot add an empty simplex.")
            for node in simplex:
                if node not in self._node:
                    if node is None:
                        raise ValueError("None cannot be a node")
                    self._node[node] = list()
                    self._node_attr[node] = self.node_attr_dict_factory()
                self._node[node].append(uid)

            try:
                self._edge[uid] = frozenset(simplex)
                self._edge_attr[uid] = self.hyperedge_attr_dict_factory()
            except:
                raise XGIError("The simplex cannot be cast to a frozenset.")

            self._edge_attr[uid].update(attr)

            # add all subfaces
            faces = self._subfaces(simplex)
            self.add_simplices_from(faces)

    def _subfaces(self, simplex):
        """Returns list of subfaces of simplex"""
        size = len(simplex)
        faces = []
        for n in range(size, 2, -1): 
            for face in combinations(simplex, n-1):
                faces.append(face)

        return faces 

    def _supfaces(self, simplex): 
        """Returns list of simplices that contain simplex"""

        return [s for s in self._edge.values() if simplex < s]

    def _supfaces_id(self, simplex): 
        """Returns list of IDs of simplices that contain simplex"""

        return [id_ for id_, s in self._edge.items() if simplex < s]

    def add_simplices_from(self, ebunch_to_add, **attr):
        """Add all the simplices in ebunch_to_add.

        Parameters
        ----------
        ebunch_to_add : container of simplices
            Each simplex given in the container will be added to the
            graph. Each simplex must be given as as a container of nodes
            or a container with the last entry as a dictionary.
        attr : keyword arguments, optional
            Simplex data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edge : add a single simplex
        add_weighted_simplices_from : convenient way to add weighted simplices

        Notes
        -----
        Adding the same simplex twice will add it only once. Currently
        cannot add empty simplices; the method skips over them.
        """

        for simplex in ebunch_to_add:

            try:
                if isinstance(simplex[-1], dict):
                    dd = simplex[-1]
                    simplex = simplex[:-1]
                else:
                    dd = {}
            except:
                pass

            if simplex and not self.has_simplex(simplex) :
                uid = self._edge_uid()

                for n in simplex:
                    if n not in self._node:
                        if n is None:
                            raise ValueError("None cannot be a node")
                        self._node[n] = list()
                        self._node_attr[n] = self.node_attr_dict_factory()
                    self._node[n].append(uid)

                try:
                    self._edge[uid] = frozenset(simplex)
                    self._edge_attr[uid] = self.hyperedge_attr_dict_factory()
                except:
                    raise XGIError("The simplex cannot be cast to a frozenset.")

                self._edge_attr[uid].update(attr)
                self._edge_attr[uid].update(dd)

                # add subfaces 
                faces = self._subfaces(simplex)
                self.add_simplices_from(faces)

    def add_weighted_simplices_from(self, ebunch_to_add, weight="weight", **attr):
        """Add weighted simplices in `ebunch_to_add` with specified weight attr

        Parameters
        ----------
        ebunch_to_add : container of simplices
            Each simplex given in the list or container will be added
            to the graph. The simplices must be given as containers.
        weight : string, optional (default= 'weight')
            The attribute name for the simplex weights to be added.
        attr : keyword arguments, optional (default= no attributes)
            simplex attributes to add/update for all simplices.

        See Also
        --------
        add_simplex : add a single simplex
        add_simplices_from : add multiple simplices

        Notes
        -----
        Adding the same simplex twice will add it only once.
        """

        try:
            self.add_edges_from(
                ((edge[:-1], {weight: edge[-1]}) for edge in ebunch_to_add), **attr
            )
        except:
            XGIError("Empty or invalid edges specified.")

    def remove_simplex_id(self, id):
        """Remove a simplex with a given id.

        This also removes all simplices of which this simplex is face,
        to preserve the simplicial complex structure.

        Parameters
        ----------
        id : Hashable
            edge ID to remove

        Raises
        ------
        XGIError
            If no edge has that ID.

        See Also
        --------
        remove_edges_from : remove a collection of edges
        """
        try:

            # remove all simplices that contain simplex
            supfaces_ids = self._supfaces_id(self._edge[id])
            self.remove_simplex_ids_from(supfaces_ids)

            # remove simplex
            for node in self.edges.members(id):
                self._node[node].remove(id)
            del self._edge[id]
            del self._edge_attr[id]

        except KeyError as e:
            raise XGIError(f"Simplex {id} is not in the Simplicialcomplex") from e

    def remove_simplex_ids_from(self, ebunch):
        """Remove all simplicies specified in ebunch.

        Parameters
        ----------
        ebunch: list or container of hashables
            Each edge id given in the list or container will be removed
            from the hypergraph.

        See Also
        --------
        remove_simplex_id : remove a single simplex by ID

        Notes
        -----
        Will fail silently if an edge in ebunch is not in the simplicial complex.
        """
        for id in ebunch:
            try:
                for node in self.edges.members(id):
                    self._node[node].remove(id)
                del self._edge[id]
                del self._edge_attr[id]
            except:
                pass

    def has_simplex(self, simplex):
        """Whether a simplex appears in the simplicial complex.

        Parameters
        ----------
        simplex : list or set
            A container of hashables that specifies an simplex

        Returns
        -------
        bool
           Whether or not simplex is as a simplex in the simplicial complex.

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.SimplicialComplex(hyperedge_list)
        >>> H.has_simplex([1, 2])
        True
        >>> H.has_simplex({1, 3})
        False
        """
        return set(simplex) in (set(self.edges.members(s)) for s in self.edges)
