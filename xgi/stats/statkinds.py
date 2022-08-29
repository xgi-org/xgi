"""Kinds of stats."""

from enum import Enum, auto


__all__ = [
    "StatKinds",
]


class StatKinds(Enum):
    CATEGORICAL = auto()
    NUMERICAL = auto()


CATEGORICAL = StatKinds.CATEGORICAL
NUMERICAL = StatKinds.NUMERICAL
