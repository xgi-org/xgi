from ..utils import IDDict, update_uid_counter
from views import NodeView, EdgeView
from ..exception import XGIError
from warnings import warn


class HigherOrderNetwork:
    _node_dict_factory = IDDict
    _node_attr_dict_factory = IDDict
    _edge_dict_factory = IDDict
    _edge_attr_dict_factory = IDDict
    _incidence_attr_dict_factory = IDDict
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
            "_hypergraph": self._hypergraph,
            "_node": self._node,
            "_node_attr": self._node_attr,
            "_edge": self._edge,
            "_edge_attr": self._edge_attr,
            "_incidence_attr": self._incidence_attr,
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
        self._hypergraph = state["_hypergraph"]
        self._node = state["_node"]
        self._node_attr = state["_node_attr"]
        self._edge = state["_edge"]
        self._edge_attr = state["_edge_attr"]
        self._incidence_attr = state["_incidence_attr"]
        self._nodeview = NodeView(self)
        self._edgeview = EdgeView(self)

    def __init__(self):
        self._node = self._node_dict_factory()
        self._edge = self._edge_dict_factory()
        self._node_attr = self._node_attr_dict_factory()
        self._edge_attr = self._edge_attr_dict_factory()
        self._incidence_attr = self._incidence_attr_dict_factory()
        self._net = self._net_attr_dict_factory()

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
                f"{attr} is not a method of Hypergraph or a "
                "recognized NodeStat or EdgeStat"
            )

        def func(node=None, *args, **kwargs):
            val = stat(*args, **kwargs).asdict()
            return val if node is None else val[node]

        func.__doc__ = f"""Equivalent to H.{word}.{attr}.asdict(). For accepted *args and
        **kwargs, see documentation of H.{word}.{attr}."""

        return func

    @property
    def num_nodes(self):
        return len(self._node)

    @property
    def num_edges(self):
        return len(self._edge)

    def clear_edges(self):
        """Remove all edges from the graph without altering any nodes."""
        for node in self.nodes:
            self._node[node] = set()
        self._edge.clear()
        self._edge_attr.clear()

    def clear(self, network_attr=True):
        """Remove all nodes and edges from the graph.

        Also removes node and edge attributes, and optionally network attributes.

        Parameters
        ----------
        network_attr : bool, optional
            Whether to remove attributes as well.
            By default, True.

        """
        self._node.clear()
        self._node_attr.clear()
        self._edge.clear()
        self._edge_attr.clear()
        if network_attr:
            self._net.clear()