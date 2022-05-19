"""Edge statisics."""

__all__ = [
    "attrs",
    "order",
]


# should close #78
# interacts with #30
# should also close #64, after we implemen the frozen stuff


def attrs(net, bunch, attrs=None):
    if isinstance(attrs, str):
        return {n: net._edge_attr[n][attrs] for n in bunch}
    elif attrs is not None:
        return {n: {a: net._edge_attr[n][a] for a in attrs} for n in bunch}
    else:
        return {n: net._edge_attr[n] for n in bunch}


def order(net, bunch, degree=None):
    if degree is None:
        return {n: len(net._edge[n]) - 1 for n in bunch}
    else:
        return {
            n: len(n for n in net._edge[n] if len(net._node[n]) == degree) - 1
            for n in bunch
        }


def size(net, bunch, degree=None):
    if degree is None:
        return {n: len(net._edge[n]) for n in bunch}
    else:
        return {
            n: len(n for n in net._edge[n] if len(net._node[n]) == degree)
            for n in bunch
        }
