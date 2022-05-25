import numpy as np
import pandas as pd
from typing import Callable
from collections import defaultdict

from . import nodestats
from . import edgestats


__all__ = ["nodestat", "EdgeStatDispatcher", "NodeStatDispatcher"]


class StatDispatcher:
    def __init__(self, network, view, module):
        self.net = network
        self.view = view
        self.module = module

    def __getattr__(self, name):
        try:
            func = getattr(self.module, name)
        except AttributeError as e:
            raise AttributeError(f"Stat '{name}' not defined") from e
        stat = NodeStat(self.net, self.view, func)
        self.__dict__[name] = stat
        return stat

    def multi(self, stats):
        return MultiNodeStat(self.net, self.view, stats)


class EdgeStatDispatcher(StatDispatcher):
    def __init__(self, network, view):
        super().__init__(network, view, edgestats)


class NodeStatDispatcher(StatDispatcher):
    def __init__(self, network, view):
        super().__init__(network, view, nodestats)


class NodeStat:
    def __init__(self, network, view, func, args=None, kwargs=None):
        self.view = view
        self.net = network
        self.args = () if args is None else args
        self.kwargs = {} if args is None else kwargs
        self.func = func

    def __call__(self, *args, **kwargs):
        return NodeStat(self.net, self.view, self.func, args=args, kwargs=kwargs)

    def __getitem__(self, node):
        return self.func(self.net, [node], *self.args, **self.kwargs)[node]

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
        return self.asnumpy().max()

    def min(self):
        return self.asnumpy().min()

    def mean(self):
        return self.asnumpy().mean()

    def median(self):
        return np.median(self.asnumpy())

    def std(self):
        return self.asnumpy().std()

    def var(self):
        return self.asnumpy().var(axis=0)

    def dist(self):
        return np.histogram(self.asnumpy(), density=True)


class MultiNodeStat(NodeStat):
    def __init__(self, network, view, stats):
        super().__init__(network, view, None)
        if isinstance(stats, NodeStat):
            raise TypeError("must pass an iterable of NodeStat, not a single NodeStat")
        elif isinstance(stats, str):
            raise TypeError("must pass an iterable of NodeStat, not str")
        self.stats = [self._get_stat(f) for f in stats]

    def _get_stat(self, s):
        if isinstance(s, str):
            return NodeStat(self.net, self.view, getattr(nodestats, s))
        elif isinstance(s, NodeStat):
            return s
        else:
            raise TypeError(f"{s.__name__} must be str or NodeStat")

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
        return {n: {s.name: result[s.name][n] for s in self.stats} for n in self.net}

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


def nodestat(func):
    setattr(nodestats, func.__name__, func)
