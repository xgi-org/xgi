import csv
import hypergraph as hg
from hypergraph.exception import HypergraphError
from ast import literal_eval

__all__ = [
    "read_edgelist",
    "write_edgelist",
    "read_weighted_edgelist",
    "write_weighted_edgelist",
]


def generate_edgelist(H, delimiter=" ", data=True):
    if data is True:
        for id in H.edges:
            e = *list(H.edges[id]), dict(H._edge_attr[id])
            yield delimiter.join(map(str, e))
    elif data is False:
        for id in H.edges:
            e = list(H.edges[id])
            yield delimiter.join(map(str, e))
    else:
        for id in H.edges:
            e = list(H.edges[id])
            try:
                e.extend([H._edge_attr[id][k] for k in data])
            except KeyError:
                pass  # missing data for this edge, should warn?
            yield delimiter.join(map(str, e))


def write_edgelist(H, path, delimiter=" ", data=True, encoding="utf-8"):
    with open(path, "wb") as file:
        for line in generate_edgelist(H, delimiter, data):
            line += "\n"
            file.write(line.encode(encoding))


def write_weighted_edgelist(H, path, delimiter=" ", encoding="utf-8"):
    write_edgelist(H, path, delimiter=delimiter, data=("weight",), encoding=encoding)


def read_weighted_edgelist(
    path,
    comments="#",
    delimiter=None,
    create_using=None,
    nodetype=None,
    encoding="utf-8",
):
    return read_edgelist(
        path,
        comments=comments,
        delimiter=delimiter,
        create_using=create_using,
        nodetype=nodetype,
        data=(("weight", float),),
        encoding=encoding,
    )


def read_edgelist(
    path,
    comments="#",
    delimiter=None,
    create_using=None,
    nodetype=None,
    data=True,
    edgetype=None,
    encoding="utf-8",
):
    with open(path, "rb") as file:
        lines = (
            line if isinstance(line, str) else line.decode(encoding) for line in file
        )
        return parse_edgelist(
            lines,
            comments=comments,
            delimiter=delimiter,
            create_using=create_using,
            nodetype=nodetype,
            data=data,
        )


def parse_edgelist(
    lines, comments="#", delimiter=None, create_using=None, nodetype=None, data=True
):
    H = hg.empty_graph(create_using)
    for line in lines:
        if comments is not None:
            p = line.find(comments)
            if p >= 0:
                line = line[:p]
            if not line:
                continue
        s = line.strip().split(delimiter)

        if data is False:
            # no data or data type specified
            edgedata = {}
        elif data is True:
            # no edge types specified
            try:  # try to evaluate as dictionary
                if delimiter == ",":
                    edgedata_str = ",".join(d)
                else:
                    edgedata_str = " ".join(d)
                edgedata = dict(literal_eval(edgedata_str.strip()))
            except Exception as e:
                raise TypeError(
                    f"Failed to convert edge data ({d}) to dictionary."
                ) from e
        else:
            try:
                d = s[-len(data) :]
                edge = s[: -len(data)]
            except:
                raise HypergraphError("Too many data columns specified.")
            edgedata = {}
            for (edge_key, edge_type), edge_value in zip(data, d):
                try:
                    edge_value = edge_type(edge_value)
                except Exception as e:
                    raise TypeError(
                        f"Failed to convert {edge_key} data {edge_value} "
                        f"to type {edge_type}."
                    ) from e
                edgedata.update({edge_key: edge_value})

        if nodetype is not None:
            try:
                edge = [nodetype(node) for node in edge]
            except Exception as e:
                raise TypeError(f"Failed to convert nodes to type {nodetype}.") from e

        H.add_edge(edge, **edgedata)
    return H
