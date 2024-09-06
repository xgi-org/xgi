"""View classes for hypergraphs.

A View class allows for inspection and querying of an underlying object but does not
allow modification.  This module provides View classes for nodes and edges of a hypergraph.
Views are automatically updaed when the hypergraph changes.

"""

from collections import defaultdict
from collections.abc import Mapping, Set
from functools import reduce

from ..exception import IDNotFound, XGIError
from ..stats import IDStat, dispatch_many_stats, dispatch_stat

__all__ = [
    "NodeView",
    "EdgeView",
    "DiNodeView",
    "DiEdgeView",
]


class IDView(Mapping, Set):
    """Base View class for accessing the ids (nodes or edges) of a Hypergraph.

    Can optionally keep track of a subset of ids.  By default all node ids or all edge
    ids are kept track of.

    Parameters
    ----------
    network : Hypergraph or Simplicial Complex
        The underlying network
    ids : iterable
        A subset of the keys in id_dict to keep track of.

    Raises
    ------
    XGIError
        If ids is not a subset of the keys of id_dict.

    """

    _id_kind = None

    __slots__ = (
        "_net",
        "_ids",
    )

    def __getstate__(self):
        """Function that allows pickling.

        Returns
        -------
        dict
            The keys access the IDs and their attributes respectively
            and the values are dictionarys from the Hypergraph class.

        """
        return {
            "_net": self._net,
            "_ids": self._ids,
        }

    def __setstate__(self, state):
        """Function that allows unpickling.

        Parameters
        ----------
        dict
            The keys access the IDs and their attributes respectively
            and the values are dictionarys from the Hypergraph class.

        """
        self._net = state["_net"]
        self._id_kind = state["_id_kind"]

    def __init__(self, network, ids=None):
        self._net = network

        if self._id_kind in {"node", "dinode"}:
            self._id_dict = None if self._net is None else network._node
            self._id_attr = None if self._net is None else network._node_attr
            self._bi_id_dict = None if self._net is None else network._edge
            self._bi_id_attr = None if self._net is None else network._edge_attr
        elif self._id_kind in {"edge", "diedge"}:
            self._id_dict = None if self._net is None else network._edge
            self._id_attr = None if self._net is None else network._edge_attr
            self._bi_id_dict = None if self._net is None else network._node
            self._bi_id_attr = None if self._net is None else network._node_attr

        if ids is None:
            self._ids = self._id_dict
        else:
            self._ids = ids

    def __getattr__(self, attr):
        stat = dispatch_stat(self._id_kind, self._net, self, attr)
        self.__dict__[attr] = stat
        return stat

    def multi(self, names):
        return dispatch_many_stats(self._id_kind, self._net, self, names)

    @property
    def ids(self):
        """The ids in this view.

        Notes
        -----
        Do not use this property for membership check. Instead of `x in view.ids`,
        always use `x in view`.  The latter is always faster.

        """
        return set(self._ids)

    def __len__(self):
        """The number of IDs."""
        return len(self._ids)

    def __iter__(self):
        """Returns an iterator over the IDs."""
        return iter(self._ids)

    def __getitem__(self, id):
        """Get the attributes of the ID.

        Parameters
        ----------
        id : hashable
            node or edge ID

        Returns
        -------
        dict
            attributes associated to the ID.

        Raises
        ------
        XGIError
            If the id is not being kept track of by this view, or if id is not in the
            hypergraph, or if id is not hashable.

        """
        if id not in self:
            raise IDNotFound(f"The ID {id} is not in this view")
        return self._id_attr[id]

    def __contains__(self, id):
        """Checks whether the ID is in the hypergraph"""
        return id in self._ids

    def __str__(self):
        """Returns a string of the list of IDs."""
        return str(list(self))

    def __repr__(self):
        """Returns a summary of the class"""
        return f"{self.__class__.__name__}({tuple(self)})"

    def __call__(self, bunch):
        """Filter to the given bunch.

        Parameters
        ----------
        bunch : Iterable
            Iterable of IDs

        Returns
        -------
        IDView
            A new view that keeps track only of the IDs in the bunch.

        """
        return self.from_view(self, bunch)

    def filterby(self, stat, val, mode="eq"):
        """Filter the IDs in this view by a statistic.

        Parameters
        ----------
        stat : str or :class:`xgi.stats.NodeStat`/:class:`xgi.stats.EdgeStat`
            `NodeStat`/`EdgeStat` object, or name of a `NodeStat`/`EdgeStat`.
        val : Any
            Value of the statistic.  Usually a single numeric value.  When mode is
            'between', must be a tuple of exactly two values.
        mode : str or function, optional
            How to compare each value to `val`.  Can be one of the following.

            * 'eq' (default): Return IDs whose value is exactly equal to `val`.
            * 'neq': Return IDs whose value is not equal to `val`.
            * 'lt': Return IDs whose value is less than `val`.
            * 'gt': Return IDs whose value is greater than `val`.
            * 'leq': Return IDs whose value is less than or equal to `val`.
            * 'geq': Return IDs whose value is greater than or equal to `val`.
            * 'between': In this mode, `val` must be a tuple `(val1, val2)`.  Return IDs
              whose value `v` satisfies `val1 <= v <= val2`.
            * function, must be able to call `mode(statistic, val)` and have it map to a bool.

        See Also
        --------
        IDView.filterby_attr : For more details, see the `tutorial
        <https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

        Examples
        --------
        By default, return the IDs whose value of the statistic is exactly equal to
        `val`.

        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
        >>> n = H.nodes
        >>> n.filterby('degree', 2)
        NodeView((2, 4, 5))

        Can choose other comparison methods via `mode`.

        >>> n.filterby('degree', 2, 'eq')
        NodeView((2, 4, 5))
        >>> n.filterby('degree', 2, 'neq')
        NodeView((1, 3))
        >>> n.filterby('degree', 2, 'lt')
        NodeView((1,))
        >>> n.filterby('degree', 2, 'gt')
        NodeView((3,))
        >>> n.filterby('degree', 2, 'leq')
        NodeView((1, 2, 4, 5))
        >>> n.filterby('degree', 2, 'geq')
        NodeView((2, 3, 4, 5))
        >>> n.filterby('degree', (2, 3), 'between')
        NodeView((2, 3, 4, 5))

        Can also pass a :class:`NodeStat` object.

        >>> n.filterby(n.degree(order=2), 2)
        NodeView((3,))

        """
        if not isinstance(stat, IDStat):
            try:
                stat = getattr(self, stat)
            except AttributeError as e:
                raise AttributeError(f'Statistic with name "{stat}" not found') from e

        values = stat.asdict()
        if mode == "eq":
            bunch = [idx for idx in self if values[idx] == val]
        elif mode == "neq":
            bunch = [idx for idx in self if values[idx] != val]
        elif mode == "lt":
            bunch = [idx for idx in self if values[idx] < val]
        elif mode == "gt":
            bunch = [idx for idx in self if values[idx] > val]
        elif mode == "leq":
            bunch = [idx for idx in self if values[idx] <= val]
        elif mode == "geq":
            bunch = [idx for idx in self if values[idx] >= val]
        elif mode == "between":
            bunch = [node for node in self if val[0] <= values[node] <= val[1]]
        elif callable(mode):
            bunch = [idx for idx in self if mode(values[idx], val)]
        else:
            raise ValueError(
                f"Unrecognized mode {mode}. mode must be one of "
                "'eq', 'neq', 'lt', 'gt', 'leq', 'geq', or 'between'."
            )
        return type(self).from_view(self, bunch)

    def filterby_attr(self, attr, val, mode="eq", missing=None):
        """Filter the IDs in this view by an attribute.

        Parameters
        ----------
        attr : string
            The name of the attribute
        val : Any
            A single value or, in the case of 'between', a list of length 2
        mode : str or function, optional
            Comparison mode. Valid options are 'eq' (default), 'neq', 'lt', 'gt',
            'leq', 'geq', or 'between'. If a function, must be able to call
            `mode(attribute, val)` and have it map to a bool.
        missing : Any, optional
            The default value if the attribute is missing. If None (default),
            ignores those IDs.


        See Also
        --------
        IDView.filterby : Identical method.  For more details, see the `tutorial
        <https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

        Notes
        -----
        Beware of using comparison modes ("lt", "gt", "leq", "geq")
        when the attribute is a string. For example, the string comparison
        `'10' < '9'` evaluates to `True`.
        """
        attrs = dispatch_stat(self._id_kind, self._net, self, "attrs")
        values = attrs(attr, missing).asdict()

        if mode == "eq":
            bunch = [
                idx for idx in self if values[idx] is not None and values[idx] == val
            ]
        elif mode == "neq":
            bunch = [
                idx for idx in self if values[idx] is not None and values[idx] != val
            ]
        elif mode == "lt":
            bunch = [
                idx for idx in self if values[idx] is not None and values[idx] < val
            ]
        elif mode == "gt":
            bunch = [
                idx for idx in self if values[idx] is not None and values[idx] > val
            ]
        elif mode == "leq":
            bunch = [
                idx for idx in self if values[idx] is not None and values[idx] <= val
            ]
        elif mode == "geq":
            bunch = [
                idx for idx in self if values[idx] is not None and values[idx] >= val
            ]
        elif mode == "between":
            bunch = [
                idx
                for idx in self
                if values[idx] is not None and val[0] <= values[idx] <= val[1]
            ]
        elif callable(mode):
            bunch = [
                idx
                for idx in self
                if values[idx] is not None and mode(values[idx], val)
            ]
        else:
            raise ValueError(
                f"Unrecognized mode {mode}. mode must be one of "
                "'eq', 'neq', 'lt', 'gt', 'leq', 'geq', or 'between'."
            )
        return type(self).from_view(self, bunch)

    def neighbors(self, id, s=1):
        """Find the neighbors of an ID.

        The neighbors of an ID are those IDs that share at least one bipartite ID.

        Parameters
        ----------
        id : hashable
            ID to find neighbors of.
        s : int, optional
            The intersection size s for two edges or nodes to be considered neighbors.
            By default, 1.

        Returns
        -------
        set
            A set of the neighboring IDs

        See Also
        --------
        ~xgi.algorithms.properties.edge_neighborhood

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.nodes.neighbors(1)
        {2}
        >>> H.nodes.neighbors(2)
        {1, 3, 4}

        """
        if s == 1:
            return {
                i for n in self._id_dict[id] for i in self._bi_id_dict[n]
            }.difference({id})
        else:
            return {
                i
                for n in self._id_dict[id]
                for i in self._bi_id_dict[n]
                if len(self._id_dict[id].intersection(self._id_dict[i])) >= s
            }.difference({id})

    def duplicates(self):
        """Find IDs that have a duplicate.

        An ID has a 'duplicate' if there exists another ID with the same bipartite
        neighbors.

        Returns
        -------
        IDView
            A view containing only those IDs with a duplicate.

        Raises
        ------
        TypeError
            When IDs are of different types. For example, ("a", 1).

        Notes
        -----
        The IDs returned are in an arbitrary order, that is duplicates are not
        guaranteed to be consecutive. For IDs with the same bipartite neighbors,
        only the first ID added is not a duplicate.

        See Also
        --------
        IDView.lookup

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[0, 1, 2], [3, 4, 2], [0, 1, 2]])
        >>> H.edges.duplicates()
        EdgeView((2,))

        Order does not matter:

        >>> H = xgi.Hypergraph([[2, 1, 0], [0, 1, 2]])
        >>> H.edges.duplicates()
        EdgeView((1,))

        Repetitions matter:

        >>> H = xgi.Hypergraph([[0, 1], [1, 0]])
        >>> H.edges.duplicates()
        EdgeView((1,))

        """
        dups = []
        hashes = defaultdict(list)
        for idx, members in self._id_dict.items():
            hashes[frozenset(members)].append(idx)
        for _, edges in hashes.items():
            if len(edges) > 1:
                try:
                    dups.extend(sorted(edges)[1:])
                except TypeError:
                    dups.extend(edges[1:])
        return self.__class__.from_view(self, bunch=dups)

    def lookup(self, neighbors):
        """Find IDs with the specified bipartite neighbors.

        Parameters
        ----------
        neighbors : Iterable
            An iterable of IDs.

        Returns
        -------
        IDView
            A view containing only those IDs whose bipartite neighbors match
            `neighbors`.

        See Also
        --------
        IDView.duplicates

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[0, 1, 2], [3, 4], [3, 4, 2]])
        >>> H.edges.lookup([3, 4])
        EdgeView((1,))
        >>> H.add_edge([3, 4])
        >>> H.edges.lookup([3, 4])
        EdgeView((1, 3))

        Can be used as a boolean check for edge existence:

        >>> if H.edges.lookup([3, 4]): print('An edge with members [3, 4] exists')
        An edge with members [3, 4] exists

        Can also be used to check for nodes that belong to a particular set of edges:

        >>> H = xgi.Hypergraph([['a', 'b', 'c'], ['a', 'd', 'e'], ['c', 'd', 'e']])
        >>> H.nodes.lookup([0, 1])
        NodeView(('a',))

        """
        sought = set(neighbors)
        found = [idx for idx, neighbors in self._id_dict.items() if neighbors == sought]
        return self.__class__.from_view(self, bunch=found)

    @classmethod
    def from_view(cls, view, bunch=None):
        """Create a view from another view.

        Allows to create a view with the same underlying data but with a different
        bunch.

        Parameters
        ----------
        view : IDView
            The view used to initialize the new object
        bunch : iterable
            IDs the new view will keep track of

        Returns
        -------
        IDView
            A view that is identical to `view` but keeps track of different IDs.

        """
        newview = cls(None)
        newview._net = view._net
        newview._id_dict = view._id_dict
        newview._id_attr = view._id_attr
        newview._bi_id_dict = view._bi_id_dict
        newview._bi_id_attr = view._bi_id_attr
        all_ids = set(view._id_dict)
        if bunch is None:
            newview._ids = all_ids
        else:
            bunch = set(bunch)
            wrong = bunch - all_ids
            if wrong:
                raise IDNotFound(f"IDs {wrong} not in the hypergraph")
            newview._ids = [i for i in view._id_dict if i in bunch]
        return newview

    def _from_iterable(self, it):
        """Construct an instance of the class from any iterable input.

        This overrides collections.abc.Set._from_iterable, which is in turn used to
        implement set operations such as &, |, ^, -.

        """
        return self.from_view(self, it)


class NodeView(IDView):
    """An IDView that keeps track of node ids.

    Parameters
    ----------
    hypergraph : Hypergraph
        The hypergraph whose nodes this view will keep track of.
    bunch : optional iterable, default None
        The node ids to keep track of.  If None (default), keep track of all node ids.

    See Also
    --------
    IDView

    Notes
    -----
    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `NodeView` class.  For more details, see the
    `tutorial
    <https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

    """

    _id_kind = "node"

    def __init__(self, H, bunch=None):
        if H is None:
            super().__init__(None, bunch)
        else:
            super().__init__(H, bunch)

    def memberships(self, n=None):
        """Get the edge ids of which a node is a member.

        Gets all the node memberships for all nodes in the view if n
        not specified.

        Parameters
        ----------
        n : hashable, optional
            Node ID. By default, None.

        Returns
        -------
        dict of sets if n is None, otherwise a set
            Edge memberships.

        Raises
        ------
        XGIError
            If `n` is not hashable or if it is not in the hypergraph.

        """
        return (
            {key: self._id_dict[key].copy() for key in self}
            if n is None
            else self._id_dict[n].copy()
        )

    def isolates(self, ignore_singletons=False):
        """Nodes that belong to no edges.

        When ignore_singletons is True, a node is considered isolated from the rest of
        the hypergraph when it is included in no edges of size two or more.  In
        particular, whether the node is part of any singleton edges is irrelevant to
        determine whether it is isolated.

        When ignore_singletons is False (default), a node is isolated only when it is a
        member of exactly zero edges, including singletons.

        Parameters
        ----------
        ignore_singletons : bool, optional
            Whether to consider singleton edges.
            By default, False.

        Returns
        -------
        NodeView containing the isolated nodes.

        See Also
        --------
        :meth:`EdgeView.singletons`

        """
        if ignore_singletons:
            nodes_in_edges = set()
            for members in self._bi_id_dict.values():
                if len(members) == 1:
                    continue
                nodes_in_edges = nodes_in_edges.union(members)
            isolates = set(self._id_dict) - nodes_in_edges
            return self.from_view(self, bunch=isolates)
        else:
            return self.filterby("degree", 0)


class EdgeView(IDView):
    """An IDView that keeps track of edge ids.

    Parameters
    ----------
    hypergraph : Hypergraph
        The hypergraph whose edges this view will keep track of.
    bunch : optional iterable, default None
        The edge ids to keep track of.  If None (default), keep track of all edge ids.

    See Also
    --------
    IDView

    Notes
    -----
    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `EdgeView` class.  For more details, see the
    `tutorial
    <https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

    """

    _id_kind = "edge"

    def __init__(self, H, bunch=None):
        if H is None:
            super().__init__(None, bunch)
        else:
            super().__init__(H, bunch)

    def members(self, e=None, dtype=list):
        """Get the node ids that are members of an edge.

        Parameters
        ----------
        e : hashable, optional
            Edge ID. By default, None.
        dtype : {list, dict}, optional
            Specify the type of the return value.
            By default, list.

        Returns
        -------
        list (if dtype is list, default)
            Edge members.
        dict (if dtype is dict)
            Edge members.
        set (if e is not None)
            Members of edge e.

        Raises
        ------
        TypeError
            If `e` is not None or a hashable
        XGIError
            If `dtype` is not dict or list
        IDNotFound
            If `e` does not exist in the hypergraph

        """
        if e is None:
            if dtype is dict:
                return {key: self._id_dict[key].copy() for key in self}
            elif dtype is list:
                return [self._id_dict[key].copy() for key in self]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return self._id_dict[e].copy()

    def singletons(self):
        """Edges that contain exactly one node.

        Returns
        -------
        EdgeView containing the singleton edges.

        See Also
        --------
        :meth:`NodeView.isolates`

        """
        return self.filterby("size", 1)

    def empty(self):
        """Edges that contain no nodes.

        Returns
        -------
        EdgeView containing the empty edges.

        See Also
        --------
        :meth:`NodeView.isolates`

        """
        return self.filterby("size", 0)

    def maximal(self, strict=False):
        """Returns the maximal edges as an EdgeView.

        Maximal edges are those that are not subsets
        of any other edges in the hypergraph. The strict
        keyword determines whether the subsets
        are strict or non-strict.

        Parameters
        ----------
        strict : bool, optional
            Whether maximal edges must strictly include all of its
            subsets (`strict=True`) or whether maximal multiedges
            are permitted (`strict=False`), by default False.
            See Notes for more details.
        Returns
        -------
        EdgeView
            The maximal edges

        Notes
        -----
        This function implements two definitions of maximal
        hyperedges: strict and non-strict. For the strict case
        (`strict=True`), we enforce that a maximal edge must
        strictly include all of its subsets and by this
        definition, multiedges can't be included. For the non-strict
        case (`strict=False`), then we add all the maximal multiedges
        with non-strict inclusion.

        There are methods for eliminating these duplicates by
        running `H.cleanup()` or `H.remove_edges_from(H.edges.duplicates())`

        References
        ----------
        https://stackoverflow.com/questions/14106121/efficient-algorithm-for-finding-all-maximal-subsets

        Example
        -------

        >>> import xgi
        >>> H = xgi.Hypergraph([{1, 2, 3},{1, 2}, {2, 3}, {2}, {2}, {3, 4}, {1, 2, 3}])
        >>> H.edges.maximal()
        EdgeView((0, 5, 6))
        >>> H.edges.maximal().members()
        [{1, 2, 3}, {3, 4}, {1, 2, 3}]
        """
        edges = self._id_dict
        nodes = self._bi_id_dict
        max_edges = set()

        if strict:
            for i, e in edges.items():
                if reduce(lambda x, y: x & y, (nodes[n] for n in e)) == {i}:
                    max_edges.add(i)
        else:
            # This data structure so that the algorithm can handle multi-edges
            dups = defaultdict(list)
            for idx, members in edges.items():
                dups[frozenset(members)].append(idx)

            for i, e in edges.items():
                # If a multi-edge has already been added to the set of
                # maximal edges, we don't need to check.
                if i not in max_edges:
                    if reduce(lambda x, y: x & y, (nodes[n] for n in e)) == set(
                        dups[frozenset(e)]
                    ):
                        max_edges.update(dups[frozenset(e)])

        return self.from_view(self, bunch=max_edges)


class DiNodeView(IDView):
    """A IDView that keeps track of node ids.

    .. warning::
        This is currently an experimental feature.

    Parameters
    ----------
    hypergraph : DiHypergraph
        The hypergraph whose nodes this view will keep track of.
    bunch : optional iterable, default None
        The node ids to keep track of.  If None (default), keep track of all node ids.

    See Also
    --------
    IDView

    Notes
    -----
    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `NodeView` class.  For more details, see the
    `tutorial
    <https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

    """

    _id_kind = "dinode"

    def __init__(self, H, bunch=None):
        if H is None:
            super().__init__(None, bunch)
        else:
            super().__init__(H, bunch)

    def dimemberships(self, n=None):
        """Get the edge ids of which a node is a member.

        Gets all the node memberships for all nodes in the view if n
        not specified.

        Parameters
        ----------
        n : hashable, optional
            Node ID. By default, None.

        Returns
        -------
        dict of directed node memberships if n is None,
            otherwise the directed memberships of a single node.

        Raises
        ------
        XGIError
            If `n` is not hashable or if it is not in the hypergraph.

        """
        return (
            {
                key: (self._id_dict[key]["in"].copy(), self._id_dict[key]["out"].copy())
                for key in self
            }
            if n is None
            else (self._id_dict[n]["in"].copy(), self._id_dict[n]["out"].copy())
        )

    def memberships(self, n=None):
        """Get the edge ids of which a node is a member.

        Gets all the node memberships for all nodes in the view if n
        not specified.

        Parameters
        ----------
        n : hashable, optional
            Node ID. By default, None.

        Returns
        -------
        dict of sets if n is None, otherwise a set
            Node memberships, regardless of whether
            that node is a sender or receiver.

        Raises
        ------
        XGIError
            If `n` is not hashable or if it is not in the dihypergraph.

        """
        return (
            {
                key: set(self._id_dict[key]["in"].union(self._id_dict[key]["out"]))
                for key in self
            }
            if n is None
            else set(self._id_dict[n]["in"].union(self._id_dict[n]["out"]))
        )

    def isolates(self):
        """Nodes that belong to no edges.

        When ignore_singletons is True, a node is considered isolated from the rest of
        the hypergraph when it is included in no edges of size two or more.  In
        particular, whether the node is part of any singleton edges is irrelevant to
        determine whether it is isolated.

        When ignore_singletons is False (default), a node is isolated only when it is a
        member of exactly zero edges, including singletons.

        Returns
        -------
        NodeView containing the isolated nodes.

        See Also
        --------
        :meth:`EdgeView.singletons`

        """
        return self.filterby("degree", 0)


class DiEdgeView(IDView):
    """An IDView that keeps track of edge ids.

    .. warning::
        This is currently an experimental feature.

    Parameters
    ----------
    hypergraph : DiHypergraph
        The hypergraph whose edges this view will keep track of.
    bunch : optional iterable, default None
        The edge ids to keep track of.  If None (default), keep track of all edge ids.

    See Also
    --------
    IDView

    Notes
    -----
    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `EdgeView` class.  For more details, see the
    `tutorial
    <https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

    """

    _id_kind = "diedge"

    def __init__(self, H, bunch=None):
        if H is None:
            super().__init__(None, bunch)
        else:
            super().__init__(H, bunch)

    def dimembers(self, e=None, dtype=list):
        """Get the node ids that are members of an edge.

        Parameters
        ----------
        e : hashable, optional
            Edge ID. By default, None.
        dtype : {list, dict}, optional
            Specify the type of the return value.
            By default, list.

        Returns
        -------
        list (if dtype is list, default)
            Directed edges.
        dict (if dtype is dict)
            Directed edges.
        set (if e is not None)
            A single directed edge.

        In all of these cases, a directed edge is
        a 2-tuple of sets, where the first entry
        is the tail, and the second entry is the head.

        Raises
        ------
        TypeError
            If `e` is not None or a hashable
        XGIError
            If `dtype` is not dict or list
        IDNotFound
            If `e` does not exist in the hypergraph

        """
        if e is None:
            if dtype is dict:
                return {
                    key: (
                        self._id_dict[key]["in"].copy(),
                        self._id_dict[key]["out"].copy(),
                    )
                    for key in self
                }
            elif dtype is list:
                return [
                    (self._id_dict[key]["in"].copy(), self._id_dict[key]["out"].copy())
                    for key in self
                ]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return (self._id_dict[e]["in"].copy(), self._id_dict[e]["out"].copy())

    def members(self, e=None, dtype=list):
        """Get the edges of a directed hypergraph.

        Parameters
        ----------
        e : hashable, optional
            Edge ID. By default, None.
        dtype : {list, dict}, optional
            Specify the type of the return value.
            By default, list.

        Returns
        -------
        list (if dtype is list, default)
            Edge members.
        dict (if dtype is dict)
            Edge members.
        set (if e is not None)
            Members of edge e.

        The members of an edge are the union of
        its head and tail sets.

        Raises
        ------
        TypeError
            If `e` is not None or a hashable
        XGIError
            If `dtype` is not dict or list
        IDNotFound
            If `e` does not exist in the hypergraph
        """
        if e is None:
            if dtype is dict:
                return {
                    key: set(self._id_dict[key]["in"].union(self._id_dict[key]["out"]))
                    for key in self
                }
            elif dtype is list:
                return [
                    set(self._id_dict[key]["in"].union(self._id_dict[key]["out"]))
                    for key in self
                ]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return set(self._id_dict[e]["in"].union(self._id_dict[e]["out"]))

    def head(self, e=None, dtype=list):
        """Get the node ids that are in the head of a directed edge.

        Parameters
        ----------
        e : hashable, optional
            Edge ID. By default, None.
        dtype : {list, dict}, optional
            Specify the type of the return value.
            By default, list.

        Returns
        -------
        list (if dtype is list, default)
            Head members.
        dict (if dtype is dict)
            Head members.
        set (if e is not None)
            Members of the head of edge e.

        Raises
        ------
        TypeError
            If `e` is not None or a hashable
        XGIError
            If `dtype` is not dict or list
        IDNotFound
            If `e` does not exist in the hypergraph

        """
        if e is None:
            if dtype is dict:
                return {key: self._id_dict[key]["out"].copy() for key in self}
            elif dtype is list:
                return [self._id_dict[key]["out"].copy() for key in self]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return self._id_dict[e]["out"].copy()

    def tail(self, e=None, dtype=list):
        """Get the node ids that are in the tail of a directed edge.

        Parameters
        ----------
        e : hashable, optional
            Edge ID. By default, None.
        dtype : {list, dict}, optional
            Specify the type of the return value.
            By default, list.

        Returns
        -------
        list (if dtype is list, default)
            Tail members.
        dict (if dtype is dict)
            Tail members.
        set (if e is not None)
            Tail members of edge e.

        Raises
        ------
        TypeError
            If `e` is not None or a hashable
        XGIError
            If `dtype` is not dict or list
        IDNotFound
            If `e` does not exist in the hypergraph

        """
        if e is None:
            if dtype is dict:
                return {key: self._id_dict[key]["in"].copy() for key in self}
            elif dtype is list:
                return [self._id_dict[key]["in"].copy() for key in self]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return self._id_dict[e]["in"].copy()

    def sources(self, e=None, dtype=list):
        """Get the nodes that are sources (senders)
        in the directed edges.

        See Also
        --------
        tail: identical method
        """
        return self.tail(e=e, dtype=dtype)

    def targets(self, e=None, dtype=list):
        """Get the nodes that are sources (senders)
        in the directed edges.

        See Also
        --------
        head: identical method

        """
        return self.head(e=e, dtype=dtype)

    def empty(self):
        """Edges with no nodes in the head or the tail.

        Returns
        -------
        DiEdgeView containing the empty edges.

        See Also
        --------
        :meth:`EdgeView.empty`

        """
        return self.filterby("size", 0)
