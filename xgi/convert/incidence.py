"""Methods for converting to and from an incidence matrix."""

from scipy.sparse import coo_array

from ..exception import XGIError
from ..generators import empty_hypergraph
from ..linalg import incidence_matrix

__all__ = ["from_incidence_matrix", "to_incidence_matrix"]


def from_incidence_matrix(d, create_using=None, nodelabels=None, edgelabels=None):
    """Create a hypergraph from an incidence matrix

    Parameters
    ----------
    d : numpy array or a scipy sparse arrary
        The incidence matrix where rows specify nodes and columns specify edges.
    create_using : Hypergraph constructor, optional
        The hypergraph object to add the data to, by default None
    nodelabels : list or 1D numpy array, optional
        The ordered list of node IDs to map the indices
        of the incidence matrix to, by default None
    edgelabels : list or 1D numpy array, optional
        The ordered list of edge IDs to map the indices
        of the incidence matrix to, by default None

    Returns
    -------
    Hypergraph object
        The constructed hypergraph

    Raises
    ------
    XGIError
        Raises an error if the specified labels are the wrong dimensions

    See Also
    --------
    ~xgi.linalg.hypergraph_matrix.incidence_matrix
    to_incidence_matrix
    """
    I = coo_array(d)
    n, m = I.shape

    if nodelabels is None:
        nodedict = dict(zip(range(n), range(n)))
    elif nodelabels is not None and len(nodelabels) != n:
        raise XGIError("Node dictionary is the wrong size.")
    else:
        nodedict = dict(zip(range(n), nodelabels))

    if edgelabels is None:
        edgedict = dict(zip(range(m), range(m)))
    elif edgelabels is not None and len(edgelabels) != m:
        raise XGIError("Edge dictionary is the wrong size.")
    else:
        edgedict = dict(zip(range(m), edgelabels))

    H = empty_hypergraph(create_using)

    for node, edge in zip(I.row, I.col):
        node = nodedict[node]
        edge = edgedict[edge]
        H.add_node_to_edge(edge, node)

    return H


def to_incidence_matrix(H, sparse=True, index=False):
    """Convert a hypergraph to an incidence matrix.

    Parameters
    ----------
    H : Hypergraph object
        The hypergraph of interest
    sparse : bool, optional
        Whether the constructed incidence matrix
        should be sparse, by default True
    index : bool, optional
        Whether to return the corresponding
        node and edge labels, by default False

    Returns
    -------
    numpy.ndarray or scipy csr_array
        The incidence matrix
    dict
        The dictionary mapping indices to node IDs, if index is True
    dict
        The dictionary mapping indices to edge IDs, if index is True

    See Also
    --------
    ~xgi.linalg.hypergraph_matrix.incidence_matrix
    from_incidence_matrix
    """
    return incidence_matrix(H, sparse=sparse, index=index)
