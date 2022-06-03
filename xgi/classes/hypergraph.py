"""Base class for undirected hypergraphs."""
from collections.abc import Hashable, Iterable
from copy import deepcopy
from warnings import warn

import numpy as np

import xgi
import xgi.convert as convert
from xgi.classes.reportviews import EdgeView, NodeView
from xgi.exception import IDNotFound, XGIError
from xgi.utils import XGICounter

__all__ = ["Hypergraph"]


class IDDict(dict):
    """A dict that holds (node or edge) IDs.

    For internal use only.  Adds input validation functionality to the internal dicts
    that hold nodes and edges in a network.

    """

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

    def __delitem__(self, item):
        try:
            return super().__delitem__(item)
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

        self._nodeview = NodeView(self)
        """A :class:`~xgi.classes.reportviews.NodeView` of the hypergraph."""

        self._edgeview = EdgeView(self)
        """An :class:`~xgi.classes.reportviews.EdgeView` of the hypergraph."""

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

    def __getattr__(self, attr):
        stat = getattr(self.nodes, attr, None)
        if stat is None:
            stat = getattr(self.edges, attr, None)
        if stat is None:
            raise AttributeError(
                f'stat "{attr}" not among available node or edge stats'
            )

        def func(node=None, /, *args, **kwargs):
            val = stat(*args, **kwargs).asdict()
            return val if node is None else val[node]

        return func

    @property
    def nodes(self):
        return self._nodeview

    @property
    def edges(self):
        return self._edgeview

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
        nodes_for_adding : iterable
            An iterable of nodes (list, dict, set, etc.).
            OR
            An iterable of (node, attribute dict) tuples.
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
        edge_neighbors = self._node[n]
        del self._node[n]
        del self._node_attr[n]
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

    def has_edge(self, edge):
        """Whether an edge is in the hypergraph.

        Parameters
        ----------
        edge : Iterable
            An iterable of hashables that specifies an edge by its member nodes.

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
        ebunch_to_add : Iterable

            An iterable of edges.  This may be a dict of the form `{edge_id:
            edge_members}`, or it may be an iterable of iterables, wher each element
            contains the members of the edge specified as valid node IDs.
            Alternatively, each element could also be a tuple in any of the following
            formats:

            * Format 1: 2-tuple (members, edge_id), or
            * Format 2: 2-tuple (members, attr), or
            * Format 3: 3-tuple (members, edge_id, attr),

            where `members` is an iterable of node IDs, `edge_id` is a hashable to use
            as edge ID, and `attr` is a dict of attributes. The first and second formats
            are unambiguous because `attr` dicts are not hashable, while `id`s must be.
            In Formats 1-3, each element of `ebunch_to_add` must have the same length,
            i.e. you cannot mix different formats.  The iterables containing edge
            members cannot be strings.

        attr : \*\*kwargs, optional
            Additional attributes to be assigned to all edges. Attribues specified via
            `ebunch_to_add` take precedence over `attr`.

        See Also
        --------
        add_edge : Add a single edge.
        add_weighted_edges_from : Convenient way to add weighted edges.

        Notes
        -----
        Adding the same edge twice will create a multi-edge. Currently
        cannot add empty edges; the method skips over them.

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph()

        When Specify edges by their members only, numeric edge IDs will be assigned
        automatically.

        >>> H.add_edges_from([[0, 1], [1, 2], [2, 3, 4]])
        >>> H.edges.members(dtype=dict)
        {0: [0, 1], 1: [1, 2], 2: [2, 3, 4]}

        Custom edge ids can be specified using a dict.

        >>> H = xgi.Hypergraph()
        >>> H.add_edges_from({'one': [0, 1], 'two': [1, 2], 'three': [2, 3, 4]})
        >>> H.edges.members(dtype=dict)
        {'one': [0, 1], 'two': [1, 2], 'three': [2, 3, 4]}

        You can use the dict format to easily add edges from another hypergraph.

        >>> H2 = xgi.Hypergraph()
        >>> H2.add_edges_from(H.edges.members(dtype=dict))
        >>> H.edges == H2.edges
        True

        Alternatively, edge ids can be specified using an iterable of 2-tuples.

        >>> H = xgi.Hypergraph()
        >>> H.add_edges_from([([0, 1], 'one'), ([1, 2], 'two'), ([2, 3, 4], 'three')])
        >>> H.edges.members(dtype=dict)
        {'one': [0, 1], 'two': [1, 2], 'three': [2, 3, 4]}

        Attributes for each edge may be specified using a 2-tuple for each edge.
        Numeric IDs will be assigned automatically.

        >>> H = xgi.Hypergraph()
        >>> edges = [
        ...     ([0, 1], {'color': 'red'}),
        ...     ([1, 2], {'age': 30}),
        ...     ([2, 3, 4], {'color': 'blue', 'age': 40}),
        ... ]
        >>> H.add_edges_from(edges)
        >>> {e: H.edges[e] for e in H.edges}
        {0: {'color': 'red'}, 1: {'age': 30}, 2: {'color': 'blue', 'age': 40}}

        Attributes and custom IDs may be specified using a 3-tuple for each edge.

        >>> H = xgi.Hypergraph()
        >>> edges = [
        ...     ([0, 1], 'one', {'color': 'red'}),
        ...     ([1, 2], 'two', {'age': 30}),
        ...     ([2, 3, 4], 'three', {'color': 'blue', 'age': 40}),
        ... ]
        >>> H.add_edges_from(edges)
        >>> {e: H.edges[e] for e in H.edges}
        {'one': {'color': 'red'}, 'two': {'age': 30}, 'three': {'color': 'blue', 'age': 40}}

        """
        # format 5 is the easiest one
        if isinstance(ebunch_to_add, dict):
            for uid, members in ebunch_to_add.items():
                try:
                    self._edge[uid] = list(members)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e
                for n in members:
                    if n not in self._node:
                        self._node[n] = []
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node[n].append(uid)
                self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
            return

        # in formats 1-4 we only know that ebunch_to_add is an iterable, so we iterate
        # over it and use the firs element to determine which format we are working with
        new_edges = iter(ebunch_to_add)
        try:
            first_edge = next(new_edges)
        except StopIteration:
            return
        try:
            first_elem = list(first_edge)[0]
        except TypeError:
            first_elem = None

        format1, format2, format3, format4 = False, False, False, False
        if isinstance(first_elem, Iterable):
            if all(isinstance(e, str) for e in first_edge):
                format1 = True
            elif len(first_edge) == 2 and issubclass(type(first_edge[1]), Hashable):
                format2 = True
            elif len(first_edge) == 2:
                format3 = True
            elif len(first_edge) == 3:
                format4 = True
        else:
            format1 = True

        if (format1 and isinstance(first_edge, str)) or (
            not format1 and isinstance(first_elem, str)
        ):
            raise XGIError("Members cannot be specified as a string")

        # now we may iterate over the rest
        e = first_edge
        while True:
            if format1:
                members, uid, eattr = e, self._edge_uid(), {}
            elif format2:
                members, uid, eattr = e[0], e[1], {}
            elif format3:
                members, uid, eattr = e[0], self._edge_uid(), e[1]
            elif format4:
                members, uid, eattr = e[0], e[1], e[2]

            try:
                self._edge[uid] = list(members)
            except TypeError as e:
                raise XGIError("Invalid ebunch format") from e

            for n in members:
                if n not in self._node:
                    self._node[n] = []
                    self._node_attr[n] = self._node_attr_dict_factory()
                self._node[n].append(uid)

            self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
            self._edge_attr[uid].update(attr)
            self._edge_attr[uid].update(eattr)

            try:
                e = next(new_edges)
            except StopIteration:
                break

    def add_weighted_edges_from(self, ebunch, weight="weight", **attr):
        """Add multiple weighted edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : iterable of edges
            Each edge given in the list or container will be added
            to the graph. The edges must be given as tuples of
            the form (node1, node2, ..., noden, weight).
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

        Example
        -------
        >>> H = xgi.Hypergraph()
        >>> edges = [(0, 1, 0.3), (0, 2, 0.8)]
        >>> H.add_weighted_edges_from(edges)
        >>> H.edges[0]
        {'weight': 0.3}


        """
        try:
            self.add_edges_from(
                ((edge[:-1], {weight: edge[-1]}) for edge in ebunch), **attr
            )
        except KeyError:
            XGIError("Empty or invalid edges specified.")

    def double_edge_swap(self, n_id1, n_id2, e_id1, e_id2, is_loopy=True):
        """Swap the edge memberships of two selected nodes, given two edges.

        Parameters
        ----------
        n_id1 : hashable
            The ID of the first node, originally a member of the first edge.
        n_id2 : hashable
            The ID of the second node, originally a member of the second edge.
        e_id1 : hashable
            The ID of the first edge.
        e_id2 : hashable
            The ID of the second edge.
        is_loopy : bool, default True
            Whether edges can be loopy.

        Raises
        ------
        XGIError
            If loopy hyperedges are created
        IDNotFound
            If user specifies nodes or edges that do not exist or
            nodes that are not part of edges.

        Examples
        --------
        Swap the memberships of two nodes.

        >>> H = xgi.Hypergraph([[1, 2, 3], [3, 4]])
        >>> H.double_edge_swap(1, 4, 0, 1)
        >>> H.edges.members()
        [[4, 2, 3], [3, 1]]
        """
        # Assign edges to modify
        try:
            temp_memberships1 = list(self._node[n_id1])
            temp_memberships1[self._node[n_id1].index(e_id1)] = e_id2

            temp_memberships2 = list(self._node[n_id2])
            temp_memberships2[self._node[n_id2].index(e_id2)] = e_id1

            temp_members1 = list(self._edge[e_id1])
            temp_members1[self._edge[e_id1].index(n_id1)] = n_id2

            temp_members2 = list(self._edge[e_id2])
            temp_members2[self._edge[e_id2].index(n_id2)] = n_id1

        except ValueError:
            raise XGIError(
                "One of the nodes specified doesn't belong to the specified edge."
            )

        if not is_loopy and (
            len(set(temp_members1)) < len(set(self._edge[e_id1]))
            or len(set(temp_members2)) < len(set(self._edge[e_id2]))
        ):
            raise XGIError("This will create a loopy hyperedge.")

        self._node[n_id1] = temp_memberships1
        self._node[n_id2] = temp_memberships2

        self._edge[e_id1] = temp_members1
        self._edge[e_id2] = temp_members2

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

    def copy(self):
        """A deep copy of the hypergraph.

        A deep copy of the hypergraph, including node, edge, and hypergraph attributes.

        Returns
        -------
        H : Hypergraph
            A copy of the hypergraph.

        """
        return xgi.hypergraphviews.subhypergraph(self)

    def dual(self):
        """The dual of the hypergraph.

        In the dual, nodes become edges and edges become nodes.

        Returns
        -------
        Hypergraph
            The dual of the hypergraph.

        """
        dual = self.__class__()
        nn = self.nodes
        dual.add_edges_from(
            (nn.memberships(n), n, deepcopy(attr)) for n, attr in nn.items()
        )
        ee = self.edges
        dual.add_nodes_from((e, deepcopy(attr)) for e, attr in ee.items())
        dual._hypergraph = deepcopy(self._hypergraph)

        return dual

    def singleton_edges(self):
        """Edges with a single member.

        Returns
        -------
        EdgeView
            View of the edges with a single member.

        """
        return self.edges.filterby("order", 0)

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
