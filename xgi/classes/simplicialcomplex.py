"""Base class for undirected simplicial complexes.

The SimplicialComplex class allows any hashable object as a node
and can associate key/value attribute pairs with each undirected simplex and node.

Multi-simplices are not allowed.
"""

from itertools import combinations, count

from ..exception import XGIError
from .hypergraph import Hypergraph
from .reportviews import EdgeView, NodeView

__all__ = ["SimplicialComplex"]


class SimplicialComplex(Hypergraph):
    r"""A class to represent undirected simplicial complexes.

    A simplicial complex is a collection of subsets of a set of *nodes* or *vertices*.
    It is a pair :math:`(V, E)`, where :math:`V` is a set of elements called
    *nodes* or *vertices*, and :math:`E` is a set whose elements are subsets of
    :math:`V`, that is, each :math:`e \in E` satisfies :math:`e \subset V`.  The
    elements of :math:`E` are called *simplices*. Additionally, if a simplex is part of
    a simplicial complex, all its faces must be too. This makes simplicial complexes
    a special case of hypergraphs.

    The SimplicialComplex class allows any hashable object as a node and can associate
    attributes to each node, simplex, or the simplicial complex itself, in the form of key/value
    pairs.


    Parameters
    ----------
    incoming_data : input simplicial complex data (optional, default: None)
        Data to initialize the simplicial complex. If None (default), an empty
        simplicial complex is created, i.e. one with no nodes or simplices.
        The data can be in the following formats:

        * simplex list
        * simplex dictionary
        * 2-column Pandas dataframe (bipartite edges)
        * Scipy/Numpy incidence matrix
        * SimplicialComplex object.

    **attr : dict, optional, default: None
        Attributes to add to the simplicial complex as key, value pairs.

    Notes
    -----
    Unique IDs are assigned to each node and simplex internally and are used to refer to
    them throughout.

    The `attr` keyword arguments are added as simplicial complex attributes. To add node
    or simplex attributes see :meth:`add_node` and :meth:`add_simplex`. Methods such as
    :meth:`add_simplex` replace :class:`Hypergraph` methods such as :meth:`add_edge`
    which here raise an error.

    Examples
    --------
    >>> import xgi
    >>> S = xgi.SimplicialComplex([[1, 2, 3], [4], [5, 6], [6, 7, 8]])
    >>> S.nodes
    NodeView((1, 2, 3, 4, 5, 6, 7, 8))
    >>> S.edges
    EdgeView((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))

    """

    def __init__(self, incoming_data=None, **attr):
        self._edge_uid = count()
        self._hypergraph = self._hypergraph_attr_dict_factory()
        self._node = self._node_dict_factory()
        self._node_attr = self._node_attr_dict_factory()
        self._edge = self._hyperedge_dict_factory()
        self._edge_attr = self._hyperedge_attr_dict_factory()

        self._nodeview = NodeView(self)
        self._edgeview = EdgeView(self)

        if incoming_data is not None:
            from ..convert import convert_to_simplicial_complex

            convert_to_simplicial_complex(incoming_data, create_using=self)
        self._hypergraph.update(attr)  # must be after convert

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
        "SimplicialComplex named 'foo' with 0 nodes and 0 simplices"

        """
        try:
            return f"{type(self).__name__} named '{self['name']}' with {self.num_nodes} nodes and {self.num_edges} simplices"
        except XGIError:
            return f"Unnamed {type(self).__name__} with {self.num_nodes} nodes and {self.num_edges} simplices"

    def add_edge(self, edge, **attr):
        """Cannot `add_edge` to SimplicialComplex, use `add_simplex` instead"""
        raise XGIError("Cannot add_edge to SimplicialComplex, use add_simplex instead")

    def add_edges_from(self, edges, **attr):
        """Cannot `add_edges_from` to SimplicialComplex, use `add_simplices_from` instead"""
        raise XGIError(
            "Cannot add_edges_from to SimplicialComplex, use add_simplices_from instead"
        )

    def add_weighted_edges_from(self, ebunch_to_add, weight="weight", **attr):
        """Cannot `add_weighted_edges_from` to SimplicialComplex, use add_weighted_simplices_from instead"""
        raise XGIError(
            "Cannot add_weighted_edges_from to SimplicialComplex, use add_weighted_simplices_from instead"
        )

    def remove_edge(self, id):
        """Cannot `remove_edge` to SimplicialComplex, use `remove_simplex` instead"""
        raise XGIError(
            "Cannot remove_edge to SimplicialComplex, use remove_simplex instead"
        )

    def remove_edges_from(self, ebunch):
        """Cannot `remove_edges_from` to SimplicialComplex, use `remove_simplices_from` instead"""
        raise XGIError(
            "Cannot remove_edges_from to SimplicialComplex, use remove_simplices_from instead"
        )

    def add_simplex(self, simplex, **attr):
        """Add a simplex to the simplicial complex, and all its subfaces that do
        not exist yet. The universal ID is automatically assigned to the simplex(s).

        Simplex attributes can be specified with keywords or by directly
        accessing the simplex's attribute dictionary. The attributes do not propagate
        to the subfaces. See examples below.

        Parameters
        ----------
        simplex : an iterable of hashables
            A list of node ids
        attr : keyword arguments, optional
            Simplex data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_simplices_from : Add a collection of simplices.

        Notes
        -----
        Currently cannot add empty edges.
        """

        if not self.has_simplex(simplex):

            # add simplex and its nodes
            if simplex:
                uid = next(self._edge_uid)
            else:
                raise XGIError("Cannot add an empty simplex.")
            for node in simplex:
                if node not in self._node:
                    if node is None:
                        raise ValueError("None cannot be a node")
                    self._node[node] = set()
                    self._node_attr[node] = self._node_attr_dict_factory()
                self._node[node].add(uid)

            try:
                self._edge[uid] = frozenset(simplex)
                self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
            except TypeError:
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
            for face in combinations(simplex, n - 1):
                faces.append(face)
        return faces

    def _supfaces(self, simplex):
        """Returns list of simplices that contain simplex"""

        return [s for s in self._edge.values() if simplex < s]

    def _supfaces_id(self, simplex):
        """Returns list of IDs of simplices that contain simplex"""

        return [id_ for id_, s in self._edge.items() if simplex < s]

    def add_simplices_from(self, ebunch_to_add, max_order=None, **attr):
        """Add all the simplices in `ebunch_to_add`.

        Parameters
        ----------
        ebunch_to_add : iterable of simplices
            Each simplex given in the iterable will be added to the
            graph. Each simplex must be given as as an iterable of nodes
            or an iterable with the last entry as a dictionary.
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

        if max_order != None:
            new_ebunch_to_add = []
            for edge in ebunch_to_add:
                if len(edge) > max_order + 1:
                    combos = combinations(edge, max_order + 1)
                    new_ebunch_to_add.extend(list(combos))
                else:
                    new_ebunch_to_add.append(edge)
            ebunch_to_add = new_ebunch_to_add

        for simplex in ebunch_to_add:
            simplex = list(simplex)
            if isinstance(simplex[-1], dict):
                dd = simplex[-1]
                simplex = simplex[:-1]
            else:
                dd = {}

            if simplex and not self.has_simplex(simplex):
                uid = next(self._edge_uid)

                for n in simplex:
                    if n not in self._node:
                        if n is None:
                            raise ValueError("None cannot be a node")
                        self._node[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node[n].add(uid)

                try:
                    self._edge[uid] = frozenset(simplex)
                    self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
                except TypeError:
                    raise XGIError("The simplex cannot be cast to a frozenset.")

                self._edge_attr[uid].update(attr)
                self._edge_attr[uid].update(dd)

                # add subfaces
                faces = self._subfaces(simplex)
                self.add_simplices_from(faces)

    def close(self):
        """Adds all missing subfaces to the complex.

        See Also
        --------
        add_simplex : add a single simplex
        add_weighted_simplices_from : convenient way to add weighted simplices

        Notes
        -----
        Adding the same simplex twice will add it only once. Currently
        cannot add empty simplices; the method skips over them.
        """
        ebunch_to_close = list(map(list, self.edges.members()))
        for simplex in ebunch_to_close:
            if isinstance(simplex[-1], dict):
                dd = simplex[-1]
                simplex = simplex[:-1]
            else:
                dd = {}

            if simplex:
                new_faces = self._subfaces(simplex)
                self.add_simplices_from(new_faces)

    def add_weighted_simplices_from(
        self, ebunch_to_add, max_order=None, weight="weight", **attr
    ):
        """Add weighted simplices in `ebunch_to_add` with specified weight attr

        Parameters
        ----------
        ebunch_to_add : iterable of simplices
            Each simplex given in the list or container will be added
            to the graph. The simplices must be given as tuples of
            the form (node1, node2, ..., noden, weight).
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

        Example
        -------
        >>> import xgi
        >>> S = xgi.SimplicialComplex()
        >>> simplices = [(0, 1, 0.3), (0, 2, 0.8)]
        >>> S.add_weighted_simplices_from(simplices)
        >>> S.edges[0]
        {'weight': 0.3}
        """

        try:
            self.add_simplices_from(
                ((edge[:-1], {weight: edge[-1]}) for edge in ebunch_to_add),
                max_order=max_order,
                **attr,
            )
        except KeyError:
            XGIError("Empty or invalid simplices specified.")

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
        ebunch: list or iterable of hashables
            Each edge id given in the list or iterable will be removed
            from the Simplicialcomplex.

        Raises
        ------
        xgi.exception.IDNotFound
            If an id in ebunch is not part of the network.

        See Also
        --------
        remove_simplex_id : remove a single simplex by ID.

        """
        for id in ebunch:
            for node in self.edges.members(id):
                self._node[node].remove(id)
            del self._edge[id]
            del self._edge_attr[id]

    def has_simplex(self, simplex):
        """Whether a simplex appears in the simplicial complex.

        Parameters
        ----------
        simplex : list or set
            An iterable of hashables that specifies an simplex

        Returns
        -------
        bool
           Whether or not simplex is as a simplex in the simplicial complex.

        Examples
        --------
        >>> import xgi
        >>> H = xgi.SimplicialComplex([[1, 2], [2, 3, 4]])
        >>> H.has_simplex([1, 2])
        True
        >>> H.has_simplex({1, 3})
        False

        """
        return set(simplex) in (set(self.edges.members(s)) for s in self.edges)
