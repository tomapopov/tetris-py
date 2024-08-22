# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from .engine import EngineCLI
from .utils import run_game


def main():
    run_game(EngineCLI)


if __name__ == "__main__":
    main()
