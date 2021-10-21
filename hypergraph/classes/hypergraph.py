"""Base class for undirected graphs.

The Graph class allows any hashable object as a node
and can associate key/value attribute pairs with each undirected edge.

Self-loops are allowed but multiple edges are not (see MultiGraph).

For directed graphs see DiGraph and MultiDiGraph.
"""
from copy import deepcopy

# from hypergraph.classes.coreviews import AdjacencyView
from hypergraph.classes.reportviews import (
    NodeView,
    EdgeView,
    NodeDegreeView,
    EdgeDegreeView,
)
from hypergraph.exception import HypergraphError, HypergraphException
import hypergraph.convert as convert
import numpy as np
from hypergraph.utils import HypergraphCounter
import hypergraph as hg

__all__ = ["Hypergraph"]


class Hypergraph:

    node_dict_factory = dict
    node_attr_dict_factory = dict
    hyperedge_dict_factory = dict
    hyperedge_attr_dict_factory = dict
    hypergraph_attr_dict_factory = dict

    def __init__(self, incoming_hypergraph_data=None, **attr):
        """Initialize a graph with edges, name, or graph attributes.

        Parameters
        ----------
        incoming_graph_data : input hypergraph (optional, default: None)
            Data to initialize graph. If None (default) an empty
            graph is created.  The data can be an edge list, or any
            NetworkX graph object.  If the corresponding optional Python
            packages are installed the data can also be a NumPy matrix
            or 2d ndarray, a SciPy sparse matrix, or a PyGraphviz graph.

        attr : keyword arguments, optional (default= no attributes)
            Attributes to add to graph as key=value pairs.
        """
        self._edge_uid = HypergraphCounter()

        self.hypergraph_attr_dict_factory = self.hypergraph_attr_dict_factory
        self.node_dict_factory = self.node_dict_factory
        self.node_attr_dict_factory = self.node_attr_dict_factory
        self.hyperedge_attr_dict_factory = self.hyperedge_attr_dict_factory

        self._hypergraph = (
            self.hypergraph_attr_dict_factory()
        )  # dictionary for graph attributes
        self._node = self.node_dict_factory()  # empty node attribute dict
        self._node_attr = self.node_attr_dict_factory()
        self._edge = self.hyperedge_dict_factory()
        self._edge_attr = self.hyperedge_attr_dict_factory()  # empty adjacency dict
        # attempt to load graph with data
        if incoming_hypergraph_data is not None:
            # convert.to_networkx_graph(incoming_hypergraph_data, create_using=self)
            convert.convert_to_hypergraph(incoming_hypergraph_data, create_using=self)
        # load graph attributes (must be after convert)
        self._hypergraph.update(attr)

    @property
    def name(self):
        """String identifier of the hypergraph.

        This hypergraph attribute appears in the attribute dict H._hypergraph
        keyed by the string `"name"`. as well as an attribute (technically
        a property) `H.name`. This is entirely user controlled.
        """
        return self._hypergraph.get("name", "")

    @name.setter
    def name(self, s):
        self._hypergraph["name"] = s

    def __str__(self):
        """Returns a short summary of the graph.

        Returns
        -------
        info : string
            Graph information as provided by `nx.info`

        Examples
        --------
        >>> H = hg.Hypergraph(name="foo")
        >>> str(H)
        "Hypergraph named 'foo' with 0 nodes and 0 edges"

        >>> H = nx.path_graph(3)
        >>> str(H)
        'Hypergraph with 3 nodes and 2 edges'

        """
        return "".join(
            [
                type(self).__name__,
                f" named {self.name!r}" if self.name else "",
                f" with {self.number_of_nodes()} nodes and {self.number_of_edges()} hyperedges",
            ]
        )

    def __iter__(self):
        """Iterate over the nodes. Use: 'for n in H'.

        Returns
        -------
        niter : iterator
            An iterator over all nodes in the hypergraph.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> [n for n in H]
        [0, 1, 2, 3]
        >>> list(H)
        [0, 1, 2, 3]
        """
        return iter(self._node)

    def __contains__(self, n):
        """Returns True if n is a node, False otherwise. Use: 'n in H'.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> 1 in H
        True
        """
        try:
            return n in self._node
        except TypeError:
            return False

    def __len__(self):
        """Returns the number of nodes in the graph. Use: 'len(H)'.

        Returns
        -------
        nnodes : int
            The number of nodes in the graph.

        See Also
        --------
        number_of_nodes: identical method
        order: identical method

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> len(H)
        4

        """
        return len(self._node)

    def __getitem__(self, n):
        """Returns a dict of neighbors of node n.  Use: 'H[n]'.

        Parameters
        ----------
        n : node
           A node in the graph.

        Returns
        -------
        adj_dict : dictionary
           The adjacency dictionary for nodes connected to n.

        Notes
        -----
        H[n] is the same as H.adj[n] and similar to H.neighbors(n)
        (which is an iterator over H.adj[n])

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H[0]
        AtlasView({1: {}})
        """
        return self.adj[n]

    @property
    def shape(self):
        return len(self._node), len(self._edge)

    def add_node(self, node_for_adding, **attr):
        """Add a single node `node_for_adding` and update node attributes.

        Parameters
        ----------
        node_for_adding : node
            A node can be any hashable Python object except None.
        attr : keyword arguments, optional
            Set or change node attributes using key=value.

        See Also
        --------
        add_nodes_from

        Examples
        --------
        >>> H = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.add_node(1)
        >>> H.add_node("Hello")
        >>> K3 = nx.Graph([(0, 1), (1, 2), (2, 0)])
        >>> H.add_node(K3)
        >>> H.number_of_nodes()
        3

        Use keywords set/change node attributes:

        >>> H.add_node(1, size=10)
        >>> H.add_node(3, weight=0.4, UTM=("13S", 382871, 3972649))

        Notes
        -----
        A hashable object is one that can be used as a key in a Python
        dictionary. This includes strings, numbers, tuples of strings
        and numbers, etc.

        On many platforms hashable items also include mutables such as
        NetworkX Graphs, though one should be careful that the hash
        doesn't change on mutables.
        """
        if node_for_adding not in self._node:
            if node_for_adding is None:
                raise ValueError("None cannot be a node")
            self._node[node_for_adding] = set()
            self._node_attr[node_for_adding] = self.node_attr_dict_factory()
        else:  # update attr even if node already exists
            self._node_attr[node_for_adding].update(attr)

    def add_nodes_from(self, nodes_for_adding, **attr):
        """Add multiple nodes.

        Parameters
        ----------
        nodes_for_adding : iterable container
            A container of nodes (list, dict, set, etc.).
            OR
            A container of (node, attribute dict) tuples.
            Node attributes are updated using the attribute dict.
        attr : keyword arguments, optional (default= no attributes)
            Update attributes for all nodes in nodes.
            Node attributes specified in nodes as a tuple take
            precedence over attributes specified via keyword arguments.

        See Also
        --------
        add_node

        Examples
        --------
        >>> H = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.add_nodes_from("Hello")
        >>> K3 = nx.Graph([(0, 1), (1, 2), (2, 0)])
        >>> H.add_nodes_from(K3)
        >>> sorted(H.nodes(), key=str)
        [0, 1, 2, 'H', 'e', 'l', 'o']

        Use keywords to update specific node attributes for every node.

        >>> H.add_nodes_from([1, 2], size=10)
        >>> H.add_nodes_from([3, 4], weight=0.4)

        Use (node, attrdict) tuples to update attributes for specific nodes.

        >>> H.add_nodes_from([(1, dict(size=11)), (2, {"color": "blue"})])
        >>> H.nodes[1]["size"]
        11
        >>> H = nx.Graph()
        >>> H.add_nodes_from(H.nodes(data=True))
        >>> H.nodes[1]["size"]
        11

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
                if n is None:
                    raise ValueError("None cannot be a node")
                self._node[n] = set()
                self._node_attr[n] = self.node_attr_dict_factory()
            self._node_attr[n].update(newdict)

    def remove_node(self, n):
        """Remove node n.

        Removes the node n and all adjacent edges.
        Attempting to remove a non-existent node will raise an exception.

        Parameters
        ----------
        n : node
           A node in the graph

        Raises
        ------
        NetworkXError
           If n is not in the graph.

        See Also
        --------
        remove_nodes_from

        Examples
        --------
        >>> H = nx.path_graph(3)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> list(H.edges)
        [(0, 1), (1, 2)]
        >>> H.remove_node(1)
        >>> list(H.edges)
        []

        """
        try:
            edge_neighbors = self.nodes[n]  # list handles self-loops (allows mutation)
            del self._node[n]
            del self._node_attr[n]
        except KeyError as e:  # NetworkXError if n not in self
            raise HypergraphError(f"The node {n} is not in the graph.") from e
        for edge in edge_neighbors:
            self._edge[edge].remove(n)  # remove all edges n-u in graph
            if len(self._edge[edge]) == 0:
                del self._edge[edge]

    def remove_nodes_from(self, nodes):
        """Remove multiple nodes.

        Parameters
        ----------
        nodes : iterable container
            A container of nodes (list, dict, set, etc.).  If a node
            in the container is not in the graph it is silently
            ignored.

        See Also
        --------
        remove_node

        Examples
        --------
        >>> H = nx.path_graph(3)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> e = list(H.nodes)
        >>> e
        [0, 1, 2]
        >>> H.remove_nodes_from(e)
        >>> list(H.nodes)
        []

        """
        for n in nodes:
            try:
                edge_neighbors = self.nodes[
                    n
                ]  # list handles self-loops (allows mutation)
                del self._node[n]
                del self._node_attr[n]
                for edge in edge_neighbors:
                    self._edge[edge].remove(n)  # remove all edges n-u in graph
                    # delete empty edges
                    if len(self._edge[edge]) == 0:
                        del self._edge[edge]
            except KeyError as e:  # NetworkXError if n not in self
                pass

    @property
    def nodes(self):
        """A NodeView of the Graph as H.nodes or H.nodes().

        Can be used as `H.nodes` for data lookup and for set-like operations.
        Can also be used as `H.nodes(data='color', default=None)` to return a
        NodeDataView which reports specific node data but no set operations.
        It presents a dict-like interface as well with `H.nodes.items()`
        iterating over `(node, nodedata)` 2-tuples and `H.nodes[3]['foo']`
        providing the value of the `foo` attribute for node `3`. In addition,
        a view `H.nodes.data('foo')` provides a dict-like interface to the
        `foo` attribute of each node. `H.nodes.data('foo', default=1)`
        provides a default for nodes that do not have attribute `foo`.

        Parameters
        ----------
        data : string or bool, optional (default=False)
            The node attribute returned in 2-tuple (n, ddict[data]).
            If True, return entire node attribute dict as (n, ddict).
            If False, return just the nodes n.

        default : value, optional (default=None)
            Value used for nodes that don't have the requested attribute.
            Only relevant if data is not True or False.

        Returns
        -------
        NodeView
            Allows set-like operations over the nodes as well as node
            attribute dict lookup and calling to get a NodeDataView.
            A NodeDataView iterates over `(n, data)` and has no set operations.
            A NodeView iterates over `n` and includes set operations.

            When called, if data is False, an iterator over nodes.
            Otherwise an iterator of 2-tuples (node, attribute value)
            where the attribute is specified in `data`.
            If data is True then the attribute becomes the
            entire data dictionary.

        Notes
        -----
        If your node data is not needed, it is simpler and equivalent
        to use the expression ``for n in H``, or ``list(H)``.

        Examples
        --------
        There are two simple ways of getting a list of all nodes in the graph:

        >>> H = nx.path_graph(3)
        >>> list(H.nodes)
        [0, 1, 2]
        >>> list(H)
        [0, 1, 2]

        To get the node data along with the nodes:

        >>> H.add_node(1, time="5pm")
        >>> H.nodes[0]["foo"] = "bar"
        >>> list(H.nodes(data=True))
        [(0, {'foo': 'bar'}), (1, {'time': '5pm'}), (2, {})]
        >>> list(H.nodes.data())
        [(0, {'foo': 'bar'}), (1, {'time': '5pm'}), (2, {})]

        >>> list(H.nodes(data="foo"))
        [(0, 'bar'), (1, None), (2, None)]
        >>> list(H.nodes.data("foo"))
        [(0, 'bar'), (1, None), (2, None)]

        >>> list(H.nodes(data="time"))
        [(0, None), (1, '5pm'), (2, None)]
        >>> list(H.nodes.data("time"))
        [(0, None), (1, '5pm'), (2, None)]

        >>> list(H.nodes(data="time", default="Not Available"))
        [(0, 'Not Available'), (1, '5pm'), (2, 'Not Available')]
        >>> list(H.nodes.data("time", default="Not Available"))
        [(0, 'Not Available'), (1, '5pm'), (2, 'Not Available')]

        If some of your nodes have an attribute and the rest are assumed
        to have a default attribute value you can create a dictionary
        from node/attribute pairs using the `default` keyword argument
        to guarantee the value is never None::

            >>> H = nx.Graph()
            >>> H.add_node(0)
            >>> H.add_node(1, weight=2)
            >>> H.add_node(2, weight=3)
            >>> dict(H.nodes(data="weight", default=1))
            {0: 1, 1: 2, 2: 3}

        """
        nodes = NodeView(self)
        # Lazy View creation: overload the (class) property on the instance
        # Then future H.nodes use the existing View
        # setattr doesn't work because attribute already exists
        self.__dict__["nodes"] = nodes
        return nodes

    def number_of_nodes(self):
        """Returns the number of nodes in the graph.

        Returns
        -------
        nnodes : int
            The number of nodes in the graph.

        See Also
        --------
        order: identical method
        __len__: identical method

        Examples
        --------
        >>> H = nx.path_graph(3)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.number_of_nodes()
        3
        """
        return len(self._node)

    def order(self):
        """Returns the number of nodes in the graph.

        Returns
        -------
        nnodes : int
            The number of nodes in the graph.

        See Also
        --------
        number_of_nodes: identical method
        __len__: identical method

        Examples
        --------
        >>> H = nx.path_graph(3)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.order()
        3
        """
        return len(self._node)

    def has_node(self, n):
        """Returns True if the graph contains the node n.

        Identical to `n in H`

        Parameters
        ----------
        n : node

        Examples
        --------
        >>> H = nx.path_graph(3)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.has_node(0)
        True

        It is more readable and simpler to use

        >>> 0 in H
        True

        """
        try:
            return n in self._node
        except TypeError:
            return False

    def add_edge(self, edge, **attr):
        """Add an edge between u and v.

        The nodes u and v will be automatically added if they are
        not already in the graph.

        Edge attributes can be specified with keywords or by directly
        accessing the edge's attribute dictionary. See examples below.

        Parameters
        ----------
        edge : an container or iterable of hashables
            A list of node ids
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edges_from : add a collection of edges

        Notes
        -----
        Adding an edge that already exists updates the edge data.

        Many NetworkX algorithms designed for weighted graphs use
        an edge attribute (by default `weight`) to hold a numerical value.

        Examples
        --------
        The following all add the edge e=(1, 2) to graph H:

        >>> H = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> e = (1, 2)
        >>> H.add_edge(1, 2)  # explicit two-node form
        >>> H.add_edge(*e)  # single edge as tuple of two nodes
        >>> H.add_edges_from([(1, 2)])  # add edges from iterable container

        Associate data to edges using keywords:

        >>> H.add_edge(1, 2, weight=3)
        >>> H.add_edge(1, 3, weight=7, capacity=15, length=342.7)

        For non-string attribute keys, use subscript notation.

        >>> H.add_edge(1, 2)
        >>> H[1][2].update({0: 5})
        >>> H.edges[1, 2].update({0: 5})
        """
        uid = self._edge_uid()
        for node in edge:
            if node not in self._node:
                if node is None:
                    raise ValueError("None cannot be a node")
                self._node[node] = set()
                self._node_attr[node] = self.node_attr_dict_factory()
            self._node[node].add(uid)

        try:
            self._edge[uid] = set(edge)
            self._edge_attr[uid] = self.hyperedge_attr_dict_factory()
        except:
            raise HypergraphError("The edge cannot be cast to a set.")

        self._edge_attr[uid].update(attr)

    def add_edges_from(self, ebunch_to_add, **attr):
        """Add all the edges in ebunch_to_add.

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the container will be added to the
            graph. The edges must be given as 2-tuples (u, v) or
            3-tuples (u, v, d) where d is a dictionary containing edge data.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edge : add a single edge
        add_weighted_edges_from : convenient way to add weighted edges

        Notes
        -----
        Adding the same edge twice has no effect but any edge data
        will be updated when each duplicate edge is added.

        Edge attributes specified in an ebunch take precedence over
        attributes specified via keyword arguments.

        Examples
        --------
        >>> H = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.add_edges_from([(0, 1), (1, 2)])  # using a list of edge tuples
        >>> e = zip(range(0, 3), range(1, 4))
        >>> H.add_edges_from(e)  # Add the path graph 0-1-2-3

        Associate data to edges

        >>> H.add_edges_from([(1, 2), (2, 3)], weight=3)
        >>> H.add_edges_from([(3, 4), (1, 4)], label="WN2898")
        """
        for e in ebunch_to_add:
            self.add_edge(e, **attr)

    def add_weighted_edges_from(self, ebunch_to_add, weight="weight", **attr):
        """Add weighted edges in `ebunch_to_add` with specified weight attr

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the list or container will be added
            to the graph. The edges must be given as 3-tuples (u, v, w)
            where w is a number.
        weight : string, optional (default= 'weight')
            The attribute name for the edge weights to be added.
        attr : keyword arguments, optional (default= no attributes)
            Edge attributes to add/update for all edges.

        See Also
        --------
        add_edge : add a single edge
        add_edges_from : add multiple edges

        Notes
        -----
        Adding the same edge twice for Graph/DiGraph simply updates
        the edge data. For MultiGraph/MultiDiGraph, duplicate edges
        are stored.

        Examples
        --------
        >>> H = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.add_weighted_edges_from([(0, 1, 3.0), (1, 2, 7.5)])
        """
        self.add_edges_from(((edge, {weight: w}) for edge, w in ebunch_to_add), **attr)

    def remove_edge(self, id):
        """Remove a hyperedge with a given id.

        Parameters
        ----------
        id : Hashable
            edge ID to remove

        Raises
        ------
        HypergraphError
            If no edge has that ID.

        See Also
        --------
        remove_edges_from : remove a collection of edges

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, etc
        >>> H.remove_edge(0, 1)
        >>> e = (1, 2)
        >>> H.remove_edge(*e)  # unpacks e from an edge tuple
        >>> e = (2, 3, {"weight": 7})  # an edge with attribute data
        >>> H.remove_edge(*e[:2])  # select first part of edge tuple
        """
        try:
            for node in self.edges[id]:
                self._node[node].remove(id)
            del self._edge[id]
        except KeyError as e:
            raise HypergraphError(f"Edge {id} is not in the graph") from e

    def remove_edges_from(self, ebunch):
        """Remove all edges specified in ebunch.

        Parameters
        ----------
        ebunch: list or container of hashables
            Each edge id given in the list or container will be removed
            from the graph.

        See Also
        --------
        remove_edge : remove a single edge

        Notes
        -----
        Will fail silently if an edge in ebunch is not in the graph.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> ebunch = [(1, 2), (2, 3)]
        >>> H.remove_edges_from(ebunch)
        """
        for id in ebunch:
            try:
                for node in self.edges[id]:
                    self._node[node].remove(id)
                del self._edge[id]
            except:
                pass

    def update(self, edges=None, nodes=None):
        """Update the graph using nodes/edges/graphs as input.

        Like dict.update, this method takes a graph as input, adding the
        graph's nodes and edges to this graph. It can also take two inputs:
        edges and nodes. Finally it can take either edges or nodes.
        To specify only nodes the keyword `nodes` must be used.

        The collections of edges and nodes are treated similarly to
        the add_edges_from/add_nodes_from methods. When iterated, they
        should yield 2-tuples (u, v) or 3-tuples (u, v, datadict).

        Parameters
        ----------
        edges : Graph object, collection of edges, or None
            The first parameter can be a graph or some edges. If it has
            attributes `nodes` and `edges`, then it is taken to be a
            Graph-like object and those attributes are used as collections
            of nodes and edges to be added to the graph.
            If the first parameter does not have those attributes, it is
            treated as a collection of edges and added to the graph.
            If the first argument is None, no edges are added.
        nodes : collection of nodes, or None
            The second parameter is treated as a collection of nodes
            to be added to the graph unless it is None.
            If `edges is None` and `nodes is None` an exception is raised.
            If the first parameter is a Graph, then `nodes` is ignored.

        Examples
        --------
        >>> H = nx.path_graph(5)
        >>> H.update(nx.complete_graph(range(4, 10)))
        >>> from itertools import combinations
        >>> edges = (
        ...     (u, v, {"power": u * v})
        ...     for u, v in combinations(range(10, 20), 2)
        ...     if u * v < 225
        ... )
        >>> nodes = [1000]  # for singleton, use a container
        >>> H.update(edges, nodes)

        Notes
        -----
        It you want to update the graph using an adjacency structure
        it is straightforward to obtain the edges/nodes from adjacency.
        The following examples provide common cases, your adjacency may
        be slightly different and require tweaks of these examples::

        >>> # dict-of-set/list/tuple
        >>> adj = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}}
        >>> e = [(u, v) for u, nbrs in adj.items() for v in nbrs]
        >>> H.update(edges=e, nodes=adj)

        >>> DG = nx.DiGraph()
        >>> # dict-of-dict-of-attribute
        >>> adj = {1: {2: 1.3, 3: 0.7}, 2: {1: 1.4}, 3: {1: 0.7}}
        >>> e = [
        ...     (u, v, {"weight": d})
        ...     for u, nbrs in adj.items()
        ...     for v, d in nbrs.items()
        ... ]
        >>> DG.update(edges=e, nodes=adj)

        >>> # dict-of-dict-of-dict
        >>> adj = {1: {2: {"weight": 1.3}, 3: {"color": 0.7, "weight": 1.2}}}
        >>> e = [
        ...     (u, v, {"weight": d})
        ...     for u, nbrs in adj.items()
        ...     for v, d in nbrs.items()
        ... ]
        >>> DG.update(edges=e, nodes=adj)

        >>> # predecessor adjacency (dict-of-set)
        >>> pred = {1: {2, 3}, 2: {3}, 3: {3}}
        >>> e = [(v, u) for u, nbrs in pred.items() for v in nbrs]

        >>> # MultiGraph dict-of-dict-of-dict-of-attribute
        >>> MDG = nx.MultiDiGraph()
        >>> adj = {
        ...     1: {2: {0: {"weight": 1.3}, 1: {"weight": 1.2}}},
        ...     3: {2: {0: {"weight": 0.7}}},
        ... }
        >>> e = [
        ...     (u, v, ekey, d)
        ...     for u, nbrs in adj.items()
        ...     for v, keydict in nbrs.items()
        ...     for ekey, d in keydict.items()
        ... ]
        >>> MDG.update(edges=e)

        See Also
        --------
        add_edges_from: add multiple edges to a graph
        add_nodes_from: add multiple nodes to a graph
        """
        if edges is not None:
            if nodes is not None:
                self.add_nodes_from(nodes)
                self.add_edges_from(edges)
            else:
                # check if edges is a Graph object
                try:
                    graph_nodes = edges.nodes
                    graph_edges = edges.edges
                except AttributeError:
                    # edge not Graph-like
                    self.add_edges_from(edges)
                else:  # edges is Graph-like
                    self.add_nodes_from(graph_nodes.data())
                    self.add_edges_from(graph_edges.data())
                    self._hypergraph.update(edges.hypergraph)
        elif nodes is not None:
            self.add_nodes_from(nodes)
        else:
            raise HypergraphError("update needs nodes or edges input")

    def has_edge(self, u, v):
        """Returns True if the edge id is in the hypergraph.

        This is the same as `v in H[u]` without KeyError exceptions.

        Parameters
        ----------
        u, v : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.

        Returns
        -------
        edge_ind : bool
            True if edge is in the graph, False otherwise.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.has_edge(0, 1)  # using two nodes
        True
        >>> e = (0, 1)
        >>> H.has_edge(*e)  #  e is a 2-tuple (u, v)
        True
        >>> e = (0, 1, {"weight": 7})
        >>> H.has_edge(*e[:2])  # e is a 3-tuple (u, v, data_dictionary)
        True

        The following syntax are equivalent:

        >>> H.has_edge(0, 1)
        True
        >>> 1 in H[0]  # though this gives KeyError if 0 not in H
        True

        """
        try:
            return v in self._node
        except KeyError:
            return False

    @property
    def edges(self):
        """An EdgeView of the Graph as H.edges or H.edges().

        edges(self, nbunch=None, data=False, default=None)

        The EdgeView provides set-like operations on the edge-tuples
        as well as edge attribute lookup. When called, it also provides
        an EdgeDataView object which allows control of access to edge
        attributes (but does not provide set-like operations).
        Hence, `H.edges[u, v]['color']` provides the value of the color
        attribute for edge `(u, v)` while
        `for (u, v, c) in H.edges.data('color', default='red'):`
        iterates through all the edges yielding the color attribute
        with default `'red'` if no color attribute exists.

        Parameters
        ----------
        nbunch : single node, container, or all nodes (default= all nodes)
            The view will only report edges incident to these nodes.
        data : string or bool, optional (default=False)
            The edge attribute returned in 3-tuple (u, v, ddict[data]).
            If True, return edge attribute dict in 3-tuple (u, v, ddict).
            If False, return 2-tuple (u, v).
        default : value, optional (default=None)
            Value used for edges that don't have the requested attribute.
            Only relevant if data is not True or False.

        Returns
        -------
        edges : EdgeView
            A view of edge attributes, usually it iterates over (u, v)
            or (u, v, d) tuples of edges, but can also be used for
            attribute lookup as `edges[u, v]['foo']`.

        Notes
        -----
        Nodes in nbunch that are not in the graph will be (quietly) ignored.
        For directed graphs this returns the out-edges.

        Examples
        --------
        >>> H = nx.path_graph(3)  # or MultiGraph, etc
        >>> H.add_edge(2, 3, weight=5)
        >>> [e for e in H.edges]
        [(0, 1), (1, 2), (2, 3)]
        >>> H.edges.data()  # default data is {} (empty dict)
        EdgeDataView([(0, 1, {}), (1, 2, {}), (2, 3, {'weight': 5})])
        >>> H.edges.data("weight", default=1)
        EdgeDataView([(0, 1, 1), (1, 2, 1), (2, 3, 5)])
        >>> H.edges([0, 3])  # only edges incident to these nodes
        EdgeDataView([(0, 1), (3, 2)])
        >>> H.edges(0)  # only edges incident to a single node (use H.adj[0]?)
        EdgeDataView([(0, 1)])
        """
        return EdgeView(self)

    def get_edge_data(self, u, v, default=None):
        """Returns the attribute dictionary associated with edge (u, v).

        This is identical to `H[u][v]` except the default is returned
        instead of an exception if the edge doesn't exist.

        Parameters
        ----------
        u, v : nodes
        default:  any Python object (default=None)
            Value to return if the edge (u, v) is not found.

        Returns
        -------
        edge_dict : dictionary
            The edge attribute dictionary.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H[0][1]
        {}

        Warning: Assigning to `H[u][v]` is not permitted.
        But it is safe to assign attributes `H[u][v]['foo']`

        >>> H[0][1]["weight"] = 7
        >>> H[0][1]["weight"]
        7
        >>> H[1][0]["weight"]
        7

        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.get_edge_data(0, 1)  # default edge data is {}
        {}
        >>> e = (0, 1)
        >>> H.get_edge_data(*e)  # tuple form
        {}
        >>> H.get_edge_data("a", "b", default=0)  # edge not in graph, return 0
        0
        """
        try:
            return self.edges.data
        except KeyError:
            return default

    @property
    def node_degree(self):
        """A NodeDegreeView for the Hypergraph as H.node_degree or H.node_degree().

        The node degree is the number of edges adjacent to the node.
        The weighted node degree is the sum of the edge weights for
        edges incident to that node.

        This object provides an iterator for (node, degree) as well as
        lookup for the degree for a single node.

        Parameters
        ----------
        nbunch : single node, container, or all nodes (default= all nodes)
            The view will only report edges incident to these nodes.

        weight : string or None, optional (default=None)
           The name of an edge attribute that holds the numerical value used
           as a weight.  If None, then each edge has weight 1.
           The degree is the sum of the edge weights adjacent to the node.

        Returns
        -------
        If a single node is requested
        deg : int
            Degree of the node

        OR if multiple nodes are requested
        nd_view : A NodeDegreeView object capable of iterating (node, degree) pairs

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.node_degree[0]  # node 0 has degree 1
        1
        >>> list(H.degree([0, 1, 2]))
        [(0, 1), (1, 2), (2, 2)]
        """
        return NodeDegreeView(self)

    @property
    def edge_degree(self):
        """A EdgeDegreeView for the Hypergraph as H.edge_degree or H.edge_degree().

        The node degree is the number of edges adjacent to the node.
        The weighted node degree is the sum of the edge weights for
        edges incident to that node.

        This object provides an iterator for (node, degree) as well as
        lookup for the degree for a single node.

        Parameters
        ----------
        nbunch : single node, container, or all nodes (default= all nodes)
            The view will only report edges incident to these nodes.

        weight : string or None, optional (default=None)
           The name of an edge attribute that holds the numerical value used
           as a weight.  If None, then each edge has weight 1.
           The degree is the sum of the edge weights adjacent to the node.

        Returns
        -------
        If a single node is requested
        deg : int
            Degree of the node

        OR if multiple nodes are requested
        nd_view : An EdgeDegreeView object capable of iterating (node, degree) pairs

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.degree[0]  # node 0 has degree 1
        1
        >>> list(H.degree([0, 1, 2]))
        [(0, 1), (1, 2), (2, 2)]
        """
        return EdgeDegreeView(self)

    def unique_edge_sizes(self, return_counts=False):
        return np.unique(list(self.edge_degree), return_counts=return_counts)

    def clear(self):
        """Remove all nodes and edges from the graph.

        This also removes the name, and all graph, node, and edge attributes.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.clear()
        >>> list(H.nodes)
        []
        >>> list(H.edges)
        []

        """
        self._node.clear()
        self._node_attr.clear()
        self._edge.clear()
        self._edge_attr.clear()
        self._hypergraph.clear()

    def clear_edges(self):
        """Remove all edges from the graph without altering nodes.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H.clear_edges()
        >>> list(H.nodes)
        [0, 1, 2, 3]
        >>> list(H.edges)
        []
        """
        for node in self.nodes:
            self._node[node] = {}
        self._edge.clear()
        self._edge_attr.clear()

    def is_multigraph(self):
        """Returns True if graph is a multigraph, False otherwise."""
        return False

    def is_directed(self):
        """Returns True if graph is directed, False otherwise."""
        return False

    def copy(self, as_view=False):
        """Returns a copy of the graph.

        The copy method by default returns an independent shallow copy
        of the graph and attributes. That is, if an attribute is a
        container, that container is shared by the original an the copy.
        Use Python's `copy.deepcopy` for new containers.

        If `as_view` is True then a view is returned instead of a copy.

        Notes
        -----
        All copies reproduce the graph structure, but data attributes
        may be handled in different ways. There are four types of copies
        of a graph that people might want.

        Deepcopy -- A "deepcopy" copies the graph structure as well as
        all data attributes and any objects they might contain.
        The entire graph object is new so that changes in the copy
        do not affect the original object. (see Python's copy.deepcopy)

        Data Reference (Shallow) -- For a shallow copy the graph structure
        is copied but the edge, node and graph attribute dicts are
        references to those in the original graph. This saves
        time and memory but could cause confusion if you change an attribute
        in one graph and it changes the attribute in the other.
        NetworkX does not provide this level of shallow copy.

        Independent Shallow -- This copy creates new independent attribute
        dicts and then does a shallow copy of the attributes. That is, any
        attributes that are containers are shared between the new graph
        and the original. This is exactly what `dict.copy()` provides.
        You can obtain this style copy using:

            >>> H = nx.path_graph(5)
            >>> H = H.copy()
            >>> H = H.copy(as_view=False)
            >>> H = nx.Graph(H)
            >>> H = H.__class__(H)

        Fresh Data -- For fresh data, the graph structure is copied while
        new empty data attribute dicts are created. The resulting graph
        is independent of the original and it has no edge, node or graph
        attributes. Fresh copies are not enabled. Instead use:

            >>> H = H.__class__()
            >>> H.add_nodes_from(H)
            >>> H.add_edges_from(H.edges)

        View -- Inspired by dict-views, graph-views act like read-only
        versions of the original graph, providing a copy of the original
        structure without requiring any memory for copying the information.

        See the Python copy module for more information on shallow
        and deep copies, https://docs.python.org/3/library/copy.html.

        Parameters
        ----------
        as_view : bool, optional (default=False)
            If True, the returned graph-view provides a read-only view
            of the original graph without actually copying any data.

        Returns
        -------
        H : Graph
            A copy of the graph.

        See Also
        --------
        to_directed: return a directed copy of the graph.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H = H.copy()

        """
        if as_view is True:
            return hg.hypergraphviews.generic_hypergraph_view(self)
        H = self.__class__()
        H._hypergraph = deepcopy(self._hypergraph)
        H._node = deepcopy(self._node)
        H._node_attr = deepcopy(self._node_attr)
        H._edge = deepcopy(self._edge)
        H._edge_attr = deepcopy(self._edge_attr)
        return H

    def dual(self, as_view=False):
        """Returns a copy of the graph.

        The copy method by default returns an independent shallow copy
        of the graph and attributes. That is, if an attribute is a
        container, that container is shared by the original an the copy.
        Use Python's `copy.deepcopy` for new containers.

        If `as_view` is True then a view is returned instead of a copy.

        Notes
        -----
        All copies reproduce the graph structure, but data attributes
        may be handled in different ways. There are four types of copies
        of a graph that people might want.

        Deepcopy -- A "deepcopy" copies the graph structure as well as
        all data attributes and any objects they might contain.
        The entire graph object is new so that changes in the copy
        do not affect the original object. (see Python's copy.deepcopy)

        Data Reference (Shallow) -- For a shallow copy the graph structure
        is copied but the edge, node and graph attribute dicts are
        references to those in the original graph. This saves
        time and memory but could cause confusion if you change an attribute
        in one graph and it changes the attribute in the other.
        NetworkX does not provide this level of shallow copy.

        Independent Shallow -- This copy creates new independent attribute
        dicts and then does a shallow copy of the attributes. That is, any
        attributes that are containers are shared between the new graph
        and the original. This is exactly what `dict.copy()` provides.
        You can obtain this style copy using:

            >>> H = nx.path_graph(5)
            >>> H = H.copy()
            >>> H = H.copy(as_view=False)
            >>> H = nx.Graph(H)
            >>> H = H.__class__(H)

        Fresh Data -- For fresh data, the graph structure is copied while
        new empty data attribute dicts are created. The resulting graph
        is independent of the original and it has no edge, node or graph
        attributes. Fresh copies are not enabled. Instead use:

            >>> H = H.__class__()
            >>> H.add_nodes_from(H)
            >>> H.add_edges_from(H.edges)

        View -- Inspired by dict-views, graph-views act like read-only
        versions of the original graph, providing a copy of the original
        structure without requiring any memory for copying the information.

        See the Python copy module for more information on shallow
        and deep copies, https://docs.python.org/3/library/copy.html.

        Parameters
        ----------
        as_view : bool, optional (default=False)
            If True, the returned graph-view provides a read-only view
            of the original graph without actually copying any data.

        Returns
        -------
        H : Graph
            A copy of the graph.

        See Also
        --------
        to_directed: return a directed copy of the graph.

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H = H.copy()

        """
        if as_view is True:
            return hg.hypergraphviews.generic_hypergraph_view(self)
        H = self.__class__()
        H._hypergraph = deepcopy(self._hypergraph)
        H._node = deepcopy(self._edge)
        H._node_attr = deepcopy(self._edge_attr)
        H._edge = deepcopy(self._node)
        H._edge_attr = deepcopy(self._node_attr)
        return H

    def subhypergraph(self, nodes):
        """Returns a SubGraph view of the subgraph induced on `nodes`.

        The induced subgraph of the graph contains the nodes in `nodes`
        and the edges between those nodes.

        Parameters
        ----------
        nodes : list, iterable
            A container of nodes which will be iterated through once.

        Returns
        -------
        H : SubGraph View
            A subgraph view of the graph. The graph structure cannot be
            changed but node/edge attributes can and are shared with the
            original graph.

        Notes
        -----
        The graph, edge and node attributes are shared with the original graph.
        Changes to the graph structure is ruled out by the view, but changes
        to attributes are reflected in the original graph.

        To create a subgraph with its own copy of the edge/node attributes use:
        H.subgraph(nodes).copy()

        For an inplace reduction of a graph to a subgraph you can remove nodes:
        H.remove_nodes_from([n for n in H if n not in set(nodes)])

        Subgraph views are sometimes NOT what you want. In most cases where
        you want to do more than simply look at the induced edges, it makes
        more sense to just create the subgraph as its own graph with code like:

        ::

            # Create a subgraph SG based on a (possibly multigraph) H
            SG = H.__class__()
            SG.add_nodes_from((n, H.nodes[n]) for n in largest_wcc)
            if SG.is_multigraph():
                SG.add_edges_from((n, nbr, key, d)
                    for n, nbrs in H.adj.items() if n in largest_wcc
                    for nbr, keydict in nbrs.items() if nbr in largest_wcc
                    for key, d in keydict.items())
            else:
                SG.add_edges_from((n, nbr, d)
                    for n, nbrs in H.adj.items() if n in largest_wcc
                    for nbr, d in nbrs.items() if nbr in largest_wcc)
            SG.graph.update(H.graph)

        Examples
        --------
        >>> H = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> H = H.subgraph([0, 1, 2])
        >>> list(H.edges)
        [(0, 1), (1, 2)]
        """
        induced_nodes = self.nbunch_iter(nodes)
        subgraph = hg.hypergraphviews.subhypergraph_view
        return subgraph(self, induced_nodes, None)

    def edge_subhypergraph(self, edges):
        """Returns the subgraph induced by the specified edges.

        The induced subgraph contains each edge in `edges` and each
        node incident to any one of those edges.

        Parameters
        ----------
        edges : iterable
            An iterable of edges in this graph.

        Returns
        -------
        H : Graph
            An edge-induced subgraph of this graph with the same edge
            attributes.

        Notes
        -----
        The graph, edge, and node attributes in the returned subgraph
        view are references to the corresponding attributes in the original
        graph. The view is read-only.

        To create a full graph version of the subgraph with its own copy
        of the edge or node attributes, use::

            H.edge_subgraph(edges).copy()

        Examples
        --------
        >>> H = nx.path_graph(5)
        >>> H = H.edge_subgraph([(0, 1), (3, 4)])
        >>> list(H.nodes)
        [0, 1, 3, 4]
        >>> list(H.edges)
        [(0, 1), (3, 4)]

        """
        subgraph = hg.hypergraphviews.subhypergraph_view
        return subgraph(self, None, edges)

    def arbitrary_subhypergraph(self, nodes, edges):
        """Returns the subgraph induced by the specified edges.

        The induced subgraph contains each edge in `edges` and each
        node incident to any one of those edges.

        Parameters
        ----------
        edges : iterable
            An iterable of edges in this graph.

        Returns
        -------
        H : Graph
            An edge-induced subgraph of this graph with the same edge
            attributes.

        Notes
        -----
        The graph, edge, and node attributes in the returned subgraph
        view are references to the corresponding attributes in the original
        graph. The view is read-only.

        To create a full graph version of the subgraph with its own copy
        of the edge or node attributes, use::

            H.edge_subgraph(edges).copy()

        Examples
        --------
        >>> H = nx.path_graph(5)
        >>> H = H.edge_subgraph([(0, 1), (3, 4)])
        >>> list(H.nodes)
        [0, 1, 3, 4]
        >>> list(H.edges)
        [(0, 1), (3, 4)]

        """
        subgraph = hg.hypergraphviews.subhypergraph_view
        return subgraph(self, nodes, edges)

    def number_of_edges(self):
        """Returns the number of edges between two nodes.

        Parameters
        ----------

        Returns
        -------
        nedges : int
            The number of edges in the graph.

        See Also
        --------
        size

        Examples
        --------
        For undirected graphs, this method counts the total number of
        edges in the graph:

        >>> H = nx.path_graph(4)
        >>> H.number_of_edges()
        3

        If you specify two nodes, this counts the total number of edges
        joining the two nodes:

        >>> H.number_of_edges(0, 1)
        1

        For directed graphs, this method can count the total number of
        directed edges from `u` to `v`:

        >>> H = nx.DiGraph()
        >>> H.add_edge(0, 1)
        >>> H.add_edge(1, 0)
        >>> H.number_of_edges(0, 1)
        1

        """
        return len(self._edge)

    def nbunch_iter(self, nbunch=None):
        """Returns an iterator over nodes contained in nbunch that are
        also in the graph.

        The nodes in nbunch are checked for membership in the graph
        and if not are silently ignored.

        Parameters
        ----------
        nbunch : single node, container, or all nodes (default= all nodes)
            The view will only report edges incident to these nodes.

        Returns
        -------
        niter : iterator
            An iterator over nodes in nbunch that are also in the graph.
            If nbunch is None, iterate over all nodes in the graph.

        Raises
        ------
        NetworkXError
            If nbunch is not a node or sequence of nodes.
            If a node in nbunch is not hashable.

        See Also
        --------
        Graph.__iter__

        Notes
        -----
        When nbunch is an iterator, the returned iterator yields values
        directly from nbunch, becoming exhausted when nbunch is exhausted.

        To test whether nbunch is a single node, one can use
        "if nbunch in self:", even after processing with this routine.

        If nbunch is not a node or a (possibly empty) sequence/iterator
        or None, a :exc:`NetworkXError` is raised.  Also, if any object in
        nbunch is not hashable, a :exc:`NetworkXError` is raised.
        """
        if nbunch is None:  # include all nodes via iterator
            bunch = iter(self._node)
        elif nbunch in self:  # if nbunch is a single node
            bunch = iter([nbunch])
        else:  # if nbunch is a sequence of nodes

            def bunch_iter(nlist, nodes):
                try:
                    for n in nlist:
                        if n in nodes:
                            yield n
                except TypeError as e:
                    exc, message = e, e.args[0]
                    # capture error for non-sequence/iterator nbunch.
                    if "iter" in message:
                        exc = HypergraphError(
                            "nbunch is not a node or a sequence of nodes."
                        )
                    # capture error for unhashable node.
                    if "hashable" in message:
                        exc = HypergraphError(
                            f"Node {n} in sequence nbunch is not a valid node."
                        )
                    raise exc

            bunch = bunch_iter(nbunch, self._node)
        return bunch
