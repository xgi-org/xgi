"""View classes for hypergraphs.

A View class allows for inspection and querying of an underlying object but does not
allow modification.  This module provides View classes for nodes, edges, degree, and
edge size of a hypergraph.  Views are automatically updaed when the hypergraph changes.

"""
from collections.abc import Mapping, Set

import numpy as np

from xgi.stats import NodeStatDispatcher, EdgeStatDispatcher
from xgi.exception import IDNotFound, XGIError

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

    __slots__ = ("_dispatcher", "_id_dict", "_id_attr", "_ids")

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
        self._ids = state["_ids"]

    def __init__(self, H, id_dict, id_attr, dispatcherclass, ids=None):
        self._dispatcher = dispatcherclass(H, self)
        self._id_dict = id_dict
        self._id_attr = id_attr

        if id_dict is None:
            self._ids = None
        else:
            self._ids = ids

    def __getattr__(self, attr):
        return getattr(self._dispatcher, attr)

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
        return iter(self._id_dict.keys()) if self._ids is None else iter(self._ids)

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
        if self._ids is None:
            return id in self._id_dict
        else:
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
        try:
            stat = getattr(self.dispatcher, stat)
        except AttributeError as e:
            raise AttributeError(f'Node statistic with name "{stat}" not found') from e
        values = stat.asdict()
        if mode == "eq":
            bunch = [node for node in self.ids if values[node] == val]
        else:
            raise ValueError(f"Unrecognized mode {mode}")
        return IDView.from_view(self, bunch)

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
            A view object that is identical to `view` but keeps track of different IDs.

        """
        newview = cls(None)
        newview._id_dict = view._id_dict
        newview._id_attr = view._id_attr
        newview._ids = set(view._id_dict.keys()) if bunch is None else set(bunch)
        return newview


class NodeView(IDView):
    """An IDView that keeps track of node ids.

    Parameters
    ----------
    hypergraph : Hypergraph
        The hypergraph whose nodes this view will keep track of.
    bunch : optional iterable, default None
        The node ids to keep track of.  If None (default), keep track of all node ids.

    """

    def __init__(self, H, bunch=None):
        if H is None:
            super().__init__(None, None, None, NodeStatDispatcher, bunch)
        else:
            super().__init__(H, H._node, H._node_attr, NodeStatDispatcher, bunch)

    def memberships(self, n=None):
        """Get the edge ids of which a node is a member.

        Parameters
        ----------
        n : hashable
            Node ID.

        Returns
        -------
        list
            Edge memberships.

        Raises
        ------
        XGIError
            If `n` is not hashable or if it is not in the hypergraph.

        """
        return self._id_dict.copy() if n is None else self._id_dict[n].copy()


class EdgeView(IDView):
    """An IDView that keeps track of edge ids.

    Parameters
    ----------
    hypergraph : Hypergraph
        The hypergraph whose edges this view will keep track of.
    bunch : optional iterable, default None
        The edge ids to keep track of.  If None (default), keep track of all edge ids.

    """

    def __init__(self, H, bunch=None):
        if H is None:
            super().__init__(None, None, None, EdgeStatDispatcher, bunch)
        else:
            super().__init__(H, H._edge, H._edge_attr, EdgeStatDispatcher, bunch)

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

        try:
            return self._id_dict[e].copy()
        except IDNotFound:
            if e is None:
                if dtype is dict:
                    return {key: self._id_dict[key] for key in self._ids}
                elif dtype is list:
                    return [self._id_dict[key] for key in self._ids]
                else:
                    raise XGIError(f"Unrecognized dtype {dtype}")
            raise IDNotFound(f"Item {e} not in this view")
