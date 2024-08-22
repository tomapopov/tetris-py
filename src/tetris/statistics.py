from collections import defaultdict
from typing import Dict

from .piece import Piece


class Statistics:

    def __init__(self):
        self._shape_counts: Dict[str, int] = defaultdict(int)

    def inc_count(self, piece: Piece) -> None:
        self._shape_counts[piece.letter] += 1

    @property
    def shape_counts(self) -> Dict[str, int]:
        return self._shape_counts
