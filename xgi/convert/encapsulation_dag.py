from ..exception import XGIError

import networkx as nx

__all__ = ["to_encapsulation_dag"]

def to_encapsulation_dag(H, relations="all"):
    """The encapsulation DAG of the hypergraph.

    An encapsulation DAG is a directed line graph
    where the nodes are hyperedges in H and an edge
    exists between two hyperedges if the larger is
    a subset of the smaller.

    Parameters
    ----------
    H : Hypergraph
        The hypergraph of interest

    Returns
    -------
    LG : networkx.DiGraph
         The line graph associated to the Hypergraph

    References
    ----------

    """

    if not (relations in ["all", "immediate", "empirical"]):
        raise XGIError(f"{relations} not a valid weights option. Choices are "
                       "'all', 'immediate', and 'empirical'.")

    # Construct the dag
    dag = nx.DiGraph()
    # Loop over hyperedges
    for he_idx in H.edges:
        # Add the hyperedge as a node
        dag.add_node(he_idx)
        # Get the hyperedge as a set
        he = H.edges.members(he_idx)
        # Get candidate encapsulation hyperedges
        candidates = _get_candidates(relations, H, he)
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

    # If empirical relations, filter out all edges except those
    # between k and maximum existing k'<k
    if relations == "empirical":
        _empirical_filter(H, dag)

    return dag


def _encapsulated(larger, smaller):
    return len(set(larger).intersection(set(smaller))) == len(smaller)

def _get_candidates(relations, H, he):
    candidates = set()
    for node in he:
        for cand_idx in H.nodes.memberships(node):
            if cand_idx not in candidates:
                cand = H.edges.members(cand_idx)
                if _check_candidate(relations, he, cand):
                    candidates.add(cand_idx)

    return candidates

def _check_candidate(relations, he, cand):
    if relations in ["all", "empirical"]:
        if len(he) != len(cand):
            return True
    elif relations == "immediate":
        if len(he) == len(cand)-1 or len(he)-1 == len(cand):
            return True
    return False

def _empirical_filter(H, dag):
    """
    Filters encapsulation DAG to only include edges between hyperedges
    of size k and the maximum existing k'.
    """
    # Loop over all edges
    for edge_idx in dag:
        preds = list(dag.predecessors(edge_idx))
        if len(preds) > 0:
            # Get the minimum superface size
            min_sup_size = min([len(H.edges.members(cand_idx)) for cand_idx in
                               preds])
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
