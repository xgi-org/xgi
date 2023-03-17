"""Base class for undirected hypergraphs."""
from collections import defaultdict
from collections.abc import Hashable, Iterable
from copy import copy, deepcopy
from itertools import count
from warnings import warn

from ..exception import XGIError
from ..utils import IDDict, update_uid_counter
from .reportviews import EdgeView, NodeView

__all__ = ["Hypergraph"]


class DiHypergraph:
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
        self._node_in = self._node_dict_factory()
        self._node_out = self._node_dict_factory()
        self._node_attr = self._node_attr_dict_factory()
        self._edge_in = self._hyperedge_dict_factory()
        self._edge_out = self._hyperedge_dict_factory()
        self._edge_attr = self._hyperedge_attr_dict_factory()

        # self._nodeview = NodeView(self)
        # """A :class:`~xgi.classes.reportviews.NodeView` of the hypergraph."""

        # self._edgeview = EdgeView(self)
        # """An :class:`~xgi.classes.reportviews.EdgeView` of the hypergraph."""

        if incoming_data is not None:
            # This import needs to happen when this function is called, not when it is
            # defined.  Otherwise, a circular import error would happen.
            from ..convert import convert_to_hypergraph

            convert_to_hypergraph(incoming_data, create_using=self)
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
                    del self._edge_attr[edge]
            for edge in out_edge_neighbors:
                self._edge_out[edge].remove(n)
                if not self._edge_out[edge]:
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
            if n not in self._node:
                warn(f"Node {n} not in hypergraph")
                continue
            self.remove_node(n)

    def add_edge(self, members, id=None, **attr):
        try:
            head = set(members["head"])
            tail = set(members["tail"])
        except TypeError:
            raise XGIError("Edge must be a dictionary with head and tail keys!")

        if not members:
            raise XGIError("Cannot add an empty edge")

        if id in self._edge_in.keys():  # check that uid is not present yet
            warn(f"uid {id} already exists, cannot add edge {members}")
            return

        uid = next(self._edge_uid) if id is None else id

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

                self._edge_attr[id] = self._hyperedge_attr_dict_factory()
                self._edge_attr[id].update(attr)
                self._edge_attr[id].update(eattr)

            try:
                e = next(new_edges)
            except StopIteration:

                if format2 or format4:
                    update_uid_counter(self, id)
                break

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