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

from collections import defaultdict
from typing import Callable

import numpy as np
import pandas as pd
from scipy.stats import moment as spmoment

from xgi.exception import IDNotFound

from . import edgestats, nodestats

__all__ = ["nodestat_func", "edgestat_func", "dispatch_stat", "dispatch_many_stats"]


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
        """Name of this stat.

        The name of a stat is used to populate the keys of dictionaries in `MultiStat`
        objects, as well as the names of columns of pandas dataframes.

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
        >>> da, d3 = H.nodes.degree, H.nodes.degree(order=3)
        >>> da.name, d3.name
        ('degree', 'degree(order=3)')
        >>> H.nodes.multi([da, d3]).asdict(transpose=True).keys()
        dict_keys(['degree', 'degree(order=3)'])
        >>> H.nodes.multi([da, d3]).aspandas().columns
        Index(['degree', 'degree(order=3)'], dtype='object')

        """
        name = f"{self.func.__name__}"
        if self.args or self.kwargs:
            args = [f"{s}" for s in self.args]
            kwargs = [f"{k}={v}" for k, v in self.kwargs.items()]
            name += "(" + ", ".join(args + kwargs) + ")"
        return name

    def __iter__(self):
        return iter(self._val.items())

    def items(self):
        return self._val.items()

    @property
    def _val(self):
        return self.func(self.net, self.view.ids, *self.args, **self.kwargs)

    def asdict(self):
        """Output the stat as a dict.

        Notes
        -----
        All stats are stored as dicts and therefore this method incurs in no overhead as
        type conversion is not necessary.

        """
        val = self._val
        return {n: val[n] for n in self.view}

    def aslist(self):
        """Output the stat as a list."""
        val = self._val
        return [val[n] for n in self.view]

    def asnumpy(self):
        """Output the stat as a numpy array."""
        return np.array(self.aslist())

    def aspandas(self):
        """Output the stat as a pandas series.

        Notes
        -----
        The `name` attribute of the returned series is set using the `name` property.

        """
        return pd.Series(self._val, name=self.name)

    def max(self):
        """The maximum value of this stat."""
        return self.asnumpy().max(axis=0)

    def min(self):
        """The minimum value of this stat."""
        return self.asnumpy().min(axis=0)

    def sum(self):
        """The sum of this stat."""
        return self.asnumpy().sum(axis=0)

    def mean(self):
        """The arithmetic mean of this stat."""
        return self.asnumpy().mean(axis=0)

    def median(self):
        """The median of this stat."""
        return np.median(self.asnumpy(), axis=0)

    def std(self):
        """The standard deviation of this stat."""
        return self.asnumpy().std(axis=0)

    def var(self):
        """The variance of this stat."""
        return self.asnumpy().var(axis=0)

    def moment(self, order=2, center=False):
        """The statistical moments of this stat.

        Parameters
        ----------
        order : int (default 2)
            The order of the moment.
        center : bool (default False)
            Whether to compute the centered (False) or uncentered/raw (True) moment.

        """
        arr = self.asnumpy()
        return spmoment(arr, moment=order) if center else np.mean(arr**order)

    def dist(self):
        return np.histogram(self.asnumpy(), density=True)


class NodeStat(IDStat):
    """An arbitrary node-quantity mapping.

    `NodeStat` objects represent a mapping that assigns a value to each node in a
    network.  For more details, see the `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    """


class EdgeStat(IDStat):
    """An arbitrary edge-quantity mapping.

    `EdgeStat` objects represent a mapping that assigns a value to each edge in a
    network.  For more details, see the `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    """


class MultiIDStat(IDStat):
    """Multiple mappings."""

    statsclass = None
    """IDStat subclass to use."""

    statsmodule = None
    """Module in which to search for mappings."""

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
    def _val(self):
        result = {s.name: s.asdict() for s in self.stats}
        return {n: {s.name: result[s.name][n] for s in self.stats} for n in self.view}

    def asdict(self, inner=dict, transpose=False):
        """Output the stats as a dict of collections.

        Parameters
        ----------
        inner : dict (default) or list
            The type of the inner collections.  If dict (default), output a dict of
            dicts.  If list, output a dict of lists.
        transpose : bool (default False)
            By default, output a dict of dicts whose outer keys are the nodes and inner
            keys are the specified stats.  If True, the outer and inner keys are
            reversed.  Only used when `inner` is `dict`.

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
        >>> m = H.nodes.multi(['degree', 'clustering'])
        >>> m.asdict() # doctest: +NORMALIZE_WHITESPACE
        {1: {'degree': 1, 'clustering': 0.0},
         2: {'degree': 2, 'clustering': 4.0},
         3: {'degree': 3, 'clustering': 1.3333333333333333},
         4: {'degree': 2, 'clustering': 3.0},
         5: {'degree': 2, 'clustering': 3.0}}
        >>> m.asdict(transpose=True) # doctest: +NORMALIZE_WHITESPACE
        {'degree': {1: 1, 2: 2, 3: 3, 4: 2, 5: 2},
        'clustering': {1: 0.0, 2: 4.0, 3: 1.3333333333333333, 4: 3.0, 5: 3.0}}

        """
        val = self._val
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
        """Output the stats as a list of collections.

        Parameters
        ----------
        inner : list (default) or dict
            The type of the inner collections.  If list (default), output a list of
            lists.  If dict, output a list of dicts.
        transpose : bool (default False)

            By default, output a list of lists where each inner list contains the stats
            of a single node.  If True, each inner list contains the values of a single
            stat of all nodes.

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
        >>> m = H.nodes.multi(['degree', 'clustering'])
        >>> m.aslist() # doctest:
        [[1, 0.0], [2, 4.0], [3, 1.3333333333333333], [2, 3.0], [2, 3.0]]
        >>> m.aslist(transpose=True)
        [[1, 2, 3, 2, 2], [0.0, 4.0, 1.3333333333333333, 3.0, 3.0]]

        """
        val = self._val
        if inner is list:
            if not transpose:
                return [list(val[n].values()) for n in self.view]
            else:
                return [s.aslist() for s in self.stats]
        elif inner is dict:
            return [val[n] for n in self.view]
        else:
            raise ValueError

    def asnumpy(self):
        """Output the stats as a numpy array.

        Notes
        -----
        Equivalent to `np.array(self.aslist(inner=list))`.

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
        >>> H.nodes.multi(['degree', 'clustering']).asnumpy()  # doctest: +NORMALIZE_WHITESPACE
        array([[1.        , 0.        ],
               [2.        , 4.        ],
               [3.        , 1.33333333],
               [2.        , 3.        ],
               [2.        , 3.        ]])

        """
        return np.array(self.aslist(inner=list))

    def aspandas(self):
        """Output the stats as a pandas dataframe.

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph([[1, 2, 3], [2, 3, 4, 5], [3, 4, 5]])
        >>> H.nodes.multi(['degree', 'clustering']).aspandas()  # doctest: +NORMALIZE_WHITESPACE
           degree  clustering
        1       1    0.000000
        2       2    4.000000
        3       3    1.333333
        4       2    3.000000
        5       2    3.000000

        """
        result = {s.name: s._val for s in self.stats}
        series = [pd.Series(v, name=k) for k, v in result.items()]
        return pd.concat(series, axis=1)

    def dist(self):
        return [np.histogram(data, density=True) for data in self.asnumpy().T]


class MultiNodeStat(MultiIDStat):
    """Multiple node-quantity mappings.

    For more details, see the `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    """

    statsclass = NodeStat
    statsmodule = nodestats


class MultiEdgeStat(MultiIDStat):
    """Multiple edge-quantity mappings.

    For more details, see the `tutorial
    <https://github.com/ComplexGroupInteractions/xgi/blob/main/tutorials/Tutorial%206%20-%20Statistics.ipynb>`_.

    """

    statsclass = EdgeStat
    statsmodule = edgestats


_dispatch_data = {
    "node": {
        "module": nodestats,
        "statclass": NodeStat,
        "multistatclass": MultiNodeStat,
    },
    "edge": {
        "module": edgestats,
        "statclass": EdgeStat,
        "multistatclass": MultiEdgeStat,
    },
}


def dispatch_stat(kind, net, view, name):
    try:
        func = getattr(_dispatch_data[kind]["module"], name)
    except AttributeError as e:
        raise AttributeError(f"Stat '{name}' not defined") from e
    return _dispatch_data[kind]["statclass"](net, view, func)


def dispatch_many_stats(kind, net, view, stats):
    return _dispatch_data[kind]["multistatclass"](net, view, stats)


def nodestat_func(func):
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
    :func:`edgestat_func`

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

    >>> H.my_degree() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError:...

    >>> H.nodes.my_degree # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError:...

    Use the `nodestat_func` decorator to turn `my_degree` into a valid stat.

    >>> original_my_degree = my_degree
    >>> my_degree = xgi.nodestat_func(my_degree)
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

    >>> @xgi.nodestat_func
    ... def my_degree(net, bunch):
    ...     return {n: 10 * net.degree(n) for n in bunch}

    """
    setattr(nodestats, func.__name__, func)
    return func


def edgestat_func(func):
    """Decorator that allows arbitrary functions to behave like :class:`EdgeStat` objects.

    Works identically to :func:`nodestat`.  For extended documentation, see
    :func:`nodestat_func`.

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
    :func:`nodestat_func`

    """
    setattr(edgestats, func.__name__, func)
    return func
