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
from .diviews import DiEdgeView, DiNodeView

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

    Notes
    -----
    Unique IDs are assigned to each node and edge internally and are used to refer to
    them throughout.

    The `attr` keyword arguments are added as hypergraph attributes. To add node or edge
    attributes see :meth:`add_node` and :meth:`add_edge`.

    In addition to the methods listed in this page, other methods defined in the `stats`
    package are also accessible via the `DiHypergraph` class.  For more details, see the
    `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    References
    ----------
    Bretto, Alain. "Hypergraph theory: An introduction."
    Mathematical Engineering. Cham: Springer (2013).
    Examples
    --------
    >>> import xgi
    >>> H = xgi.DiHypergraph([([1, 2, 3], [4]), ([5, 6], [6, 7, 8])])
    >>> H.nodes
    DiNodeView((1, 2, 3, 4, 5, 6, 7, 8))
    >>> H.edges
    DiEdgeView((0, 1))
    >>> [[sorted(h), sorted(t)] for h, t in H.edges.dimembers()]
    [[[1, 2, 3], [4]], [[5, 6], [6, 7, 8]]]
    >>> [sorted(e) for e in H.edges.members()]
    [[1, 2, 3, 4], [5, 6, 7, 8]]
    """
    _node_dict_factory = IDDict
    _node_attr_dict_factory = IDDict
    _hyperedge_dict_factory = IDDict
    _hyperedge_attr_dict_factory = IDDict
    _hypergraph_attr_dict_factory = dict

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
            "_hypergraph": self._hypergraph,
            "_node_in": self._node_in,
            "_node_out": self._node_out,
            "_node_attr": self._node_attr,
            "_edge_in": self._edge_in,
            "_edge_out": self._edge_out,
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
        self._hypergraph = state["_hypergraph"]
        self._node_in = state["_node_in"]
        self._node_out = state["_node_out"]
        self._node_attr = state["_node_attr"]
        self._edge_in = state["_edge_in"]
        self._edge_out = state["_edge_out"]
        self._edge_attr = state["_edge_attr"]
        self._nodeview = DiNodeView(self)
        self._edgeview = DiEdgeView(self)

    def __init__(self, incoming_data=None, **attr):
        self._edge_uid = count()
        self._hypergraph = self._hypergraph_attr_dict_factory()

        self._node_in = self._node_dict_factory()
        self._node_out = self._node_dict_factory()
        self._node_attr = self._node_attr_dict_factory()

        self._edge_in = self._hyperedge_dict_factory()
        self._edge_out = self._hyperedge_dict_factory()
        self._edge_attr = self._hyperedge_attr_dict_factory()

        self._nodeview = DiNodeView(self)
        """A :class:`~xgi.core.direportviews.DiNodeView` of the directed hypergraph."""

        self._edgeview = DiEdgeView(self)
        """An :class:`~xgi.core.direportviews.DiEdgeView` of the directed hypergraph."""

        if incoming_data is not None:
            # This import needs to happen when this function is called, not when it is
            # defined.  Otherwise, a circular import error would happen.
            from ..convert import convert_to_dihypergraph

            convert_to_dihypergraph(incoming_data, create_using=self)
        self._hypergraph.update(attr)  # must be after convert

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
        return iter(self._node_in)

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
            return n in self._node_in
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
        return len(self._node_in)

    def __getitem__(self, attr):
        """Read dihypergraph attribute."""
        try:
            return self._hypergraph[attr]
        except KeyError:
            raise XGIError("This attribute has not been set.")

    def __setitem__(self, attr, val):
        """Write dihypergraph attribute."""
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
                f"{attr} is not a method of DiHypergraph or a recognized DiNodeStat or DiEdgeStat"
            )

        def func(node=None, *args, **kwargs):
            val = stat(*args, **kwargs).asdict()
            return val if node is None else val[node]

        func.__doc__ = f"""Equivalent to H.{word}.{attr}.asdict(). For accepted *args and
        **kwargs, see documentation of H.{word}.{attr}."""

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
        >>> H = xgi.DiHypergraph(hyperedge_list)
        >>> H.num_nodes
        4

        """
        return len(self._node_in)

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
        >>> H = xgi.DiHypergraph(hyperedge_list)
        >>> H.num_edges
        1
        """
        return len(self._edge_in)

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
        if node not in self._node_in:
            self._node_in[node] = set()
            self._node_out[node] = set()
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
                newnode = n not in self._node_in
                newdict = attr
            except TypeError:
                n, ndict = n
                newnode = n not in self._node_in
                newdict = attr.copy()
                newdict.update(ndict)
            if newnode:
                self._node_in[n] = set()
                self._node_out[n] = set()
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
            A node in the dihypergraph

        strong : bool (default False)
            Whether to execute weak or strong removal.

        Raises
        ------
        XGIError
           If n is not in the dihypergraph.

        See Also
        --------
        remove_nodes_from

        """
        out_edge_neighbors = self._node_in[n]
        in_edge_neighbors = self._node_out[n]
        del self._node_in[n]
        del self._node_out[n]
        del self._node_attr[n]

        if strong:
            for edge in in_edge_neighbors.union(out_edge_neighbors):
                del self._edge_in[edge]
                del self._edge_out[edge]
                del self._edge_attr[edge]
        else:  # weak removal
            for edge in in_edge_neighbors:
                self._edge_in[edge].remove(n)

            for edge in out_edge_neighbors:
                self._edge_out[edge].remove(n)

            # remove empty edges
            for edge in in_edge_neighbors.union(out_edge_neighbors):
                if not self._edge_in[edge] and not self._edge_out[edge]:
                    del self._edge_in[edge]
                    del self._edge_out[edge]
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
            if n not in self._node_in:
                warn(f"Node {n} not in dihypergraph")
                continue
            self.remove_node(n)

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
            An list or tuple (size 2) of iterables. The first entry contains the
            elements of the tail and the second entry contains the elements
            of the head.
        id : hashable, default None
            Id of the new edge. If None, a unique numeric ID will be created.
        **attr : dict, optional
            Attributes of the new edge.

        Raises
        -----
        XGIError
            If `members` is empty or is not a list or tuple.

        See Also
        --------
        add_edges_from : Add a collection of edges.

        Examples
        --------

        Add edges with or without specifying an edge id.

        >>> import xgi
        >>> H = xgi.DiHypergraph()
        >>> H.add_edge(([1, 2, 3], [2, 3, 4]))
        >>> H.add_edge(([3, 4], set()), id='myedge')
        """
        if not members:
            raise XGIError("Cannot add an empty edge")

        if isinstance(members, (tuple, list)):
            tail = members[0]
            head = members[1]
        else:
            raise XGIError("Directed edge must be a list or tuple!")

        if not head and not tail:
            raise XGIError("Cannot add an empty edge")

        uid = next(self._edge_uid) if id is None else id

        if id in self._edge_in.keys():  # check that uid is not present yet
            warn(f"uid {id} already exists, cannot add edge {members}")
            return

        self._edge_in[uid] = set()
        self._edge_out[uid] = set()

        for node in tail:
            if node not in self._node_in:
                self._node_in[node] = set()
                self._node_out[node] = set()
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node_in[node].add(uid)
            self._edge_out[uid].add(node)

        for node in head:
            if node not in self._node_out:
                self._node_in[node] = set()
                self._node_out[node] = set()
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node_out[node].add(uid)
            self._edge_in[uid].add(node)

        self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
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

        attr : \*\*kwargs, optional
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
        >>> H = xgi.DiHypergraph()

        When specifying edges by their members only, numeric edge IDs will be assigned
        automatically.

        >>> H.add_edges_from([([0, 1], [1, 2]), ([2, 3, 4], [])])
        >>> H.edges.dimembers(dtype=dict)
        {0: ({0, 1}, {1, 2}), 1: ({2, 3, 4}, set())}

        Custom edge ids can be specified using a dict.

        >>> H = xgi.DiHypergraph()
        >>> H.add_edges_from({'one': ([0, 1], [1, 2]), 'two': ([2, 3, 4], [])})
        >>> H.edges.dimembers(dtype=dict)
        {'one': ({0, 1}, {1, 2}), 'two': ({2, 3, 4}, set())}

        You can use the dict format to easily add edges from another hypergraph.

        >>> H2 = xgi.DiHypergraph()
        >>> H2.add_edges_from(H.edges.dimembers(dtype=dict))
        >>> H.edges == H2.edges
        True

        Alternatively, edge ids can be specified using an iterable of 2-tuples.

        >>> H = xgi.DiHypergraph()
        >>> H.add_edges_from([(([0, 1], [1, 2]), 'one'), (([2, 3, 4], []), 'two')])
        >>> H.edges.dimembers(dtype=dict)
        {'one': ({0, 1}, {1, 2}), 'two': ({2, 3, 4}, set())}

        Attributes for each edge may be specified using a 2-tuple for each edge.
        Numeric IDs will be assigned automatically.

        >>> H = xgi.DiHypergraph()
        >>> edges = [
        ...     (([0, 1], [1, 2]), {'color': 'red'}),
        ...     (([2, 3, 4], []), {'color': 'blue', 'age': 40}),
        ... ]
        >>> H.add_edges_from(edges)
        >>> {e: H.edges[e] for e in H.edges}
        {0: {'color': 'red'}, 1: {'color': 'blue', 'age': 40}}

        Attributes and custom IDs may be specified using a 3-tuple for each edge.

        >>> H = xgi.DiHypergraph()
        >>> edges = [
        ...     (([0, 1], [1, 2]), 'one', {'color': 'red'}),
        ...     (([2, 3, 4], []), 'two', {'color': 'blue', 'age': 40}),
        ... ]
        >>> H.add_edges_from(edges)
        >>> {e: H.edges[e] for e in H.edges}
        {'one': {'color': 'red'}, 'two': {'color': 'blue', 'age': 40}}

        """
        # format 5 is the easiest one
        if isinstance(ebunch_to_add, dict):
            for id, members in ebunch_to_add.items():
                if id in self._edge_in.keys():  # check that uid is not present yet
                    warn(f"uid {id} already exists, cannot add edge {members}.")
                    continue

                if isinstance(members, (tuple, list)):
                    tail = members[0]
                    head = members[1]
                else:
                    raise XGIError("Directed edge must be a list or tuple!")

                try:
                    self._edge_in[id] = set(head)
                    self._edge_out[id] = set(tail)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e

                for n in tail:
                    if n not in self._node_in:
                        self._node_in[n] = set()
                        self._node_out[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node_in[n].add(id)
                self._edge_attr[id] = self._hyperedge_attr_dict_factory()

                for n in head:
                    if n not in self._node_in:
                        self._node_in[n] = set()
                        self._node_out[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node_out[n].add(id)

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

            if id in self._edge_in.keys():  # check that uid is not present yet
                warn(f"uid {id} already exists, cannot add edge {members}.")
            else:
                try:
                    tail = members[0]
                    head = members[1]
                    self._edge_out[id] = set(tail)
                    self._edge_in[id] = set(head)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e

                for node in tail:
                    if node not in self._node_in:
                        self._node_in[node] = set()
                        self._node_out[node] = set()
                        self._node_attr[node] = self._node_attr_dict_factory()
                    self._node_in[node].add(id)
                    self._edge_out[id].add(node)

                for node in head:
                    if node not in self._node_out:
                        self._node_in[node] = set()
                        self._node_out[node] = set()
                        self._node_attr[node] = self._node_attr_dict_factory()
                    self._node_out[node].add(id)
                    self._edge_in[id].add(node)

                self._edge_attr[id] = self._hyperedge_attr_dict_factory()
                self._edge_attr[id].update(attr)
                self._edge_attr[id].update(eattr)

            try:
                e = next(new_edges)
            except StopIteration:
                if format2 or format4:
                    update_uid_counter(self, id)
                break

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
        head = self._edge_in[id].copy()
        tail = self._edge_out[id].copy()

        for node in head:
            self._node_out[node].remove(id)
        for node in tail:
            self._node_in[node].remove(id)

        del self._edge_in[id]
        del self._edge_out[id]
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
            head = self._edge_in[id].copy()
            tail = self._edge_out[id].copy()

            for node in head:
                self._node_out[node].remove(id)
            for node in tail:
                self._node_in[node].remove(id)

            del self._edge_in[id]
            del self._edge_out[id]
            del self._edge_attr[id]

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
                        self._edge_attr[id][name] = value
                    except IDNotFound:
                        warn(f"Edge {e} does not exist!")
            except AttributeError:
                # treat `values` as a constant
                for e in self._edge_in:
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

    def clear(self, hypergraph_attr=True):
        """Remove all nodes and edges from the graph.

        Also removes node and edge attributes, and optionally hypergraph attributes.

        Parameters
        ----------
        hypergraph_attr : bool, optional
            Whether to remove hypergraph attributes as well.
            By default, True.

        """
        self._node_in.clear()
        self._node_out.clear()
        self._node_attr.clear()
        self._edge_in.clear()
        self._edge_out.clear()
        self._edge_attr.clear()
        if hypergraph_attr:
            self._hypergraph.clear()

    def copy(self):
        """A deep copy of the dihypergraph.

        A deep copy of the dihypergraph, including node, edge, and hypergraph attributes.

        Returns
        -------
        H : DiHypergraph
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
        cp._hypergraph = deepcopy(self._hypergraph)

        cp._edge_uid = copy(self._edge_uid)

        return cp

    def freeze(self):
        """Method for freezing a dihypergraph which prevents it from being modified

        See Also
        --------
        frozen : Method that raises an error when a user tries to modify the hypergraph
        is_frozen : Check whether a dihypergraph is frozen

        Examples
        --------
        >>> import xgi
        >>> diedgelist = [([1, 2], [2, 3, 4])]
        >>> H = xgi.DiHypergraph(diedgelist)
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
        >>> H = xgi.DiHypergraph(edges)
        >>> H.freeze()
        >>> H.is_frozen()
        True

        """
        try:
            return self.frozen
        except AttributeError:
            return False
