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
import xgi
from xgi.exception import XGIError

__all__ = [
    "NodeView",
    "EdgeView",
    "DegreeView",
    "EdgeSizeView",
]

# ID View Base Class
class IDView(Mapping, Set):
    """A Base View class to act as H.nodes and H.edges for a Hypergraph."""

    __slots__ = ("_ids", "_id_attrs")

    def __getstate__(self):
        """Function that allows pickling of the IDs (write)

        Returns
        -------
        dict of dict
            The keys access the IDs and their attributes respectively
            and the values are dictionarys from the Hypergraph class.
        """
        return {"_ids": self._ids, "_id_attrs": self._id_attrs}

    def __setstate__(self, state):
        """Function that allows pickling of the IDs (read)

        Parameters
        ----------
        state : dict of dict
            The keys access the IDs and their attributes respectively
            and the values are dictionarys from the Hypergraph class.
        """
        self._ids = state["_ids"]
        self._id_attrs = state["_id_attrs"]

    def __init__(self, ids, id_attrs):
        """Initialize the IDView with IDs and associated attributes
        Parameters
        ----------
        ids : dict
            Specifies IDs and the associated adjacency list
        id_attrs : dict
            Specifies IDs and their associated attributes.
        """
        self._ids = ids
        self._id_attrs = id_attrs

    # Mapping methods
    # Mapping methods
    def __len__(self):
        """Return the number of IDs
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
        try:
            return self._id_attrs[id]
        except KeyError:
            raise XGIError(f"The ID {id} is not in the hypergraph")
        except:
            if isinstance(id, slice):
                raise XGIError(
                    f"{type(self).__name__} does not support slicing, "
                    f"try list(H.nodes)[{id.start}:{id.stop}:{id.step}]"
                )

    # Set methods
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


# ID Degree View Base Class
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

    def __init__(self, ids, id_attrs, id_bunch=None, weight=None):
        """Initialize the DegreeView object
        Parameters
        ----------
        ids : dict
            A dictionary with IDs as keys and a list of bipartite relations
            as values
        id_attrs : dict
            A dictionary with IDs as keys and a dictionary of properties as values.
            Used to weight the degree.
        nbunch : ID, container of IDs, or None meaning all IDs (default=None)
            The IDs for which to find the degree
        weight : hashable, optional
            The name of the attribute to weight the degree, by default None.
        """
        self._ids = (
            ids
            if id_bunch is None
            else {id: val for id, val in ids.items() if id in id_bunch}
        )
        self._id_attrs = id_attrs
        self._weight = weight

    def __call__(self, id_bunch=None, weight=None):
        """Get the degree of specified IDs
        Parameters
        ----------
        nbunch : ID, container of IDs, or None, optional
            The IDs for which to find the degree, by default None
        weight : hashable, optional
            The name of the attribute to weight the degree, by default None
        Returns
        -------
        DegreeView
            The degrees of the hypergraph
        """
        if id_bunch is None:
            if weight == self._weight:
                return self
            return self.__class__(self._ids, self._id_attrs, None, weight)
        try:
            if id_bunch in self._ids:
                if weight == self._weight:
                    return self[id_bunch]
                return self.__class__(self._ids, self._id_attrs, None, weight)[id_bunch]
        except TypeError:
            pass
        return self.__class__(self._ids, self._id_attrs, id_bunch, weight)

    def __getitem__(self, id):
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
        weight = self._weight
        if weight is None:
            return len(self._ids[id])
        return sum(self._id_attrs[dd].get(weight, 1) for dd in self._ids(id))

    def __iter__(self):
        """Returns an iterator of ID, degree pairs.
        Yields
        -------
        iterator of tuples
            Each entry is an ID, degree (Weighted or unweighted) pair.
        """
        weight = self._weight
        if weight is None:
            for id in self._ids:
                yield (id, len(self._ids[id]))
        else:
            for id in self._ids:
                elements = self._ids[id]
                deg = sum(self._id_attrs[dd].get(weight, 1) for dd in elements)
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


class NodeView(IDView):
    """Class for representing the nodes.

    Much of the functionality in this class inherits from IDView
    """

    def __init__(self, hypergraph):
        super(NodeView, self).__init__(hypergraph._node, hypergraph._node_attr)

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
            return self._ids[n]
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

    def __init__(self, hypergraph):
        super(EdgeView, self).__init__(hypergraph._edge, hypergraph._edge_attr)

    def members(self, e):
        """Get the nodes that are members of an edge.

        Given an edge ID, this method returns the node IDs
        that are members of this edge.

        Parameters
        ----------
        e : hashable
            edge ID

        Returns
        -------
        list
            edge members

        Raises
        ------
        xgi.XGIError
            Returns an error if the user tries passing in a slice or if
            the edge ID does not exist in the hypergraph.
        """
        try:
            return self._ids[e]
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

    def __init__(self, hypergraph, nbunch=None, weight=None):
        super().__init__(
            hypergraph._node, hypergraph._edge_attr, id_bunch=nbunch, weight=weight
        )


class EdgeSizeView(IDDegreeView):
    """Class for representing the edge sizes.

    This class inherits all its functionality from IDDegreeView
    """

    def __init__(self, hypergraph, ebunch=None, weight=None):
        super().__init__(
            hypergraph._edge, hypergraph._node_attr, id_bunch=ebunch, weight=weight
        )
