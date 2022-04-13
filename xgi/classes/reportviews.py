"""
View Classes provide node, edge, degree, and edge size "views" of a hypergraph.

A view means a read-only object that is quick to create, automatically
updated when the hypergraph changes, and provides basic access like `n in V`,
`for n in V`, `V[n]` and sometimes set operations.

The views are read-only iterable containers that are updated as the
hypergraph is updated. As with dicts, the hypergraph should not be updated
while iterating through the view. Views can be iterated multiple times.

Edge and Node views also allow data attribute lookup.
The resulting attribute dict is writable as `H.edges[3]['color']='red'`
Degree views allow lookup of degree values for single nodes.
Weighted degree is supported with the `weight` argument.

NodeView
========

    `V = H.nodes` (or `V = H.nodes()`) allows `len(V)`, `n in V`, set
    operations e.H. "H.nodes & H.nodes", and `dd = H.nodes[n]`, where
    `dd` is the node data dict. Iteration is over the nodes by default.

EdgeView
========

    `V = H.edges` or `V = H.edges()` allows iteration over edges as well as
    `e in V`, set operations and edge data lookup by edge ID `dd = H.edges[2]`.
    Iteration is over edge IDs for Hypergraph.

    Set operations are currently performed by id, not by set equivalence.
    This may be in future functionality. As it stands, however, the same edge
    can be added more than once using different IDs

DegreeView
==========

    `V = H.degree` allows iteration over (node, degree) pairs as well
    as lookup: `deg=V[n]`. Weighted degree using edge data attributes
    is provided via `V = H.degree(weight='attr_name')` where any string
    with the attribute name can be used. `weight=None` is the default.
    No set operations are implemented for degrees, use NodeView.

    The argument `nbunch` restricts iteration to nodes in nbunch.
    The DegreeView can still look up any node even if nbunch is specified.

EdgeSizeView
============

    `V = H.edge_size` allows iteration over (edge, size) pairs as well
    as lookup: `size=V[e]`. Weighted edge size using node data attributes
    is provided via `V = H.edge_size(weight='attr_name')` where any string
    with the attribute name can be used. `weight=None` is the default.
    No set operations are implemented for edge size, use EdgeView.

    The argument `nbunch` restricts iteration to nodes in nbunch.
    The EdgeSizeView can still look up any node even if nbunch is specified.
"""
from collections.abc import Mapping, Set

import numpy as np

from xgi.exception import XGIError

__all__ = [
    "NodeView",
    "EdgeView",
    "DegreeView",
    "EdgeSizeView",
]


class IDView(Mapping, Set):
    """A Base View class to act as H.nodes and H.edges for a Hypergraph."""

    __slots__ = ("_id_dict", "_id_attr", "_ids")

    def __getstate__(self):
        """Function that allows pickling of the IDs (write)

        Returns
        -------
        dict of dict
            The keys access the IDs and their attributes respectively
            and the values are dictionarys from the Hypergraph class.

        """
        return {
            "_id_dict": self._id_dict,
            "_id_attr": self._id_attr,
            "_ids": self._ids,
        }

    def __setstate__(self, state):
        """Function that allows pickling of the IDs (read)

        Parameters
        ----------
        state : dict of dict
            The keys access the IDs and their attributes respectively
            and the values are dictionarys from the Hypergraph class.

        """
        self._id_dict = state["_id_dict"]
        self._id_attr = state["_id_attr"]
        self._ids = state["_ids"]

    def __init__(self, id_dict, id_attr, ids=None):
        """Initialize the IDView with IDs and associated attributes

        Parameters
        ----------
        id_dict : dict
            The original dict this is a view of.
        id_attrs : dict
            The original attribute dict this is a view of.
        ids : iterable
            A subset of the keys in id_dict to keep track of.

        """
        self._id_dict = id_dict
        self._id_attr = id_attr
        if id_dict is None:
            self._ids = None
        else:
            self._ids = list(id_dict.keys()) if ids is None else list(ids)

    def __len__(self):
        """Return the number of IDs.

        Returns
        -------
        int
            Number of IDs

        """
        return len(self._ids)

    def __iter__(self):
        """Returns an iterator over the IDs.

        Returns
        -------
        iterator of hashables
            Each entry is an ID in the hypergraph.

        """
        return iter(self._ids)

    def __getitem__(self, id):
        """Get the attributes of the ID.

        Parameters
        ----------
        id : hashable
            node ID

        Returns
        -------
        dict
            Node attributes.

        Raises
        ------
        xgi.XGIError
            Returns an error if the user tries passing in a slice or if
            the node does not exist in the hypergraph.

        """
        if id not in self._ids:
            raise XGIError(f"The ID {id} is not in this view")

        try:
            return self._id_attr[id]
        except KeyError as e:
            raise XGIError(f"The ID {id} is not in the hypergraph") from e

    def __contains__(self, id):
        """Checks whether the ID is in the hypergraph
        Parameters
        ----------
        id : hashable
            A unique ID
        Returns
        -------
        bool
            True if the ID is in the hypergraph, False otherwise.
        """
        return id in self._ids

    def __str__(self):
        """Returns a string of the list of IDs.

        Returns
        -------
        string
            the list of IDs.
        """
        return str(list(self))

    def __repr__(self):
        """Returns a summary of the class

        Returns
        -------
        string
            The class name with the IDs.
        """
        return f"{self.__class__.__name__}({tuple(self)})"

    def __call__(self, size):
        """Filter the results by size."""
        bunch = [id for id in self._id_dict if len(self._id_dict[id]) == size]
        return self.from_view(self, bunch)

    @classmethod
    def from_view(cls, view, bunch=None):
        """Create a view from another view.

        Allows to create a view with the same underlying data but with a different
        bunch.

        """
        newview = cls(None)
        newview._id_dict = view._id_dict
        newview._id_attr = view._id_attr
        newview._ids = set(view._id_dict.keys()) if bunch is None else set(bunch)
        return newview


class IDDegreeView:
    """A View class for the degree of IDs in a Hypergraph
    The functionality is like dict.items() with (ID, degree) pairs.
    Additional functionality includes read-only lookup of degree,
    and calling with optional features nbunch (for only a subset of IDs)
    and weight (use weights to compute degree).
    Notes
    -----
    IDDegreeView can still lookup any ID even if nbunch is specified.
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
        """Initialize the DegreeView object
        Parameters
        ----------
        ids : dict
            A dictionary with IDs as keys and a list of bipartite relations
            as values
        id_attrs : dict
            A dictionary with IDs as keys and a dictionary
            of properties as values. Used to weight the degree.
        neighbor_ids : dict
            A dictionary with neighboring IDs as keys and
            a list of bipartite neighbors as values. Used when the degree order
            is specified.
        nbunch : ID, container of IDs, or None meaning all IDs (default=None)
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
        """Get the degree for an ID
        Parameters
        ----------
        id : hashable
            Unique ID
        Returns
        -------
        float
            The degree of an ID, weighted or unweighted
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
        """Returns the number of IDs/degrees
        Returns
        -------
        int
            Number of IDs/degrees
        """
        return len(self._ids)

    def __str__(self):
        """Returns a string of IDs.
        Returns
        -------
        string
            A string of the list of IDs.
        """
        return str(list(self._ids))

    def __repr__(self):
        """A string representation of the degrees
        Returns
        -------
        string
            A string representation of the IDDegreeView
            with the class name and a dictionary of
            the ID, degree pairs
        """
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
                        [i for i in nbrs if len(self._neighbor_ids[i]) == self._order]
                    )
            else:
                for id, nbrs in self._ids.items():
                    degrees[id] = sum(
                        self._id_attrs[i].get(self._weight, 1)
                        for i in nbrs
                        if len(self._neighbor_ids[i]) == self._order
                    )
        return degrees


class NodeView(IDView):
    """Class for representing the nodes.

    Much of the functionality in this class inherits from IDView
    """

    def __init__(self, hypergraph, bunch=None):
        if hypergraph is None:
            super().__init__(None, None, bunch)
        else:
            super().__init__(hypergraph._node, hypergraph._node_attr, bunch)

    def __call__(self, degree):
        """Filter the results by size."""
        return super().__call__(size=degree)

    def memberships(self, n):
        """Get the edges of which a node is a member.

        Given a node ID, this method returns the edge IDs
        of which this node is a member.

        Parameters
        ----------
        n : hashable
            node ID

        Returns
        -------
        list
            edge members

        Raises
        ------
        xgi.XGIError
            Returns an error if the user tries passing in a slice or if
            the node ID does not exist in the hypergraph.

        """
        try:
            return self._id_dict[n]
        except KeyError:
            raise XGIError(f"The node ID {n} is not in the hypergraph")
        except TypeError:
            if isinstance(n, slice):
                raise XGIError(
                    f"{type(self).__name__} does not support slicing, "
                    f"try list(H.nodes)[{n.start}:{n.stop}:{n.step}]"
                )


class EdgeView(IDView):
    """Class for representing the edges.

    Much of the functionality in this class inherits from IDView
    """

    def __init__(self, hypergraph, bunch=None):
        if hypergraph is None:
            super().__init__(None, None, bunch)
        else:
            super().__init__(hypergraph._edge, hypergraph._edge_attr, bunch)

    def __call__(self, order):
        """Filter the results by size."""
        return super().__call__(size=order+1)

    def members(self, e=None, dtype=list):
        """Get the nodes that are members of an edge.

        Given an edge ID, this method returns the node IDs
        that are members of this edge.

        Parameters
        ----------
        e : hashable
            edge ID
        dtype : list
            spectify the type of the return value

        Returns
        -------
        list (if dtype is list, default)
            edge members
        dict (if dtype is dict)
            edge members, if multiple nodes are requested

        Raises
        ------
        xgi.XGIError
            Returns an error if the user tries passing in a slice or if
            the edge ID does not exist in the hypergraph.
        """
        if e is None:
            if dtype is dict:
                return self._id_dict.copy()
            elif dtype is list:
                return list(self._id_dict.values())
            else:
                raise XGIError(f"Unrecognized dtype {dtype}")

        try:
            return self._id_dict[e]
        except KeyError:
            raise XGIError(f"The edge ID {e} is not in the hypergraph")
        except TypeError:
            if isinstance(e, slice):
                raise XGIError(
                    f"{type(self).__name__} does not support slicing, "
                    f"try list(H.edges)[{e.start}:{e.stop}:{e.step}]"
                )


class DegreeView(IDDegreeView):
    """Class for representing the degrees.

    This class inherits all its functionality from IDDegreeView
    """

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
    """Class for representing the edge sizes.

    This class inherits all its functionality from IDDegreeView
    """

    def __init__(self, hypergraph, ebunch=None, weight=None, dtype="dict"):
        super().__init__(
            hypergraph._edge,
            hypergraph._node_attr,
            hypergraph._node,
            id_bunch=ebunch,
            weight=weight,
            dtype=dtype,
        )
