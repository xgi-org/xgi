"""Base class for undirected simplicial complexes.

The SimplicialComplex class allows any hashable object as a node
and can associate key/value attribute pairs with each undirected simplex and node.

Multi-simplices are not allowed.
"""

from collections.abc import Hashable, Iterable
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

    def add_simplex(self, members, id=None, **attr):
        """Add a simplex to the simplicial complex, and all its subfaces that do
        not exist yet.

        Simplex attributes can be specified with keywords or by directly
        accessing the simplex's attribute dictionary. The attributes do not propagate
        to the subfaces.

        Parameters
        ----------
        members : Iterable
            An iterable of the ids of the nodes contained in the new simplex.
        id : hashable, default None
            Id of the new simplex. If None, a unique numeric ID will be created.
        **attr : dict, optional
            Attributes of the new simplex.

        Raises
        -----
        XGIError
            If `members` is empty.

        See Also
        --------
        add_simplices_from : Add a collection of simplices.

        Notes
        -----
        Currently cannot add empty simplices.

        Examples
        --------

        Add simplices with or without specifying an simplex id.

        >>> import xgi
        >>> S = xgi.SimplicialComplex()
        >>> S.add_simplex([1, 2, 3])
        >>> S.edges.members() # doctest: +NORMALIZE_WHITESPACE
        [frozenset({1, 2, 3}), frozenset({1, 2}),
            frozenset({1, 3}), frozenset({2, 3})]
        >>> S.add_simplex([3, 4], id='myedge')
        >>> S.edges
        EdgeView((0, 1, 2, 3, 'myedge'))

        Access attributes using square brackets.  By default no attributes are created.

        >>> S.edges[0]
        {}
        >>> S.add_simplex([1, 4], color='red', place='peru')
        >>> S.edges
        EdgeView((0, 1, 2, 3, 'myedge', 4))
        >>> S.edges[4]
        {'color': 'red', 'place': 'peru'}
        """

        try:
            members = frozenset(members)
        except TypeError:
            raise XGIError("The simplex cannot be cast to a frozenset.")

        if not members:
            raise XGIError("Cannot add an empty edge")

        if not self.has_simplex(members):

            uid = next(self._edge_uid) if not id else id
            self._edge[uid] = set()
            for node in members:
                if node not in self._node:
                    if node is None:
                        raise ValueError("None cannot be a node")
                    self._node[node] = set()
                    self._node_attr[node] = self._node_attr_dict_factory()
                self._node[node].add(uid)

            self._edge[uid] = members
            self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
            self._edge_attr[uid].update(attr)

            # add all subfaces
            faces = self._subfaces(members)
            self.add_simplices_from(faces)

    def _subfaces(self, simplex, all=True):
        """Returns list of subfaces of simplex.

        Parameters
        ----------
        simplex: an iterable of hashables
            A list of node ids
        all: bool, default: True
            Whether to return all of the subfaces or just
            those of the order below

        Returns
        -------
        faces: list of iterables
            The list containing the subfaces of the
            given simplex

        """
        size = len(simplex)
        faces = []
        if all:
            for n in range(size, 2, -1):
                for face in combinations(simplex, n - 1):
                    faces.append(face)
        else:
            for face in combinations(simplex, size - 1):
                faces.append(face)
        return faces

    def _supfaces(self, simplex):
        """Returns list of simplices that contain simplex"""

        return [s for s in self._edge.values() if simplex < s]

    def _supfaces_id(self, simplex):
        """Returns list of IDs of simplices that contain simplex"""

        return [id_ for id_, s in self._edge.items() if simplex < s]

    def add_simplices_from(self, ebunch_to_add, max_order=None, **attr):
        """Add multiple edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : Iterable

            An iterable of simplices.  This may be an iterable of iterables (Format 1),
            where each element contains the members of the simplex specified as valid node IDs.
            Alternatively, each element could also be a tuple in any of the following
            formats:

            * Format 2: 2-tuple (members, simplex_id), or
            * Format 3: 2-tuple (members, attr), or
            * Format 4: 3-tuple (members, simplex_id, attr),

            where `members` is an iterable of node IDs, `simplex_id` is a hashable to use
            as simplex ID, and `attr` is a dict of attributes. Finally, `ebunch_to_add`
            may be a dict of the form `{simplex_id: simplex_members}` (Format 5).

            Formats 2 and 3 are unambiguous because `attr` dicts are not hashable, while `id`s must be.
            In Formats 2-4, each element of `ebunch_to_add` must have the same length,
            i.e. you cannot mix different formats.  The iterables containing simplex
            members cannot be strings.

        attr : \*\*kwargs, optional
            Additional attributes to be assigned to all simplices. Attribues specified via
            `ebunch_to_add` take precedence over `attr`.

        See Also
        --------
        add_simplex : add a single simplex
        add_weighted_simplices_from : convenient way to add weighted simplices

        Notes
        -----
        Adding the same simplex twice will add it only once. Currently
        cannot add empty simplices; the method skips over them.

        Examples
        --------
        >>> import xgi
        >>> S = xgi.SimplicialComplex()

        When specifying simplices by their members only, numeric simplex IDs will be assigned
        automatically.

        >>> S.add_simplices_from([[0, 1], [1, 2], [2, 3, 4]])
        >>> S.edges.members(dtype=dict)
        {0: frozenset({0, 1}), 1: frozenset({1, 2}), 2: frozenset({2, 3, 4}), 3: frozenset({2, 3}), 4: frozenset({2, 4}), 5: frozenset({3, 4})}

        Custom simplex ids can be specified using a dict.

        >>> S = xgi.SimplicialComplex()
        >>> S.add_simplices_from({'one': [0, 1], 'two': [1, 2], 'three': [2, 3, 4]})
        >>> S.edges.members(dtype=dict)
        {'one': frozenset({0, 1}), 'two': frozenset({1, 2}), 'three': frozenset({2, 3, 4}), 0: frozenset({2, 3}), 1: frozenset({2, 4}), 2: frozenset({3, 4})}

        You can use the dict format to easily add simplices from another simplicial complex.

        >>> S2 = xgi.SimplicialComplex()
        >>> S2.add_simplices_from(S.edges.members(dtype=dict))
        >>> S.edges == S2.edges
        True

        Alternatively, simplex ids can be specified using an iterable of 2-tuples.

        >>> S = xgi.SimplicialComplex()
        >>> S.add_simplices_from([([0, 1], 'one'), ([1, 2], 'two'), ([2, 3, 4], 'three')])
        >>> S.edges.members(dtype=dict)
        {'one': frozenset({0, 1}), 'two': frozenset({1, 2}), 'three': frozenset({2, 3, 4}), 0: frozenset({2, 3}), 1: frozenset({2, 4}), 2: frozenset({3, 4})}

        Attributes for each simplex may be specified using a 2-tuple for each simplex.
        Numeric IDs will be assigned automatically.

        >>> S = xgi.SimplicialComplex()
        >>> simplices = [
        ...     ([0, 1], {'color': 'red'}),
        ...     ([1, 2], {'age': 30}),
        ...     ([2, 3, 4], {'color': 'blue', 'age': 40}),
        ... ]
        >>> S.add_simplices_from(simplices)
        >>> {e: S.edges[e] for e in S.edges}
        {0: {'color': 'red'}, 1: {'age': 30}, 2: {'color': 'blue', 'age': 40}, 3: {}, 4: {}, 5: {}}

        Attributes and custom IDs may be specified using a 3-tuple for each simplex.

        >>> S = xgi.SimplicialComplex()
        >>> simplices = [
        ...     ([0, 1], 'one', {'color': 'red'}),
        ...     ([1, 2], 'two', {'age': 30}),
        ...     ([2, 3, 4], 'three', {'color': 'blue', 'age': 40}),
        ... ]
        >>> S.add_simplices_from(simplices)
        >>> {e: S.edges[e] for e in S.edges}
        {'one': {'color': 'red'}, 'two': {'age': 30}, 'three': {'color': 'blue', 'age': 40}, 0: {}, 1: {}, 2: {}}

        """

        # format 5 is the easiest one
        if isinstance(ebunch_to_add, dict):
            for uid, members in ebunch_to_add.items():

                # check that it does not exist yet (based on members, not ID)
                if not members or self.has_simplex(members):
                    continue

                if max_order != None:
                    if len(members) > max_order + 1:
                        combos = combinations(members, max_order + 1)
                        self.add_simplices_from(list(combos), max_order=None)

                        continue
                try:
                    self._edge[uid] = frozenset(members)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e
                for n in members:
                    if n not in self._node:
                        self._node[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node[n].add(uid)
                self._edge_attr[uid] = self._hyperedge_attr_dict_factory()

                # add subfaces
                faces = self._subfaces(members)
                self.add_simplices_from(faces)

            # If we don't set the start of self._edge_uid correctly, it will start at 0,
            # which will overwrite any existing edges when calling add_edge().  First, we
            # use the somewhat convoluted float(e).is_integer() instead of using
            # isinstance(e, int) because there exist integer-like numeric types (such as
            # np.int32) which fail the isinstance() check.
            edges_with_int_id = [
                int(e)
                for e in self.edges
                if (not isinstance(e, str)) and float(e).is_integer()
            ]

            # Then, we set the start at one plus the maximum edge ID that is an integer,
            # because count() only yields integer IDs.
            start = max(edges_with_int_id) + 1 if edges_with_int_id else 0
            self._edge_uid = count(start=start)

            return

        # in formats 1-4 we only know that ebunch_to_add is an iterable, so we iterate
        # over it and use the firs element to determine which format we are working with
        new_edges = iter(ebunch_to_add)
        try:
            first_edge = next(new_edges)
        except StopIteration:
            return
        try:
            first_elem = list(first_edge)[0]
        except TypeError:
            first_elem = None

        format1, format2, format3, format4 = False, False, False, False
        if isinstance(first_elem, Iterable):
            if all(isinstance(e, str) for e in first_edge):
                format1 = True
            elif len(first_edge) == 2 and issubclass(type(first_edge[1]), Hashable):
                format2 = True
            elif len(first_edge) == 2:
                format3 = True
            elif len(first_edge) == 3:
                format4 = True
        else:
            format1 = True

        if (format1 and isinstance(first_edge, str)) or (
            not format1 and isinstance(first_elem, str)
        ):
            raise XGIError("Members cannot be specified as a string")

        # now we may iterate over the rest
        e = first_edge
        while True:
            if format1:
                members, uid, eattr = e, None, {}  # uid now set below
            elif format2:
                members, uid, eattr = e[0], e[1], {}
            elif format3:
                members, uid, eattr = e[0], None, e[1]  # uid now set below
            elif format4:
                members, uid, eattr = e[0], e[1], e[2]

            # check that it does not exist yet (based on members, not ID)
            if not members or self.has_simplex(members):
                try:
                    e = next(new_edges)
                except StopIteration:
                    break

                continue

            # needs to go after the check for existence, otherwise
            # we're skipping ID numbers when edges already exist
            if format1 or format3:
                uid = next(self._edge_uid)

            if max_order != None:
                if len(members) > max_order + 1:
                    combos = combinations(members, max_order + 1)
                    self.add_simplices_from(list(combos), max_order=None)

                    try:
                        e = next(new_edges)
                    except StopIteration:
                        break

                    continue

            try:
                self._edge[uid] = frozenset(members)
            except TypeError as e:
                raise XGIError("Invalid ebunch format") from e

            for n in members:
                if n not in self._node:
                    self._node[n] = set()
                    self._node_attr[n] = self._node_attr_dict_factory()
                self._node[n].add(uid)

            self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
            self._edge_attr[uid].update(attr)
            self._edge_attr[uid].update(eattr)

            # add subfaces
            faces = self._subfaces(members)
            self.add_simplices_from(faces)

            try:
                e = next(new_edges)
            except StopIteration:

                if format2 or format4:
                    # If we don't set the start of self._edge_uid correctly, it will start at 0,
                    # which will overwrite any existing edges when calling add_edge().  First, we
                    # use the somewhat convoluted float(e).is_integer() instead of using
                    # isinstance(e, int) because there exist integer-like numeric types (such as
                    # np.int32) which fail the isinstance() check.
                    edges_with_int_id = [
                        int(e)
                        for e in self.edges
                        if (not isinstance(e, str)) and float(e).is_integer()
                    ]

                    # Then, we set the start at one plus the maximum edge ID that is an integer,
                    # because count() only yields integer IDs.
                    start = max(edges_with_int_id) + 1 if edges_with_int_id else 0
                    self._edge_uid = count(start=start)

                break

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
        return frozenset(simplex) in self._edge.values()
