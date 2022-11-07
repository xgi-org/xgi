"""Base class for undirected hypergraphs."""
from collections.abc import Hashable, Iterable
from copy import deepcopy
from itertools import count
from warnings import warn

from ..exception import IDNotFound, XGIError
from .reportviews import EdgeView, NodeView

__all__ = ["Hypergraph"]


class IDDict(dict):
    """A dict that holds (node or edge) IDs.

    For internal use only.  Adds input validation functionality to the internal dicts
    that hold nodes and edges in a network.

    """

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError as e:
            raise IDNotFound(f"ID {item} not found") from e

    def __setitem__(self, item, value):
        if item is None:
            raise XGIError("None cannot be a node or edge")
        try:
            return dict.__setitem__(self, item, value)
        except TypeError as e:
            raise TypeError(f"ID {item} not a valid type") from e

    def __delitem__(self, item):
        try:
            return dict.__delitem__(self, item)
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

    The `attr` keyword arguments are added as hypergraph attributes. To add node or edge
    attributes see :meth:`add_node` and :meth:`add_edge`.

    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `Hypergraph` class.  For more details, see the
    `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

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
        self._edge_uid = count()
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
            # This import needs to happen when this function is called, not when it is
            # defined.  Otherwise, a circular import error would happen.
            from ..convert import convert_to_hypergraph

            convert_to_hypergraph(incoming_data, create_using=self)
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
        word = "nodes"
        if stat is None:
            stat = getattr(self.edges, attr, None)
            word = "edges"
        if stat is None:
            word = None
            raise AttributeError(
                f"{attr} is not a method of Hypergraph or a recognized NodeStat or EdgeStat"
            )

        def func(node=None, *args, **kwargs):
            val = stat(*args, **kwargs).asdict()
            return val if node is None else val[node]

        func.__doc__ = f"""Equivalent to H.{word}.{attr}.asdict(). For accepted *args and
        **kwargs, see documentation of H.{word}.{attr}."""

        return func

    def __lshift__(self, H2):
        """Adds the edges of a hypergraph to the current hypergraph
        and updates the attributes.

        The node/edge attributes of the new hypergraph take precedence.

        Relabels all the edge IDs to preserve all the edges but
        keeps the node labels the same.

        Parameters
        ----------
        H2 : Hypergraph
            The hypergraph to update with.

        Returns
        -------
        Hypergraph
            The updated hypergraph

        Notes
        -----
        Addition is not quite commutative; the attributes of nodes and edges
        may be overwritten depending on whether they are first or second
        to be added. In addition, the edge IDs are assigned based on the order
        in which the edges are added, but does not functionally change the
        structure of the hypergraph.

        Examples
        --------

        >>> import xgi
        >>> H1 = xgi.Hypergraph([[1, 2], [2, 3]])
        >>> H2 = xgi.Hypergraph([[1, 3, 4]])
        >>> H = H1 << H2
        >>> H.edges.members()
        [{1, 2}, {2, 3}, {1, 3, 4}]
        """
        tempH = Hypergraph()
        tempH.add_edges_from(zip(self._edge.values(), self._edge_attr.values()))
        tempH.add_nodes_from(zip(self._node.keys(), self._node_attr.values()))

        tempH.add_edges_from(zip(H2._edge.values(), H2._edge_attr.values()))
        tempH.add_nodes_from(zip(H2._node.keys(), H2._node_attr.values()))

        tempH._hypergraph = deepcopy(self._hypergraph)
        tempH._hypergraph.update(deepcopy(H2._hypergraph))

        return tempH

    @property
    def nodes(self):
        """A :class:`NodeView` of this network."""
        return self._nodeview

    @property
    def edges(self):
        """An :class:`EdgeView` of this network."""
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
            self._node[node] = set()
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
                self._node[n] = set()
                self._node_attr[n] = self._node_attr_dict_factory()
            self._node_attr[n].update(newdict)

    def remove_node(self, n, strong=False):
        """Remove a single node.

        The removal may be weak (default) or strong.  In weak removal, the node is
        removed from each of its containing edges.  If it is contained in any singleton
        edges, then these are also removed.  In strong removal, all edges containing the
        node are removed, regardless of size.

        Parameters
        ----------
        n : node
            A node in the hypergraph

        strong : bool (default False)
            Whether to execute weak or strong removal.

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

        if strong:
            for edge in edge_neighbors:
                del self._edge[edge]
                del self._edge_attr[edge]
        else:  # weak removal
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

        Add edges with or without specifying an edge id.

        >>> import xgi
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
        members = set(members)
        if not members:
            raise XGIError("Cannot add an empty edge")

        uid = next(self._edge_uid) if not id else id
        self._edge[uid] = set()
        for node in members:
            if node not in self._node:
                self._node[node] = set()
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node[node].add(uid)
            self._edge[uid].add(node)

        self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
        self._edge_attr[uid].update(attr)

    def add_edges_from(self, ebunch_to_add, **attr):
        """Add multiple edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : Iterable

            An iterable of edges.  This may be a dict of the form `{edge_id:
            edge_members}`, or it may be an iterable of iterables, where each element
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

        When specifying edges by their members only, numeric edge IDs will be assigned
        automatically.

        >>> H.add_edges_from([[0, 1], [1, 2], [2, 3, 4]])
        >>> H.edges.members(dtype=dict)
        {0: {0, 1}, 1: {1, 2}, 2: {2, 3, 4}}

        Custom edge ids can be specified using a dict.

        >>> H = xgi.Hypergraph()
        >>> H.add_edges_from({'one': [0, 1], 'two': [1, 2], 'three': [2, 3, 4]})
        >>> H.edges.members(dtype=dict)
        {'one': {0, 1}, 'two': {1, 2}, 'three': {2, 3, 4}}

        You can use the dict format to easily add edges from another hypergraph.

        >>> H2 = xgi.Hypergraph()
        >>> H2.add_edges_from(H.edges.members(dtype=dict))
        >>> H.edges == H2.edges
        True

        Alternatively, edge ids can be specified using an iterable of 2-tuples.

        >>> H = xgi.Hypergraph()
        >>> H.add_edges_from([([0, 1], 'one'), ([1, 2], 'two'), ([2, 3, 4], 'three')])
        >>> H.edges.members(dtype=dict)
        {'one': {0, 1}, 'two': {1, 2}, 'three': {2, 3, 4}}

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
                    self._edge[uid] = set(members)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e
                for n in members:
                    if n not in self._node:
                        self._node[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node[n].add(uid)
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
                members, uid, eattr = e, next(self._edge_uid), {}
            elif format2:
                members, uid, eattr = e[0], e[1], {}
            elif format3:
                members, uid, eattr = e[0], next(self._edge_uid), e[1]
            elif format4:
                members, uid, eattr = e[0], e[1], e[2]

            try:
                self._edge[uid] = set(members)
            except TypeError as e:
                raise XGIError("Invalid ebunch format") from e

            for n in members:
                if n not in self._node:
                    self._node[n] = set()
                    self._node_attr[n] = self._node_attr_dict_factory()
                self._node[n].add(uid)

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

        Examples
        --------
        >>> import xgi
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

    def double_edge_swap(self, n_id1, n_id2, e_id1, e_id2):
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

        Raises
        ------
        XGIError
            If loopy hyperedges are created
        IDNotFound
            If user specifies nodes or edges that do not exist or
            nodes that are not part of edges.

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [3, 4]])
        >>> H.double_edge_swap(1, 4, 0, 1)
        >>> H.edges.members()
        [{2, 3, 4}, {1, 3}]

        """
        # Assign edges to modify
        try:

            temp_memberships1 = list(self._node[n_id1])
            temp_memberships1[temp_memberships1.index(e_id1)] = e_id2

            temp_memberships2 = list(self._node[n_id2])
            temp_memberships2[temp_memberships2.index(e_id2)] = e_id1

            temp_members1 = list(self._edge[e_id1])
            temp_members1[temp_members1.index(n_id1)] = n_id2

            temp_members2 = list(self._edge[e_id2])
            temp_members2[temp_members2.index(n_id2)] = n_id1

        except ValueError as e:
            raise XGIError(
                "One of the nodes specified doesn't belong to the specified edge."
            ) from e

        if len(set(temp_members1)) < len(set(self._edge[e_id1])) or len(
            set(temp_members2)
        ) < len(set(self._edge[e_id2])):
            raise XGIError("This will create a loopy hyperedge.")

        self._node[n_id1] = set(temp_memberships1)
        self._node[n_id2] = set(temp_memberships2)

        self._edge[e_id1] = set(temp_members1)
        self._edge[e_id2] = set(temp_members2)

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
        >>> import xgi
        >>> H = xgi.Hypergraph()
        >>> H.add_edge(['apple', 'banana'], 'fruits')
        >>> H.add_node_to_edge('fruits', 'pear')
        >>> H.add_node_to_edge('veggies', 'lettuce')
        >>> d = H.edges.members(dtype=dict)
        >>> {id: sorted(list(e)) for id, e in d.items()}
        {'fruits': ['apple', 'banana', 'pear'], 'veggies': ['lettuce']}

        """
        if edge not in self._edge:
            self._edge[edge] = set()
            self._edge_attr[edge] = {}
        if node not in self._node:
            self._node[node] = set()
            self._node_attr[node] = {}
        self._edge[edge].add(node)
        self._node[node].add(edge)

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

        Raises
        ------
        xgi.exception.IDNotFound
            If an id in ebunch is not part of the network.

        See Also
        --------
        remove_edge : remove a single edge.

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
        try:
            self._node[node].remove(edge)
        except KeyError as e:
            raise XGIError(f"Node {node} not in the hypergraph") from e
        except ValueError as e:
            raise XGIError(f"Node {node} not in edge {edge}") from e

        try:
            self._edge[edge].remove(node)
        except KeyError as e:
            raise XGIError(f"Edge {edge} not in the hypergraph") from e
        except ValueError as e:
            raise XGIError(f"Edge {edge} does not contain node {node}") from e

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
            self._node[node] = set()
        self._edge.clear()
        self._edge_attr.clear()

    def copy(self):
        """A deep copy of the hypergraph.

        A deep copy of the hypergraph, including node, edge, and hypergraph attributes.

        Returns
        -------
        H : Hypergraph
            A copy of the hypergraph.

        Notes
        -----

        There is no guarantee that performing similar operations on a hypergraph and its
        copy after the copy is made will yield the same results.  For example,

        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [4], [5, 6], [6, 7, 8]])
        >>> H.add_edge([1, 3, 5], id=10)
        >>> K = H.copy()
        >>> H.add_edge([2, 4]); K.add_edge([2, 4]);
        >>> list(H.edges) == list(K.edges)
        False

        The difference is the IDs assigned to new edges:

        >>> H.edges
        EdgeView((0, 1, 2, 3, 10, 4))
        >>> K.edges
        EdgeView((0, 1, 2, 3, 10, 11))

        """
        copy = self.__class__()
        nn = self.nodes
        copy.add_nodes_from((n, deepcopy(attr)) for n, attr in nn.items())
        ee = self.edges
        copy.add_edges_from(
            (e, id, deepcopy(self.edges[id]))
            for id, e in ee.members(dtype=dict).items()
        )
        copy._hypergraph = deepcopy(self._hypergraph)

        # If we don't set the start of copy._edge_uid correctly, it will start at 0,
        # which will overwrite any existing edges when calling add_edge().  First, we
        # use the somewhat convoluted float(e).is_integer() instead of using
        # isinstance(e, int) because there exist integer-like numeric types (such as
        # np.int32) which fail the isinstance() check.
        edges_with_int_id = [int(e) for e in self.edges if float(e).is_integer()]

        # Then, we set the start at one plus the maximum edge ID that is an integer,
        # because count() only yields integer IDs.
        start = max(edges_with_int_id) + 1 if edges_with_int_id else 0
        copy._edge_uid = count(start=start)

        return copy

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

    def cleanup(
        self,
        isolates=False,
        singletons=False,
        multiedges=False,
        relabel=True,
        in_place=True,
    ):
        """Removes potentially undesirable artifacts from the hypergraph.

        Parameters
        ----------
        isolates : bool, optional
            Whether isolated nodes are allowed, by default False
        singletons : bool, optional
            Whether singleton edges are allowed, by default False
        multiedges : bool, optional
            Whether multiedges are allowed, by default False
        relabel : bool, optional
            Whether to convert all node and edge labels to sequential integers, by default True
        in_place : bool, optional
            Whether to modify the current hypergraph or output a new one, by default True
        """
        if in_place:
            if not multiedges:
                self.remove_edges_from(self.edges.duplicates())
            if not singletons:
                self.remove_edges_from(self.edges.singletons())
            if not isolates:
                self.remove_nodes_from(self.nodes.isolates())
            if relabel:
                from .function import convert_labels_to_integers

                temp = convert_labels_to_integers(self).copy()

                nn = temp.nodes
                ee = temp.edges

                self.clear()
                self.add_nodes_from((n, deepcopy(attr)) for n, attr in nn.items())
                self.add_edges_from(
                    (e, id, deepcopy(temp.edges[id]))
                    for id, e in ee.members(dtype=dict).items()
                )
                self._hypergraph = deepcopy(temp._hypergraph)
        else:
            H = self.copy()
            if not multiedges:
                H.remove_edges_from(H.edges.duplicates())
            if not singletons:
                H.remove_edges_from(H.edges.singletons())
            if not isolates:
                H.remove_nodes_from(H.nodes.isolates())
            if relabel:
                from .function import convert_labels_to_integers

                H = convert_labels_to_integers(H)

            return H
