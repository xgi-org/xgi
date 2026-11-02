"""Generate growing simplicial complexes."""

from inspect import Parameter, signature

import numpy as np

from ..core import SimplicialComplex
from ..utils.utilities import subfaces

__all__ = [
    "pseudofractal_simplicial_complex",
    "apollonian_complex",
    "network_geometry_flavor",
]


def pseudofractal_simplicial_complex(order, n_iter):
    r"""
    Generate the pseudofractal simplicial complex of order `order`.

    Starting with a single d-simplex (d = `order`), at each iteration a new
    node is attached to every existing (d-1)-simplex, forming a new d-simplex
    (with all its subfaces). This process is deterministic.

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

    Raises
    ------
    ValueError
        If `order` is less than 2.

    Notes
    -----
    The size grows exponentially with `n_iter`. After :math:`t` iterations, the
    complex has :math:`((d+1)^{t+1} - 1)/d` simplices of order :math:`d`, i.e.,
    :math:`\mathcal{O}((d+1)^t)`, and :math:`d` more nodes than that.
    For example, ``order=2, n_iter=10`` gives 88,573 triangles and
    ``order=3, n_iter=10`` gives 1,398,101 tetrahedra.

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

    if order < 2:
        raise ValueError("order must be at least 2.")

    S = SimplicialComplex()

    # initialize the first d-simplex
    first_simplex = tuple(range(order + 1))
    S.add_simplex(first_simplex)

    # generate simplices iteratively
    for it in range(1, n_iter + 1):
        # Find all (order - 1)-simplices present in the complex
        nodes = S.nodes
        subfaces = S.edges.filterby("order", order - 1).members(dtype=list)
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
    r"""
    Generate the apollonian complex of order `order`.

    Starting with a single d-simplex (d = `order`), at each iteration a new
    node is attached to every (d-1)-simplex that contains a node added in the
    previous iteration, forming a new d-simplex (with all its subfaces).
    This process is deterministic.

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

    Raises
    ------
    ValueError
        If `order` is less than 2.

    Notes
    -----
    The size grows exponentially with `n_iter`, but more slowly than for
    :func:`pseudofractal_simplicial_complex`. After :math:`t` iterations, the
    complex has :math:`1 + (d+1)(d^t - 1)/(d-1)` simplices of order :math:`d`,
    i.e., :math:`\mathcal{O}(d^t)`, and :math:`d` more nodes than that.
    For example, ``order=2, n_iter=10`` gives 3,070 triangles and
    ``order=3, n_iter=10`` gives 118,097 tetrahedra.

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

    if order < 2:
        raise ValueError("order must be at least 2.")

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
        subfaces_previous_iter = S.edges.filterby("order", order - 1).members(
            dtype=list
        )

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
    r"""
    Generate a Network Geometry with Flavor (NGF) simplicial complex.

    The model grows a d-dimensional simplicial complex (d = `order`), starting
    from a single d-simplex. At each iteration, a new node is attached to an
    existing (d-1)-simplex :math:`\alpha`, forming a new d-simplex (with all
    its subfaces). Which (d-1)-simplex is chosen depends on the energies of
    its nodes and on the flavor `s`, which sets whether (d-1)-simplices
    already shared by several d-simplices are forbidden (``s=-1``), neutral
    (``s=0``), or favored (``s=1``).

    Each node :math:`i` gets a fixed energy :math:`\epsilon_i`, drawn from
    `energy_distribution` when it is added. The energy of a (d-1)-simplex
    is the sum of the energies of its nodes,
    :math:`\epsilon_\alpha = \sum_{i \in \alpha} \epsilon_i`. At each
    iteration, :math:`\alpha` is chosen with probability

    .. math::

        \Pi_\alpha \propto e^{-\beta \epsilon_\alpha} (1 + s\, n_\alpha),

    where :math:`n_\alpha` is the number of d-simplices containing
    :math:`\alpha`, minus one. There is no energy threshold: lower-energy
    (d-1)-simplices are more likely to be chosen, and `beta` sets how strongly.
    For ``beta=0``, energies play no role.

    The flavor `s` sets how the choice depends on :math:`n_\alpha`:

    * ``s=-1``: only (d-1)-simplices contained in a single d-simplex can be
      chosen, so each one ends up in at most two d-simplices. The result is a
      discrete manifold.
    * ``s=0``: the choice depends on the energies only.
    * ``s=1``: (d-1)-simplices contained in many d-simplices are more likely
      to be chosen (preferential attachment).

    Parameters
    ----------
    order : int
        The order d of the simplices to add. Must be at least 1.
    s : {-1, 0, 1}
        The flavor parameter.
    beta : float
        The inverse temperature. Higher values favor low-energy
        (d-1)-simplices more strongly.
    n_iter : int
        The number of new nodes (and d-simplices) to add.
    energy_distribution : callable, optional
        A function that returns one node energy. It can either take a
        :class:`numpy.random.Generator` as its only argument, e.g.
        ``lambda rng: rng.exponential(1.0)``, in which case energies are
        reproducible with `seed`, or take no argument, e.g.
        ``lambda: np.random.exponential(1.0)``, in which case it handles its
        own randomness. By default, energies are uniform in [0, 10).
    seed : int, numpy.random.Generator, or None, optional
        The seed for the random number generator. By default, None.

    Returns
    -------
    S : xgi.SimplicialComplex
        The generated NGF simplicial complex.

    Raises
    ------
    ValueError
        If `order` is less than 1 or `s` is not -1, 0, or 1.

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
    if order < 1:
        raise ValueError("order must be at least 1.")
    if s not in {-1, 0, 1}:
        raise ValueError("s must be -1, 0, or 1.")

    rng = np.random.default_rng(seed)

    if energy_distribution is None:
        sample_energy = lambda: rng.uniform(0, 10)
    elif _n_required_args(energy_distribution) == 0:
        sample_energy = energy_distribution
    else:
        sample_energy = lambda: energy_distribution(rng)

    S = SimplicialComplex()

    # create initial d-simplex
    initial_simplex = list(range(order + 1))
    energy_nodes = {node: sample_energy() for node in initial_simplex}
    S.add_simplex(initial_simplex)

    # number of d-simplices attached to each (d-1)-simplex
    face_counts = {}

    def count_faces(simplex):
        for face in subfaces([simplex], order=order - 1):
            face = tuple(sorted(face))
            face_counts[face] = face_counts.get(face, 0) + 1

    count_faces(initial_simplex)

    for new_node in range(order + 1, order + 1 + n_iter):
        # attachment weights exp(-beta * energy) * (1 + s * (count - 1)),
        # computed in log space to avoid underflow at large beta
        faces = []
        log_weights = []
        for face, count in face_counts.items():
            multiplicity = 1 + s * (count - 1)
            if multiplicity <= 0:
                continue  # s = -1: face already shared by two simplices
            energy = sum(energy_nodes[node] for node in face)
            faces.append(face)
            log_weights.append(-beta * energy + np.log(multiplicity))

        log_weights = np.array(log_weights)
        probs = np.exp(log_weights - log_weights.max())
        probs /= probs.sum()

        # attach a new node to the chosen (d-1)-simplex
        chosen_face = faces[rng.choice(len(faces), p=probs)]
        energy_nodes[new_node] = sample_energy()
        new_simplex = list(chosen_face) + [new_node]
        S.add_simplex(new_simplex)
        count_faces(new_simplex)

    return S


def _n_required_args(func):
    """Number of positional arguments `func` needs (0 if it cannot be inspected)."""
    try:
        params = signature(func).parameters.values()
    except (TypeError, ValueError):
        return 0
    return sum(
        p.default is Parameter.empty
        and p.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
        for p in params
    )
