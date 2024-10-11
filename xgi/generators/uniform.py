"""Generate random uniform hypergraphs."""

import itertools
import operator
import random
import warnings
from functools import reduce

import numpy as np
from scipy.special import comb

from ..exception import XGIError
from .classic import complete_hypergraph, empty_hypergraph

__all__ = [
    "uniform_hypergraph_configuration_model",
    "uniform_HSBM",
    "uniform_HPPM",
    "uniform_erdos_renyi_hypergraph",
]


def uniform_hypergraph_configuration_model(k, m, seed=None):
    """
    A function to generate an m-uniform configuration model

    Parameters
    ----------
    k : dictionary
        This is a dictionary where the keys are node ids
        and the values are node degrees.
    m : int
        specifies the hyperedge size
    seed : integer or None (default)
        The seed for the random number generator

    Returns
    -------
    Hypergraph object
        The generated hypergraph

    Warns
    -----
    warnings.warn
        If the sums of the degrees are not divisible by m, the
        algorithm still runs, but raises a warning and adds an
        additional connection to random nodes to satisfy this
        condition.

    Notes
    -----
    This algorithm normally creates multi-edges and loopy hyperedges.
    We remove the loopy hyperedges.

    References
    ----------
    "The effect of heterogeneity on hypergraph contagion models"
    by Nicholas W. Landry and Juan G. Restrepo
    https://doi.org/10.1063/5.0020034


    Example
    -------
    >>> import xgi
    >>> import random
    >>> n = 1000
    >>> m = 3
    >>> k = {1: 1, 2: 2, 3: 3, 4: 3}
    >>> H = xgi.uniform_hypergraph_configuration_model(k, m)

    """
    if seed is not None:
        random.seed(seed)

    # Making sure we have the right number of stubs
    remainder = sum(k.values()) % m
    if remainder != 0:
        warnings.warn(
            "This degree sequence is not realizable. "
            "Increasing the degree of random nodes so that it is."
        )
        random_ids = random.sample(list(k.keys()), int(round(m - remainder)))
        for id in random_ids:
            k[id] = k[id] + 1

    stubs = []
    # Creating the list to index through
    for id in k:
        stubs.extend([id] * int(k[id]))

    H = empty_hypergraph()
    H.add_nodes_from(k.keys())

    while len(stubs) != 0:
        u = random.sample(range(len(stubs)), m)
        edge = set()
        for index in u:
            edge.add(stubs[index])
        if len(edge) == m:
            H.add_edge(edge)

        for index in sorted(u, reverse=True):
            del stubs[index]

    return H


def uniform_HSBM(n, m, p, sizes, seed=None):
    r"""Create a uniform hypergraph stochastic block model (HSBM).

    This uses a fast method for generating hyperedges
    so that instead of the algorithm being of complexity
    :math:`\mathcal{O}(N^m)`, it can be as fast as
    :math:`\mathcal{O}(m(N + |E|))`. See the references
    for more details.

    Parameters
    ----------
    n : int
        The number of nodes
    m : int
        The hyperedge size
    p : m-dimensional numpy array
        tensor of probabilities between communities
    sizes : list or 1D numpy array
        The sizes of the community blocks in order
    seed : integer or None (default)
        The seed for the random number generator

    Returns
    -------
    Hypergraph
        The constructed SBM hypergraph

    Raises
    ------
    XGIError
        - If the length of sizes and p do not match.
        - If p is not a tensor with every dimension equal
        - If p is not m-dimensional
        - If the entries of p are not in the range [0, 1]
        - If the sum of the vector of sizes does not equal the number of nodes.
    Exception
        If there is an integer overflow error

    See Also
    --------
    uniform_HPPM

    Notes
    -----
    Because XGI only stores edges as sets, when self-loops occur,
    they become smaller edges (for example, the edge (0, 0, 0)
    will be mapped to {0}). However, because this is explicitly
    a *uniform* method, we discard these edges so that this is the case.
    For sparse networks, this is a rare occurrence and this method offers
    an order of magnitude speedup.

    References
    ----------
    Nicholas W. Landry and Juan G. Restrepo,
    "Opinion disparity in hypergraphs with community structure",
    Phys. Rev. E **108**, 034311 (2024).
    https://doi.org/10.1103/PhysRevE.108.034311
    """

    # Check if dimensions match
    if len(sizes) != np.size(p, axis=0):
        raise XGIError("'sizes' and 'p' do not match.")
    if len(np.shape(p)) != m:
        raise XGIError("The dimension of p does not match m")
    # Check that p has the same length over every dimension.
    if len(set(np.shape(p))) != 1:
        raise XGIError("'p' must be a square tensor.")
    if np.max(p) > 1 or np.min(p) < 0:
        raise XGIError("Entries of 'p' not in [0, 1].")
    if np.sum(sizes) != n:
        raise XGIError("Sum of sizes does not match n")

    if seed is not None:
        np.random.seed(seed)

    node_labels = range(n)
    H = empty_hypergraph()
    H.add_nodes_from(node_labels)

    block_range = range(len(sizes))
    # Split node labels in a partition (list of sets).
    size_cumsum = [sum(sizes[0:x]) for x in range(0, len(sizes) + 1)]
    partition = [
        list(node_labels[size_cumsum[x] : size_cumsum[x + 1]])
        for x in range(0, len(size_cumsum) - 1)
    ]

    for block in itertools.product(block_range, repeat=m):
        if p[block] == 1:  # Test edges cases p_ij = 0 or 1
            edges = itertools.product((partition[i] for i in block_range))
            for e in edges:
                H.add_edge(e)
        elif p[block] > 0:
            partition_sizes = [len(partition[i]) for i in block]
            max_index = reduce(operator.mul, partition_sizes, 1)
            if max_index < 0:
                raise Exception("Index overflow error!")
            index = np.random.geometric(p[block]) - 1

            while index < max_index:
                indices = _index_to_edge_partition(index, partition_sizes, m)
                e = {partition[block[i]][indices[i]] for i in range(m)}
                # edge ids are not guaranteed to be unique
                # and when casting to a set, they will no
                # longer be of size m.
                # for instance (0, 0, 0) becomes {0}
                # if we accept these edges, the hypergraph
                # will not longer be uniform, so we discard them.
                if len(e) == m:
                    H.add_edge(e)
                index += np.random.geometric(p[block])
    return H


def uniform_HPPM(n, m, k, epsilon, rho=0.5, seed=None):
    r"""Construct the m-uniform hypergraph planted partition model (m-HPPM)

    This uses a fast method for generating hyperedges
    so that instead of the algorithm being of complexity
    :math:`\mathcal{O}(N^m)`, it can be as fast as
    :math:`\mathcal{O}(m(N + |E|))`. See the references
    for more details.

    Parameters
    ----------
    n : int > 0
        Number of nodes
    m : int > 0
        Hyperedge size
    k : float > 0
        Mean degree
    epsilon : float > 0
        Imbalance parameter
    rho : float between 0 and 1, optional
        The fraction of nodes in community 1, default 0.5
    seed : integer or None (default)
        The seed for the random number generator

    Returns
    -------
    Hypergraph
        The constructed m-HPPM hypergraph.

    Raises
    ------
    XGIError
        - If rho is not between 0 and 1
        - If the mean degree is negative.
        - If epsilon is not between 0 and 1

    See Also
    --------
    uniform_HSBM

    Notes
    -----
    Because XGI only stores edges as sets, when self-loops occur,
    they become smaller edges (for example, the edge (0, 0, 0)
    will be mapped to {0}). However, because this is explicitly
    a *uniform* method, we discard these edges so that this is the case.
    For sparse networks, this is a rare occurrence and this method offers
    an order of magnitude speedup.

    References
    ----------
    Nicholas W. Landry and Juan G. Restrepo,
    "Opinion disparity in hypergraphs with community structure",
    Phys. Rev. E **108**, 034311 (2024).
    https://doi.org/10.1103/PhysRevE.108.034311
    """

    if rho < 0 or rho > 1:
        raise XGIError("The value of rho must be between 0 and 1")
    if k < 0:
        raise XGIError("The mean degree must be non-negative")
    if epsilon < 0 or epsilon > 1:
        raise XGIError("epsilon must be between 0 and 1")

    sizes = [int(rho * n), n - int(rho * n)]

    p = k / (m * n ** (m - 1))
    # ratio of inter- to intra-community edges
    q = rho**m + (1 - rho) ** m
    r = 1 / q - 1
    p_in = (1 + r * epsilon) * p
    p_out = (1 - epsilon) * p

    p = p_out * np.ones([2] * m)
    p[tuple([0] * m)] = p_in
    p[tuple([1] * m)] = p_in

    return uniform_HSBM(n, m, p, sizes, seed=seed)


def uniform_erdos_renyi_hypergraph(n, m, p, p_type="prob", multiedges=False, seed=None):
    r"""Generate an m-uniform Erdős–Rényi hypergraph

    This creates a hypergraph with `n` nodes where
    hyperedges of size `m` are created at random
    with probability (or to obtain a mean degree of) `p`.

    This uses a fast method for generating hyperedges
    so that instead of the algorithm being of complexity
    :math:`\mathcal{O}(N^m)`, it can be as fast as
    :math:`\mathcal{O}(m(N + |E|))`. See the references
    for more details.

    Parameters
    ----------
    n : int > 0
        Number of nodes
    m : int > 0
        Hyperedge size
    p : float or int >= 0
        Probability of an m-hyperedge if p_type="prob" and
        mean expected degree if p_type="degree"
    p_type : str, optional
        Determines the way p is interpreted (see p for detail).
        Valid options are "prob" or "degree", by default "prob"
    multiedges : bool, optional
        Whether or not to allow multiedges. If True, there
        can be significant speedups but at the cost of creating
        (potentially unwanted) artifacts. When multiedges=True,
        it treats each edge permutation as distinct, which can
        lead to multiedges, especially for dense hypergraphs.
        For sparse hypergraphs, however, this is unlikely to
        be the case.
        By default, False.
    seed : integer or None (default)
        The seed for the random number generator

    Returns
    -------
    Hypergraph
        The Erdos Renyi hypergraph

    See Also
    --------
    ~xgi.generators.random.random_hypergraph

    Notes
    -----
    When `multiedges=True`, there is the possibility of generating
    (potentially unwanted) artifacts, like multiedges and loopy
    hyperedges which are not present in the original Erdos-Renyi model.
    Because hypergraphs in XGI only store edges as sets, when an edge
    such as (0, 0, 0) is generated will be mapped to {0}. However,
    because this is explicitly a *uniform* method, we discard these edges.
    For sparse networks, this is a rare occurrence and allowing these
    artifacts offers an order of magnitude speedup. Although allowing
    loopy hyperedges and multiedges is not the default behavior, this
    (as well as the associated performance boost) is enabled by setting
    `multiedges=True`.

    References
    ----------
    Nicholas W. Landry and Juan G. Restrepo,
    "Opinion disparity in hypergraphs with community structure",
    Phys. Rev. E **108**, 034311 (2024).
    https://doi.org/10.1103/PhysRevE.108.034311
    """
    if seed is not None:
        np.random.seed(seed)

    if p_type == "degree":
        if multiedges:
            q = p / (m * n ** (m - 1))  # wiring probability
        else:
            q = p * n / (m * comb(n, m))
    elif p_type == "prob":
        q = p
    else:
        raise XGIError("Invalid p_type!")

    if q > 1 or q < 0:
        raise XGIError("Probability not in [0, 1].")

    if q == 1 and not multiedges:
        return complete_hypergraph(n, order=m - 1)
    if q == 0:
        H = empty_hypergraph()
        H.add_nodes_from(range(n))
        return H

    H = empty_hypergraph()
    H.add_nodes_from(range(n))

    if multiedges:
        max_index = n**m
        f = _index_to_edge_prod
    else:
        max_index = comb(n, m, exact=True)
        f = _index_to_edge_comb

    index = np.random.geometric(q) - 1  # -1 b/c zero indexing
    while index <= max_index:
        e = set(f(index, n, m))
        # if f corresponds to _index_to_edge_prod,
        # edge ids are not guaranteed to be unique
        # and when casting to a set, they will no
        # longer be of size m.
        # for instance (0, 0, 0) becomes {0}
        # if we accept these edges, the hypergraph
        # will not longer be uniform, so we discard them.
        if len(e) == m:
            H.add_edge(e)
        # We no longer subtract 1 because if we did, the minimum
        # value of the right-hand side would be zero, meaning that
        # we sample the same index multiple times.
        index += np.random.geometric(q)
    return H


def _index_to_edge_prod(index, n, m):
    """Generate a hyperedge from an index given the
    number of nodes and size of hyperedges.

    In this method, it treats each edge permutation as distinct, which can
    lead to multiedges and loopy edges, especially for dense hypergraphs.
    Imagine that there is a hypergraph with 4 nodes and an edge size of 3.
    We write out each edge (allowing duplicate entries) incrementing the last entry first,
    followed by the second-to-last entry and so on, with each edge corresponding to an index
    starting at zero. For example, (0, 0, 0) has index 0, (0, 0, 1) has index 1,
    (0, 0, 2) has index 2, (0, 0, 3) has index 3, (0, 1, 0) has index 4, and so on.
    This function will, for instance,
    return (0, 0, 3) for index 3, network size 4, and edge size 3.

    Because hypergraphs in XGI only store edges as sets, the edge (0, 0, 0),
    for example, generated by this function will be mapped to {0}. However,
    because this is explicitly a *uniform* method, we discard these edges.
    For sparse networks, this is a rare occurrence and this method offers
    an order of magnitude speedup.

    Parameters
    ----------
    index : int > 0
        The index of the hyperedge in the list of all possible hyperedges.
    n : int > 0
        The number of nodes
    m : int > 0
        The hyperedge size.

    Returns
    -------
    list
        The hyperedge to which that index corresponds

    See Also
    --------
    _index_to_edge_partition
    _index_to_edge_comb

    References
    ----------
    https://stackoverflow.com/questions/53834707/element-at-index-in-itertools-product
    """
    return [(index // (n**r) % n) for r in range(m - 1, -1, -1)]


def _index_to_edge_comb(index, n, m):
    """Generate a hyperedge from an index given the number of nodes and size of hyperedges.

    Imagine that there is a hypergraph with 4 nodes and an edge size of 3.
    We write out each edge incrementing the last entry first, followed by the
    second-to-last entry and so on, with each edge corresponding to an index
    starting at zero. For example, (0, 1, 2) has index 0, (0, 1, 3) has index 0,
    (0, 2, 3) has index 2, and (1, 2, 3) has index 3. This function will, for instance,
    return (0, 2, 3) for index 2, network size 4, and edge size 3.


    In this function, we prohibit multiedges, so each edge corresponds to a
    unique index.

    Parameters
    ----------
    index : int >= 0
        The index of the hyperedge in the list of all possible hyperedges.
    n : int > 0
        The number of nodes
    m : int > 0
        The hyperedge size.

    Returns
    -------
    list
        The hyperedge to which that index corresponds

    See Also
    --------
    _index_to_edge_partition
    _index_to_edge_prod

    References
    ----------
    https://math.stackexchange.com/questions/1227409/indexing-all-combinations-without-making-list
    """
    c = []
    r = index + 1  # makes it zero indexed
    j = -1
    for s in range(1, m + 1):
        cs = j + 1
        while r - comb(n - 1 - cs, m - s, exact=True) > 0:
            r -= comb(n - 1 - cs, m - s, exact=True)
            cs += 1
        c.append(cs)
        j = cs
    return c


def _index_to_edge_partition(index, partition_sizes, m):
    """Generate a hyperedge from an index given the
    number of nodes, size of hyperedges, and community sizes.

    Imagine that there is a hypergraph with 10 nodes, an edge size of 3,
    and two communities, the first of size 8 and the second of size 2.
    We start out by specifying which community each node belongs to
    and index into each community. For example, suppose the nodes
    belong to communities 1, 1, and 2. Thene write out each edge
    (allowing duplicate entries) incrementing the last entry first,
    followed by the second-to-last entry and so on, with each edge
    corresponding to an index starting at zero. For example, (0, 0, 0) has index 0,
    (0, 0, 1) has index 1, (0, 1, 0) has index 2, (0, 1, 1) has index 3,
    (0, 2, 0) has index 4, and so on. These are indices in each partition,
    however, and we need the original labels of each node in each partition
    to recover the nodes in each edge.

    Parameters
    ----------
    index : int > 0
        The index of the hyperedge in the list of all possible hyperedges.
    partition_sizes : list or numpy array
        The sizes of the partitions to which the nodes belong.
    m : int > 0
        The hyperedge size.

    Returns
    -------
    list
        The indices in each partition to which that index corresponds

    See Also
    --------
    _index_to_edge_prod
    _index_to_edge_comb

    """
    try:
        return [
            int(index // np.prod(partition_sizes[r + 1 :]) % partition_sizes[r])
            for r in range(m)
        ]
    except KeyError:
        raise Exception("Invalid parameters")
