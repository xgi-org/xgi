## Tensor times same vector in all but one (TTSV1) and all but two (TTSV2)
from collections import defaultdict
from itertools import combinations
from math import factorial

import numpy as np
from numpy import prod
from scipy.signal import convolve
from scipy.sparse import coo_array
from scipy.special import binom as binomial

__all__ = [
    "pairwise_incidence",
    "ttsv1",
    "ttsv2",
]


def pairwise_incidence(edgedict, max_size):
    """Create pairwise adjacency dictionary from hyperedge list dictionary

    Parameters
    ----------
    edgedict : dict
        edge IDs are keys, edges are values
    max_size : int
        the size of the largest edge in the hypergraph

    Returns
    -------
    pairs : dict
        a dictionary with node pairs as keys and the hyperedges they appear in as values
    """
    pairs = defaultdict(set)
    for e, edge in edgedict.items():
        for i, j in combinations(sorted(edge), 2):
            pairs[(i, j)].add(e)
        for n in edge:
            pairs[(n, n)].add(e)

        if len(edge) < max_size:
            for n in edge:
                pairs[(n, n)].add(e)
    return pairs


def banerjee_coeff(size, max_size):
    r"""Return the Banerjee alpha coefficient

    This coefficient measures the size of the set of edge blowups
    defined in the corresponding references below. For example,
    for the edge :math:`e=\{1, 3\}` in a rank 3 hypergraph, we have
    the following blowup.

    .. math::
        \beta(e) = \{1, 1, 3\}, \{1, 3, 1\}, \{1, 3, 3\}, \{3, 1, 1\}, \{3, 1, 3\}, \{3, 3, 1\}

    Parameters
    ----------
    size : int
        size of given hyperedge
    max_size : int
        maximum hyperedge size

    Returns
    -------
    float
        the Banerjee coefficient

    References
    ----------
    Anirban Banerjee, Arnab Char, and Bibhash Mondal,
    "Spectra of general hypergraphs"
    Linear Algebra and its Applications, **518**, 14-30 (2017),
    https://doi.org/10.1016/j.laa.2016.12.022

    Scalable Tensor Methods for Nonuniform Hypergraphs,
    Sinan Aksoy, Ilya Amburg, Stephen Young,
    https://doi.org/10.1137/23M1584472
    """
    return sum(
        ((-1) ** j) * binomial(size, j) * (size - j) ** max_size
        for j in range(size + 1)
    )


def get_gen_coef_subset_expansion(edge_values, node_value, r):
    k = len(edge_values)
    subset_vector = [0]
    subset_lengths = [0]
    for i in range(k):
        for t in range(len(subset_vector)):
            subset_vector.append(subset_vector[t] + edge_values[i])
            subset_lengths.append(subset_lengths[t] + 1)
    for i in range(len(subset_lengths)):
        subset_lengths[i] = (-1) ** (k - subset_lengths[i])
        # subset_lengths[i] = -1 if (k - subset_lengths[i]) % 2 == 1 else 1
    total = sum(
        [
            (node_value + subset_vector[i]) ** r * subset_lengths[i]
            for i in range(len(subset_lengths))
        ]
    )
    return total / factorial(r)


def get_gen_coef_fft(edge_without_node, a, node, l, r):
    coefs = np.array([(a[node] ** i) / factorial(i) for i in range(r)])
    for u in edge_without_node:
        _coefs = np.array([a[u] ** i / factorial(i) for i in range(r - l + 2)])
        _coefs[0] = 0
        coefs = convolve(coefs, _coefs)[0:r]
    gen_fun_coef = coefs[-1]
    return gen_fun_coef


def get_gen_coef_fft_fast_array(edge_without_node, a, node, l, r):
    coefs = [1]
    for i in range(1, r):
        coefs.append(coefs[-1] * a[node] / i)
    coefs = np.array(coefs)
    for u in edge_without_node:
        _coefs = [1]
        for i in range(1, r - l + 2):
            _coefs.append(_coefs[-1] * a[u] / i)
        _coefs = np.array(_coefs)
        _coefs[0] = 0
        coefs = convolve(coefs, _coefs)[0:r]
    gen_fun_coef = coefs[-1]
    return gen_fun_coef


def ttsv1(E, H, r, a):
    n = len(E)
    s = np.zeros(n)
    r_minus_1_factorial = factorial(r - 1)
    for node, edges in E.items():
        c = 0
        for e in edges:
            l = len(H[e])
            alpha = banerjee_coeff(l, r)
            edge_without_node = [v for v in H[e] if v != node]
            if l == r:
                gen_fun_coef = prod(a[edge_without_node])
            elif 2 ** (l - 1) < r * (l - 1):
                gen_fun_coef = get_gen_coef_subset_expansion(
                    a[edge_without_node], a[node], r - 1
                )
            else:
                gen_fun_coef = get_gen_coef_fft_fast_array(
                    edge_without_node, a, node, l, r
                )
            c += r_minus_1_factorial * l * gen_fun_coef / alpha
        s[node] = c
    return s


def ttsv2(E, H, r, a, n):
    s = {}
    r_minus_2_factorial = factorial(r - 2)
    for nodes, edges in E.items():
        v1 = nodes[0]
        v2 = nodes[1]
        c = 0
        for e in edges:
            l = len(H[e])
            alpha = banerjee_coeff(l, r)
            edge_without_node = [v for v in H[e] if v != v1 and v != v2]
            if v1 != v2:
                if 2 ** (l - 2) < (r - 2) * (l - 2):
                    gen_fun_coef = get_gen_coef_subset_expansion(
                        a[edge_without_node], a[v1] + a[v2], r - 2
                    )
                else:
                    coefs = [1]
                    for i in range(1, r - 1):
                        coefs.append(coefs[-1] * (a[v1] + a[v2]) / i)
                    coefs = np.array(coefs)
                    for u in H[e]:
                        if u != v1 and u != v2:
                            _coefs = [1]
                            for i in range(1, r - l + 2):
                                _coefs.append(_coefs[-1] * a[u] / i)
                            _coefs = np.array(_coefs)
                            _coefs[0] = 0
                            coefs = convolve(coefs, _coefs)[0 : r - 1]
                    gen_fun_coef = coefs[-1]
            else:
                if 2 ** (l - 1) < (r - 2) * (l - 1):
                    gen_fun_coef = get_gen_coef_subset_expansion(
                        a[edge_without_node], a[v1], r - 2
                    )
                else:
                    coefs = [1]
                    for i in range(1, r - 1):
                        coefs.append(coefs[-1] * (a[v1]) / i)
                    coefs = np.array(coefs)
                    for u in H[e]:
                        if u != v1 and u != v2:
                            _coefs = [1]
                            for i in range(1, r - l + 1):
                                _coefs.append(_coefs[-1] * a[v1] / i)
                            _coefs = np.array(_coefs)
                            _coefs[0] = 0
                            coefs = convolve(coefs, _coefs)[0 : r - 1]
                    gen_fun_coef = coefs[-1]
            c += r_minus_2_factorial * l * gen_fun_coef / alpha
        s[nodes] = c
        if v1 == v2:
            s[nodes] /= 2
    first = np.zeros(len(s))
    second = np.zeros(len(s))
    value = np.zeros(len(s))
    for i, k in enumerate(s.keys()):
        first[i] = k[0]
        second[i] = k[1]
        value[i] = s[k]
    Y = coo_array((value, (first, second)), (n, n))
    return Y + Y.T
