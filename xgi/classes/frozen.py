"""Class for a hypergraph that can be frozen."""

from functools import lru_cache

from xgi.classes import Hypergraph

__all__ = ["FrozenHypergraph"]


def cache_when_frozen(method):

    @lru_cache
    def cached(self, *args, **kwargs):
        return method(self, *args, **kwargs)

    def wrapper(self, *args, **kwargs):
        if self.frozen:
            return cached(self, *args, **kwargs)
        else:
            return method(self, *args, **kwargs)

    return wrapper


class FrozenHypergraph(Hypergraph):
    """Hypergraph that can be frozen by calling freeze().

    A frozen hypergraph caches the results of many of its methods and will therefore be
    much faster (but use more memory) than a standard hypergraph.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._frozen = False

    @property
    def frozen(self):
        return self._frozen

    def freeze(self):
        self._frozen = True

    @cache_when_frozen
    def is_uniform(self):
        return super().is_uniform()
