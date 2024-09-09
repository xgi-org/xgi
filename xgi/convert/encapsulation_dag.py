import networkx as nx

from ..exception import XGIError

__all__ = ["to_encapsulation_dag", "empirical_subsets_filter"]


def to_encapsulation_dag(H, subset_types="all"):
    """The encapsulation DAG (Directed Acyclic Graph) of
    the hypergraph H.

    An encapsulation DAG is a directed line graph
    where the nodes are hyperedges in H and a directed edge
    exists from a larger hyperedge to a smaller hyperedge if
    the smaller is a subset of the larger.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    subset_types : str, optional
        Type of relations to include. Options are:

        * "all" : all subset relationships
        * "immediate" : only subset relationships between hyperedges of
          adjacent sizes (i.e., edges from k to k-1)
        * "empirical" : A relaxation of the "immediate" option where only
          subset relationships between hyperedges of size k and subsets
          of maximum size k'<k existing in the hypergraph are included.
          For example, a hyperedge of size 5 may have no immediate
          encapsulation relationships with hyperedges of size 4, but may
          encapsulate hyperedegs of size 3, which will be included if
          using this setting (whereas relationships with subsets of size 2
          would not be included).

    Returns
    -------
    LG : networkx.DiGraph
         The line graph associated to the Hypergraph

    Examples
    --------
    >>> import xgi
    >>> from xgi.convert import to_encapsulation_dag, empirical_subsets_filter
    >>> H = xgi.Hypergraph([["a","b","c"], ["b","c","f"], ["a","b"], ["c", "e"], ["a"], ["f"]])
    >>> dag = to_encapsulation_dag(H)
    >>> dag.edges()
    OutEdgeView([(0, 2), (0, 4), (2, 4), (1, 5)])
    >>> dag = to_encapsulation_dag(H, subset_types="immediate")
    >>> dag.edges()
    OutEdgeView([(0, 2), (2, 4)])
    >>> dag = to_encapsulation_dag(H, subset_types="empirical")
    >>> dag.edges()
    OutEdgeView([(0, 2), (2, 4), (1, 5)])

    References
    ----------
    "Encapsulation Structure and Dynamics in Hypergraphs", by Timothy LaRock
    & Renaud Lambiotte. https://arxiv.org/abs/2307.04613

    """
    if not (subset_types in ["all", "immediate", "empirical"]):
        raise XGIError(
            f"{subset_types} not a valid subset_types option. Choices are "
            "'all', 'immediate', and 'empirical'."
        )

    # Construct the dag
    dag = nx.DiGraph()
    # Loop over hyperedges
    for he_idx in H.edges:
        # Add the hyperedge as a node
        dag.add_node(he_idx)
        # Get the hyperedge as a set
        he = H.edges.members(he_idx)
        # Get candidate encapsulation hyperedges
        candidates = _get_candidates(subset_types, H, he)
        # for each candidate
        candidates_checked = set()
        for cand_idx in candidates:
            if cand_idx in candidates_checked:
                continue
            cand = H.edges.members(cand_idx)
            if len(he) > len(cand):
                if _encapsulated(he, cand):
                    dag.add_edge(he_idx, cand_idx)
            elif len(cand) > len(he):
                if _encapsulated(cand, he):
                    dag.add_edge(cand_idx, he_idx)

    # If empirically closest subsets, filter out all edges except those
    # between k and maximum existing k'<k
    if subset_types == "empirical":
        empirical_subsets_filter(H, dag)

    return dag


def _encapsulated(larger, smaller):
    """Test if a larger hyperedge encapsulates a smaller hyperedge.

    Parameters
    ----------
    larger : Set
        larger hyperedge
    smaller : Set
        smaller hyperedge
    Returns
    -------
    _ : Bool
        True if the size of the intersection between larger and smaller is
            the same as the size of smaller.

    """
    return len(set(larger).intersection(set(smaller))) == len(smaller)


def _get_candidates(subset_types, H, he):
    """Get the candidate hyperedges for encapsulation by he based on the subset type.

    Parameters
    ----------
    subset_types : str
        Type of subset relationships
    H : Hypergraph
        The hypergraph
    he : Set
        The hyperedge

    Returns
    -------
    candidates : Set
        A set of hyperedge IDs to check for encapsulation by hyperedge he

    """
    candidates = set()
    for node in he:
        for cand_idx in H.nodes.memberships(node):
            if cand_idx not in candidates:
                cand = H.edges.members(cand_idx)
                if _check_candidate(subset_types, he, cand):
                    candidates.add(cand_idx)

    return candidates


def _check_candidate(subset_types, he, cand):
    """Check whether a hyperedge cand is a candidate to be encapsulated by
    hyperedge he based on subset_types.

    Parameters
    ----------
    subset_types : str
        Type of subset relationships
    he : Set
        The hyperedge
    cand : Set
        The candidate

    Returns
    -------
    is_candidate : bool
        True if cand is a valid candidate to be encapsulated by he, False
        otherwise.
    """
    is_candidate = False
    if subset_types in ["all", "empirical"]:
        if len(he) != len(cand):
            is_candidate = True
    elif subset_types == "immediate":
        if len(he) == len(cand) - 1 or len(he) - 1 == len(cand):
            is_candidate = True
    return is_candidate


def empirical_subsets_filter(H, dag):
    """
    Filters encapsulation DAG of H in place to only include edges between hyperedges
    of size k and the maximum existing k'.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest
    dag : nx.DiGraph
        The encapsulation dag of H constructed with to_encapsulation_dag(H, subset_types="all")

    Returns
    -------
    dag : networkx.DiGraph
         The filtered line graph (also modified in place)

    References
    ----------
    "Encapsulation Structure and Dynamics in Hypergraphs", by Timothy LaRock
    & Renaud Lambiotte. https://arxiv.org/abs/2307.04613

    """
    # Loop over all edges
    for edge_idx in dag:
        preds = list(dag.predecessors(edge_idx))
        if len(preds) > 0:
            # Get the minimum superface size
            min_sup_size = min([len(H.edges.members(cand_idx)) for cand_idx in preds])
            # Keep only the superfaces with that size
            to_remove = []
            for cand_idx in preds:
                if len(H.edges.members(cand_idx)) != min_sup_size:
                    dag.remove_edge(cand_idx, edge_idx)

        # Repeat for subsets
        outs = list(dag.successors(edge_idx))
        if len(outs) > 0:
            max_sub_size = max([len(H.edges.members(sub_idx)) for sub_idx in outs])
            for cand_idx in outs:
                if len(H.edges.members(cand_idx)) != max_sub_size:
                    dag.remove_edge(edge_idx, cand_idx)
    return dag
