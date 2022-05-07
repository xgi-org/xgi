"""View classes for hypergraphs.

A View class allows for inspection and querying of an underlying object but does not
allow modification.  This module provides View classes for nodes, edges, degree, and
edge size of a hypergraph.  Views are automatically updaed when the hypergraph changes.

"""
from collections.abc import Mapping, Set

import numpy as np

from xgi.exception import IDNotFound, XGIError

__all__ = [
    "NodeView",
    "EdgeView",
    "DegreeView",
    "EdgeSizeView",
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

    __slots__ = ("_id_dict", "_id_attr", "_ids")

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

    def __init__(self, id_dict, id_attr, ids=None):
        self._id_dict = id_dict
        self._id_attr = id_attr
        if id_dict is None:
            self._ids = None
        else:
            if ids is None:
                self._ids = list(id_dict.keys())
            else:
                if not set(ids).issubset(id_dict.keys()):
                    raise XGIError("ids must be a subset of the keys of id_dict")
                self._ids = list(ids)

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
            Node attributes.

        Raises
        ------
        XGIError
            If the id is not being kept track of by this view, or if id is not in the
            hypergraph, or if id is not hashable.

        """
        if id not in self._ids:
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

    def __call__(self, size):
        """Filter the results by size.

        Parameters
        ----------
        size : int
            The size of the ids to keep track of.

        Returns
        -------
        IDView
            A View that keeps track only of the ids in this view with the given size.

        """
        bunch = [id for id in self._id_dict if len(self._id_dict[id]) == size]
        return self.from_view(self, bunch)

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


class IDDegreeView:
    """Base View class for the size (node degree or edge order) of IDs in a Hypergraph.

    Parameters
    ----------
    ids : dict
        A dictionary with IDs as keys and a list of bipartite relations
        as values.
    id_attrs : dict
        A dictionary with IDs as keys and a dictionary of properties as values.  Used to
        weight the degree.
    neighbor_ids : dict
        A dictionary with neighboring IDs as keys and a list of bipartite neighbors as
        values. Used when the degree order is specified.
    nbunch : ID, iterable of IDs, or None meaning all IDs (default=None)
        The IDs for which to find the degree
    weight : hashable, optional
        The name of the attribute to weight the degree, by default None.
    order : int, default: None
        Specifies the size of the neighbors for which
        the degree should be computed.
    dtype : str, default : dict
        Specifies the data type when __getitem__ is called. Valid choices are
        dict, list, or nparray.

    """

    __slots__ = ("_ids", "_id_attrs", "_weight")

    def __init__(
        self,
        ids,
        id_attrs,
        neighbor_ids,
        id_bunch=None,
        weight=None,
        order=None,
        dtype="dict",
    ):
        self._id_attrs = id_attrs
        self._neighbor_ids = neighbor_ids
        self._weight = weight
        self._order = order
        if dtype not in {"dict", "list", "nparray"}:
            raise XGIError("Invalid datatype!")
        self._dtype = dtype

        if id_bunch is None:
            self._ids = ids
        elif isinstance(id_bunch, int):
            if id_bunch in ids:
                self._ids = {id_bunch: ids[id_bunch]}
            else:
                raise XGIError("ID does not exist in the hypergraph!")
        else:
            self._ids = {id: val for id, val in ids.items() if id in id_bunch}

        self._deg = self._get_degrees()

    def __getitem__(self, id_bunch):
        """Get the degree for an ID.

        Parameters
        ----------
        id : hashable
            Unique ID.

        Returns
        -------
        float
            The degree of an ID, weighted or unweighted.

        """
        try:
            return self._deg[id_bunch]
        except TypeError:
            degs = {id: deg for id, deg in self if id in id_bunch}
            if self._dtype == "dict":
                return degs
            elif self._dtype == "list":
                return list(degs.values())
            elif self._dtype == "nparray":
                return np.array(list(degs.values()))
        except KeyError:
            raise XGIError("Invalid ID specified!")

    def __iter__(self):
        """Returns an iterator of ID, degree pairs.

        Yields
        -------
        iterator of tuples
            Each entry is an ID, degree (Weighted or unweighted) pair.

        """
        for id, deg in self._deg.items():
            yield (id, deg)

    def __len__(self):
        """Returns the number of IDs/degrees."""
        return len(self._ids)

    def __str__(self):
        """Returns a string of IDs."""
        return str(list(self._ids))

    def __repr__(self):
        """A string representation of the degrees."""
        return f"{self.__class__.__name__}({dict(self)})"

    def _get_degrees(self):
        degrees = dict()
        if self._order is None:
            if self._weight is None:
                for id, nbrs in self._ids.items():
                    degrees[id] = len(nbrs)
            else:
                for id, nbrs in self._ids.items():
                    degrees[id] = sum(
                        self._id_attrs[dd].get(self._weight, 1) for dd in nbrs
                    )
        else:
            if self._weight is None:
                for id, nbrs in self._ids.items():
                    degrees[id] = len(
                        [
                            i
                            for i in nbrs
                            if len(self._neighbor_ids[i]) == self._order + 1
                        ]
                    )
            else:
                for id, nbrs in self._ids.items():
                    degrees[id] = sum(
                        self._id_attrs[i].get(self._weight, 1)
                        for i in nbrs
                        if len(self._neighbor_ids[i]) == self._order + 1
                    )
        return degrees


class NodeView(IDView):
    """An IDView that keeps track of node ids.

    Parameters
    ----------
    hypergraph : Hypergraph
        The hypergraph whose nodes this view will keep track of.
    bunch : optional iterable, default None
        The node ids to keep track of.  If None (default), keep track of all node ids.

    """

    def __init__(self, hypergraph, bunch=None):
        if hypergraph is None:
            super().__init__(None, None, bunch)
        else:
            super().__init__(hypergraph._node, hypergraph._node_attr, bunch)

    def __call__(self, degree):
        """Return a new view that keeps track only of the nodes of the given degree."""
        return super().__call__(size=degree)

    def memberships(self, n):
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
        try:
            return self._id_dict[n].copy()
        except KeyError as e:
            raise XGIError(f"The node ID {n} is not in the hypergraph") from e
        except TypeError as e:
            if isinstance(n, slice):
                raise XGIError(
                    f"{type(self).__name__} does not support slicing, "
                    f"try list(H.nodes)[{n.start}:{n.stop}:{n.step}]"
                ) from e


class EdgeView(IDView):
    """An IDView that keeps track of edge ids.

    Parameters
    ----------
    hypergraph : Hypergraph
        The hypergraph whose edges this view will keep track of.
    bunch : optional iterable, default None
        The edge ids to keep track of.  If None (default), keep track of all edge ids.

    """

    def __init__(self, hypergraph, bunch=None):
        if hypergraph is None:
            super().__init__(None, None, bunch)
        else:
            super().__init__(hypergraph._edge, hypergraph._edge_attr, bunch)

    def __call__(self, order):
        """Filter the results by size."""
        return super().__call__(size=order + 1)

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
        XGIError
            If `e` is a slice or if `e` does not exist in the hypergraph.

        """
        try:
            return self._id_dict[e].copy()
        except TypeError as e:
            if isinstance(e, slice):
                raise XGIError(
                    f"{type(self).__name__} does not support slicing, "
                    f"try list(H.edges)[{e.start}:{e.stop}:{e.step}]"
                ) from e
        except IDNotFound:
            if e is None:
                if dtype is dict:
                    return {key: self._id_dict[key] for key in self._ids}
                elif dtype is list:
                    return [self._id_dict[key] for key in self._ids]
                else:
                    raise XGIError(f"Unrecognized dtype {dtype}")
            raise IDNotFound(f"Item {e} not in this view")


class DegreeView(IDDegreeView):
    """An IDDegreeView that keeps track of node degree."""

    def __init__(self, hypergraph, nbunch=None, weight=None, order=None, dtype="dict"):
        super().__init__(
            hypergraph._node,
            hypergraph._edge_attr,
            hypergraph._edge,
            id_bunch=nbunch,
            weight=weight,
            order=order,
            dtype=dtype,
        )


class EdgeSizeView(IDDegreeView):
    """An IDDegreeView that keeps track of edge size."""

    def __init__(self, hypergraph, ebunch=None, weight=None, dtype="dict"):
        super().__init__(
            hypergraph._edge,
            hypergraph._node_attr,
            hypergraph._node,
            id_bunch=ebunch,
            weight=weight,
            dtype=dtype,
        )
