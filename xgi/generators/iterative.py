"""Generate iterative hypergraphs."""

import itertools
import operator
import random
import warnings
from functools import reduce

import numpy as np
from scipy.special import comb

from ..exception import XGIError
from ..utils import geometric
from .classic import complete_hypergraph, empty_hypergraph

__all__ = [
    "pseudofractal_simplicial_complex",
    "apollonian_complex",
]


def pseudofractal_simplicial_complex(order, n_iter):
    """
    Generate the pseudofractal simplicial complex of order `order`.

    Starting with a single d-simplex, at each iteration, the function adds new (d+1)-simplices 
    by attaching a new vertex to all existing (d-1)-simplices (as well as all their subfaces). 
    This process is deterministic.

    Parameters
    ----------
        order : int
            The order of the simplices to add (e.g., 2 for triangles, 3 for tetrahedra, etc.).
        n_iter : int
            The number of iterations to generate simplices.

    Returns
    -------
        S : xgi.SimplicialComplex
            Generated simplicial complex

    See also
    --------
    apollonian_complex


    References
    ----------
    Nurisso, M., Morandini, M., Lucas, M., Vaccarino, F., Gili, T., & Petri, G. (2024).   
    "Higher-order Laplacian Renormalization."  
    arXiv preprint arXiv:2401.11298.  
    https://arxiv.org/abs/2401.11298  
    """

    S = xgi.SimplicialComplex()

    # initialize the first d-simplex
    first_simplex = tuple(range(order + 1))
    S.add_simplex(first_simplex)

    # generate simplices iteratively
    for it in range(1, n_iter + 1):
        # Find all (order - 1)-simplices present in the complex
        nodes = S.nodes
        subfaces = S.edges.filterby("order", order - 1).members()
        max_index = max(nodes)
        new_simplices = []

        for subface in subfaces:
            # create a new simplex by adding the new vertex to the existing d-simplex
            max_index += 1  # new vertex index

            new_simplex = (*subface, max_index)
            new_simplices.append(new_simplex)

        S.add_simplices_from(new_simplices)

    return S


def apollonian_complex(order, n_iter):
    """
    Generate the apollonian complex of order `order`.

    Starting with a single d-simplex, at each iteration, the function adds new (d+1)-simplices  
    by attaching a new vertex to (d-1)-simplices that contain at least one newly added node.  
    This process is deterministic and generates a simplicial complex.  


    Parameters
    ----------
        order : int
            The order of the simplices to add (e.g., 2 for triangles, 3 for tetrahedra, etc.).
        n_iter : int
            The maximum iteration to generate simplices.

    Returns
    -------
        S : xgi.SimplicialComplex
            Generated simplicial complex

    See also
    --------
    pseudofractal_simplicial_complex

    References
    ----------
    Nurisso, M., Morandini, M., Lucas, M., Vaccarino, F., Gili, T., & Petri, G. (2024).   
    "Higher-order Laplacian Renormalization."  
    arXiv preprint arXiv:2401.11298.  
    https://arxiv.org/abs/2401.11298
    """
    
    S = xgi.SimplicialComplex()

    # initialize the first d-simplex
    first_simplex = tuple(range(order + 1))
    S.add_simplex(first_simplex)

    new_simplices = [first_simplex]
    new_indices = list(first_simplex)

    # generate simplices iteratively
    for it in range(1, n_iter + 1):
        # find all (order - 1)-simplices present in the complex
        nodes = S.nodes
        subfaces_previous_iter = S.edges.filterby("order", order - 1).members()

        # keep only those attached to new nodes
        subfaces_previous_iter = [
            subface
            for subface in subfaces_previous_iter
            if any(new_index in subface for new_index in new_indices)
        ]

        max_index = max(nodes)
        new_simplices = []
        new_indices = []

        for subface in subfaces_previous_iter:
            # create a new simplex by adding the new vertex to the existing d-simplex
            max_index += 1  # New vertex index

            new_simplex = (*subface, max_index)
            new_simplices.append(new_simplex)
            new_indices.append(max_index)

        S.add_simplices_from(new_simplices)

    return S
