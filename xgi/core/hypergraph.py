"""Base class for undirected hypergraphs."""

import random
from collections import defaultdict
from collections.abc import Hashable, Iterable
from copy import copy, deepcopy
from itertools import count
from warnings import warn

from ..exception import IDNotFound, XGIError, frozen
from ..utils import IDDict, update_uid_counter
from .views import EdgeView, NodeView

__all__ = ["Hypergraph"]


class Hypergraph:
    r"""A hypergraph is a collection of subsets of a set of *nodes* or *vertices*.

    A hypergraph is a pair :math:`(V, E)`, where :math:`V` is a set of elements called
    *nodes* or *vertices*, and :math:`E` is a set whose elements are subsets of
    :math:`V`, that is, each :math:`e \in E` satisfies :math:`e \subset V`.  The
    elements of :math:`E` are called *hyperedges* or simply *edges*.

    The Hypergraph class allows any hashable object as a node and can associate
    attributes to each node, edge, or the hypergraph itself, in the form of key/value
    pairs. In this representation, multiedges are allowed.

    Parameters
    ----------
    incoming_data : input hypergraph data, optional
        Data to initialize the hypergraph. If None (default), an empty
        hypergraph is created, i.e. one with no nodes or edges.
        The data can be in the following formats:

        * hyperedge list
        * hyperedge dictionary
        * 2-column Pandas dataframe (bipartite edges)
        * Incidence matrix: numpy ndarray or scipy.sparse array
        * Hypergraph object
        * SimplicialComplex object

    **attr : dict, optional
        Attributes to add to the hypergraph as key, value pairs.
        By default, None.

    See Also
    --------
    ~xgi.core.simplicialcomplex.SimplicialComplex
    ~xgi.core.dihypergraph.DiHypergraph

    Notes
    -----
    Unique IDs are assigned to each node and edge internally and are used to refer to
    them throughout.

    The `attr` keyword arguments are added as hypergraph attributes. To add node or edge
    attributes see :meth:`add_node` and :meth:`add_edge`.

    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `Hypergraph` class.  For more details, see the
    `tutorial
    <https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

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
    _edge_dict_factory = IDDict
    _edge_attr_dict_factory = IDDict
    _net_attr_dict_factory = dict

    def __getstate__(self):
        """Function that allows pickling.

        Returns
        -------
        dict
            The keys label the hyeprgraph dict and the values
            are dictionarys from the Hypergraph class.

        Notes
        -----
        This allows the python multiprocessing module to be used.

        """
        return {
            "_edge_uid": self._edge_uid,
            "_net_attr": self._net_attr,
            "_node": self._node,
            "_node_attr": self._node_attr,
            "_edge": self._edge,
            "_edge_attr": self._edge_attr,
        }

    def __setstate__(self, state):
        """Function that allows unpickling of a hypergraph.

        Parameters
        ----------
        state
            The keys access the dictionary names the values are the
            dictionarys themselves from the Hypergraph class.

        Notes
        -----
        This allows the python multiprocessing module to be used.
        """
        self._edge_uid = state["_edge_uid"]
        self._net_attr = state["_net_attr"]
        self._node = state["_node"]
        self._node_attr = state["_node_attr"]
        self._edge = state["_edge"]
        self._edge_attr = state["_edge_attr"]
        self._nodeview = NodeView(self)
        self._edgeview = EdgeView(self)

    def __init__(self, incoming_data=None, **attr):
        self._edge_uid = count()
        self._net_attr = self._net_attr_dict_factory()
        self._node = self._node_dict_factory()
        self._node_attr = self._node_attr_dict_factory()
        self._edge = self._edge_dict_factory()
        self._edge_attr = self._edge_attr_dict_factory()

        self._nodeview = NodeView(self)
        """A :class:`~xgi.core.views.NodeView` of the hypergraph."""

        self._edgeview = EdgeView(self)
        """An :class:`~xgi.core.views.EdgeView` of the hypergraph."""

        if incoming_data is not None:
            # This import needs to happen when this function is called, not when it is
            # defined.  Otherwise, a circular import error would happen.
            from ..convert import to_hypergraph

            to_hypergraph(incoming_data, create_using=self)
        self._net_attr.update(attr)  # must be after convert

    def __str__(self):
        """Returns a short summary of the hypergraph.

        Returns
        -------
        string
            Hypergraph information

        """
        try:
            return (
                f"{type(self).__name__} named {self['name']} "
                f"with {self.num_nodes} nodes and {self.num_edges} hyperedges"
            )
        except XGIError:
            return (
                f"Unnamed {type(self).__name__} with "
                f"{self.num_nodes} nodes and {self.num_edges} hyperedges"
            )

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
            return self._net_attr[attr]
        except KeyError:
            raise XGIError("This attribute has not been set.")

    def __setitem__(self, attr, val):
        """Write hypergraph attribute."""
        self._net_attr[attr] = val

    def __getattr__(self, attr):
        stat = getattr(self.nodes, attr, None)
        word = "nodes"
        if stat is None:
            stat = getattr(self.edges, attr, None)
            word = "edges"
        if stat is None:
            word = None
            raise AttributeError(
                f"{attr} is not a method of Hypergraph or a "
                "recognized NodeStat or EdgeStat"
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

        tempH.add_nodes_from(zip(self._node.keys(), self._node_attr.values()))
        tempH.add_nodes_from(zip(H2._node.keys(), H2._node_attr.values()))

        tempH.add_edges_from(zip(self._edge.values(), self._edge_attr.values()))
        tempH.add_edges_from(zip(H2._edge.values(), H2._edge_attr.values()))

        tempH._net_attr = deepcopy(self._net_attr)
        tempH._net_attr.update(deepcopy(H2._net_attr))

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
        set_node_attributes

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
        set_node_attributes
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

    def remove_node(self, n, strong=False, remove_empty=True):
        """Remove a single node.

        The removal may be weak (default) or strong.  In weak removal, the node is
        removed from each of its containing edges.  If it is contained in any singleton
        edges, then these are also removed.  In strong removal, all edges containing the
        node are removed, regardless of size.

        Parameters
        ----------
        n : node
            A node in the hypergraph
        strong : bool, optional
            Whether to execute weak or strong removal. By default, False.
        remove_empty : bool, optional
            Whether to remove empty edges. By default, True.

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
            for e in edge_neighbors:
                node_neighbors = self._edge[e]
                del self._edge[e]
                del self._edge_attr[e]
                for node in node_neighbors.difference({n}):
                    self._node[node].remove(e)
        else:  # weak removal
            for edge in edge_neighbors:
                self._edge[edge].remove(n)
                if not self._edge[edge] and remove_empty:
                    del self._edge[edge]
                    del self._edge_attr[edge]

    def remove_nodes_from(self, nodes, strong=False, remove_empty=True):
        """Remove multiple nodes.

        Parameters
        ----------
        nodes : iterable
            An iterable of nodes.
        strong : bool, optional
            Whether to execute weak or strong removal. By default, False.
        remove_empty : bool, optional
            Whether to remove empty edges. By default, True.

        See Also
        --------
        remove_node

        """
        for n in nodes:
            if n not in self:
                warn(f"Node {n} not in hypergraph")
                continue
            self.remove_node(n, strong=strong, remove_empty=remove_empty)

    def set_node_attributes(self, values, name=None):
        """Sets node attributes from a given value or dictionary of values.

        Parameters
        ----------
        values : scalar value, dict-like
            What the node attribute should be set to.  If `values` is
            not a dictionary, then it is treated as a single attribute value
            that is then applied to every node in `H`.  This means that if
            you provide a mutable object, like a list, updates to that object
            will be reflected in the node attribute for every node.
            The attribute name will be `name`.

            If `values` is a dict or a dict of dict, it should be keyed
            by node to either an attribute value or a dict of attribute key/value
            pairs used to update the node's attributes.
        name : string, optional
            Name of the node attribute to set if values is a scalar, by default None.

        See Also
        --------
        set_edge_attributes
        add_node
        add_nodes_from

        Notes
        -----
        After computing some property of the nodes of a hypergraph, you may
        want to assign a node attribute to store the value of that property
        for each node.

        If you provide a list as the second argument, updates to the list
        will be reflected in the node attribute for each node.

        If you provide a dictionary of dictionaries as the second argument,
        the outer dictionary is assumed to be keyed by node to an inner
        dictionary of node attributes for that node.

        Note that if the dictionary contains nodes that are not in `G`, the
        values are silently ignored.

        """
        # Set node attributes based on type of `values`
        if name is not None:  # `values` must not be a dict of dict
            if isinstance(values, dict):  # `values` is a dict
                for n, v in values.items():
                    try:
                        self._node_attr[n][name] = v
                    except IDNotFound:
                        warn(f"Node {n} does not exist!")
            else:  # `values` is a constant
                for n in self:
                    self._node_attr[n][name] = values
        else:  # `values` must be dict of dict
            try:
                for n, d in values.items():
                    try:
                        self._node_attr[n].update(d)
                    except IDNotFound:
                        warn(f"Node {n} does not exist!")
            except (TypeError, ValueError, AttributeError):
                raise XGIError("Must pass a dictionary of dictionaries")

    def add_edge(self, members, id=None, **attr):
        """Add one edge with optional attributes.

        Parameters
        ----------
        members : Iterable
            An iterable of the ids of the nodes contained in the new edge.
        id : hashable, optional
            Id of the new edge. If None (default), a unique numeric ID will be created.
        **attr : dict, optional
            Attributes of the new edge.

        Raises
        -----
        XGIError
            If `members` is empty.

        See Also
        --------
        add_edges_from : Add a collection of edges.
        set_edge_attributes

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

        if id in self._edge.keys():  # check that uid is not present yet
            warn(f"uid {id} already exists, cannot add edge {members}")
            return

        uid = next(self._edge_uid) if id is None else id

        self._edge[uid] = set()
        for node in members:
            if node not in self._node:
                self._node[node] = set()
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node[node].add(uid)
            self._edge[uid].add(node)

        self._edge_attr[uid] = self._edge_attr_dict_factory()
        self._edge_attr[uid].update(attr)

        if id:  # set self._edge_uid correctly
            update_uid_counter(self, id)

    def add_edges_from(self, ebunch_to_add, **attr):
        r"""Add multiple edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : Iterable

            An iterable of edges.  This may be an iterable of iterables (Format 1),
            where each element contains the members of the edge specified as valid node
            IDs.  Alternatively, each element could also be a tuple in any of the
            following formats:

            * Format 2: 2-tuple (members, edge_id), or
            * Format 3: 2-tuple (members, attr), or
            * Format 4: 3-tuple (members, edge_id, attr),

            where `members` is an iterable of node IDs, `edge_id` is a hashable to use
            as edge ID, and `attr` is a dict of attributes. Finally, `ebunch_to_add` may
            be a dict of the form `{edge_id: edge_members}` (Format 5).

            Formats 2 and 3 are unambiguous because `attr` dicts are not hashable, while
            `id`s must be.  In Formats 2-4, each element of `ebunch_to_add` must have
            the same length, i.e. you cannot mix different formats.  The iterables
            containing edge members cannot be strings.

        **attr : kwargs, optional
            Additional attributes to be assigned to all edges. Attribues specified via
            `ebunch_to_add` take precedence over `attr`.

        See Also
        --------
        add_edge : Add a single edge.
        add_weighted_edges_from : Convenient way to add weighted edges.
        set_edge_attributes

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
            for id, members in ebunch_to_add.items():
                if id in self._edge.keys():  # check that uid is not present yet
                    warn(f"uid {id} already exists, cannot add edge {members}.")
                    continue
                try:
                    self._edge[id] = set(members)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e
                for n in members:
                    if n not in self._node:
                        self._node[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node[n].add(id)
                self._edge_attr[id] = self._edge_attr_dict_factory()

                update_uid_counter(self, id)

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
                members, id, eattr = e, next(self._edge_uid), {}
            elif format2:
                members, id, eattr = e[0], e[1], {}
            elif format3:
                members, id, eattr = e[0], next(self._edge_uid), e[1]
            elif format4:
                members, id, eattr = e[0], e[1], e[2]

            if id in self._edge.keys():  # check that uid is not present yet
                warn(f"uid {id} already exists, cannot add edge {members}.")
            else:
                try:
                    self._edge[id] = set(members)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e

                for n in members:
                    if n not in self._node:
                        self._node[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node[n].add(id)

                self._edge_attr[id] = self._edge_attr_dict_factory()
                self._edge_attr[id].update(attr)
                self._edge_attr[id].update(eattr)

            try:
                e = next(new_edges)
            except StopIteration:
                if format2 or format4:
                    update_uid_counter(self, id)
                break

    def add_weighted_edges_from(self, ebunch, weight="weight", **attr):
        """Add multiple weighted edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : iterable of edges
            Each edge given in the list or container will be added
            to the graph. The edges must be given as tuples of
            the form (node1, node2, ..., noden, weight).
        weight : string, optional
            The attribute name for the edge weights to be added,
            by default "weight".
        attr : keyword arguments, optional
            Edge attributes to add/update for all edges.

        See Also
        --------
        add_edge : Add a single edge.
        add_edges_from : Add multiple edges.
        set_edge_attributes
        get_edge_attributes

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

    def set_edge_attributes(self, values, name=None):
        """Set the edge attributes from a value or a dictionary of values.

        Parameters
        ----------
        values : scalar value, dict-like
            What the edge attribute should be set to.  If `values` is
            not a dictionary, then it is treated as a single attribute value
            that is then applied to every edge in `H`.  This means that if
            you provide a mutable object, like a list, updates to that object
            will be reflected in the edge attribute for each edge.  The attribute
            name will be `name`.
            If `values` is a dict or a dict of dict, it should be keyed
            by edge ID to either an attribute value or a dict of attribute
            key/value pairs used to update the edge's attributes.
        name : string, optional
            Name of the edge attribute to set if values is a scalar. By default, None.

        See Also
        --------
        set_node_attributes
        add_edge
        add_edges_from

        Notes
        -----
        Note that if the dict contains edge IDs that are not in `H`, they are
        silently ignored.

        """
        if name is not None:
            # `values` does not contain attribute names
            try:
                for e, value in values.items():
                    try:
                        self._edge_attr[e][name] = value
                    except IDNotFound:
                        warn(f"Edge {e} does not exist!")
            except AttributeError:
                # treat `values` as a constant
                for e in self._edge:
                    self._edge_attr[e][name] = values
        else:
            try:
                for e, d in values.items():
                    try:
                        self._edge_attr[e].update(d)
                    except IDNotFound:
                        warn(f"Edge {e} does not exist!")
            except AttributeError:
                raise XGIError(
                    "name property has not been set and a "
                    "dict-of-dicts has not been provided."
                )

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
        IDNotFound
            If user specifies nodes or edges that do not exist or
            nodes that are not part of edges.
        XGIError
            If the swap does not preserve edge sizes.

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
            # Initialize temporary copies to modify
            temp_memberships1 = self._node[n_id1].copy()
            temp_memberships2 = self._node[n_id2].copy()
            temp_members1 = self._edge[e_id1].copy()
            temp_members2 = self._edge[e_id2].copy()

            # remove old nodes from edges
            temp_members1.remove(n_id1)
            temp_members2.remove(n_id2)

            # swap nodes
            temp_members1.add(n_id2)
            temp_members2.add(n_id1)

            # Now we handle the memberships
            # remove old nodes from edges
            temp_memberships1.remove(e_id1)
            temp_memberships2.remove(e_id2)

            # swap nodes
            temp_memberships1.add(e_id2)
            temp_memberships2.add(e_id1)

        except KeyError as e:

            raise IDNotFound(
                "One of the nodes specified doesn't belong to the specified edge."
            ) from e

        if (
            len(temp_memberships1) != len(self._node[n_id1])
            or len(temp_memberships2) != len(self._node[n_id2])
            or len(temp_members1) != len(self._edge[e_id1])
            or len(temp_members2) != len(self._edge[e_id2])
        ):
            raise XGIError("This swap does not preserve edge sizes.")

        self._node[n_id1] = temp_memberships1
        self._node[n_id2] = temp_memberships2

        self._edge[e_id1] = temp_members1
        self._edge[e_id2] = temp_members2

    def random_edge_shuffle(self, e_id1=None, e_id2=None):
        """Randomly redistributes nodes between two hyperedges.

        The process is as follows:

        1. randomly select two hyperedges
        2. place all their nodes into a single bucket
        3. randomly redistribute the nodes between those two hyperedges

        Parameters
        ----------
        e_id1 : node ID, optional
            ID of first edge to shuffle.
        e_id2 : node ID, optional
            ID of second edge to shuffle.

        Note
        ----
        After shuffling, the sizes of the two hyperedges are unchanged.
        Edge IDs and attributes are also unchanged.
        If the same node appears in both hyperedges, then this is still true after reshuffling.
        If either `e_id1` or `e_id2` is not provided, then two random edges are selected.

        References
        ----------
        Philip S Chodrow, 2020.
        "Configuration models of random hypergraphs."
        Journal of Complex Networks, 8(3).
        https://doi.org/10.1093/comnet/cnaa018

        Example
        -------
        >>> import xgi
        >>> random.seed(42)
        >>> H = xgi.Hypergraph([[1, 2, 3], [3, 4], [4, 5]])
        >>> H.random_edge_shuffle()
        >>> H.edges.members()
        [{2, 4, 5}, {3, 4}, {1, 3}]

        """
        if len(self._edge) < 2:
            raise ValueError("Hypergraph must have at least two edges.")

        # select two random edges
        if e_id1 is None or e_id2 is None:
            e_id1, e_id2 = random.sample(list(self._edge), 2)

        # extract edges (lists of nodes)
        e1 = self._edge[e_id1]
        e2 = self._edge[e_id2]

        # nodes in both edges should not be shuffled
        nodes_both = e1 & e2
        e1 -= nodes_both
        e2 -= nodes_both

        # put all nodes in a single bucket
        nodes = e1 | e2

        # randomly redistribute nodes between the two edges
        e1_new = set(random.sample(list(nodes), len(e1)))
        e2_new = nodes - e1_new

        # update edge memberships
        for n_id in e1_new & e2:
            self._node[n_id].remove(e_id2)
            self._node[n_id].add(e_id1)

        for n_id in e2_new & e1:
            self._node[n_id].remove(e_id1)
            self._node[n_id].add(e_id2)

        # add nodes in both edges back
        e1_new |= nodes_both
        e2_new |= nodes_both

        # update hypergraph
        self._edge[e_id1] = e1_new
        self._edge[e_id2] = e2_new

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
        remove_node_from_edge

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
        for node in self._edge[id].copy():
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
            for node in self._edge[id].copy():
                self._node[node].remove(id)
            del self._edge[id]
            del self._edge_attr[id]

    def remove_node_from_edge(self, edge, node, remove_empty=True):
        """Remove a node from an existing edge.

        Parameters
        ----------
        edge : hashable
            The edge ID
        node : hashable
            The node ID
        remove_empty : bool, optional
            Whether empty edges are removed. By default, True.

        Raises
        ------
        XGIError
            If either the node or edge does not exist.

        See Also
        --------
        remove_node
        remove_edge
        add_node_to_edge

        Notes
        -----
        If edge is left empty as a result of removing node from it, the edge is also
        removed.

        """
        if edge not in self._edge:
            raise XGIError(f"Edge {edge} not in the hypergraph")
        elif node not in self._node:
            raise XGIError(f"Node {node} not in the hypergraph")
        elif node not in self._edge[edge]:
            raise XGIError(f"Edge {edge} does not contain node {node}")
        else:
            self._edge[edge].remove(node)

        self._node[node].remove(edge)

        if not self._edge[edge] and remove_empty:
            del self._edge[edge]
            del self._edge_attr[edge]

    def update(self, *, edges=None, nodes=None):
        """Add nodes or edges to the hypergraph.

        Parameters
        ----------
        edges : Iterable, optional
            Edges to be added. By default, None.
        nodes : Iterable, optional
            Nodes to be added. By default, None.

        See Also
        --------
        add_edges_from: Add multiple edges.
        add_nodes_from: Add multiple nodes.

        """
        if nodes:
            self.add_nodes_from(nodes)
        if edges:
            self.add_edges_from(edges)

    def clear(self, remove_net_attr=True):
        """Remove all nodes and edges from the graph.

        Also removes node and edge attributes, and optionally hypergraph attributes.

        Parameters
        ----------
        remove_net_attr : bool, optional
            Whether to remove hypergraph attributes as well.
            By default, True.

        """
        self._node.clear()
        self._node_attr.clear()
        self._edge.clear()
        self._edge_attr.clear()
        if remove_net_attr:
            self._net_attr.clear()

    def clear_edges(self):
        """Remove all edges from the graph without altering any nodes."""
        for node in self.nodes:
            self._node[node] = set()
        self._edge.clear()
        self._edge_attr.clear()

    def merge_duplicate_edges(
        self, rename="first", merge_rule="first", multiplicity=None
    ):
        """Merges edges which have the same members.

        Parameters
        ----------
        rename : str, optional
            Either "first" (default), "tuple", or "new".
            If "first", the new edge ID is the first of the sorted
            duplicate edge IDs. If "tuple", the new edge ID is a
            tuple of the sorted duplicate edge IDs. If "new", a
            new ID will be selected automatically.
        merge_rule : str, optional
            Either "first" (default) or "union".
            If "first", takes the attributes of the first duplicate.
            If "union", takes the set of attributes of all the duplicates.
        multiplicity : str, optional
            The attribute in which to store the multiplicity of the hyperedge,
            by default None.

        Raises
        ------
        XGIError
            If invalid rename or merge_rule specified.

        Warns
        -----
        If the user chooses merge_rule="union". Tells the
        user that they can no longer draw based on this stat.

        Examples
        --------

        >>> import xgi
        >>> edges = [{1, 2}, {1, 2}, {1, 2}, {3, 4, 5}, {3, 4, 5}]
        >>> edge_attrs = dict()
        >>> edge_attrs[0] = {"color": "blue"}
        >>> edge_attrs[1] = {"color": "red", "weight": 2}
        >>> edge_attrs[2] = {"color": "yellow"}
        >>> edge_attrs[3] = {"color": "purple"}
        >>> edge_attrs[4] = {"color": "purple", "name": "test"}
        >>> H = xgi.Hypergraph(edges)
        >>> H.set_edge_attributes(edge_attrs)
        >>> H.edges
        EdgeView((0, 1, 2, 3, 4))

        There are several ways to rename the duplicate edges after merging:

        1. The merged edge ID is the first duplicate edge ID.

        >>> H1 = H.copy()
        >>> H1.merge_duplicate_edges()
        >>> H1.edges
        EdgeView((0, 3))

        2. The merged edge ID is a tuple of all the duplicate edge IDs.

        >>> H2 = H.copy()
        >>> H2.merge_duplicate_edges(rename="tuple")
        >>> H2.edges
        EdgeView(((0, 1, 2), (3, 4)))

        3. The merged edge ID is assigned a new edge ID.

        >>> H3 = H.copy()
        >>> H3.merge_duplicate_edges(rename="new")
        >>> H3.edges
        EdgeView((5, 6))

        We can also specify how we would like to combine the attributes
        of the merged edges:

        1. The attributes are the attributes of the first merged edge.

        >>> H4 = H.copy()
        >>> H4.merge_duplicate_edges()
        >>> H4.edges[0]
        {'color': 'blue'}

        2. The attributes are the union of every attribute that each merged
        edge has. If a duplicate edge doesn't have that attribute, it is set
        to None.

        >>> H5 = H.copy()
        >>> H5.merge_duplicate_edges(merge_rule="union")
        >>> H5.edges[0] == {'color': {'blue', 'red', 'yellow'}, 'weight':{2, None}}
        True

        3. We can also set the attributes to the intersection, i.e.,
        if a particular attribute is the same across the duplicate
        edges, we use this attribute, otherwise, we set it to None.

        >>> H6 = H.copy()
        >>> H6.merge_duplicate_edges(merge_rule="intersection")
        >>> H6.edges[0] == {'color': None, 'weight': None}
        True
        >>> H6.edges[3] == {'color': 'purple', 'name': None}
        True

        We can also choose to store the multiplicity of the edge
        as an attribute. The user simply provides the string of
        the attribute which stores it. Note that this will not prevent
        other attributes from being over written (e.g., weight), so
        be careful that the attribute is not already in use.

        >>> H7 = H.copy()
        >>> H7.merge_duplicate_edges(multiplicity="mult")
        >>> H7.edges[0]['mult'] == 3
        True
        """
        dups = []
        hashes = defaultdict(list)
        for idx, members in self._edge.items():
            hashes[frozenset(members)].append(idx)

        new_edges = list()
        for members, dup_ids in hashes.items():
            if len(dup_ids) > 1:
                dups.extend(dup_ids)

                if rename == "first":
                    new_id = sorted(dup_ids)[0]
                elif rename == "tuple":
                    new_id = tuple(sorted(dup_ids))
                elif rename == "new":
                    new_id = next(self._edge_uid)
                else:
                    raise XGIError("Invalid ID renaming scheme!")

                if merge_rule == "first":
                    id = min(dup_ids)
                    new_attrs = deepcopy(self._edge_attr[id])
                elif merge_rule == "union":
                    attrs = {field for id in dup_ids for field in self._edge_attr[id]}
                    new_attrs = {
                        attr: {self._edge_attr[id].get(attr) for id in dup_ids}
                        for attr in attrs
                    }
                elif merge_rule == "intersection":
                    attrs = {field for id in dup_ids for field in self._edge_attr[id]}
                    set_attrs = {
                        attr: {self._edge_attr[id].get(attr) for id in dup_ids}
                        for attr in attrs
                    }
                    new_attrs = {
                        attr: (None if len(val) != 1 else next(iter(val)))
                        for attr, val in set_attrs.items()
                    }
                else:
                    raise XGIError("Invalid merge rule!")

                if multiplicity is not None:
                    new_attrs[multiplicity] = len(dup_ids)
                new_edges.append((members, new_id, new_attrs))
        self.remove_edges_from(dups)
        self.add_edges_from(new_edges)

        if merge_rule == "union":
            warn(
                "You will not be able to color/draw by "
                "merged attributes with xgi.draw()!"
            )

    def copy(self):
        """A deep copy of the hypergraph.

        A deep copy of the hypergraph, including node, edge, and hypergraph attributes.

        Returns
        -------
        H : Hypergraph
            A copy of the hypergraph.

        """
        cp = self.__class__()
        nn = self.nodes
        cp.add_nodes_from((n, deepcopy(attr)) for n, attr in nn.items())
        ee = self.edges
        cp.add_edges_from(
            (e, id, deepcopy(self.edges[id]))
            for id, e in ee.members(dtype=dict).items()
        )
        cp._net_attr = deepcopy(self._net_attr)

        cp._edge_uid = copy(self._edge_uid)

        return cp

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
        dual._net_attr = deepcopy(self._net_attr)

        return dual

    def cleanup(
        self,
        isolates=False,
        singletons=False,
        multiedges=False,
        connected=True,
        relabel=True,
        in_place=True,
    ):
        """Removes potentially undesirable artifacts from the hypergraph.

        Parameters
        ----------
        isolates : bool, optional
            Whether isolated nodes are allowed, by default False.
        singletons : bool, optional
            Whether singleton edges are allowed, by default False.
        multiedges : bool, optional
            Whether multiedges are allowed, by default False.
        connected : bool, optional
            Whether the returned hypergraph should be connected. If true,
            returns the hypergraph induced on the largest connected component.
            By default, False.
        relabel : bool, optional
            Whether to convert all node and edge labels to sequential integers, by
            default True.
        in_place : bool, optional
            Whether to modify the current hypergraph or output a new one, by default
            True.

        """
        if in_place:
            _H = self
        else:
            _H = self.copy()
        if not multiedges:
            _H.merge_duplicate_edges()
        if not singletons:
            _H.remove_edges_from(_H.edges.singletons())
        if not isolates:
            _H.remove_nodes_from(_H.nodes.isolates())
        if connected:
            from ..algorithms import largest_connected_hypergraph

            largest_connected_hypergraph(_H, in_place=True)
        if relabel:
            from ..utils import convert_labels_to_integers

            convert_labels_to_integers(_H, in_place=True)

        return _H

    def freeze(self):
        """Method for freezing a hypergraph which prevents it from being modified

        See Also
        --------
        ~xgi.exception.frozen : Method that raises an error when a user tries to modify the hypergraph
        is_frozen : Check whether a hypergraph is frozen

        Examples
        --------
        >>> import xgi
        >>> edges = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(edges)
        >>> H.freeze()
        >>> H.add_node(5)
        Traceback (most recent call last):
        xgi.exception.XGIError: Frozen higher-order network can't be modified

        """
        self.add_node = frozen
        self.add_nodes_from = frozen
        self.remove_node = frozen
        self.remove_nodes_from = frozen
        self.add_edge = frozen
        self.add_edges_from = frozen
        self.add_weighted_edges_from = frozen
        self.remove_edge = frozen
        self.remove_edges_from = frozen
        self.add_node_to_edge = frozen
        self.remove_node_from_edge = frozen
        self.clear = frozen
        self.frozen = True

    @property
    def is_frozen(self):
        """Checks whether a dihypergraph is frozen

        Returns
        -------
        bool
            True if hypergraph is frozen, false if not.

        See Also
        --------
        freeze : A method to prevent a hypergraph from being modified.

        Examples
        --------
        >>> import xgi
        >>> edges = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(edges)
        >>> H.freeze()
        >>> H.is_frozen
        True

        """
        try:
            return self.frozen
        except AttributeError:
            return False
