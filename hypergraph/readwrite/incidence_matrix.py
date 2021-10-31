import hypergraph as hg
import numpy as np

__all__ = [
    "read_incidence_matrix",
    "write_incidence_matrix",
]


def read_incidence_matrix(
    path, comments="#", delimiter=None, create_using=None, encoding="utf-8"
):
    return hg.from_incidence_matrix(
        np.loadtxt(path, comments=comments, delimiter=delimiter, encoding=encoding),
        create_using=create_using,
    )


def write_incidence_matrix(H, path, delimiter=" ", encoding="utf-8"):
    I = hg.incidence_matrix(H, sparse=False)
    np.savetxt(path, I, delimiter=delimiter, newline="\n", encoding=encoding)
