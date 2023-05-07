"""Base class for directed hypergraphs."""
from collections import defaultdict
from collections.abc import Hashable, Iterable
from copy import copy, deepcopy
from itertools import count
from warnings import warn

from ..exception import XGIError
from ..utils import IDDict, update_uid_counter
# from .direportviews import EdgeView, NodeView

__all__ = ["DiHypergraph"]


class DiHypergraph:
    r"""A directed hypergraph (dihypergraph) is a collection of directed
    interactions
    
    
    ordered pairs,
    $(e^+, e^-)$, where $e^+$ is known as the tail and is the set of senders in
    this interaction, and $e^-$ is known as the head and is the set of receivers
    in the interaction.

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

    def __init__(self, **attr):
        self._edge_uid = count()
        self._hypergraph = self._hypergraph_attr_dict_factory()
        self._node_in = self._node_dict_factory()
        self._node_out = self._node_dict_factory()
        self._node_attr = self._node_attr_dict_factory()
        self._edge_in = self._hyperedge_dict_factory()
        self._edge_out = self._hyperedge_dict_factory()
        self._edge_attr = self._hyperedge_attr_dict_factory()

        self._hypergraph.update(attr)  # must be after convert

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
        return len(self._node_in)

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
        return len(self._edge_in)

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
        out_edge_neighbors = self._node_in[n]
        in_edge_neighbors = self._node_out[n]
        del self._node_in[n]
        del self._node_out[n]
        del self._node_attr[n]

        if strong:
            for edge in in_edge_neighbors:
                del self._edge_in[edge]
                del self._edge_attr[edge]
            for edge in out_edge_neighbors:
                del self._edge_out[edge]
                del self._edge_attr[edge]
        else:  # weak removal
            for edge in in_edge_neighbors:
                self._edge_in[edge].remove(n)
                if not self._edge_in[edge]:
                    del self._edge_in[edge]
                    del self._edge_out[edge]
                    del self._edge_attr[edge]
            for edge in out_edge_neighbors:
                self._edge_out[edge].remove(n)
                if not self._edge_out[edge]:
                    del self._edge_out[edge]
                    del self._edge_in[edge]
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
        >>> H = xgi.DiHypergraph()
        >>> H.add_edge({"head": [1, 2, 3], "tail": [2, 3, 4]})
        >>> H.add_edge({"head": [3, 4], "tail":{}}, id='myedge')
        """
        if isinstance(members, {tuple, list}):
            tail = members[0]
            head = members[1]
        elif type(members) == dict:
            tail = set(members["tail"])
            head = set(members["head"])
        else:
            raise XGIError("Directed edge must be a dictionary, list, or tuple!")

        if not members:
            raise XGIError("Cannot add an empty edge")

        uid = next(self._edge_uid) if id is None else id

        if id in self._edge_in.keys():  # check that uid is not present yet
            warn(f"uid {id} already exists, cannot add edge {members}")
            return

        self._edge_in[uid] = set()
        self._edge_out[uid] = set()

        for node in head:
            if node not in self._node_out:
                self._node_in[node] = set()
                self._node_out[node] = set()
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node_out[node].add(uid)
            self._edge_in[uid].add(node)

        for node in tail:
            if node not in self._node_in:
                self._node_in[node] = set()
                self._node_out[node] = set()
                self._node_attr[node] = self._node_attr_dict_factory()
            self._node_in[node].add(uid)
            self._edge_out[uid].add(node)

        self._edge_attr[uid] = self._hyperedge_attr_dict_factory()
        self._edge_attr[uid].update(attr)

        if id:  # set self._edge_uid correctly
            update_uid_counter(self, id)

    def add_edges_from(self, ebunch_to_add, **attr):
        """Add multiple edges with optional attributes.

        Parameters
        ----------
        ebunch_to_add : Iterable

            An iterable of edges.  This may be an iterable of iterables (Format 1),
            where each element contains the members of the edge specified as valid node IDs.
            Alternatively, each element could also be a tuple in any of the following
            formats:

            * Format 2: 2-tuple (members, edge_id), or
            * Format 3: 2-tuple (members, attr), or
            * Format 4: 3-tuple (members, edge_id, attr),

            where `members` is an iterable of node IDs, `edge_id` is a hashable to use
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
            for id, members in ebunch_to_add.items():
                if isinstance(members, {tuple, list}):
                    tail = members[0]
                    head = members[1]
                elif type(members) == dict:
                    tail = set(members["tail"])
                    head = set(members["head"])
                else:
                    raise XGIError("Directed edge must be a dictionary, list, or tuple!")
                
                if id in self._edge_in.keys():  # check that uid is not present yet
                    warn(f"uid {id} already exists, cannot add edge {members}.")
                    continue
                try:
                    self._edge_in[id] = set(head)
                    self._edge_out[id] = set(tail)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e

                for n in head:
                    if n not in self._node_in:
                        self._node_in[n] = set()
                        self._node_out[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node_out[n].add(id)

                for n in tail:
                    if n not in self._node_in:
                        self._node_in[n] = set()
                        self._node_out[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node_in[n].add(id)
                self._edge_attr[id] = self._hyperedge_attr_dict_factory()

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
        if not isinstance(first_edge, dict):
            if len(first_edge) == 2 and issubclass(type(first_edge[1]), Hashable):
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

            if id in self._edge_in.keys():  # check that uid is not present yet
                warn(f"uid {id} already exists, cannot add edge {members}.")
            else:
                try:
                    head = set(members["head"])
                    tail = set(members["tail"])
                except TypeError:
                    raise XGIError("Edge must be a dictionary with head and tail keys!")

                try:
                    self._edge_in[id] = set(head)
                    self._edge_out[id] = set(tail)
                except TypeError as e:
                    raise XGIError("Invalid ebunch format") from e

                for n in head:
                    if n not in self._node_out:
                        self._node_in[n] = set()
                        self._node_out[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node_out[n].add(id)

                for n in tail:
                    if n not in self._node_in:
                        self._node_in[n] = set()
                        self._node_out[n] = set()
                        self._node_attr[n] = self._node_attr_dict_factory()
                    self._node_in[n].add(id)

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
