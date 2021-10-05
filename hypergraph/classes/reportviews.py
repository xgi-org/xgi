"""
View Classes provide node, edge and degree "views" of a hypergraph.

Views for nodes, edges and degree are provided for all base hypergraph classes.
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
    as lookup: `deg=V[n]`. There are many flavors of DegreeView
    for In/Out/Directed/Multi. For Directed Hypergraphs, `H.degree`
    counts both in and out going edges. `H.out_degree` and
    `H.in_degree` count only specific directions.
    Weighted degree using edge data attributes is provide via
    `V = H.degree(weight='attr_name')` where any string with the
    attribute name can be used. `weight=None` is the default.
    No set operations are implemented for degrees, use NodeView.

    The argument `nbunch` restricts iteration to nodes in nbunch.
    The DegreeView can still lookup any node even if nbunch is specified.

EdgeView
========

    `V = H.edges` or `V = H.edges()` allows iteration over edges as well as
    `e in V`, set operations and edge data lookup `dd = H.edges[2, 3]`.
    Iteration is over 2-tuples `(u, v)` for Hypergraph/DiHypergraph. For multihypergraphs
    edges 3-tuples `(u, v, key)` are the default but 2-tuples can be obtained
    via `V = H.edges(keys=False)`.

    Set operations for directed hypergraphs treat the edges as a set of 2-tuples.
    For undirected hypergraphs, 2-tuples are not a unique representation of edges.
    So long as the set being compared to contains unique representations
    of its edges, the set operations will act as expected. If the other
    set contains both `(0, 1)` and `(1, 0)` however, the result of set
    operations may contain both representations of the same edge.

EdgeDataView
============

    Edge data can be reported using an EdgeDataView typically created
    by calling an EdgeView: `DV = H.edges(data='weight', default=1)`.
    The EdgeDataView allows iteration over edge tuples, membership checking
    but no set operations.

    Iteration depends on `data` and `default` and for multihypergraph `keys`
    If `data is False` (the default) then iterate over 2-tuples `(u, v)`.
    If `data is True` iterate over 3-tuples `(u, v, datadict)`.
    Otherwise iterate over `(u, v, datadict.get(data, default))`.
    For Multihypergraphs, if `keys is True`, replace `u, v` with `u, v, key`
    to create 3-tuples and 4-tuples.

    The argument `nbunch` restricts edges to those incident to nodes in nbunch.
"""
from copy import deepcopy
from collections.abc import Mapping, Set
import hypergraph as hg

__all__ = [
    "NodeView",
    "NodeDataView",
    "EdgeView",
    "EdgeDataView",
    "NodeDegreeView",
    "EdgeDegreeView",
]


# NodeViews
class NodeView(Mapping, Set):
    """A NodeView class to act as H.nodes for a NetworkX Hypergraph

    Set operations act on the nodes without considering data.
    Iteration is over nodes. Node data can be looked up like a dict.
    Use NodeDataView to iterate over node data or to specify a data
    attribute for lookup. NodeDataView is created by calling the NodeView.

    Parameters
    ----------
    hypergraph : Hypergraph hypergraph-like class

    Examples
    --------
    >>> H = nx.path_graph(3)
    >>> NV = H.nodes()
    >>> 2 in NV
    True
    >>> for n in NV:
    ...     print(n)
    0
    1
    2
    >>> assert NV & {1, 2, 3} == {1, 2}

    >>> H.add_node(2, color="blue")
    >>> NV[2]
    {'color': 'blue'}
    >>> H.add_node(8, color="red")
    >>> NDV = H.nodes(data=True)
    >>> (2, NV[2]) in NDV
    True
    >>> for n, dd in NDV:
    ...     print((n, dd.get("color", "aqua")))
    (0, 'aqua')
    (1, 'aqua')
    (2, 'blue')
    (8, 'red')
    >>> NDV[2] == NV[2]
    True

    >>> NVdata = H.nodes(data="color", default="aqua")
    >>> (2, NVdata[2]) in NVdata
    True
    >>> for n, dd in NVdata:
    ...     print((n, dd))
    (0, 'aqua')
    (1, 'aqua')
    (2, 'blue')
    (8, 'red')
    >>> NVdata[2] == NV[2]  # NVdata gets 'color', NV gets datadict
    False
    """

    __slots__ = ("_nodes","_node_attrs")

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
    def __call__(self, data=False, default=None):
        if data is False:
            return self
        return NodeDataView(self._nodes, data, default)

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
    """A DataView class for nodes of a NetworkX Hypergraph

    The main use for this class is to iterate through node-data pairs.
    The data can be the entire data-dictionary for each node, or it
    can be a specific attribute (with default) for each node.
    Set operations are enabled with NodeDataView, but don't work in
    cases where the data is not hashable. Use with caution.
    Typically, set operations on nodes use NodeView, not NodeDataView.
    That is, they use `H.nodes` instead of `H.nodes(data='foo')`.

    Parameters
    ==========
    hypergraph : NetworkX hypergraph-like class
    data : bool or string (default=False)
    default : object (default=None)
    """

    __slots__ = ("_node_attrs", "_data", "_default")

    def __getstate__(self):
        return {"_node_attrs": self._node_attrs, "_data": self._data, "_default": self._default}

    def __setstate__(self, state):
        self._node_attrs = state["_node_attrs"]
        self._data = state["_data"]
        self._default = state["_default"]

    def __init__(self, nodedict, data=False, default=None):
        self._node_attrs = nodedict
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
class NodeDegreeView:
    """A View class for degree of nodes in a Hypergraph

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

    Examples
    --------
    >>> H = nx.path_graph(3)
    >>> DV = H.degree()
    >>> assert DV[2] == 1
    >>> assert sum(deg for n, deg in DV) == 4

    >>> DVweight = H.degree(weight="span")
    >>> H.add_edge(1, 2, span=34)
    >>> DVweight[2]
    34
    >>> DVweight[0]  #  default edge weight is 1
    1
    >>> sum(span for n, span in DVweight)  # sum weighted degrees
    70

    >>> DVnbunch = H.degree(nbunch=(1, 2))
    >>> assert len(list(DVnbunch)) == 2  # iteration over nbunch only
    """
    __slots__ = ("_hypergraph","_nodes","_edges", "_weight")

    def __init__(self, H, nbunch=None, weight=None):
        self._hypergraph = H
        self._nodes = H.nodes if nbunch is None else {id : val for id, val in H.nodes.items() if id in nbunch}
        self._edges = H.edges
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
        return sum(self._edges[dd].get(weight, 1) for dd in self._nodes(n))

    def __iter__(self):
        weight = self._weight
        if weight is None:
            for n in self._nodes:
                yield (n, len(self._nodes(n)))
        else:
            for n in self.nodes:
                elements = self._nodes(n)
                deg = sum(self._edges[dd].get(weight, 1) for dd in elements)
                yield (n, deg)

    def __len__(self):
        return len(self._nodes)

    def __str__(self):
        return str(list(self._nodes))

    def __repr__(self):
        return f"{self.__class__.__name__}({dict(self)})"

# DegreeViews
class EdgeDegreeView:
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

    Examples
    --------
    >>> H = nx.path_graph(3)
    >>> DV = H.degree()
    >>> assert DV[2] == 1
    >>> assert sum(deg for n, deg in DV) == 4

    >>> DVweight = H.degree(weight="span")
    >>> H.add_edge(1, 2, span=34)
    >>> DVweight[2]
    34
    >>> DVweight[0]  #  default edge weight is 1
    1
    >>> sum(span for n, span in DVweight)  # sum weighted degrees
    70

    >>> DVnbunch = H.degree(nbunch=(1, 2))
    >>> assert len(list(DVnbunch)) == 2  # iteration over nbunch only
    """
    __slots__ = ("_hypergraph","_nodes","_edges", "_weight")

    def __init__(self, H, nbunch=None, weight=None):
        self._hypergraph = H
        self._edges = H.edges if nbunch is None else {id : val for id, val in H.edges.items() if id in nbunch}
        self._nodes = H.nodes
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
        return sum(self._nodes[dd].get(weight, 1) for dd in self._edges(e))

    def __iter__(self):
        weight = self._weight
        if weight is None:
            for e in self._edges:
                yield (e, len(self._edges(e)))
        else:
            for e in self._edges:
                elements = self._edges(e)
                deg = sum(self._nodes[dd].get(weight, 1) for dd in elements)
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
        return {"_edge_attrs": self._edge_attrs, "_data": self._data, "_default": self._default}

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
    """A EdgeView class for outward edges of a Hypergraph"""

    __slots__ = ("_edges")

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
        """
        Return a read-only view of edge data.

        Parameters
        ----------
        data : bool or edge attribute key
            If ``data=True``, then the data view maps each edge to a dictionary
            containing all of its attributes. If `data` is a key in the edge
            dictionary, then the data view maps each edge to its value for
            the keyed attribute. In this case, if the edge doesn't have the
            attribute, the `default` value is returned.
        default : object, default=None
            The value used when an edge does not have a specific attribute
        nbunch : container of nodes, optional (default=None)
            Allows restriction to edges only involving certain nodes. All edges
            are considered by default.

        Returns
        -------
        dataview
            Returns an `EdgeDataView` for undirected Hypergraphs, `OutEdgeDataView`
            for DiHypergraphs, `MultiEdgeDataView` for MultiHypergraphs and
            `OutMultiEdgeDataView` for MultiDiHypergraphs.

        Notes
        -----
        If ``data=False``, returns an `EdgeView` without any edge data.

        See Also
        --------
        EdgeDataView
        OutEdgeDataView
        MultiEdgeDataView
        OutMultiEdgeDataView

        Examples
        --------
        >>> H = nx.Hypergraph()
        >>> H.add_edges_from([
        ...     (0, 1, {"dist": 3, "capacity": 20}),
        ...     (1, 2, {"dist": 4}),
        ...     (2, 0, {"dist": 5})
        ... ])

        Accessing edge data with ``data=True`` (the default) returns an
        edge data view object listing each edge with all of its attributes:

        >>> H.edges.data()
        EdgeDataView([(0, 1, {'dist': 3, 'capacity': 20}), (0, 2, {'dist': 5}), (1, 2, {'dist': 4})])

        If `data` represents a key in the edge attribute dict, a dataview listing
        each edge with its value for that specific key is returned:

        >>> H.edges.data("dist")
        EdgeDataView([(0, 1, 3), (0, 2, 5), (1, 2, 4)])

        `nbunch` can be used to limit the edges:

        >>> H.edges.data("dist", nbunch=[0])
        EdgeDataView([(0, 1, 3), (0, 2, 5)])

        If a specific key is not found in an edge attribute dict, the value
        specified by `default` is used:

        >>> H.edges.data("capacity")
        EdgeDataView([(0, 1, 20), (0, 2, None), (1, 2, None)])

        Note that there is no check that the `data` key is present in any of
        the edge attribute dictionaries:

        >>> H.edges.data("speed")
        EdgeDataView([(0, 1, None), (0, 2, None), (1, 2, None)])
        """
        if nbunch is None and data is False:
            return self
        return self.dataview(self, nbunch, data, default)

    # String Methods
    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)})"
