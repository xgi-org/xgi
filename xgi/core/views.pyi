"""Type stubs for views module.

Declares built-in stats as typed attributes on view classes so that static
analysis tools (Pylance, PyCharm, mypy) can provide autocomplete and type
checking for the stats interface.
"""

from collections.abc import Mapping, Set
from typing import Any, Callable, Hashable, Iterable, Iterator

from ..stats import DiEdgeStat, DiNodeStat, EdgeStat, NodeStat

class IDView:
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator: ...
    def __contains__(self, item: Hashable) -> bool: ...
    def __getitem__(self, item: Hashable) -> dict: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    def filterby(self, stat: str, val: Any, mode: str = "eq") -> IDView: ...
    def filterby_attr(
        self, attr: str, val: Any, mode: str = "eq", missing: Any = None
    ) -> IDView: ...
    @property
    def ids(self) -> set: ...
    def neighbors(self, id: Hashable, s: int = 1) -> set: ...
    def duplicates(self) -> set: ...
    def lookup(self, query: set) -> set: ...
    def multi(self, names: Iterable) -> Any: ...
    @classmethod
    def from_view(cls, view: IDView, bunch: Any = None) -> IDView: ...

class NodeView(IDView):
    # Built-in stats
    attrs: NodeStat
    degree: NodeStat
    average_neighbor_degree: NodeStat
    clustering_coefficient: NodeStat
    local_clustering_coefficient: NodeStat
    two_node_clustering_coefficient: NodeStat
    clique_eigenvector_centrality: NodeStat
    h_eigenvector_centrality: NodeStat
    z_eigenvector_centrality: NodeStat
    node_edge_centrality: NodeStat
    katz_centrality: NodeStat
    local_simplicial_fraction: NodeStat
    local_edit_simpliciality: NodeStat
    local_face_edit_simpliciality: NodeStat

    def memberships(self, n: Hashable | None = None) -> dict | set: ...
    def isolates(self, ignore_singletons: bool = False) -> NodeView: ...

class EdgeView(IDView):
    # Built-in stats
    attrs: EdgeStat
    order: EdgeStat
    size: EdgeStat
    node_edge_centrality: EdgeStat

    def members(
        self, e: Hashable | None = None, dtype: type = list
    ) -> list | dict | set: ...
    def singletons(self) -> EdgeView: ...
    def empty(self) -> EdgeView: ...
    def maximal(self, strict: bool = False) -> EdgeView: ...

class DiNodeView(IDView):
    # Built-in stats
    attrs: DiNodeStat
    degree: DiNodeStat
    in_degree: DiNodeStat
    out_degree: DiNodeStat

    def dimemberships(
        self, n: Hashable | None = None
    ) -> dict | tuple[set, set]: ...
    def memberships(self, n: Hashable | None = None) -> dict | set: ...
    def isolates(self) -> DiNodeView: ...

class DiEdgeView(IDView):
    # Built-in stats
    attrs: DiEdgeStat
    order: DiEdgeStat
    size: DiEdgeStat
    head_order: DiEdgeStat
    head_size: DiEdgeStat
    tail_order: DiEdgeStat
    tail_size: DiEdgeStat

    def dimembers(
        self, e: Hashable | None = None, dtype: type = list
    ) -> list | dict | tuple[set, set]: ...
    def members(
        self, e: Hashable | None = None, dtype: type = list
    ) -> list | dict | set: ...
    def head(
        self, e: Hashable | None = None, dtype: type = list
    ) -> list | dict | set: ...
    def tail(
        self, e: Hashable | None = None, dtype: type = list
    ) -> list | dict | set: ...
