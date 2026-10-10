from enum import IntEnum


class Cell(IntEnum):
    EMPTY = 0
    AGENT = 1
    TARGET = 2
    OBSTACLES = 3
