"""View classes for dihypergraphs.

A View class allows for inspection and querying of an underlying object but does not
allow modification.  This module provides View classes for nodes and edges of a dihypergraph.
Views are automatically updaed when the dihypergraph changes.

"""

from collections.abc import Mapping, Set

from ..exception import IDNotFound, XGIError
from ..stats import IDStat, dispatch_many_stats, dispatch_stat

__all__ = [
    "DiNodeView",
    "DiEdgeView",
]


class DiIDView(Mapping, Set):
    """Base View class for accessing the ids (nodes or edges) of a DiHypergraph.

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

        if self._id_kind == "dinode":
            self._in_id_dict = None if self._net is None else network._node_in
            self._out_id_dict = None if self._net is None else network._node_out
            self._id_attr = None if self._net is None else network._node_attr
            self._bi_in_id_dict = None if self._net is None else network._edge_in
            self._bi_out_id_dict = None if self._net is None else network._edge_out
            self._bi_id_attr = None if self._net is None else network._edge_attr
        elif self._id_kind == "diedge":
            self._in_id_dict = None if self._net is None else network._edge_in
            self._out_id_dict = None if self._net is None else network._edge_out
            self._id_attr = None if self._net is None else network._edge_attr
            self._bi_in_id_dict = None if self._net is None else network._node_in
            self._bi_out_id_dict = None if self._net is None else network._node_out
            self._bi_id_attr = None if self._net is None else network._node_attr

        if ids is None:
            self._ids = self._in_id_dict
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
        return set(self._in_id_dict) if self._ids is None else self._ids

    def __len__(self):
        """The number of IDs."""
        return len(self._in_id_dict) if self._ids is None else len(self._ids)

    def __iter__(self):
        """Returns an iterator over the IDs."""
        if self._ids is None:
            return iter({}) if self._in_id_dict is None else iter(self._in_id_dict)
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
        """Checks whether the ID is in the dihypergraph"""
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
        stat : str or :class:`xgi.stats.DiNodeStat`/:class:`xgi.stats.DiEdgeStat`
            `DiNodeStat`/`DiEdgeStat` object, or name of a `DiNodeStat`/`DiEdgeStat`.
        val : Any
            Value of the statistic.  Usually a single numeric value.  When mode is
            'between', must be a tuple of exactly two values.
        mode : str, optional
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
        IDView.filterby_attr : For more details, see the `tutorial
        <https://github.com/xgi-org/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

        Examples
        --------
        By default, return the IDs whose value of the statistic is exactly equal to
        `val`.

        >>> import xgi
        >>> H = xgi.DiHypergraph([([1, 2, 3], [2, 3, 4, 5]), ([3, 4, 5], [])])
        >>> n = H.nodes
        >>> n.filterby('degree', 2)
        DiNodeView((3, 4, 5))

        Can choose other comparison methods via `mode`.

        >>> n.filterby('degree', 2, 'eq')
        DiNodeView((3, 4, 5))
        >>> n.filterby('degree', 2, 'neq')
        DiNodeView((1, 2))
        >>> n.filterby('degree', 2, 'lt')
        DiNodeView((1, 2))
        >>> n.filterby('degree', 2, 'gt')
        DiNodeView(())
        >>> n.filterby('degree', 2, 'leq')
        DiNodeView((1, 2, 3, 4, 5))
        >>> n.filterby('degree', 2, 'geq')
        DiNodeView((3, 4, 5))
        >>> n.filterby('degree', (2, 3), 'between')
        DiNodeView((3, 4, 5))
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
        mode : str, optional
            Comparison mode. Valid options are 'eq' (default), 'neq', 'lt', 'gt',
            'leq', 'geq', or 'between'.
        missing : Any, optional
            The default value if the attribute is missing. If None (default),
            ignores those IDs.


        See Also
        --------
        DiIDView.filterby : Identical method.  For more details, see the `tutorial
        <https://github.com/xgi-org/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

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
        DiIDView
            A view that is identical to `view` but keeps track of different IDs.

        """
        newview = cls(None)
        newview._net = view._net
        newview._in_id_dict = view._in_id_dict
        newview._out_id_dict = view._out_id_dict
        newview._id_attr = view._id_attr
        newview._bi_in_id_dict = view._bi_in_id_dict
        newview._bi_out_id_dict = view._bi_out_id_dict
        newview._bi_id_attr = view._bi_id_attr
        all_ids = set(view._in_id_dict)
        if bunch is None:
            newview._ids = all_ids
        else:
            bunch = set(bunch)
            wrong = bunch - all_ids
            if wrong:
                raise IDNotFound(f"IDs {wrong} not in the hypergraph")
            newview._ids = bunch
        return newview

    def _from_iterable(self, it):
        """Construct an instance of the class from any iterable input.

        This overrides collections.abc.Set._from_iterable, which is in turn used to
        implement set operations such as &, |, ^, -.

        """
        return self.from_view(self, it)


class DiNodeView(DiIDView):
    """An DiIDView that keeps track of node ids.

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
    DiIDView

    Notes
    -----
    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `NodeView` class.  For more details, see the
    `tutorial
    <https://github.com/xgi-org/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

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
                key: (self._out_id_dict[key].copy(), self._in_id_dict[key].copy())
                for key in self
            }
            if n is None
            else (self._out_id_dict[n].copy(), self._in_id_dict[n].copy())
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
                key: set(self._out_id_dict[key].union(self._in_id_dict[key]))
                for key in self
            }
            if n is None
            else set(self._out_id_dict[n].union(self._in_id_dict[n]))
        )


class DiEdgeView(DiIDView):
    """An DiIDView that keeps track of edge ids.

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
    DiIDView

    Notes
    -----
    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `EdgeView` class.  For more details, see the
    `tutorial
    <https://github.com/xgi-org/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

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
                    key: (self._out_id_dict[key].copy(), self._in_id_dict[key].copy())
                    for key in self
                }
            elif dtype is list:
                return [
                    (self._out_id_dict[key].copy(), self._in_id_dict[key].copy())
                    for key in self
                ]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return (self._out_id_dict[e].copy(), self._in_id_dict[e].copy())

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

        The

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
                    key: set(self._out_id_dict[key].union(self._in_id_dict[key]))
                    for key in self
                }
            elif dtype is list:
                return [
                    set(self._out_id_dict[key].union(self._in_id_dict[key]))
                    for key in self
                ]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return set(self._out_id_dict[e].union(self._in_id_dict[e]))

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
                return {key: self._in_id_dict[key].copy() for key in self}
            elif dtype is list:
                return [self._in_id_dict[key].copy() for key in self]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return self._in_id_dict[e].copy()

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
                return {key: self._out_id_dict[key].copy() for key in self}
            elif dtype is list:
                return [self._out_id_dict[key].copy() for key in self]
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        if e not in self:
            raise IDNotFound(f'ID "{e}" not in this view')

        return self._out_id_dict[e].copy()

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
