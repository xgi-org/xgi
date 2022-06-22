from collections import defaultdict

import numpy as np
from numpy.linalg import norm

from ..classes import is_uniform
from ..exception import XGIError
from ..utils.utilities import convert_labels_to_integers

__all__ = ["CEC_centrality", "HEC_centrality", "ZEC_centrality"]


def CEC_centrality(H, max_iter=10, tol=1e-6, return_eigval=False):

    new_H = convert_labels_to_integers(H, "old-label")

    l = 0
    x = np.random.uniform(size=(H.num_nodes))

    for iter in range(max_iter):
        new_x = apply(new_H, x)
        new_l = norm(new_x) / norm(x)
        new_x = new_x / norm(new_x)
        if abs(l - new_l) <= tol:
            break
        x = new_x.copy()
        l = new_l
    if return_eigval:
        return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, new_x)}, new_l
    return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, new_x)}


def ZEC_centrality(H, max_iter=10, tol=1e-6, return_eigval=False):

    new_H = convert_labels_to_integers(H, "old-label")

    g = lambda v, e: np.prod(v[list(e)])

    l = 0
    x = np.random.uniform(size=(new_H.num_nodes))
    for i in range(max_iter):
        new_x = apply(new_H, x, g)
        new_l = norm(new_x) / norm(x)
        new_x = new_x / norm(new_x)
        if abs(l - new_l) <= tol:
            break
        x = new_x.copy()
        l = new_l
    if return_eigval:
        return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, new_x)}, new_l
    return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, new_x)}


def HEC_centrality(H, max_iter=10, tol=1e-6, return_eigval=False):
    new_H = convert_labels_to_integers(H, "old-label")

    m = is_uniform(H)
    if not m:
        raise XGIError("This method is not defined for non-uniform hypergraphs.")
    f = lambda v, m: np.power(v, 1.0 / m)
    g = lambda v, x: np.prod(v[list(x)])

    l = 0
    x = np.random.uniform(size=(new_H.num_nodes))
    for i in range(max_iter):
        new_x = apply(new_H, x, g)
        new_x = f(new_x, m)
        new_l = norm(new_x) / norm(x)
        new_x = new_x / norm(new_x)
        if abs(l - new_l) <= tol:
            break
        x = new_x.copy()
        l = new_l
    if return_eigval:
        return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, new_x)}, new_l
    return {new_H.nodes[n]["old-label"]: c for n, c in zip(new_H.nodes, new_x)}


def apply(H, x, g=lambda v, e: np.sum(v[list(e)])):
    new_x = np.zeros(H.num_nodes)
    for edge in H.edges.members():
        # ordered permutations
        for shift in range(len(edge)):
            new_x[edge[shift]] += g(x, edge[shift + 1 :] + edge[:shift])
    return new_x
