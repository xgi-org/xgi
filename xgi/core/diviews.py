"""View classes for dihypergraphs.

A View class allows for inspection and querying of an underlying object but does not
allow modification.  This module provides View classes for nodes and edges of a dihypergraph.
Views are automatically updaed when the dihypergraph changes.

"""

from collections.abc import Mapping, Set

from ..exception import IDNotFound, XGIError
from ..stats import IDStat, dispatch_many_stats, dispatch_stat
from .views import IDView

__all__ = [
    "DiNodeView",
    "DiEdgeView",
]


class DiNodeView(IDView):
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
    <https://xgi.readthedocs.io/en/stable/api/tutorials/Tutorial%206%20-%20Statistics.html>`_.

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
    <https://xgi.readthedocs.io/en/stable/api/tutorials/Tutorial%206%20-%20Statistics.html>`_.

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
