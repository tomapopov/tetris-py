from abc import ABC, abstractmethod


class Scorer(ABC):
    """
    Abstract scorer class with an add_to_score method.
    This can be subclassed to implement specific scoring systems.
    """

    def __init__(self):
        self._score = 0

    @abstractmethod
    def add_to_score(self, lines_cleared: int, level: int) -> None:
        """
        Increments the score based on the type of scoring system
        :param lines_cleared: number of lines cleared
        :param level: current level the player is on
        :return: Nonw
        """
        ...

    @property
    def score(self) -> int:
        return self._score


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
    def add_to_score(self, lines_cleared: int, level: int) -> None:
        # Note 'level' is not used here
        assert 1 <= lines_cleared <= 4, f"Lines cleared should be 1-4, can't score {lines_cleared}!"
        self._score += self._LINES_TO_POINTS[lines_cleared]

