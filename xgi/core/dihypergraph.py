"""Base class for directed hypergraphs.

.. warning::
    This is currently an experimental feature.

"""

from collections.abc import Hashable, Iterable
from copy import copy, deepcopy
from itertools import count
from warnings import warn

from ..exception import IDNotFound, XGIError, frozen
from ..utils import IDDict, update_uid_counter
from .views import DiEdgeView, DiNodeView

__all__ = ["DiHypergraph"]


class DiHypergraph:
    r"""A dihypergraph is a collection of directed interactions of arbitrary size.

    .. warning::
        This is currently an experimental feature.

    More formally, a directed hypergraph (dihypergraph) is a pair :math:`(V, E)`,
    where :math:`V` is a set of elements called *nodes* or *vertices*,
    and :math:`E` is the set of directed hyperedges.
    A directed hyperedge is an ordered pair, :math:`(e^+, e^-)`,
    where :math:`e^+ \subset V`, the set of senders, is known as the "tail" and
    :math:`e^-\subset V`, the set of receivers, is known as the "head".
    The equivalent undirected edge, is :math:`e = e^+ \cap e^-` and
    the edge size is defined as :math:`|e|`.

    The DiHypergraph class allows any hashable object as a node and can associate
    attributes to each node, edge, or the hypergraph itself, in the form of key/value
    pairs.

    Multiedges and self-loops are allowed.

    Parameters
    ----------
    incoming_data : input directed hypergraph data (optional, default: None)
        Data to initialize the dihypergraph. If None (default), an empty
        hypergraph is created, i.e. one with no nodes or edges.
        The data can be in the following formats:

        * directed hyperedge list
        * directed hyperedge dictionary
        * DiHypergraph object.

    **attr : dict, optional, default: None
        Attributes to add to the hypergraph as key, value pairs.

    See Also
    --------
    ~xgi.core.hypergraph.Hypergraph

    Notes
    -----
    Unique IDs are assigned to each node and edge internally and are used to refer to
    them throughout.

    The `attr` keyword arguments are added as hypergraph attributes. To add node or edge
    attributes see :meth:`add_node` and :meth:`add_edge`.

    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `DiHypergraph` class.  For more details, see the
    `tutorial
    <https://xgi.readthedocs.io/en/stable/api/tutorials/focus_6.html>`_.

    References
    ----------
    Bretto, Alain. "Hypergraph theory: An introduction."
    Mathematical Engineering. Cham: Springer (2013).
    Examples
    --------
    >>> import xgi
    >>> DH = xgi.DiHypergraph([([1, 2, 3], [4]), ([5, 6], [6, 7, 8])])
    >>> DH.nodes
    DiNodeView((1, 2, 3, 4, 5, 6, 7, 8))
    >>> DH.edges
    DiEdgeView((0, 1))
    >>> [[sorted(h), sorted(t)] for h, t in DH.edges.dimembers()]
    [[[1, 2, 3], [4]], [[5, 6], [6, 7, 8]]]
    >>> [sorted(e) for e in DH.edges.members()]
    [[1, 2, 3, 4], [5, 6, 7, 8]]
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
            The keys label the hypergraph dict and the values
            are dictionaries from the DiHypergraph class.

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
        """Function that allows unpickling of a dihypergraph.

        Parameters
        ----------
        state
            The keys access the dictionary names the values are the
            dictionarys themselves from the DiHypergraph class.

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
        self._nodeview = DiNodeView(self)
        self._edgeview = DiEdgeView(self)

    def __init__(self, incoming_data=None, **attr):
        self._edge_uid = count()
        self._net_attr = self._net_attr_dict_factory()

        self._node = self._node_dict_factory()
        self._node_attr = self._node_attr_dict_factory()

        self._edge = self._edge_dict_factory()
        self._edge_attr = self._edge_attr_dict_factory()

        self._nodeview = DiNodeView(self)
        """A :class:`~xgi.core.views.DiNodeView` of the directed hypergraph."""

        self._edgeview = DiEdgeView(self)
        """An :class:`~xgi.core.views.DiEdgeView` of the directed hypergraph."""

        if incoming_data is not None:
            # This import needs to happen when this function is called, not when it is
            # defined.  Otherwise, a circular import error would happen.
            from ..convert import to_dihypergraph

            to_dihypergraph(incoming_data, create_using=self)
        self._net_attr.update(attr)  # must be after convert

    def __str__(self):
        """Returns a short summary of the directed hypergraph.

        Returns
        -------
        string
            DiHypergraph information

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
            An iterator over all nodes in the dihypergraph.
        """
        return iter(self._node)

    def __contains__(self, n):
        """Check for if a node is in this dihypergraph.

        Parameters
        ----------
        n : hashable
            node ID

        Returns
        -------
        bool
            Whether the node exists in the dihypergraph.
        """
        try:
            return n in self._node
        except TypeError:
            return False

    def __len__(self):
        """Number of nodes in the dihypergraph.

        Returns
        -------
        int
            The number of nodes in the dihypergraph.

        See Also
        --------
        num_nodes : identical method
        num_edges : number of edges in the dihypergraph

        """
        return len(self._node)

    def __getitem__(self, attr):
        """Read dihypergraph attribute."""
        try:
            return self._net_attr[attr]
        except KeyError:
            raise XGIError("This attribute has not been set.")

    def __setitem__(self, attr, val):
        """Write dihypergraph attribute."""
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
                f"{attr} is not a method of DiHypergraph or a recognized DiNodeStat or DiEdgeStat"
            )

        def func(node=None, *args, **kwargs):
            val = stat(*args, **kwargs).asdict()
            return val if node is None else val[node]

        func.__doc__ = f"""Equivalent to DH.{word}.{attr}.asdict(). For accepted *args and
        **kwargs, see documentation of DH.{word}.{attr}."""

        return func

    @property
    def num_nodes(self):
        """The number of nodes in the dihypergraph.

        Returns
        -------
        int
            The number of nodes in the dihypergraph.

        See Also
        --------
        num_edges : returns the number of edges in the dihypergraph

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [([1, 2], [2, 3, 4])]
        >>> DH = xgi.DiHypergraph(hyperedge_list)
        >>> DH.num_nodes
        4

        """
        return len(self._node)

    @property
    def num_edges(self):
        """The number of directed edges in the dihypergraph.

        Returns
        -------
        int
            The number of directed edges in the dihypergraph.

        See Also
        --------
        num_nodes : returns the number of nodes in the dihypergraph

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [([1, 2], [2, 3, 4])]
        >>> DH = xgi.DiHypergraph(hyperedge_list)
        >>> DH.num_edges
        1
        """
        return len(self._edge)

    @property
    def nodes(self):
        """A :class:`DiNodeView` of this network."""
        return self._nodeview

    @property
    def edges(self):
        """An :class:`DiEdgeView` of this network."""
        return self._edgeview

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
        If node is already in the dihypergraph, its attributes are still updated.

        """
        if node not in self._node:
            self._node[node] = {"in": set(), "out": set()}
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
                self._node[n] = {"in": set(), "out": set()}
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
            A node in the dihypergraph
        strong : bool (default False)
            Whether to execute weak or strong removal.
        remove_empty : bool, optional
            Whether to remove empty edges (0 members in both head and tail).
            By default, True.

        Raises
        ------
        XGIError
           If n is not in the dihypergraph.

        See Also
        --------
        remove_nodes_from

        """
        edge_neighbors = self._node[n]
        del self._node[n]
        del self._node_attr[n]

        if strong:
            for edge in edge_neighbors["in"].union(edge_neighbors["out"]):
                del self._edge[edge]
                del self._edge_attr[edge]
        else:  # weak removal
            for edge in edge_neighbors["in"]:
                self._edge[edge]["out"].remove(n)

            for edge in edge_neighbors["out"]:
                self._edge[edge]["in"].remove(n)

            # remove empty edges
            for edge in edge_neighbors["in"].union(edge_neighbors["out"]):
                if (
                    not self._edge[edge]["in"]
                    and not self._edge[edge]["out"]
                    and remove_empty
                ):
                    del self._edge[edge]
                    del self._edge_attr[edge]

    def remove_nodes_from(self, nodes, strong=False, remove_empty=True):
        """Remove multiple nodes.

        Parameters
        ----------
        nodes : iterable
            An iterable of nodes.
        strong : bool (default False)
            Whether to execute weak or strong removal.
        remove_empty : bool, optional
            Whether to remove empty edges (0 members in both head and tail).
            By default, True.

        See Also
        --------
        remove_node

        """
        for n in nodes:
            if n not in self._node:
                warn(f"Node {n} not in dihypergraph")
                continue
            self.remove_node(n, strong=strong, remove_empty=remove_empty)

    def set_node_attributes(self, values, name=None):
        """Sets node attributes from a given value or dictionary of values.

        Parameters
        ----------
        values : scalar value, dict-like
            What the node attribute should be set to.  If `values` is
            not a dictionary, then it is treated as a single attribute value
            that is then applied to every node in `DH`.  This means that if
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
            An list or tuple (size 2) of iterables. The first entry contains the
            elements of the tail and the second entry contains the elements
            of the head.
        id : hashable, default None
            Id of the new edge. If None, a unique numeric ID will be created.
        **attr : dict, optional
            Attributes of the new edge.

        See Also
        --------
        add_edges_from : Add a collection of edges.

        Examples
        --------

        Add edges with or without specifying an edge id.

        >>> import xgi
        >>> DH = xgi.DiHypergraph()
        >>> DH.add_edge(([1, 2, 3], [2, 3, 4]))
        >>> DH.add_edge(([3, 4], set()), id='myedge')
        """
        if isinstance(members, (tuple, list)):
            tail = members[0]
            head = members[1]
        else:
            raise XGIError("Directed edge must be a list or tuple!")

        uid = next(self._edge_uid) if id is None else id

        if id in self._edge.keys():  # check that uid is not present yet
            warn(f"uid {id} already exists, cannot add edge {members}")
            return

        self._edge[uid] = {"in": set(), "out": set()}

        for node in tail:
            if node not in self._node:
                self._node[node] = {"in": set(), "out": set()}
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node[node]["out"].add(uid)
            self._edge[uid]["in"].add(node)

        for node in head:
            if node not in self._node:
                self._node[node] = {"in": set(), "out": set()}
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node[node]["in"].add(uid)
            self._edge[uid]["out"].add(node)

        self._edge_attr[uid] = self._edge_attr_dict_factory()
        self._edge_attr[uid].update(attr)

        if id:  # set self._edge_uid correctly
            update_uid_counter(self, id)

    def add_edges_from(self, ebunch_to_add, **attr):
        """Add multiple directed edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : Iterable

            Note that here, when we refer to an edge, as in the `add_edge` method,
            it is a list or tuple (size 2) of iterables. The first entry contains the
            elements of the tail and the second entry contains the elements
            of the head.

            An iterable of edges.  This may be an iterable of edges (Format 1),
            where each edge is in the format described above.

            Alternatively, each element could also be a tuple in any of the following
            formats:

            * Format 2: 2-tuple (edge, edge_id), or
            * Format 4: 3-tuple (edge, edge_id, attr),

            where `edge` is in the format described above, `edge_id` is a hashable to use
            as edge ID, and `attr` is a dict of attributes. Finally, `ebunch_to_add`
            may be a dict of the form `{edge_id: edge_members}` (Format 5).

            Formats 2 and 3 are unambiguous because `attr` dicts are not hashable, while `id`s must be.
            In Formats 2-4, each element of `ebunch_to_add` must have the same length,
            i.e. you cannot mix different formats.  The iterables containing edge
            members cannot be strings.

        **attr : kwargs, optional
            Additional attributes to be assigned to all edges. Attribues specified via
            `ebunch_to_add` take precedence over `attr`.

        See Also
        --------
        add_edge : Add a single edge.

        Notes
        -----
        Adding the same edge twice will create a multi-edge. Currently
        cannot add empty edges; the method skips over them.

        Examples
        --------
        >>> import xgi
        >>> DH = xgi.DiHypergraph()

        When specifying edges by their members only, numeric edge IDs will be assigned
        automatically.

        >>> DH.add_edges_from([([0, 1], [1, 2]), ([2, 3, 4], [])])
        >>> DH.edges.dimembers(dtype=dict)
        {0: ({0, 1}, {1, 2}), 1: ({2, 3, 4}, set())}

        Custom edge ids can be specified using a dict.

        >>> DH = xgi.DiHypergraph()
        >>> DH.add_edges_from({'one': ([0, 1], [1, 2]), 'two': ([2, 3, 4], [])})
        >>> DH.edges.dimembers(dtype=dict)
        {'one': ({0, 1}, {1, 2}), 'two': ({2, 3, 4}, set())}

        You can use the dict format to easily add edges from another hypergraph.

        >>> DH2 = xgi.DiHypergraph()
        >>> DH2.add_edges_from(DH.edges.dimembers(dtype=dict))
        >>> DH.edges == DH2.edges
        True

        Alternatively, edge ids can be specified using an iterable of 2-tuples.

        >>> DH = xgi.DiHypergraph()
        >>> DH.add_edges_from([(([0, 1], [1, 2]), 'one'), (([2, 3, 4], []), 'two')])
        >>> DH.edges.dimembers(dtype=dict)
        {'one': ({0, 1}, {1, 2}), 'two': ({2, 3, 4}, set())}

        Attributes for each edge may be specified using a 2-tuple for each edge.
        Numeric IDs will be assigned automatically.

        >>> DH = xgi.DiHypergraph()
        >>> edges = [
        ...     (([0, 1], [1, 2]), {'color': 'red'}),
        ...     (([2, 3, 4], []), {'color': 'blue', 'age': 40}),
        ... ]
        >>> DH.add_edges_from(edges)
        >>> {e: DH.edges[e] for e in DH.edges}
        {0: {'color': 'red'}, 1: {'color': 'blue', 'age': 40}}

        Attributes and custom IDs may be specified using a 3-tuple for each edge.

        >>> DH = xgi.DiHypergraph()
        >>> edges = [
        ...     (([0, 1], [1, 2]), 'one', {'color': 'red'}),
        ...     (([2, 3, 4], []), 'two', {'color': 'blue', 'age': 40}),
        ... ]
        >>> DH.add_edges_from(edges)
        >>> {e: DH.edges[e] for e in DH.edges}
        {'one': {'color': 'red'}, 'two': {'color': 'blue', 'age': 40}}

        """
        # format 5 is the easiest one
        if isinstance(ebunch_to_add, dict):
            for id, members in ebunch_to_add.items():
                if id in self._edge.keys():  # check that uid is not present yet
                    warn(f"uid {id} already exists, cannot add edge {members}.")
                    continue

                if isinstance(members, (tuple, list)):
                    tail = members[0]
                    head = members[1]
                else:
                    raise XGIError("Directed edge must be a list or tuple!")

                try:
                    self._edge[id] = {"in": set(tail), "out": set(head)}
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e

                for n in tail:
                    if n not in self._node:
                        self._node[n] = {"in": set(), "out": set()}
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node[n]["out"].add(id)
                self._edge_attr[id] = self._edge_attr_dict_factory()

                for n in head:
                    if n not in self._node:
                        self._node[n] = {"in": set(), "out": set()}
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node[n]["in"].add(id)

                update_uid_counter(self, id)

            return
        # in formats 1-4 we only know that ebunch_to_add is an iterable, so we iterate
        # over it and use the firs element to determine which format we are working with
        new_edges = iter(ebunch_to_add)
        try:
            first_edge = next(new_edges)
        except StopIteration:
            return

        second_elem = list(first_edge)[1]

        format1, format2, format3, format4 = False, False, False, False

        if (
            isinstance(second_elem, Iterable)
            and not isinstance(second_elem, str)
            and not isinstance(second_elem, dict)
        ):
            format1 = True
        else:
            if len(first_edge) == 3:
                format4 = True
            elif len(first_edge) == 2 and issubclass(type(first_edge[1]), Hashable):
                format2 = True
            elif len(first_edge) == 2:
                format3 = True

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
                    tail = members[0]
                    head = members[1]
                    self._edge[id] = {"in": set(tail), "out": set(head)}
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e

                for node in tail:
                    if node not in self._node:
                        self._node[node] = {"in": set(), "out": set()}
                        self._node_attr[node] = self._node_attr_dict_factory()
                    self._node[node]["out"].add(id)
                    self._edge[id]["in"].add(node)

                for node in head:
                    if node not in self._node:
                        self._node[node] = {"in": set(), "out": set()}
                        self._node_attr[node] = self._node_attr_dict_factory()
                    self._node[node]["in"].add(id)
                    self._edge[id]["out"].add(node)

                self._edge_attr[id] = self._edge_attr_dict_factory()
                self._edge_attr[id].update(attr)
                self._edge_attr[id].update(eattr)

            try:
                e = next(new_edges)
            except StopIteration:
                if format2 or format4:
                    update_uid_counter(self, id)
                break

    def add_node_to_edge(self, edge, node, direction):
        """Add one node to an existing edge.

        If the node or edge IDs do not exist, they are created.

        Parameters
        ----------
        edge : hashable
            edge ID
        node : hashable
            node ID
        direction : str
            "in" or "out" indicates that the node should be added to
            the tail or head respectively.

        See Also
        --------
        add_node
        add_edge
        remove_node_from_edge
        """
        if direction == "in":
            ed = "in"
            nd = "out"
        elif direction == "out":
            ed = "out"
            nd = "in"
        else:
            raise XGIError("Invalid direction!")

        if edge not in self._edge:
            self._edge[edge] = {"in": set(), "out": set()}
            self._edge_attr[edge] = {}
        if node not in self._node:
            self._node[node] = {"in": set(), "out": set()}
            self._node_attr[node] = {}

        self._edge[edge][ed].add(node)
        self._node[node][nd].add(edge)

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
        edge = self._edge[id].copy()

        for node in edge["in"]:
            self._node[node]["out"].remove(id)
        for node in edge["out"]:
            self._node[node]["in"].remove(id)

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
            edge = self._edge[id].copy()

            for node in edge["in"]:
                self._node[node]["out"].remove(id)
            for node in edge["out"]:
                self._node[node]["in"].remove(id)

            del self._edge[id]
            del self._edge_attr[id]

    def remove_node_from_edge(self, edge, node, direction, remove_empty=True):
        """Remove a node from an existing edge.

        Parameters
        ----------
        edge : hashable
            The edge ID
        node : hashable
            The node ID
        direction : str
            "in" or "out" indicates that the node should be removed from
            the tail or head respectively.

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
        if direction == "in":
            ed = "in"
            nd = "out"
        elif direction == "out":
            ed = "out"
            nd = "in"
        else:
            raise XGIError("Invalid direction!")

        if edge not in self._edge:
            raise XGIError(f"Edge {edge} not in the hypergraph")
        if node not in self._node:
            raise XGIError(f"Node {node} not in the hypergraph")
        elif node not in self._edge[edge][ed]:
            raise XGIError(f"{ed}-edge {edge} does not contain node {node}")
        else:
            self._edge[edge][ed].remove(node)

        self._node[node][nd].remove(edge)

        if not self._edge[edge]["in"] and not self._edge[edge]["out"] and remove_empty:
            del self._edge[edge]
            del self._edge_attr[edge]

    def set_edge_attributes(self, values, name=None):
        """Set the edge attributes from a value or a dictionary of values.

        Parameters
        ----------
        values : scalar value, dict-like
            What the edge attribute should be set to.  If `values` is
            not a dictionary, then it is treated as a single attribute value
            that is then applied to every edge in `DH`.  This means that if
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
        Note that if the dict contains edge IDs that are not in `DH`, they are
        silently ignored.

        """
        if name is not None:
            # `values` does not contain attribute names
            try:
                for e, value in values.items():
                    try:
                        self._edge_attr[id][name] = value
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

    def copy(self):
        """A deep copy of the dihypergraph.

        A deep copy of the dihypergraph, including node, edge, and hypergraph attributes.

        Returns
        -------
        DH : DiHypergraph
            A copy of the hypergraph.

        """
        cp = self.__class__()
        nn = self.nodes
        cp.add_nodes_from((n, deepcopy(attr)) for n, attr in nn.items())
        ee = self.edges
        cp.add_edges_from(
            (e, id, deepcopy(self.edges[id]))
            for id, e in ee.dimembers(dtype=dict).items()
        )
        cp._net_attr = deepcopy(self._net_attr)

        cp._edge_uid = copy(self._edge_uid)

        return cp

    def cleanup(self, isolates=False, relabel=True, in_place=True):
        if in_place:
            _DH = self
        else:
            _DH = self.copy()

        if not isolates:
            _DH.remove_nodes_from(_DH.nodes.isolates())
        if relabel:
            from ..utils import convert_labels_to_integers

            convert_labels_to_integers(_DH, in_place=True)

        return _DH

    def freeze(self):
        """Method for freezing a dihypergraph which prevents it from being modified

        See Also
        --------
        ~xgi.exception.frozen : Method that raises an error when a user tries to modify the hypergraph
        is_frozen : Check whether a dihypergraph is frozen

        Examples
        --------
        >>> import xgi
        >>> diedgelist = [([1, 2], [2, 3, 4])]
        >>> DH = xgi.DiHypergraph(diedgelist)
        >>> DH.freeze()
        >>> DH.add_node(5)
        Traceback (most recent call last):
        xgi.exception.XGIError: Frozen higher-order network can't be modified

        """
        self.add_node = frozen
        self.add_nodes_from = frozen
        self.remove_node = frozen
        self.remove_nodes_from = frozen
        self.add_edge = frozen
        self.add_edges_from = frozen
        self.remove_edge = frozen
        self.remove_edges_from = frozen
        self.clear = frozen
        self.frozen = True

    @property
    def is_frozen(self):
        """Checks whether a hypergraph is frozen

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
        >>> edges = [([1, 2], [2, 3, 4])]
        >>> DH = xgi.DiHypergraph(edges)
        >>> DH.freeze()
        >>> DH.is_frozen
        True

        """
        try:
            return self.frozen
        except AttributeError:
            return False
