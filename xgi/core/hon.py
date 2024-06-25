from itertools import count
from warnings import warn

from ..exception import IDNotFound, XGIError
from ..utils import IDDict


class HigherOrderNetwork:
    _node_dict_factory = IDDict
    _node_attr_dict_factory = IDDict
    _edge_dict_factory = IDDict
    _edge_attr_dict_factory = IDDict
    _incidence_attr_dict_factory = IDDict
    _net_attr_dict_factory = dict

    def __init__(self, nodeview, edgeview):
        self._node = self._node_dict_factory()
        self._edge = self._edge_dict_factory()
        self._node_attr = self._node_attr_dict_factory()
        self._edge_attr = self._edge_attr_dict_factory()
        self._incidence_attr = self._incidence_attr_dict_factory()
        self._net_attr = self._net_attr_dict_factory()
        self._edge_uid = count()

        self._nodeview = nodeview(self)
        self._edgeview = edgeview(self)

    def __iter__(self):
        """Iterate over the nodes.

        Returns
        -------
        iterator
            An iterator over all nodes in the higher-order network.
        """
        return iter(self._node)

    def __contains__(self, n):
        """Check for if a node is in this higher-order network.

        Parameters
        ----------
        n : hashable
            node ID

        Returns
        -------
        bool
            Whether the node exists in the higher-order network.
        """
        try:
            return n in self._node
        except TypeError:
            return False

    def __len__(self):
        """Number of nodes in the higher-order network.

        Returns
        -------
        int
            The number of nodes in the higher-order network.

        See Also
        --------
        num_nodes : identical method
        num_edges : number of edges in the higher-order network

        """
        return len(self._node)

    def __getitem__(self, attr):
        """Read higher-order network attribute."""
        try:
            return self._net_attr[attr]
        except KeyError:
            raise XGIError("This attribute has not been set.")

    def __setitem__(self, attr, val):
        """Write higher-order network attribute."""
        self._net_attr[attr] = val

    @property
    def num_nodes(self):
        return len(self._node)

    @property
    def num_edges(self):
        return len(self._edge)

    @property
    def nodes(self):
        """A :class:`NodeView` of this network."""
        return self._nodeview

    @property
    def edges(self):
        """An :class:`EdgeView` of this network."""
        return self._edgeview

    @property
    def is_frozen(self):
        """Checks whether a simplicial complex is frozen

        Returns
        -------
        bool
            True if simplicial complex is frozen, false if not.

        See Also
        --------
        freeze : A method to prevent a simplicial complex from being modified.

        Examples
        --------
        >>> import xgi
        >>> edges = [[1, 2], [2, 3, 4]]
        >>> S = xgi.SimplicialComplex(edges)
        >>> S.freeze()
        >>> S.is_frozen
        True
        """
        try:
            return self.frozen
        except AttributeError:
            return False

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
        After computing some property of the nodes of a higher-order network, you may
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

    def clear_edges(self):
        """Remove all edges from the graph without altering any nodes."""
        for node in self.nodes:
            self._node[node] = set()
        self._edge.clear()
        self._edge_attr.clear()
        self._incidence_attr.clear()

    def clear(self, clear_network_attrs=True):
        """Remove all nodes and edges from the graph.

        Also removes node and edge attributes, and optionally network attributes.

        Parameters
        ----------
        clear_network_attrs : bool, optional
            Whether to remove attributes as well.
            By default, True.

        """
        self._node.clear()
        self._node_attr.clear()
        self._edge.clear()
        self._edge_attr.clear()
        self._incidence_attr.clear()
        if clear_network_attrs:
            self._net_attr.clear()
