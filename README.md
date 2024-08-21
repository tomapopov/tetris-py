# Tetris Game

[![Build](https://github.com/tomapopov/tetris-game/actions/workflows/python-build.yml/badge.svg)](https://github.com/tomapopov/tetris-game/actions/workflows/python-build.yml)

A Tetris game written in Python. 

This has 2 possible interfaces:
- pygame GUI (the default/main version)
- command-line (minimal/basic version with reduced functionality)

## Install

### pip
The preferred way to install Tetris is via pip:

```sh
pip install tetris-py
```

To play, you then simply run:
```
tetris-py
```

For the CLI version, use `tetris-py-cli` instead.

### source
An alternative way is to simply clone the repo and use the `./run` script:

```
git clone git@github.com:tomapopov/tetris-py.git
cd tetris-py
./run
```

For the CLI version, use `./run_cli` instead.


## Dependencies
The GUI version uses the `pygame` package, which is listed in `requirements.txt`.

