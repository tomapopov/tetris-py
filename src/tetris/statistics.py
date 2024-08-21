from collections import defaultdict
from typing import Dict, Type

from src.tetris.piece import Piece


class Statistics:

    def __init__(self):
        self._shape_counts: Dict[str, int] = defaultdict(int)

    def inc_count(self, shape: Piece):
        self._shape_counts[shape.letter] += 1

    @property
    def shape_counts(self) -> Dict[str, int]:
        return self._shape_counts
