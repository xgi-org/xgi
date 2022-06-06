"""Statistics of networks, their nodes, and edges.

Any mapping that assigns some quantity to each node of a network is considered a node
statistic.  For example, the degree is a node-integer mapping, while a node attribute
that assigns a string label to each node is a node-string mapping.  The `stats` package
provides a common interface to all such mappings.

Each such mapping is accessible via the `H.nodes` view.  For example, the degree of all
nodes supports type conversion using the `as*` methods.

>>> import xgi
>>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
>>> H.nodes.degree.asdict()
{1: 1, 2: 2, 3: 3, 4: 2, 5: 2}
>>> H.nodes.degree.aslist()
[1, 2, 3, 2, 2]

Another feature is the ability to filter the nodes of a network by degree.

>>> H.nodes.filterby('degree', 2)
NodeView((2, 4, 5))

The power of the stats package is that any other node statistic that can be conceived of
as a node-quantity mapping is given the same interface.  For example, node attributes
get the same treatment:

>>> H.add_nodes_from([
...     (1, {"color": "red", "name": "horse"}),
...     (2, {"color": "blue", "name": "pony"}),
...     (3, {"color": "yellow", "name": "zebra"}),
...     (4, {"color": "red", "name": "orangutan", "age": 20}),
...     (5, {"color": "blue", "name": "fish", "age": 2}),
... ])
>>> H.nodes.attrs('color').asdict()
{1: 'red', 2: 'blue', 3: 'yellow', 4: 'red', 5: 'blue'}
>>> H.nodes.attrs('color').aslist()
['red', 'blue', 'yellow', 'red', 'blue']
>>> H.nodes.filterby_attr('color', 'red')
NodeView((1, 4))

Many other features are available, including edge-statistics, and user-defined
statistics.  For more details, see the `tutorial
<https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

"""

import numpy as np
import pandas as pd
from typing import Callable
from collections import defaultdict

from xgi.exception import IDNotFound

from . import nodestats
from . import edgestats


__all__ = ["nodestat", "edgestat", "EdgeStatDispatcher", "NodeStatDispatcher"]


class StatDispatcher:
    """For internal use; create :class:`NodeStat` or :class:`EdgeStat` objects.

    See Also
    --------
    NodeStatDispatcher
    EdgeStatDispatcher

    """

    def __init__(self, network, view, module, statsclass, multistatsclass):
        self.net = network
        self.view = view
        self.module = module
        self.statsclass = statsclass
        self.multistatsclass = multistatsclass

    def __getattr__(self, name):
        try:
            func = getattr(self.module, name)
        except AttributeError as e:
            raise AttributeError(f"Stat '{name}' not defined") from e
        stat = self.statsclass(self.net, self.view, func)
        self.__dict__[name] = stat
        return stat

    def multi(self, stats):
        """Create a :class:`MultiStat` object.

        See Also
        --------
        MultiNodeStat
        MultiEdgeStat

        Examples
        -------
        See the `tutorial
        <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

        """
        return self.multistatsclass(self.net, self.view, stats)


class EdgeStatDispatcher(StatDispatcher):
    """For internal use; a :class:`StatDispatcher` for edge stats.

    Examples
    -------
    See the `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    """

    def __init__(self, network, view):
        super().__init__(network, view, edgestats, EdgeStat, MultiEdgeStat)


class NodeStatDispatcher(StatDispatcher):
    """For internal use; a :class:`StatDispatcher` for node stats.

    Examples
    -------
    See the `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    """

    def __init__(self, network, view):
        super().__init__(network, view, nodestats, NodeStat, MultiNodeStat)


class IDStat:
    """Mapping between nodes or edges and a quantity or property."""

    def __init__(self, network, view, func, args=None, kwargs=None):
        self.view = view
        self.net = network
        self.args = () if args is None else args
        self.kwargs = {} if args is None else kwargs
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.__class__(self.net, self.view, self.func, args=args, kwargs=kwargs)

    def __getitem__(self, id):
        if id not in self.view:
            raise IDNotFound(f'ID "{id}" not in this view')
        return self.func(self.net, [id], *self.args, **self.kwargs)[id]

    def __repr__(self):
        cls = self.__class__.__name__
        fnc = self.func.__name__
        out = f"{cls}('{fnc}'"
        if self.args:
            out += f", args={self.args}"
        if self.kwargs:
            out += f", kwargs={self.kwargs}"
        out += ")"
        return out

    @property
    def name(self):
        name = f"{self.func.__name__}"
        if self.args or self.kwargs:
            args = [f"{s}" for s in self.args]
            kwargs = [f"{k}={v}" for k, v in self.kwargs.items()]
            name += "(" + ", ".join(args + kwargs) + ")"
        return name

    def __iter__(self):
        return iter(self.val.items())

    @property
    def val(self):
        return self.func(self.net, self.view.ids, *self.args, **self.kwargs)

    def asdict(self):
        val = self.val
        return {n: val[n] for n in self.view}

    def aslist(self):
        val = self.val
        return [val[n] for n in self.view]

    def asnumpy(self):
        return np.array(self.aslist())

    def aspandas(self):
        return pd.Series(self.val)

    def max(self):
        return self.asnumpy().max(axis=0)

    def min(self):
        return self.asnumpy().min(axis=0)

    def mean(self):
        return self.asnumpy().mean(axis=0)

    def median(self):
        return np.median(self.asnumpy(), axis=0)

    def std(self):
        return self.asnumpy().std(axis=0)

    def var(self):
        return self.asnumpy().var(axis=0)

    def dist(self):
        return np.histogram(self.asnumpy(), density=True)


class NodeStat(IDStat):
    pass


class EdgeStat(IDStat):
    pass


class MultiIDStat(IDStat):
    """Multiple mappings."""

    statsclass = None
    statsmodule = None

    def __init__(self, network, view, stats):
        super().__init__(network, view, None)
        if isinstance(stats, self.statsclass):
            name = self.statsclass.__name__
            raise TypeError(f"must pass an iterable of {name}, not a single {name}")
        elif isinstance(stats, str):
            raise TypeError(
                f"must pass an iterable of {self.statsclass.__name__}, not str"
            )
        self.stats = [self._get_stat(f) for f in stats]

    def _get_stat(self, s):
        if isinstance(s, str):
            return self.statsclass(self.net, self.view, getattr(self.statsmodule, s))
        elif isinstance(s, self.statsclass):
            return s
        else:
            raise TypeError(f"{s.__name__} must be str or {self.statsclass.__name__}")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            + "("
            + ", ".join(s.name for s in self.stats)
            + ")"
        )

    @property
    def name(self):
        return "[" + ", ".join(s.name for s in self.stats) + "]"

    @property
    def val(self):
        result = {s.name: s.asdict() for s in self.stats}
        return {n: {s.name: result[s.name][n] for s in self.stats} for n in self.view}

    def asdict(self, inner=dict, transpose=False):
        """transpose is used when inner=dict, otherwise ignored."""
        val = self.val
        if inner is dict:
            if not transpose:
                return {n: val[n] for n in self.view}
            else:
                return {s.name: s.asdict() for s in self.stats}
        elif inner is list:
            return {n: list(val[n].values()) for n in self.view}
        else:
            raise ValueError

    def aslist(self, inner=list, transpose=False):
        val = self.val
        if inner is list:
            if not transpose:
                return [list(val[n].values()) for n in self.view]
            else:
                return [s.aslist() for s in self.stats]
        elif inner is dict:
            return [val[n] for n in self.view]
        else:
            raise ValueError

    def asarray(self):
        return np.array(self.aslist(inner=list))

    def aspandas(self):
        result = {s.name: s.val for s in self.stats}
        series = [pd.Series(v, name=k) for k, v in result.items()]
        return pd.concat(series, axis=1)

    def dist(self):
        return [np.histogram(data, density=True) for data in self.asnumpy().T]


class MultiNodeStat(MultiIDStat):
    statsclass = NodeStat
    statsmodule = nodestats


class MultiEdgeStat(MultiIDStat):
    statsclass = EdgeStat
    statsmodule = edgestats


def nodestat(func):
    """Decorator that allows arbitrary functions to behave like :class:`NodeStat` objects.

    Parameters
    ----------
    func : callable
        Function or callable with signature `func(net, bunch)`, where `net` is the
        network and `bunch` is an iterable of nodes in `net`.  The call `func(net,
        bunch)` must return a dict with pairs of the form `(node: value)` where `node` is
        in `bunch` and `value` is the value of the statistic at `node`.

    Returns
    -------
    callable
        The decorated callable unmodified, after registering it in the `stats` framework.

    See Also
    --------
    :class:`edgestat`

    Notes
    -----
    The user must make sure that `func` is such that, if `res` is defined as `res =
    func(net, bunch)`, then `res` has keys in the same order as they are found in
    `bunch`.  Since python dicts preserve order, it is enough for `func` to create the
    returned dict by iterating over `bunch`.


    Examples
    --------
    >>> import xgi
    >>> H = xgi.Hypergraph([[1, 2], [3, 4], [4, 5, 6]])

    The following function defines a node-integer mapping.

    >>> def my_degree(net, bunch):
    ...     return {n: 10 * net.degree(n) for n in bunch}

    Node statistics can be called from the network or from the NodeView.

    >>> H.degree()
    {1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1}
    >>> H.nodes.degree
    NodeStat('degree')

    However, `my_degree` is not recognized as a node statistic.

    >>> H.my_degree()
    Traceback (most recent call last):
    AttributeError: stat "my_degree" not among available node or edge stats
    >>> H.nodes.my_degree
    Traceback (most recent call last):
    AttributeError: Stat 'my_degree' not defined

    Use the `nodestat` decorator to turn `my_degree` into a valid stat.

    >>> original_my_degree = my_degree
    >>> my_degree = xgi.nodestat(my_degree)
    >>> H.my_degree()
    {1: 10, 2: 10, 3: 10, 4: 20, 5: 10, 6: 10}
    >>> H.nodes.my_degree
    NodeStat('my_degree')

    Now the entirety of the interface of stat objects is available.

    >>> H.nodes.filterby('my_degree', 20)
    NodeView((4,))
    >>> H.nodes.multi(['degree', 'my_degree']).aspandas()
       degree  my_degree
    1       1         10
    2       1         10
    3       1         10
    4       2         20
    5       1         10
    6       1         10

    Note the passed function is left unmodified.

    >>> my_degree is original_my_degree
    True

    The previous usage of `nodestat` is made for explanatory purposes.  A more typical
    use of `nodestat` is the following.

    >>> @xgi.nodestat
    ... def my_degree(net, bunch):
    ...     return {n: 10 * net.degree(n) for n in bunch}

    """
    setattr(nodestats, func.__name__, func)
    return func


def edgestat(func):
    """Decorator that allows arbitrary functions to behave like :class:`EdgeStat` objects.

    Works identically to :func:`nodestat`.  For extended documentation, see
    :func:`nodestat`.

    Parameters
    ----------
    func : callable
        Function or callable with signature `func(net, bunch)`, where `net` is the
        network and `bunch` is an iterable of edges in `net`.  The call `func(net,
        bunch)` must return a dict with pairs of the form `(edge: value)` where `edge`
        is in `bunch` and `value` is the value of the statistic at `edge`.

    Returns
    -------
    callable
        The decorated callable unmodified, after registering it in the `stats` framework.

    See Also
    --------
    :class:`nodestat`

    """
    setattr(edgestats, func.__name__, func)
    return func
