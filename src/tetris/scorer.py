# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from abc import ABC, abstractmethod


class Scorer(ABC):
    """
    Abstract scorer class with an add_to_score method.
    This can be subclassed to implement specific scoring systems.
    """

    def __init__(self):
        self.reset()

    def add_to_score(self, lines_cleared: int) -> bool:
        """
        Increments the score based on the type of scoring system
        :param lines_cleared: number of lines cleared
        :param level: current level the player is on
        :return: True if reached new level, False otherwise
        """
        assert 1 <= lines_cleared <= 4, f"Lines cleared should be 1-4, can't score {lines_cleared}!"
        return self._add_to_score(lines_cleared)

    @abstractmethod
    def _add_to_score(self, lines_cleared: int) -> bool:
        ...

    @property
    def score(self) -> int:
        return self._score


    @property
    def level(self) -> int:
        return self._level

    @property
    def lines_cleared(self) -> int:
        return self._lines_cleared

    def reset(self) -> None:
        self._score = 0
        self._level = 0
        self._lines_cleared = 0


class SimpleScorer(Scorer):
    """
    A simple scorer that uses a single rule based on lines cleared,
     without taking level into account.
    """
    _LINES_TO_POINTS = {
        1: 40,
        2: 100,
        3: 300,
        4: 1200,
    }
    _LINES_CLEARED_PER_LEVEL_INCR = 10

    def _add_to_score(self, lines_cleared: int) -> bool:
        self._lines_cleared += lines_cleared
        self._score += self._LINES_TO_POINTS[lines_cleared] * (self.level + 1)
        new_level = self._lines_cleared // self._LINES_CLEARED_PER_LEVEL_INCR
        changed = new_level > self._level
        if changed:
            self._level = new_level
        return changed
