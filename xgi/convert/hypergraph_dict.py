from ..exception import XGIError
from ..generators import empty_hypergraph

__all__ = ["dict_to_hypergraph"]


def dict_to_hypergraph(data, nodetype=None, edgetype=None, max_order=None):
    """
    A function to read a file in a standardized JSON format.

    Parameters
    ----------
    data: dict
        A dictionary in the hypergraph JSON format
    nodetype: type, optional
        Type that the node IDs will be cast to
    edgetype: type, optional
        Type that the edge IDs will be cast to
    max_order: int, optional
        Maximum order of edges to add to the hypergraph

    Returns
    -------
    A Hypergraph object
        The loaded hypergraph

    Raises
    ------
    XGIError
        If the JSON is not in a format that can be loaded.

    See Also
    --------
    read_json

    """
    H = empty_hypergraph()
    try:
        H._hypergraph.update(data["hypergraph-data"])
    except KeyError:
        raise XGIError("Failed to get hypergraph data attributes.")

    try:
        for id, dd in data["node-data"].items():
            if nodetype is not None:
                try:
                    id = nodetype(id)
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert edge IDs to type {nodetype}."
                    ) from e
            H.add_node(id, **dd)
    except KeyError:
        raise XGIError("Failed to import node attributes.")

    try:
        for id, edge in data["edge-dict"].items():
            if max_order and len(edge) > max_order + 1:
                continue
            if edgetype is not None:
                try:
                    id = edgetype(id)
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert the edge with ID {id} to type {edgetype}."
                    ) from e

            if nodetype is not None:
                try:
                    edge = {nodetype(n) for n in edge}
                except ValueError as e:
                    raise TypeError(
                        f"Failed to convert nodes to type {nodetype}."
                    ) from e
            H.add_edge(edge, id)

    except KeyError as e:
        raise XGIError("Failed to import edge dictionary.") from e

    try:
        if edgetype is None:
            edge_data = {
                key: val for key, val in data["edge-data"].items() if key in H.edges
            }
        else:
            edge_data = {
                edgetype(e): dd
                for e, dd in data["edge-data"].items()
                if edgetype(e) in H.edges
            }

        H.set_edge_attributes(edge_data)
    except KeyError as e:
        raise XGIError("Failed to import edge attributes.") from e

    return H
