"""Base class for undirected hypergraphs."""
from copy import deepcopy
from warnings import warn

import numpy as np

import xgi
import xgi.convert as convert
from xgi.classes.reportviews import DegreeView, EdgeSizeView, EdgeView, NodeView
from xgi.exception import IDNotFound, XGIError
from xgi.utils import XGICounter

__all__ = ["Hypergraph"]


class IDDict(dict):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError as e:
            raise IDNotFound(f"ID {item} not found") from e

    def __setitem__(self, item, value):
        if item is None:
            raise XGIError("None cannot be a node or edge")
        try:
            return super().__setitem__(item, value)
        except KeyError as e:
            raise IDNotFound(f"ID {item} not found") from e


class Hypergraph:
    r"""A hypergraph is a collection of subsets of a set of *nodes* or *vertices*.

    A hypergraph is a pair :math:`(V, E)`, where :math:`V` is a set of elements called
    *nodes* or *vertices*, and :math:`E` is a set whose elements are subsets of
    :math:`V`, that is, each :math:`e \in E` satisfies :math:`e \subset V`.  The
    elements of :math:`E` are called *hyperedges* or simply *edges*.

    The Hypergraph class allows any hashable object as a node and can associate
    attributes to each node, edge, or the hypergraph itself, in the form of key/value
    pairs.

    Multiedges and self-loops are allowed.

    Parameters
    ----------
    incoming_data : input hypergraph data (optional, default: None)
        Data to initialize the hypergraph. If None (default), an empty
        hypergraph is created, i.e. one with no nodes or edges.
        The data can be in the following formats:

        * hyperedge list
        * hyperedge dictionary
        * 2-column Pandas dataframe (bipartite edges)
        * Scipy/Numpy incidence matrix
        * Hypergraph object.

    **attr : dict, optional, default: None
        Attributes to add to the hypergraph as key, value pairs.

    Notes
    -----
    Unique IDs are assigned to each node and edge internally and are used to refer to
    them throughout.

    The attr keyword arguments are added as hypergraph attributes. To add node or ede
    attributes see :meth:`add_node` and :meth:`add_edge`.

    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph([[1, 2, 3], [4], [5, 6], [6, 7, 8]])
    >>> H.nodes
    NodeView((1, 2, 3, 4, 5, 6, 7, 8))
    >>> H.edges
    EdgeView((0, 1, 2, 3))

    """
    _node_dict_factory = IDDict
    _node_attr_dict_factory = IDDict
    _hyperedge_dict_factory = IDDict
    _hyperedge_attr_dict_factory = IDDict
    _hypergraph_attr_dict_factory = dict

    def __init__(self, incoming_data=None, **attr):
        self._edge_uid = XGICounter()
        self._hypergraph = self._hypergraph_attr_dict_factory()
        self._node = self._node_dict_factory()
        self._node_attr = self._node_attr_dict_factory()
        self._edge = self._hyperedge_dict_factory()
        self._edge_attr = self._hyperedge_attr_dict_factory()

        if incoming_data is not None:
            convert.convert_to_hypergraph(incoming_data, create_using=self)
        self._hypergraph.update(attr)  # must be after convert

    def __str__(self):
        """Returns a short summary of the hypergraph.

        Returns
        -------
        string
            Hypergraph information

        """
        try:
            return f"{type(self).__name__} named {self['name']} with {self.num_nodes} nodes and {self.num_edges} hyperedges"
        except XGIError:
            return f"Unnamed {type(self).__name__} with {self.num_nodes} nodes and {self.num_edges} hyperedges"

    def __iter__(self):
        """Iterate over the nodes.

        Returns
        -------
        iterator
            An iterator over all nodes in the hypergraph.
        """
        return iter(self._node)

    def __contains__(self, n):
        """Check for if a node is in this hypergraph.

        Parameters
        ----------
        n : hashable
            node ID

        Returns
        -------
        bool
            Whether the node exists in the hypergraph.
        """
        try:
            return n in self._node
        except TypeError:
            return False

    def __len__(self):
        """Number of nodes in the hypergraph.

        Returns
        -------
        int
            The number of nodes in the hypergraph.

        See Also
        --------
        num_nodes : identical method
        num_edges : number of edges in the hypergraph

        """
        return len(self._node)

    def __getitem__(self, attr):
        """Read hypergraph attribute."""
        try:
            return self._hypergraph[attr]
        except KeyError:
            raise XGIError("This attribute has not been set.")

    def __setitem__(self, attr, val):
        """Write hypergraph attribute."""
        self._hypergraph[attr] = val

    @property
    def num_nodes(self):
        """The number of nodes in the hypergraph.

        Returns
        -------
        int
            The number of nodes in the hypergraph.

        See Also
        --------
        num_edges : returns the number of edges in the hypergraph

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.num_nodes
        4

        """
        return len(self._node)

    @property
    def num_edges(self):
        """The number of edges in the hypergraph.

        Returns
        -------
        int
            The number of edges in the hypergraph.

        See Also
        --------
        num_nodes : returns the number of nodes in the hypergraph

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.num_edges
        2

        """
        return len(self._edge)

    def neighbors(self, n):
        """Find the neighbors of a node.

        The neighbors of a node are those nodes that appear in at least one edge with
        said node.

        Parameters
        ----------
        n : node
            Node to find neighbors of.

        Returns
        -------
        set
            A set of the neighboring nodes

        See Also
        --------
        egonet

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.neighbors(1)
        {2}
        >>> H.neighbors(2)
        {1, 3, 4}

        """
        return {i for e in self._node[n] for i in self._edge[e]}.difference({n})

    def egonet(self, n, include_self=False):
        """The egonet of the specified node.

        The egonet of a node `n` in a hypergraph `H` is another hypergraph whose nodes
        are the neighbors of `n` and its edges are all the edges in `H` that contain
        `n`.  Usually, the egonet do not include `n` itself.  This can be controlled
        with `include_self`.

        Parameters
        ----------
        n : node
            Node whose egonet is needed.
        include_self : bool (default False)
            Whether the egonet contains `n`.

        Returns
        -------
        list
            An edgelist of the egonet of `n`.

        See Also
        --------
        neighbors

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [3, 4], [4, 5, 6]])
        >>> H.neighbors(3)
        {1, 2, 4}
        >>> H.egonet(3)
        [[1, 2], [4]]
        >>> H.egonet(3, include_self=True)
        [[1, 2, 3], [3, 4]]

        """
        if include_self:
            return [self.edges.members(e) for e in self.nodes.memberships(n)]
        else:
            return [
                [x for x in self.edges.members(e) if x != n]
                for e in self.nodes.memberships(n)
            ]

    def add_node(self, node, **attr):
        """Add one node with optional attributes.

        Parameters
        ----------
        node : node
            A node can be any hashable Python object except None.
        attr : keyword arguments, optional
            Set or change node attributes using key=value.

        See Also
        --------
        add_nodes_from

        Notes
        -----
        If node is already in the hypergraph, its attributes are still updated.

        """
        if node not in self._node:
            self._node[node] = []
            self._node_attr[node] = self._node_attr_dict_factory()
        self._node_attr[node].update(attr)

    def add_nodes_from(self, nodes_for_adding, **attr):
        """Add multiple nodes with optional attributes.

        Parameters
        ----------
        nodes_for_adding : iterable container
            A container of nodes (list, dict, set, etc.).
            OR
            A container of (node, attribute dict) tuples.
            Node attributes are updated using the attribute dict.
        attr : keyword arguments, optional (default= no attributes)
            Update attributes for all nodes in nodes.
            Node attributes specified in nodes as a tuple take
            precedence over attributes specified via keyword arguments.

        See Also
        --------
        add_node

        """
        for n in nodes_for_adding:
            try:
                newnode = n not in self._node
                newdict = attr
            except TypeError:
                n, ndict = n
                newnode = n not in self._node
                newdict = attr.copy()
                newdict.update(ndict)
            if newnode:
                self._node[n] = []
                self._node_attr[n] = self._node_attr_dict_factory()
            self._node_attr[n].update(newdict)

    def remove_node(self, n):
        """Remove a single node and all adjacent hyperedges.

        Parameters
        ----------
        n : node
           A node in the hypergraph

        Raises
        ------
        XGIError
           If n is not in the hypergraph.

        See Also
        --------
        remove_nodes_from

        """
        try:
            edge_neighbors = self._node[n]
            del self._node[n]
            del self._node_attr[n]
        except KeyError as e:
            raise XGIError(f"The node {n} is not in the graph.") from e
        for edge in edge_neighbors:
            self._edge[edge].remove(n)
            if not self._edge[edge]:
                del self._edge[edge]
                del self._edge_attr[edge]

    def remove_nodes_from(self, nodes):
        """Remove multiple nodes.

        Parameters
        ----------
        nodes : iterable
            An iterable of nodes.

        See Also
        --------
        remove_node

        """
        for n in nodes:
            if n not in self._node:
                warn(f"Node {n} not in hypergraph")
                continue
            self.remove_node(n)

    @property
    def nodes(self):
        """A NodeView of the hypergraph.

        Can be used as `H.nodes` for data lookup and for set-like operations.
        Can also be used as `H.nodes[id]` to return a
        dictionary of the node attributes.

        Returns
        -------
        NodeView
            Allows set-like operations over the nodes as well as node
            attribute dict lookup.

        Notes
        -----
        Membership tests and iterating over nodes can also be done via the hpyergraph.
        That is, ``n in H.nodes`` is equivalent to ``n in H``, and ``for n in H`` is
        equivalent to ``for n in H.nodes``.

        """
        nodes = NodeView(self)
        # Lazy View creation: overload the (class) property on the instance
        # Then future H.nodes use the existing View
        # setattr doesn't work because attribute already exists
        self.__dict__["nodes"] = nodes
        return nodes

    def has_node(self, n):
        """Whether the specified node is in the hypergraph.

        Identical to ``n in H`` and ``n in H.nodes``.

        Parameters
        ----------
        n : node

        Returns
        -------
        bool
            Whether the node exists in the hypergraph

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.has_node(1), 1 in H, 1 in H.nodes
        (True, True, True)
        >>> H.has_node(0), 0 in H, 0 in H.nodes
        (False, False, False)

        """
        try:
            return n in self._node
        except TypeError:
            return False

    def has_edge(self, edge):
        """Whether an edge is in the hypergraph.

        Parameters
        ----------
        edge : Iterable
            A container of hashables that specifies an edge.

        Returns
        -------
        bool
           Whether or not edge is as an edge in the hypergraph.

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.has_edge([1, 2])
        True
        >>> H.has_edge({1, 3})
        False

        """
        return set(edge) in (set(self.edges.members(e)) for e in self.edges)

    def add_edge(self, members, id=None, **attr):
        """Add one edge with optional attributes.

        Parameters
        ----------
        members : Iterable
            An iterable of the ids of the nodes contained in the new edge.
        id : hashable, default None
            Id of the new edge. If None, a unique numeric ID will be created.
        **attr : dict, optional
            Attributes of the new edge.

        Raises
        -----
        XGIError
            If `members` is empty.

        See Also
        --------
        add_edges_from : Add a collection of edges.

        Examples
        --------

        Add edges with ir without specifying an edge id.

        >>> H = xgi.Hypergraph()
        >>> H.add_edge([1, 2, 3])
        >>> H.add_edge([3, 4], id='myedge')
        >>> H.edges
        EdgeView((0, 'myedge'))

        Access attributes using square brackets.  By default no attributes are created.

        >>> H.edges[0]
        {}
        >>> H.add_edge([1, 4], color='red', place='peru')
        >>> H.edges
        EdgeView((0, 'myedge', 1))
        >>> H.edges[1]
        {'color': 'red', 'place': 'peru'}

        """
        members = list(members)
        if not members:
            raise XGIError("Cannot add an empty edge")

        uid = self._edge_uid() if not id else id
        self._edge[uid] = []
        for node in members:
            if node not in self._node:
                self._node[node] = []
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node[node].append(uid)
            self._edge[uid].append(node)

        self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
        self._edge_attr[uid].update(attr)

    def add_edges_from(self, ebunch_to_add, **attr):
        """Add multiple edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the container will be added to the
            graph. Each edge must be given as as a container of nodes
            or a container with the last entry as a dictionary.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edge : Add a single edge.
        add_weighted_edges_from : Convenient way to add weighted edges.

        Notes
        -----
        Adding the same edge twice will create a multi-edge. Currently
        cannot add empty edges; the method skips over them.

        """
        for e in ebunch_to_add:
            if isinstance(e[-1], dict):
                dd = e[-1]
                e = e[:-1]
            else:
                dd = {}
            if not e:
                continue

            uid = self._edge_uid()
            self._edge[uid] = []
            for n in e:
                if n not in self._node:
                    self._node[n] = []
                    self._node_attr[n] = self._node_attr_dict_factory()
                self._node[n].append(uid)
                self._edge[uid].append(n)

            self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
            self._edge_attr[uid].update(attr)
            self._edge_attr[uid].update(dd)

    def add_weighted_edges_from(self, ebunch, weight="weight", **attr):
        """Add multiple weighted edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the list or container will be added
            to the graph. The edges must be given as containers.
        weight : string, optional (default= 'weight')
            The attribute name for the edge weights to be added.
        attr : keyword arguments, optional (default= no attributes)
            Edge attributes to add/update for all edges.

        See Also
        --------
        add_edge : Add a single edge.
        add_edges_from : Add multiple edges.

        Notes
        -----
        Adding the same edge twice creates a multiedge.

        """
        try:
            self.add_edges_from(
                ((edge[:-1], {weight: edge[-1]}) for edge in ebunch), **attr
            )
        except KeyError:
            XGIError("Empty or invalid edges specified.")

    def add_node_to_edge(self, edge, node):
        """Add one node to an existing edge.

        If the node or edge IDs do not exist, they are created.

        Parameters
        ----------
        edge : hashable
            edge ID
        node : hashable
            node ID

        See Also
        --------
        add_node
        add_edge

        Examples
        --------
        >>> H = xgi.Hypergraph()
        >>> H.add_edge(['apple', 'banana'], 'fruits')
        >>> H.add_node_to_edge('fruits', 'pear')
        >>> H.add_node_to_edge('veggies', 'lettuce')
        >>> H.edges.members(dtype=dict)
        {'fruits': ['apple', 'banana', 'pear'], 'veggies': ['lettuce']}

        """
        if edge not in self._edge:
            self._edge[edge] = []
            self._edge_attr[edge] = {}
        if node not in self._node:
            self._node[node] = []
            self._node_attr[node] = {}
        self._edge[edge].append(node)
        self._node[node].append(edge)

    def remove_edge(self, id):
        """Remove one edge.

        Parameters
        ----------
        id : Hashable
            edge ID to remove

        Raises
        ------
        XGIError
            If no edge has that ID.

        See Also
        --------
        remove_edges_from : Remove multiple edges.

        """
        for node in self.edges.members(id):
            self._node[node].remove(id)
        del self._edge[id]
        del self._edge_attr[id]

    def remove_edges_from(self, ebunch):
        """Remove multiple edges.

        Parameters
        ----------
        ebunch: Iterable
            Edges to remove.

        See Also
        --------
        remove_edge : remove a single edge

        Notes
        -----
        Will fail silently if an edge in ebunch is not in the hypergraph.

        """
        for id in ebunch:
            for node in self.edges.members(id):
                self._node[node].remove(id)
            del self._edge[id]
            del self._edge_attr[id]

    def remove_node_from_edge(self, edge, node):
        """Remove a node from an existing edge.

        Parameters
        ----------
        edge : hashable
            The edge ID
        node : hashable
            The node ID

        Raises
        ------
        XGIError
            If either the node or edge does not exist.

        Notes
        -----
        If edge is left empty as a result of removing node from it, the edge is also
        removed.

        """
        self._edge[edge].remove(node)
        self._node[node].remove(edge)
        if len(self._edge[edge]) == 0:
            del self._edge[edge]
            del self._edge_attr[edge]

        try:
            self._node[node].remove(edge)
        except KeyError as e:
            raise XGIError(f"Node {node} not in the hypergraph") from e
        except ValueError as e:
            raise XGIError(f"Node {node} not in edge {edge}") from e

        if not self._edge[edge]:
            del self._edge[edge]
            del self._edge_attr[edge]

    def update(self, *, edges=None, nodes=None):
        """Add nodes or edges to the hypergraph.

        Parameters
        ----------
        edges : Iterable, optional
            Edges to be added.
        nodes : Iterable, optional
            Nodes to be added.

        See Also
        --------
        add_edges_from: Add multiple edges.
        add_nodes_from: Add multiple nodes.

        """
        if nodes:
            self.add_nodes_from(nodes)
        if edges:
            self.add_edges_from(edges)

    @property
    def edges(self):
        """An EdgeView of the hypergraph.

        The EdgeView provides set-like operations on the edge IDs as well as edge
        attribute lookup.

        Parameters
        ----------
        e : hashable or None (default = None)
            The edge ID to access

        Returns
        -------
        edges : EdgeView
            A view of edges in the hypergraph.

        """
        edges = EdgeView(self)
        # Lazy View creation: overload the (class) property on the instance
        # Then future H.edges use the existing View
        # setattr doesn't work because attribute already exists
        self.__dict__["edges"] = edges
        return edges

    def get_edge_data(self, id, default=None):
        """Get the attributes of an edge.

        This is identical to `H._edge_attr[id]` except the default is returned
        instead of an exception if the edge doesn't exist.

        Parameters
        ----------
        id : Hashable
            edge ID
        default: Any, default None
            Value to return if the edge ID is not found.

        Returns
        -------
        edge_dict : dictionary
            The edge attribute dictionary.

        """
        try:
            return self.edges[id]
        except KeyError:
            return default

    def degree(self, nbunch=None, weight=None, order=None, dtype="dict"):
        """A DegreeView for the Hypergraph.

        The degree is the number of edges adjacent to the node.
        The weighted node degree is the sum of the edge weights for
        edges incident to that node.

        This object provides an iterator for (node, degree) as well as
        lookup for the degree for a single node.

        Parameters
        ----------
        nbunch : single node, container, or None, default: None
            The view will only report edges incident to these nodes. If None
            is specified, the degree of all nodes is computed.
        weight : string or None, default: None
           The name of an edge attribute that holds the numerical value used
           as a weight.  If None, then each edge has weight 1.
           The degree is the sum of the edge weights adjacent to the node.
        order : int or None, default: None
            The size edges for which to compute the degree. If None is
            specified, all edges are considered.
        dtype : str, default: "dict"
            The datatype to return


        Returns
        -------
        If a single node is requested
        float or int
            Degree of the node

        OR if multiple nodes are requested
        DegreeView object
            The degrees of the hypergraph capable of iterating (node, degree) pairs

        """
        degree = DegreeView(
            self, nbunch=nbunch, weight=weight, order=order, dtype=dtype
        )

        # handles the single node case.
        if nbunch in self:
            return degree[nbunch]
        return degree

    def edge_size(self, ebunch=None, weight=None, dtype="dict"):
        """A EdgeSizeView for the Hypergraph as H.edge_size or H.edge_size().

        The edge degree is the number of nodes in that edge, or the edge size.
        The weighted edge degree is the sum of the node weights for
        nodes in that edge.

        This object provides an iterator for (edge, degree) as well as
        lookup for the degree for a single edge.

        Parameters
        ----------
        ebunch : single edge, container, or all edges (default= all edges)
            The view will only report sizes of these edges.
        weight : string or None, optional (default=None)
           The name of an node attribute that holds the numerical value used
           as a weight.  If None, then each node has weight 1.
           The size is the sum of the node weights adjacent to the edge.
        dtype : str, default: "dict"
            The datatype to return

        Returns
        -------
        If a single edge is requested
        int
            size of the edge.

        OR if multiple edges are requested
        EdgeSizeView object
            The sizes of the hypergraph edges capable of iterating (edge, size) pairs

        """
        edge_sizes = EdgeSizeView(self, ebunch=ebunch, weight=weight, dtype=dtype)
        if ebunch in self:
            return edge_sizes[ebunch]
        return edge_sizes

    def clear(self, hypergraph_attr=True):
        """Remove all nodes and edges from the graph.

        Also removes node and edge attribues, and optionally hypergraph attributes.

        Parameters
        ----------
        hypergraph_attr : bool, default True
            Whether to remove hypergraph attributes as well

        """
        self._node.clear()
        self._node_attr.clear()
        self._edge.clear()
        self._edge_attr.clear()
        if hypergraph_attr:
            self._hypergraph.clear()

    def clear_edges(self):
        """Remove all edges from the graph without altering any nodes."""
        for node in self.nodes:
            self._node[node] = {}
        self._edge.clear()
        self._edge_attr.clear()

    def copy(self, as_view=False):
        """A copy of the hypergraph.

        The copy method by default returns a deep copy of the hypergraph
        and attributes. Use the "as_view" flag to for a frozen copy of
        the hypergraph with references to the original

        If `as_view` is True then a view is returned instead of a copy.

        Parameters
        ----------
        as_view : bool, optional (default=False)
            If True, the returned hypergraph view provides a read-only view
            of the original hypergraph without actually copying any data.

        Returns
        -------
        H : Hypergraph
            A copy of the hypergraph.

        Notes
        -----
        All copies reproduce the hypergraph structure, but data attributes
        may be handled in different ways. There are two options that this
        method provides.

        Deepcopy -- A "deepcopy" copies the graph structure as well as
        all data attributes and any objects they might contain.
        The entire hypergraph object is new so that changes in the copy
        do not affect the original object. (see Python's copy.deepcopy)

        View -- Inspired by dict-views, graph-views act like read-only
        versions of the original graph, providing a copy of the original
        structure without requiring any memory for copying the information.

        See the Python copy module for more information on shallow
        and deep copies, https://docs.python.org/3/library/copy.html.

        """
        if as_view is True:
            return xgi.hypergraphviews.generic_hypergraph_view(self)
        H = self.__class__()
        H._hypergraph = deepcopy(self._hypergraph)
        H._node = deepcopy(self._node)
        H._node_attr = deepcopy(self._node_attr)
        H._edge = deepcopy(self._edge)
        H._edge_attr = deepcopy(self._edge_attr)
        return H

    def dual(self):
        """The dual of the hypergraph.

        In the dual, nodes become edges and edges become nodes.

        Returns
        -------
        Hypergraph
            The dual of the hypergraph.

        """
        dual = self.__class__()
        dual._hypergraph = deepcopy(self._hypergraph)
        dual._node = deepcopy(self._edge)
        dual._node_attr = deepcopy(self._edge_attr)
        dual._edge = deepcopy(self._node)
        dual._edge_attr = deepcopy(self._node_attr)
        return dual

    def subhypergraph(self, nodes):
        """The subhypergraph induced by the specified nodes.

        The induced subhypergraph of the hypergraph contains the nodes in `nodes`
        and the edges that only contain those nodes.

        Parameters
        ----------
        nodes : list, iterable
            A container of nodes which will be iterated through once.

        Returns
        -------
        H : SubHypergraphView
            A subhypergraph view of the hypergraph. The hypergraph structure
            cannot be changed but node/edge attributes can and are shared with the
            original hypergraph.

        Notes
        -----
        The hypergraph, edge and node attributes are shared with the original
        hypergraph. Changes to the hypergraph structure is ruled out by the view,
        but changes to attributes are reflected in the original hypergraph.

        For an inplace reduction of a hypergraph to a subhypergraph you can remove nodes:
        H.remove_nodes_from([n for n in H if n not in set(nodes)])

        """
        induced_nodes = self.nbunch_iter(nodes)
        subhypergraph = xgi.hypergraphviews.subhypergraph_view
        return subhypergraph(self, induced_nodes, None)

    def edge_subhypergraph(self, edges):
        """The subhypergraph with only the edges specified.

        The list of nodes is not affected, potentially leading to a disconnected
        hypergraph.

        Parameters
        ----------
        edges : list, iterable
            A container of edge ids which will be iterated through once.

        Returns
        -------
        H : SubHypergraphView
            A subhypergraph view of the hypergraph. The hypergraph structure
            cannot be changed but node/edge attributes can and are shared with the
            original hypergraph.

        Notes
        -----
        The hypergraph, edge and node attributes are shared with the original
        hypergraph. Changes to the hypergraph structure is ruled out by the view,
        but changes to attributes are reflected in the original hypergraph.

        For an inplace reduction of a hypergraph to a subhypergraph you can remove nodes:
        H.remove_edges_from([n for n in H if n not in set(nodes)])

        """
        subhypergraph = xgi.hypergraphviews.subhypergraph_view
        return subhypergraph(self, None, edges)

    def arbitrary_subhypergraph(self, nodes, edges):
        """The subhypergraph with specified nodes and edges.

        This subhypergraph contains the list of nodes induced by the edges
        as well as additional nodes specified.

        Parameters
        ----------
        nodes : list, iterable
            A container of nodes which will be iterated through once.

        edges : list, iterable
            A container of edge ids which will be iterated through once.

        Returns
        -------
        H : SubHypergraphView
            A subhypergraph view of the hypergraph. The hypergraph structure
            cannot be changed but node/edge attributes can and are shared with the
            original hypergraph.

        Notes
        -----
        The hypergraph, edge and node attributes are shared with the original
        hypergraph. Changes to the hypergraph structure is ruled out by the view,
        but changes to attributes are reflected in the original hypergraph.

        """
        subhypergraph = xgi.hypergraphviews.subhypergraph_view
        return subhypergraph(self, nodes, edges)

    def nbunch_iter(self, nbunch=None):
        """Returns an iterator over nodes contained in nbunch.

        The nodes in nbunch are checked for membership in the hypergraph
        and if not are silently ignored.

        Parameters
        ----------
        nbunch : single node, container, or all nodes (default= all nodes)
            The view will only report edges incident to these nodes.

        Returns
        -------
        niter : iterator
            An iterator over nodes in nbunch that are also in the hypergraph.
            If nbunch is None, iterate over all nodes in the hypergraph.

        Raises
        ------
        XGIError
            If nbunch is not a node or sequence of nodes.
            If a node in nbunch is not hashable.

        See Also
        --------
        Hypergraph.__iter__

        Notes
        -----
        When nbunch is an iterator, the returned iterator yields values
        directly from nbunch, becoming exhausted when nbunch is exhausted.

        To test whether nbunch is a single node, one can use
        "if nbunch in self:", even after processing with this routine.

        If nbunch is not a node or a (possibly empty) sequence/iterator
        or None, a :exc:`XGIError` is raised.  Also, if any object in
        nbunch is not hashable, a :exc:`XGIError` is raised.

        """
        if nbunch is None:  # include all nodes via iterator
            bunch = iter(self._node)
        elif nbunch in self:  # if nbunch is a single node
            bunch = iter([nbunch])
        else:  # if nbunch is a sequence of nodes

            def bunch_iter(nlist, nodes):
                try:
                    for n in nlist:
                        if n in nodes:
                            yield n
                except TypeError as e:
                    exc, message = e, e.args[0]
                    # capture error for non-sequence/iterator nbunch.
                    if "iter" in message:
                        exc = XGIError("nbunch is not a node or a sequence of nodes.")
                    # capture error for unhashable node.
                    if "hashable" in message:
                        exc = XGIError(
                            f"Node {n} in sequence nbunch is not a valid node."
                        )
                    raise exc

            bunch = bunch_iter(nbunch, self._node)
        return bunch

    def max_edge_order(self):
        """The maximum order of edges in the hypergraph.

        Returns
        -------
        int
            Maximum order of edges in hypergraph.

        """
        if self._edge:
            d_max = max(len(edge) for edge in self._edge.values()) - 1
        else:
            d_max = 0 if self._node else None
        return d_max

    def is_possible_order(self, d):
        """Whether the specified order is between 1 and the maximum order.

        Parameters
        ----------
        d : int
            Order for which to check.

        Returns
        -------
        bool
            Whether `d` is a possible order.

        """
        d_max = self.max_edge_order()
        return (d >= 1) and (d <= d_max)

    def singleton_edges(self):
        """Edges with a single member.

        Returns
        -------
        EdgeView
            View of the edges with a single member.

        """
        return self.edges(order=0)

    def remove_singleton_edges(self):
        """Removes all singletons edges from the hypergraph"""
        singleton_ids = [
            id_ for id_, members in self._edge.items() if len(members) == 1
        ]
        self.remove_edges_from(singleton_ids)

    def isolates(self, ignore_singletons=True):
        """Nodes that belong to no edges.

        When ignore_singletons is True (default), a node is considered isolated frmo the
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
        set
            Isolated nodes.

        See Also
        --------
        remove_isolates

        """
        nodes_in_edges = set()
        for idx in self.edges:
            edge = self.edges.members(idx)
            if ignore_singletons and len(edge) == 1:
                continue
            nodes_in_edges = nodes_in_edges.union(edge)
        return set(self.nodes) - nodes_in_edges

    def remove_isolates(self, ignore_singletons=True):
        """Remove all nodes that belong to no edges.

        Parameters
        ----------
        ignore_singletons : bool, default False
            Whether to consider singleton edges when searching for isolated nodes.

        See Also
        --------
        isolates

        """
        self.remove_nodes_from(self.isolates(ignore_singletons))

    def duplicate_edges(self):
        """A list of all duplicate edges.

        Returns
        -------
        list
            All edges with a duplicate.

        See also
        --------
        remove_duplicates

        """
        edges = [tuple(e) for e in self._edge.values()]
        edges_unique, counts = np.unique(edges, return_counts=True)
        return list(edges_unique[np.where(counts > 1)])

    def is_uniform(self):
        """Order of uniformity if the hypergraph is uniform, or False.

        A hypergraph is uniform if all its edges have the same order.

        Returns d if the hypergraph is d-uniform, that is if all edges
        in the hypergraph (excluding singletons) have the same degree d.
        Returns False if not uniform.

        Returns
        -------
        d : int or False
            If the hypergraph is d-uniform, return d, or False otherwise.

        Examples
        --------
        This function can be used as a boolean check:

        >>> H = xgi.Hypergraph([(0, 1, 2), (1, 2, 3), (2, 3, 4)])
        >>> H.is_uniform()
        2
        >>> if H.is_uniform(): print('H is uniform!')
        H is uniform!

        """
        edge_sizes = {len(members) for _, members in self._edge.items()}
        if 1 in edge_sizes:
            edge_sizes.remove(1)  # discard singleton edges

        if not edge_sizes or len(edge_sizes) != 1:
            return False

        return edge_sizes.pop() - 1  # order of all edges
