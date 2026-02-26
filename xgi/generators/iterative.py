"""Generate iterative hypergraphs."""

from ..core import SimplicialComplex

__all__ = [
    "pseudofractal_simplicial_complex",
    "apollonian_complex",
    "network_geometry_flavor",
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
    network_geometry_flavor

    References
    ----------
    Nurisso, M., Morandini, M., Lucas, M., Vaccarino, F., Gili, T., & Petri, G. (2024).
    "Higher-order Laplacian Renormalization."
    arXiv preprint arXiv:2401.11298.
    https://arxiv.org/abs/2401.11298
    """

    S = SimplicialComplex()

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
    network_geometry_flavor

    References
    ----------
    Nurisso, M., Morandini, M., Lucas, M., Vaccarino, F., Gili, T., & Petri, G. (2024).
    "Higher-order Laplacian Renormalization."
    arXiv preprint arXiv:2401.11298.
    https://arxiv.org/abs/2401.11298
    """

    S = SimplicialComplex()

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


def network_geometry_flavor(
    order, s, beta, n_iter, energy_distribution=None, seed=None
):
    """
    Generate a Network Geometry with Flavor (NGF) simplicial complex.

    The model grows a d-dimensional simplicial complex (where d is `order`) by iteratively attaching
    d-simplices to existing (d-1)-simplices, with attachment probabilities controlled
    by the flavor parameter `s` and an energy-based selection process.

    Parameters
    ----------
    order : int
        The order of the simplices to add.
    s : int
        The flavor parameter (-1, 0, or 1).
    beta : float
        The inverse temperature parameter controlling randomness.
    n_iter : int
        The total number of d-simplices to generate.
    energy_dist : callable, optional
        A function to sample vertex energies (default: uniform [0,10)).
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    S : xgi.SimplicialComplex
        The generated NGF simplicial complex.

    See also
    --------
    apollonian_complex
    pseudofractal_simplicial_complex

    References
    ----------
    Bianconi, G., & Rahmede, C. (2016).
    "Network geometry with flavor: from complexity to quantum geometry."
    Physical Review E, 93(3), 032315.
    https://arxiv.org/abs/1511.04539
    """
    if seed is not None:
        np.random.seed(seed)

    # initialize the hypergraph
    S = xgi.SimplicialComplex()

    # assign energies to vertices
    if energy_distribution is None:
        energy_distribution = lambda: np.random.uniform(0, 9)

    energy_nodes = {}

    # create initial d-simplex
    initial_simplex = list(range(order + 1))
    for node in initial_simplex:
        energy_nodes[node] = energy_distribution()
    S.add_simplex(initial_simplex)

    # track (d-1)-simplices and their counts
    face_counts = {}

    def count_face(face):
        """Adds or updates a (d-1)-simplex count."""
        face = tuple(sorted(face))
        if face in face_counts:
            face_counts[face] += 1
        else:
            face_counts[face] = 1

    # initialize (d-1)-simplices from the first simplex
    for face in xgi.subfaces([initial_simplex], order=order - 1):
        count_face(face)

    # iterative growth
    for it in range(order + 2, order + 2 + n_iter):
        # compute attachment probabilities
        Z = 0
        probs = {}

        for face, count in face_counts.items():
            energy = sum(energy_nodes[node] for node in face)
            weight = np.exp(-beta * energy) * (1 + s * (count - 1))
            if s == -1 and count >= 2:
                weight = 0  # Prevent further attachment to these faces
            probs[face] = weight
            Z += weight

        # normalize probabilities
        if Z == 0:
            break  # no valid attachment sites left

        for face in probs:
            probs[face] /= Z

        # choose a (d-1)-simplex to attach the new simplex
        chosen_idx = np.random.choice(len(probs), p=list(probs.values()))
        chosen_face = list(probs.keys())[chosen_idx]

        # add new node and new simplex
        new_node = it
        energy_nodes[new_node] = energy_distribution()
        new_simplex = list(chosen_face) + [new_node]
        S.add_simplex(new_simplex)

        # update face counts
        for face in xgi.subfaces([new_simplex], order=order - 1):
            count_face(face)

    return S
