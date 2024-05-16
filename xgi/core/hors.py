from ..utils import IDDict, update_uid_counter
from views import NodeView, EdgeView
from ..exception import XGIError
from warnings import warn


class HigherOrderSystem:
    _node_dict_factory = IDDict
    _node_attr_dict_factory = IDDict
    _edge_dict_factory = IDDict
    _edge_attr_dict_factory = IDDict
    _incidence_attr_dict_factory = IDDict
    _net_attr_dict_factory = dict

    def __init__(self, data=None, directed=False):
        self._node = self._node_dict_factory()
        self._edge = self._edge_dict_factory()
        self._node_attr = self._node_attr_dict_factory()
        self._edge_attr = self._edge_attr_dict_factory()
        self._incidence_attr = self._incidence_attr_dict_factory()
        self._net = self._net_attr_dict_factory()
        self._nodeview = NodeView(self)
        self._edgeview = EdgeView(self)
        self._directed = directed

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
        return len(self._node)

    @property
    def num_edges(self):
        return len(self._edge)

    def add_node(self, node, **attr):
        if node not in self._node:
            self._node[node] = [set(), set()] if self.directed else set()
            self._node_attr[node] = self._node_attr_dict_factory()
        self._node_attr[node].update(attr)


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
    >>> DH = xgi.DiHypergraph()
    >>> DH.add_edge(([1, 2, 3], [2, 3, 4]))
    >>> DH.add_edge(([3, 4], set()), id='myedge')
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

# 3 ideas:
# 1) _edge and _node for all classes: _edge is either a list or set or a 2-list of lists or sets.
# Not super explainable, tho. Could make it a dict of dict, tho?
# 2) _edge_in and _edge_out for all classes: undirected uses the _edge_in only
# 3) base-level add/remove edges/nodes, cleanup.

# The dual (in my opinion) implies that we should use approach 1.
# not 