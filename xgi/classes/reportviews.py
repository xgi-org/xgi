"""View classes for hypergraphs.

A View class allows for inspection and querying of an underlying object but does not
allow modification.  This module provides View classes for nodes, edges, degree, and
edge size of a hypergraph.  Views are automatically updaed when the hypergraph changes.

"""

from collections import defaultdict
from collections.abc import Mapping, Set

from ..exception import IDNotFound, XGIError
from ..stats import IDStat, dispatch_many_stats, dispatch_stat

__all__ = [
    "NodeView",
    "EdgeView",
]


class IDView(Mapping, Set):
    """Base View class for accessing the ids (nodes or edges) of a Hypergraph.

    Can optionally keep track of a subset of ids.  By default all node ids or all edge
    ids are kept track of.

    Parameters
    ----------
    id_dict : dict
        The original dict this is a view of.
    id_attrs : dict
        The original attribute dict this is a view of.
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
        "_id_dict",
        "_id_attr",
        "_bi_id_dict",
        "_bi_id_attr",
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
            "_id_dict": self._id_dict,
            "_id_attr": self._id_attr,
            "_bi_id_dict": self._bi_id_dict,
            "_bi_id_attr": self._bi_id_attr,
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
        self._id_dict = state["_id_dict"]
        self._id_attr = state["_id_attr"]
        self._bi_id_dict = state["_bi_id_dict"]
        self._bi_id_attr = state["_bi_id_attr"]
        self._ids = state["_ids"]

    def __init__(self, network, id_dict, id_attr, bi_id_dict, bi_id_attr, ids=None):
        self._net = network
        self._id_dict = id_dict
        self._id_attr = id_attr
        self._bi_id_dict = bi_id_dict
        self._bi_id_attr = bi_id_attr

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
        return set(self._id_dict.keys()) if self._ids is None else self._ids

    def __len__(self):
        """The number of IDs."""
        return len(self._id_dict) if self._ids is None else len(self._ids)

    def __iter__(self):
        """Returns an iterator over the IDs."""
        if self._ids is None:
            return iter({}) if self._id_dict is None else iter(self._id_dict.keys())
        else:
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
            Node attributes.

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
        stat : str or :class:`xgi.stats.NodeStat`
            `NodeStat` object, or name of a `NodeStat`.
        val : Any
            Value of the statistic.  Usually a single numeric value.  When mode is
            'between', must be a tuple of exactly two values.
        mode : str
            How to compare each value to `val`.  Can be one of the following.

            * 'eq' (default): Return IDs whose value is exactly equal to `val`.
            * 'neq': Return IDs whose value is not equal to `val`.
            * 'lt': Return IDs whose value is less than `val`.
            * 'gt': Return IDs whose value is greater than `val`.
            * 'leq': Return IDs whose value is less than or equal to `val`.
            * 'geq': Return IDs whose value is greater than or equal to `val`.
            * 'between': In this mode, `val` must be a tuple `(val1, val2)`.  Return IDs
              whose value `v` satisfies `val1 <= v <= val2`.

        See Also
        --------
        For more details, see the `tutorial
        <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

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
        else:
            raise ValueError(
                f"Unrecognized mode {mode}. mode must be one of 'eq', 'neq', 'lt', 'gt', 'leq', 'geq', or 'between'."
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
        mode : str, default: "eq"
            Comparison mode. Valid options are 'eq', 'neq', 'lt', 'gt',
            'leq', 'geq', or 'between'.
        missing : Any, default: None
            The default value if the attribute is missing. If None,
            ignores those IDs.


        See Also
        --------
        Works identically to `filterby`.  For more details, see the `tutorial
        <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

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
        else:
            raise ValueError(
                f"Unrecognized mode {mode}. mode must be one of 'eq', 'neq', 'lt', 'gt', 'leq', 'geq', or 'between'."
            )
        return type(self).from_view(self, bunch)

    def neighbors(self, id):
        """Find the neighbors of an ID.

        The neighbors of an ID are those IDs that share at least one bipartite ID.

        Parameters
        ----------
        id : hashable
            ID to find neighbors of.
        Returns
        -------
        set
            A set of the neighboring IDs

        See Also
        --------
        edge_neighborhood

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
        return {i for n in self._id_dict[id] for i in self._bi_id_dict[n]}.difference(
            {id}
        )

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
                dups.extend(sorted(edges)[1:])
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
            The view used to initialze the new object
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
        all_ids = set(view._id_dict.keys())
        if bunch is None:
            newview._ids = all_ids
        else:
            bunch = set(bunch)
            wrong = bunch - all_ids
            if wrong:
                raise IDNotFound(f"Nodes {wrong} not in the hypergraph")
            newview._ids = bunch
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

    Notes
    -----
    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `NodeView` class.  For more details, see the
    `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    """

    _id_kind = "node"

    def __init__(self, H, bunch=None):
        if H is None:
            super().__init__(None, None, None, None, None, bunch)
        else:
            super().__init__(H, H._node, H._node_attr, H._edge, H._edge_attr, bunch)

    def memberships(self, n=None):
        """Get the edge ids of which a node is a member.

        Gets all the node memberships for all nodes in the view if n
        not specified.

        Parameters
        ----------
        n : hashable
            Node ID.

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
            {key: self._id_dict[key] for key in self}
            if n is None
            else self._id_dict[n].copy()
        )

    def isolates(self, ignore_singletons=True):
        """Nodes that belong to no edges.

        When ignore_singletons is True (default), a node is considered isolated from the
        rest of the hypergraph when it is included in no edges of size two or more.  In
        particular, whether the node is part of any singleton edges is irrelevant to
        determine whether it is isolated.

        When ignore_singletons is False, a node is isolated only when it is a member of
        exactly zero edges, including singletons.

        Parameters
        ----------
        ignore_singletons : bool, default False
            Whether to consider singleton edges.

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

    Notes
    -----
    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `EdgeView` class.  For more details, see the
    `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    """

    _id_kind = "edge"

    def __init__(self, H, bunch=None):
        if H is None:
            super().__init__(None, None, None, None, None, bunch)
        else:
            super().__init__(H, H._edge, H._edge_attr, H._node, H._node_attr, bunch)

    def members(self, e=None, dtype=list):
        """Get the node ids that are members of an edge.

        Parameters
        ----------
        e : hashable
            Edge ID.
        dtype : type, default list
            Specify the type of the return value.

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
                return {key: self._id_dict[key] for key in self}
            elif dtype is list:
                return [self._id_dict[key] for key in self]
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
