"""Node statisics."""

import xgi
from itertools import combinations

__all__ = [
    "attrs",
    "degree",
    "average_neighbor_degree",
    "clustering",
]


def attrs(net, bunch, attr=None, missing=None):
    if isinstance(attr, str):
        return {n: net._node_attr[n].get(attr, missing) for n in bunch}
    elif attr is None:
        return {n: net._node_attr[n] for n in bunch}
    else:
        raise ValueError('"attr" must be str or None')


def degree(net, bunch, order=None, weight=None):
    if order is None and weight is None:
        return {n: len(net._node[n]) for n in bunch}
    if order is None and weight:
        return {
            n: sum(net._edge_attr[e].get(weight, 1) for e in net._node[n])
            for n in bunch
        }
    if order is not None and weight is None:
        return {
            n: len([e for e in net._node[n] if len(net._edge[e]) == order + 1])
            for n in bunch
        }
    if order is not None and weight:
        return {
            n: sum(
                net._edge_attr[e].get(weight, 1)
                for e in net._node[n]
                if len(net._edge[e]) == order + 1
            )
            for n in bunch
        }


def average_neighbor_degree(net, bunch):
    result = {}
    for n in bunch:
        neighbors = net.neighbors(n)
        result[n] = sum(len(net._node[nbr]) for nbr in neighbors)
        result[n] = result[n] / len(neighbors) if neighbors else 0
    return result


def clustering(net, bunch):
    adj = xgi.adjacency_matrix(net)
    mat = adj.dot(adj).dot(adj)
    result = {}
    for n in bunch:
        deg = len(net.nodes.memberships(n))
        denom = deg * (deg - 1) / 2
        if denom <= 0:
            result[n] = 0.0
        else:
            result[n] = mat[n, n] / denom / 2
    return result
