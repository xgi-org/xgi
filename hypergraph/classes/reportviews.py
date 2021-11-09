"""
View Classes provide node, edge and degree "views" of a hypergraph.

A view means a read-only object that is quick to create, automatically
updated when the hypergraph changes, and provides basic access like `n in V`,
`for n in V`, `V[n]` and sometimes set operations.

The views are read-only iterable containers that are updated as the
hypergraph is updated. As with dicts, the hypergraph should not be updated
while iterating through the view. Views can be iterated multiple times.

Edge and Node views also allow data attribute lookup.
The resulting attribute dict is writable as `H.edges[3, 4]['color']='red'`
Degree views allow lookup of degree values for single nodes.
Weighted degree is supported with the `weight` argument.

NodeView
========

    `V = H.nodes` (or `V = H.nodes()`) allows `len(V)`, `n in V`, set
    operations e.H. "H.nodes & H.nodes", and `dd = H.nodes[n]`, where
    `dd` is the node data dict. Iteration is over the nodes by default.

NodeDataView
============

    To iterate over (node, data) pairs, use arguments to `H.nodes()`
    to create a DataView e.H. `DV = H.nodes(data='color', default='red')`.
    The DataView iterates as `for n, color in DV` and allows
    `(n, 'red') in DV`. Using `DV = H.nodes(data=True)`, the DataViews
    use the full datadict in writeable form also allowing contain testing as
    `(n, {'color': 'red'}) in VD`. DataViews allow set operations when
    data attributes are hashable.

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
==========

    `V = H.edge_size` allows iteration over (edge, size) pairs as well
    as lookup: `size=V[e]`. Weighted edge size using node data attributes
    is provided via `V = H.edge_size(weight='attr_name')` where any string
    with the attribute name can be used. `weight=None` is the default.
    No set operations are implemented for edge size, use EdgeView.

    The argument `nbunch` restricts iteration to nodes in nbunch.
    The EdgeSizeView can still look up any node even if nbunch is specified.

EdgeView
========

    `V = H.edges` or `V = H.edges()` allows iteration over edges as well as
    `e in V`, set operations and edge data lookup by edge ID `dd = H.edges[2]`.
    Iteration is over edge IDs for Hypergraph.

    Set operations are currently performed by id, not by set equivalence.
    This may be in future functionality. As it stands, however, the same edge
    can be added more than once using different IDs

EdgeDataView
============

    Edge data can be reported using an EdgeDataView typically created
    by calling an EdgeView: `DV = H.edges(data='weight', default=1)`.
    The EdgeDataView allows iteration over edge ids.

    The argument `nbunch` restricts edges to those incident to nodes in nbunch.
"""
from collections.abc import Mapping, Set
import hypergraph as hg

__all__ = [
    "NodeView",
    "NodeDataView",
    "EdgeView",
    "EdgeDataView",
    "DegreeView",
    "EdgeSizeView",
]


# NodeViews
class NodeView(Mapping, Set):
    """A NodeView class to act as H.nodes for a Hypergraph

    Attributes
    ----------
    data : NodeDataView object
        A NodeDataView of the node attributes
    """

    __slots__ = ("_nodes", "_node_attrs")

    def __getstate__(self):
        return {"_nodes": self._nodes, "_node_attrs": self._node_attrs}

    def __setstate__(self, state):
        self._nodes = state["_nodes"]
        self._node_attrs = state["_node_attrs"]

    def __init__(self, hypergraph):
        self._nodes = hypergraph._node
        self._node_attrs = hypergraph._node_attr

    # Mapping methods
    def __len__(self):
        return len(self._nodes)

    def __iter__(self):
        return iter(self._nodes)

    def __getitem__(self, n):
        if isinstance(n, slice):
            raise hg.HypergraphError(
                f"{type(self).__name__} does not support slicing, "
                f"try list(H.nodes)[{n.start}:{n.stop}:{n.step}]"
            )
        return self._nodes[n]

    # Set methods
    def __contains__(self, n):
        return n in self._nodes

    @classmethod
    def _from_iterable(cls, it):
        return set(it)

    # DataView method
    def __call__(self, n):
        if isinstance(n, slice):
            raise hg.HypergraphError(
                f"{type(self).__name__} does not support slicing, "
                f"try list(H.nodes)[{n.start}:{n.stop}:{n.step}]"
            )
        return self._nodes[n]

    def data(self, data=True, default=None):
        """
        Return a read-only view of node data.

        Parameters
        ----------
        data : bool or node data key, default=True
            If ``data=True`` (the default), return a `NodeDataView` object that
            maps each node to *all* of its attributes. `data` may also be an
            arbitrary key, in which case the `NodeDataView` maps each node to
            the value for the keyed attribute. In this case, if a node does
            not have the `data` attribute, the `default` value is used.
        default : object, default=None
            The value used when a node does not have a specific attribute.

        Returns
        -------
        NodeDataView
            The layout of the returned NodeDataView depends on the value of the
            `data` parameter.

        Notes
        -----
        If ``data=False``, returns a `NodeView` object without data.

        See Also
        --------
        NodeDataView

        Examples
        --------
        >>> H = hg.Hypergraph()
        >>> H.add_nodes_from([
        ...     (0, {"color": "red", "weight": 10}),
        ...     (1, {"color": "blue"}),
        ...     (2, {"color": "yellow", "weight": 2})
        ... ])

        Accessing node data with ``data=True`` (the default) returns a
        NodeDataView mapping each node to all of its attributes:

        >>> H.nodes.data()
        NodeDataView({0: {'color': 'red', 'weight': 10}, 1: {'color': 'blue'}, 2: {'color': 'yellow', 'weight': 2}})

        If `data` represents  a key in the node attribute dict, a NodeDataView mapping
        the nodes to the value for that specific key is returned:

        >>> H.nodes.data("color")
        NodeDataView({0: 'red', 1: 'blue', 2: 'yellow'}, data='color')

        If a specific key is not found in an attribute dict, the value specified
        by `default` is returned:

        >>> H.nodes.data("weight", default=-999)
        NodeDataView({0: 10, 1: -999, 2: 2}, data='weight')

        Note that there is no check that the `data` key is in any of the
        node attribute dictionaries:

        >>> H.nodes.data("height")
        NodeDataView({0: None, 1: None, 2: None}, data='height')
        """
        if data is False:
            return self
        return NodeDataView(self._node_attrs, data, default)

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({tuple(self)})"

    def members(self, n):
        return self._nodes[n]


class NodeDataView(Set):
    """A DataView class for nodes of a Hypergraph

    The main use for this class is to iterate through node-data pairs.
    The data can be the entire data-dictionary for each node, or it
    can be a specific attribute (with default) for each node.
    Set operations are enabled with NodeDataView, but don't work in
    cases where the data is not hashable. Use with caution.
    Typically, set operations on nodes use NodeView, not NodeDataView.
    That is, they use `H.nodes` instead of `H.nodes(data='foo')`.
    """

    __slots__ = ("_node_attrs", "_data", "_default")

    def __getstate__(self):
        return {
            "_node_attrs": self._node_attrs,
            "_data": self._data,
            "_default": self._default,
        }

    def __setstate__(self, state):
        self._node_attrs = state["_node_attrs"]
        self._data = state["_data"]
        self._default = state["_default"]

    def __init__(self, node_attrs, data=False, default=None):
        self._node_attrs = node_attrs
        self._data = data
        self._default = default

    @classmethod
    def _from_iterable(cls, it):
        try:
            return set(it)
        except TypeError as err:
            if "unhashable" in str(err):
                msg = " : Could be b/c data=True or your values are unhashable"
                raise TypeError(str(err) + msg) from err
            raise

    def __len__(self):
        return len(self._node_attrs)

    def __iter__(self):
        data = self._data
        if data is False:
            return iter(self._node_attrs)
        if data is True:
            return iter(self._node_attrs.items())
        return (
            (n, dd[data] if data in dd else self._default)
            for n, dd in self._node_attrs.items()
        )

    def __contains__(self, n):
        try:
            node_in = n in self._node_attrs
        except TypeError:
            n, d = n
            return n in self._node_attrs and self[n] == d
        if node_in is True:
            return node_in
        try:
            n, d = n
        except (TypeError, ValueError):
            return False
        return n in self._node_attrs and self[n] == d

    def __getitem__(self, n):
        if isinstance(n, slice):
            raise hg.HypergraphError(
                f"{type(self).__name__} does not support slicing, "
                f"try list(H.nodes.data())[{n.start}:{n.stop}:{n.step}]"
            )
        ddict = self._node_attrs[n]
        data = self._data
        if data is False or data is True:
            return ddict
        return ddict[data] if data in ddict else self._default

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        name = self.__class__.__name__
        if self._data is False:
            return f"{name}({tuple(self)})"
        if self._data is True:
            return f"{name}({dict(self)})"
        return f"{name}({dict(self)}, data={self._data!r})"


# DegreeViews
class DegreeView:
    """A View class for the degree of nodes in a Hypergraph

    The functionality is like dict.items() with (node, degree) pairs.
    Additional functionality includes read-only lookup of node degree,
    and calling with optional features nbunch (for only a subset of nodes)
    and weight (use edge weights to compute degree).

    Parameters
    ==========
    hypergraph : Hypergraph hypergraph-like class
    nbunch : node, container of nodes, or None meaning all nodes (default=None)
    weight : bool or string (default=None)

    Notes
    -----
    DegreeView can still lookup any node even if nbunch is specified.
    """

    __slots__ = ("_hypergraph", "_nodes", "_edges", "_edge_attrs", "_weight")

    def __init__(self, H, nbunch=None, weight=None):
        self._hypergraph = H
        self._nodes = (
            H.nodes
            if nbunch is None
            else {id: val for id, val in H.nodes.items() if id in nbunch}
        )
        self._edges = H.edges
        self._edge_attrs = H._edge_attr
        self._weight = weight

    def __call__(self, nbunch=None, weight=None):
        if nbunch is None:
            if weight == self._weight:
                return self
            return self.__class__(self._hypergraph, None, weight)
        try:
            if nbunch in self._nodes:
                if weight == self._weight:
                    return self[nbunch]
                return self.__class__(self._hypergraph, None, weight)[nbunch]
        except TypeError:
            pass
        return self.__class__(self._hypergraph, nbunch, weight)

    def __getitem__(self, n):
        weight = self._weight
        if weight is None:
            return len(self._nodes(n))
        return sum(self._edge_attrs[dd].get(weight, 1) for dd in self._nodes(n))

    def __iter__(self):
        weight = self._weight
        if weight is None:
            for n in self._nodes:
                yield (n, len(self._nodes(n)))
        else:
            for n in self._nodes:
                elements = self._nodes(n)
                deg = sum(self._edge_attrs[dd].get(weight, 1) for dd in elements)
                yield (n, deg)

    def __len__(self):
        return len(self._nodes)

    def __str__(self):
        return str(list(self._nodes))

    def __repr__(self):
        return f"{self.__class__.__name__}({dict(self)})"


# DegreeViews
class EdgeSizeView:
    """A View class for degree of edges in a Hypergraph

    The functionality is like dict.items() with (node, degree) pairs.
    Additional functionality includes read-only lookup of node degree,
    and calling with optional features nbunch (for only a subset of nodes)
    and weight (use edge weights to compute degree).

    Parameters
    ==========
    hypergraph : Hypergraph hypergraph-like class
    nbunch : node, container of nodes, or None meaning all nodes (default=None)
    weight : bool or string (default=None)

    Notes
    -----
    DegreeView can still lookup any node even if nbunch is specified.
    """

    __slots__ = ("_hypergraph", "_edges", "_nodes", "_node_attrs", "_weight")

    def __init__(self, H, nbunch=None, weight=None):
        self._hypergraph = H
        self._edges = (
            H.edges
            if nbunch is None
            else {id: val for id, val in H.edges.items() if id in nbunch}
        )
        self._nodes = H.nodes
        self._node_attrs = H._node_attr
        self._weight = weight

    def __call__(self, nbunch=None, weight=None):
        if nbunch is None:
            if weight == self._weight:
                return self
            return self.__class__(self._hypergraph, None, weight)
        try:
            if nbunch in self._edges:
                if weight == self._weight:
                    return self[nbunch]
                return self.__class__(self._hypergraph, None, weight)[nbunch]
        except TypeError:
            pass
        return self.__class__(self._hypergraph, nbunch, weight)

    def __getitem__(self, e):
        weight = self._weight
        if weight is None:
            return len(self._edges(e))
        return sum(self._node_attrs[dd].get(weight, 1) for dd in self._edges(e))

    def __iter__(self):
        weight = self._weight
        if weight is None:
            for e in self._edges:
                yield (e, len(self._edges(e)))
        else:
            for e in self._edges:
                elements = self._edges(e)
                deg = sum(self._node_attrs[dd].get(weight, 1) for dd in elements)
                yield (e, deg)

    def __len__(self):
        return len(self._edges)

    def __str__(self):
        return str(list(self._edges))

    def __repr__(self):
        return f"{self.__class__.__name__}({dict(self)})"


# EdgeDataViews
class EdgeDataView:
    """EdgeDataView for edges of Hypergraph"""

    __slots__ = ("_edge_attrs", "_data", "_default")

    def __getstate__(self):
        return {
            "_edge_attrs": self._edge_attrs,
            "_data": self._data,
            "_default": self._default,
        }

    def __setstate__(self, state):
        self._edge_attrs = state["_edge_attrs"]
        self._data = state["_data"]
        self._default = state["_default"]

    def __init__(self, edgedict, data=False, default=None):
        self._edge_attrs = edgedict
        self._data = data
        self._default = default

    @classmethod
    def _from_iterable(cls, it):
        try:
            return set(it)
        except TypeError as err:
            if "unhashable" in str(err):
                msg = " : Could be b/c data=True or your values are unhashable"
                raise TypeError(str(err) + msg) from err
            raise

    def __len__(self):
        return len(self._edge_attrs)

    def __iter__(self):
        data = self._data
        if data is False:
            return iter(self._edge_attrs)
        if data is True:
            return iter(self._edge_attrs.items())
        return (
            (n, dd[data] if data in dd else self._default)
            for n, dd in self._edge_attrs.items()
        )

    def __contains__(self, n):
        try:
            edge_in = n in self._edge_attrs
        except TypeError:
            n, d = n
            return n in self._edge_attrs and self[n] == d
        if edge_in is True:
            return edge_in
        try:
            n, d = n
        except (TypeError, ValueError):
            return False
        return n in self._edge_attrs and self[n] == d

    def __getitem__(self, n):
        if isinstance(n, slice):
            raise hg.HypergraphError(
                f"{type(self).__name__} does not support slicing, "
                f"try list(H.nodes.data())[{n.start}:{n.stop}:{n.step}]"
            )
        ddict = self._edge_attrs[n]
        data = self._data
        if data is False or data is True:
            return ddict
        return ddict[data] if data in ddict else self._default

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        name = self.__class__.__name__
        if self._data is False:
            return f"{name}({tuple(self)})"
        if self._data is True:
            return f"{name}({dict(self)})"
        return f"{name}({dict(self)}, data={self._data!r})"


# EdgeViews    have set operations and no data reported
class EdgeView(Set, Mapping):
    """A EdgeView class for the edges of a Hypergraph"""

    __slots__ = "_edges"

    def __getstate__(self):
        return {"_edges": self._edges}

    def __setstate__(self, state):
        self._graph = G = state["_edges"]

    dataview = EdgeDataView

    def __init__(self, H):
        self._edges = H._edge

    # Set methods
    def __len__(self):
        return len(self._edges)

    def __iter__(self):
        return iter(self._edges)

    def __contains__(self, e):
        try:
            return self._edges[e]
        except KeyError:
            return False

    # get edge members
    def __getitem__(self, e):
        if isinstance(e, slice):
            raise hg.HypergraphError(
                f"{type(self).__name__} does not support slicing, "
                f"try list(H.edges)[{e.start}:{e.stop}:{e.step}]"
            )
        return self._edges[e]

    # get edge members
    def __call__(self, e):
        if isinstance(e, slice):
            raise hg.HypergraphError(
                f"{type(self).__name__} does not support slicing, "
                f"try list(H.edges)[{e.start}:{e.stop}:{e.step}]"
            )
        return self._edges[e]

    def members(self, e):
        return self._edges[e]

    def data(self, data=True, default=None, nbunch=None):
        
        if nbunch is None and data is False:
            return self
        return self.dataview(self, nbunch, data, default)

    # String Methods
    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)})"
