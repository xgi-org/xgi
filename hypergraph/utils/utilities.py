from collections import defaultdict


class HypergraphCounter:
    def __init__(self):
        self._count = 0

    def __call__(self):
        temp = self._count
        self._count += 1
        return temp


def get_dual(edge_dict):
    node_dict = defaultdict(set)
    for edge_id, members in edge_dict.items():
        for node in members:
            node_dict[node].add(edge_id)

    return node_dict
