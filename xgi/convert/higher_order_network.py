"""Methods for converting to higher-order network objects."""

from copy import deepcopy

import pandas as pd
from numpy import matrix, ndarray
from scipy.sparse import (
    coo_array,
    coo_matrix,
    csc_array,
    csc_matrix,
    csr_array,
    csr_matrix,
    lil_array,
    lil_matrix,
)

from ..algorithms.properties import max_edge_order
from ..core import DiHypergraph, Hypergraph, SimplicialComplex
from ..exception import XGIError
from ..generators import empty_dihypergraph, empty_hypergraph, empty_simplicial_complex
from .hyperedges import from_hyperedge_dict, from_hyperedge_list
from .incidence import from_incidence_matrix
from .pandas import from_bipartite_pandas_dataframe
from .simplex import from_simplex_dict

__all__ = [
    "to_hypergraph",
    "to_dihypergraph",
    "to_simplicial_complex",
    "cut_to_order",
]


def to_hypergraph(data, create_using=None):
    """Make a hypergraph from a known data structure.

    The preferred way to call this is automatically from the class constructor.

    Parameters
    ----------
    data : object to be converted
        Current known types are:
         * a Hypergraph object
         * a SimplicialComplex object
         * list-of-iterables
         * dict-of-iterables
         * Pandas DataFrame (bipartite edgelist)
         * numpy matrix
         * numpy ndarray
         * scipy sparse matrix
    create_using : Hypergraph constructor, optional (default=Hypergraph)
        Hypergraph type to create. If hypergraph instance, then cleared before
        populated.

    Returns
    -------
    Hypergraph object
        A hypergraph constructed from the data

    See Also
    --------
    ~xgi.utils.utilities.from_max_simplices : Constructs a hypergraph from the maximal simplices of a simplicial complex.

    """
    if data is None:
        return empty_hypergraph(create_using)

    elif isinstance(data, Hypergraph) and not isinstance(data, SimplicialComplex):
        H = empty_hypergraph(create_using)
        H.add_nodes_from((n, attr) for n, attr in data.nodes.items())
        ee = data.edges
        H.add_edges_from((ee.members(e), e, deepcopy(attr)) for e, attr in ee.items())
        H._net_attr = deepcopy(data._net_attr)
        return H

    elif isinstance(data, DiHypergraph):
        H = empty_hypergraph(create_using)
        H.add_nodes_from((n, attr) for n, attr in data.nodes.items())
        ee = data.edges
        H.add_edges_from((ee.members(e), e, deepcopy(attr)) for e, attr in ee.items())
        H._net_attr = deepcopy(data._net_attr)
        if not isinstance(create_using, DiHypergraph):
            return H

    elif isinstance(data, SimplicialComplex):
        H = empty_hypergraph(create_using)
        H.add_nodes_from((n, attr) for n, attr in data.nodes.items())
        ee = data.edges
        H.add_edges_from((ee.members(e), e, deepcopy(attr)) for e, attr in ee.items())
        H._net_attr = deepcopy(data._net_attr)
        return H

    elif isinstance(data, list):
        # edge list
        result = from_hyperedge_list(data, create_using)
        if not isinstance(create_using, Hypergraph):
            return result

    elif isinstance(data, pd.DataFrame):
        result = from_bipartite_pandas_dataframe(data, create_using)
        if not isinstance(create_using, Hypergraph):
            return result

    elif isinstance(data, dict):
        # edge dict in the form we need
        result = from_hyperedge_dict(data, create_using)
        if not isinstance(create_using, Hypergraph):
            return result

    elif isinstance(
        data,
        (
            ndarray,
            matrix,
            csr_array,
            csc_array,
            coo_array,
            lil_array,
            csr_matrix,
            csc_matrix,
            coo_matrix,
            lil_matrix,
        ),
    ):
        from_incidence_matrix(data, create_using)

    else:
        raise XGIError("Input data has unsupported type.")


def to_dihypergraph(data, create_using=None):
    """Make a dihypergraph from a known data structure.

    The preferred way to call this is automatically from the class constructor.

    Parameters
    ----------
    data : object to be converted
        Current known types are:
         * a DiHypergraph object
         * a SimplicialComplex object
         * list-of-iterables
         * dict-of-iterables
         * Pandas DataFrame (bipartite edgelist)
         * numpy matrix
         * numpy ndarray
         * scipy sparse matrix
    create_using : Hypergraph constructor, optional (default=Hypergraph)
        Hypergraph type to create. If hypergraph instance, then cleared before populated.

    Returns
    -------
    Hypergraph object
        A hypergraph constructed from the data

    """
    if data is None:
        return empty_dihypergraph(create_using)

    elif isinstance(data, DiHypergraph):
        H = empty_dihypergraph(create_using)
        H.add_nodes_from((n, attr) for n, attr in data.nodes.items())
        ee = data.edges
        H.add_edges_from((ee.dimembers(e), e, deepcopy(attr)) for e, attr in ee.items())
        H._net_attr = deepcopy(data._net_attr)
        if not isinstance(create_using, DiHypergraph):
            return H

    elif isinstance(data, list):
        # edge list
        result = from_hyperedge_list(data, create_using)
        if not isinstance(create_using, DiHypergraph):
            return result

    elif isinstance(data, dict):
        # edge dict in the form we need
        result = from_hyperedge_dict(data, create_using)
        if not isinstance(create_using, DiHypergraph):
            return result

    else:
        raise XGIError("Input data has unsupported type.")


from ..generators import empty_simplicial_complex


def to_simplicial_complex(data, create_using=None):
    """Make a hypergraph from a known data structure.
    The preferred way to call this is automatically
    from the class constructor.

    Parameters
    ----------
    data : object to be converted
        Current known types are:
         * a SimplicialComplex object
         * a Hypergraph object
         * list-of-iterables
         * dict-of-iterables
         * Pandas DataFrame (bipartite edgelist)
         * numpy matrix
         * numpy ndarray
         * scipy sparse matrix
    create_using : Hypergraph graph constructor, optional (default=Hypergraph)
        Hypergraph type to create. If hypergraph instance, then cleared before
        populated.

    Returns
    -------
    Hypergraph object
        A hypergraph constructed from the data

    """

    if data is None:
        return empty_simplicial_complex(create_using)

    elif isinstance(data, SimplicialComplex):
        H = empty_simplicial_complex(create_using)
        H.add_nodes_from((n, attr) for n, attr in data.nodes.items())
        ee = data.edges
        H.add_simplices_from(
            (ee.members(e), e, deepcopy(attr)) for e, attr in ee.items()
        )
        H._net_attr = deepcopy(data._net_attr)
        return H

    elif isinstance(data, Hypergraph):
        H = empty_simplicial_complex(create_using)
        H.add_nodes_from((n, attr) for n, attr in data.nodes.items())
        ee = data.edges
        H.add_simplices_from(
            (ee.members(e), e, deepcopy(attr)) for e, attr in ee.items()
        )
        return H

    elif isinstance(data, list):
        # edge list
        result = from_hyperedge_list(data, create_using)
        if not isinstance(create_using, SimplicialComplex):
            return to_simplicial_complex(result)

    elif isinstance(data, pd.DataFrame):
        result = from_bipartite_pandas_dataframe(data, create_using)
        if not isinstance(create_using, SimplicialComplex):
            return to_simplicial_complex(result)

    elif isinstance(data, dict):
        result = from_simplex_dict(data, create_using)
        if not isinstance(create_using, SimplicialComplex):
            return to_simplicial_complex(result)
    elif isinstance(
        data,
        (
            ndarray,
            matrix,
            csr_array,
            csc_array,
            coo_array,
            lil_array,
            csr_matrix,
            csc_matrix,
            coo_matrix,
            lil_matrix,
        ),
    ):
        # incidence matrix
        raise XGIError(
            "Not implemented: construction of a SimplicialComplex from incidence matrix"
        )
    else:
        raise XGIError("Input data has unsupported type.")


def cut_to_order(H, order):
    """Returns a copy of the higher-order network with edges of order less than or equal to the given order.

    Parameters
    ----------
    H : Hypergraph
        The higher-order network to cut
    order : int
        The order of the edges to keep
    Returns
    -------
    Hypergraph object
        A copy of the higher-order network with edges of order less than or equal to the given order

    """
    _H = H.copy()
    max_order = max_edge_order(H)
    if order > max_order:
        raise XGIError(f"The order must be less than or equal to {max_order}")
    if order != max_order:
        bunch = _H.edges.filterby("order", order, "gt")
        if type(_H) == SimplicialComplex:
            _H.remove_simplex_ids_from(bunch)
        else:
            _H.remove_edges_from(bunch)
    return _H
