# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from .engine import EnginePygame
from .utils import run_game


if __name__ == "__main__":
    run_game(EnginePygame)
