import numpy as np

from ..exception import XGIError
from ..linalg import adjacency_matrix

__all__ = [
    "local_clustering_coefficient",
    "clustering_coefficient",
    "two_node_clustering_coefficient",
]


def local_clustering_coefficient(H):
    """Compute the local clusterin coefficient

    Parameters
    ----------
    H : Hypergraph
        Hypergraph

    Returns
    -------
    dict
        keys are node IDs and values are the
        clustering coefficients.

    References
    ----------
    "Properties of metabolic graphs: biological organization or representation artifacts?"
    by Wanding Zhou and Luay Nakhleh.
    https://doi.org/10.1186/1471-2105-12-132

    "Hypergraphs for predicting essential genes using multiprotein complex data"
    by Florian Klimm, Charlotte M. Deane, and Gesine Reinert.
    https://doi.org/10.1093/comnet/cnaa028

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(3, [1, 1])
    >>> cc = xgi.local_clustering_coefficient(H)
    >>> cc
    {0: 1.0, 1: 1.0, 2: 1.0}
    """
    result = {}

    memberships = H.nodes.memberships()
    members = H.edges.members()

    for n in H.nodes:
        ev = list(memberships[n])
        dv = len(ev)
        if dv == 0:
            result[n] = np.NaN
        elif dv == 1:
            result[n] = 0
        else:
            total_eo = 0
            # go over all pairs of edges pairwise
            for e1 in range(dv):
                edge1 = members[e1]
                for e2 in range(e1):
                    edge2 = members[e2]
                    # set differences for the hyperedges
                    D1 = set(edge1) - set(edge2)
                    D2 = set(edge2) - set(edge1)
                    # if edges are the same by definition the extra overlap is zero
                    if len(D1.union(D2)) == 0:
                        eo = 0
                    else:
                        # otherwise we have to look at their neighbours
                        # the neighbours of D1 and D2, respectively.
                        neighD1 = {i for d in D1 for i in H.nodes.neighbors(d)}
                        neighD2 = {i for d in D2 for i in H.nodes.neighbors(d)}
                        # compute the extra overlap [len() is used for cardinality of edges]
                        eo = (
                            len(neighD1.intersection(D2))
                            + len(neighD2.intersection(D1))
                        ) / len(
                            D1.union(D2)
                        )  # add it up
                    # add it up
                    total_eo = total_eo + eo

            # include normalisation by degree k*(k-1)/2
            result[n] = 2 * total_eo / (dv * (dv - 1))
    return result


def clustering_coefficient(H):
    """Return the clustering coefficients for
    each node in a Hypergraph.

    Parameters
    ----------
    H : Hypergraph
        Hypergraph

    Returns
    -------
    dict
        nodes are keys, clustering coefficients are values.

    References
    ----------
    "Clustering Coefficients in Protein Interaction Hypernetworks"
    by Suzanne Gallagher and Debra Goldberg.
    DOI: 10.1145/2506583.2506635

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(3, [1, 1])
    >>> cc = xgi.clustering_coefficient(H)
    >>> cc
    {0: 1.0, 1: 1.0, 2: 1.0}
    """
    adj, index = adjacency_matrix(H, index=True)
    node_to_index = {n: i for i, n in index.items()}
    mat = adj.dot(adj).dot(adj)
    result = {}
    for n in H.nodes:
        neighbors = len(H.nodes.neighbors(n))
        denom = neighbors * (neighbors - 1) / 2
        if denom == 0:
            result[n] = np.NaN
        else:
            i = node_to_index[n]
            result[n] = 0.5 * mat[i, i] / denom
    return result


def two_node_clustering_coefficient(H, kind="union"):
    """Return the clustering coefficients for
    each node in a Hypergraph.

    This definition averages over all of the
    two-node clustering coefficients involving the node.

    Parameters
    ----------
    H : Hypergraph
        Hypergraph

    Returns
    -------
    dict
        nodes are keys, clustering coefficients are values.

    References
    ----------
    "Clustering Coefficients in Protein Interaction Hypernetworks"
    by Suzanne Gallagher and Debra Goldberg.
    DOI: 10.1145/2506583.2506635

    Example
    -------
    >>> import xgi
    >>> H = xgi.random_hypergraph(3, [1, 1])
    >>> cc = xgi.two_node_clustering_coefficient(H, kind="union")
    >>> cc
    {0: 0.5, 1: 0.5, 2: 0.5}
    """
    result = {}
    memberships = H.nodes.memberships()
    for n in H.nodes:
        neighbors = H.nodes.neighbors(n)
        if not neighbors:
            result[n] = np.NaN
        else:
            result[n] = 0.0
            for v in neighbors:
                result[n] += _uv_cc(n, v, memberships, kind=kind) / len(neighbors)
    return result


def _uv_cc(u, v, memberships, kind="union"):
    """Helper function to compute the two-node
    clustering coefficient.

    Parameters
    ----------
    u : hashable
        First node
    v : hashable
        Second node
    memberships : dict
        node IDs are keys, edge IDs to which they belong
        are values.
    kind : str, optional
        Type of clustering coefficient to compute, by default "union".
        Options:

        - "union"
        - "max"
        - "min"

    Returns
    -------
    float
        The clustering coefficient

    Raises
    ------
    XGIError
        If an invalid clustering coefficient kind
        is specified.

    References
    ----------
    "Clustering Coefficients in Protein Interaction Hypernetworks"
    by Suzanne Gallagher and Debra Goldberg.
    DOI: 10.1145/2506583.2506635
    """
    m_u = memberships[u]
    m_v = memberships[v]

    num = len(m_u.intersection(m_v))

    if kind == "union":
        denom = len(m_u.union(m_v))
    elif kind == "min":
        denom = min(len(m_u), len(m_v))
    elif kind == "max":
        denom = max(len(m_u), len(m_v))
    else:
        raise XGIError("Invalid kind of clustering.")

    if denom == 0:
        return np.NaN

    return num / denom
