import os

from src.AI.path_finding import PathFinder
from src.items.cell import Cell

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "yes"

from typing import cast

import pygame as pg

from src.items.board import Board


def main() -> None:
    _ = pg.init()

    screen = pg.display.set_mode((280, 240))
    clock = pg.time.Clock()
    running: bool = True
    board = Board()

    HARDCODED_BOARD: list[list[int]] = [
        [Cell.AGENT, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        [Cell.EMPTY, Cell.EMPTY, Cell.TARGET, Cell.OBSTACLES, Cell.EMPTY],
        [Cell.EMPTY, Cell.OBSTACLES, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.OBSTACLES, Cell.TARGET],
    ]

    board.setBoard(HARDCODED_BOARD)

    path_finder = PathFinder(board)
    while running:
        # When exit even -> exit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                key = cast(int, event.key)
                if key == pg.K_r:
                    return main()
                if key == pg.K_ESCAPE:
                    running = False
                if key == pg.K_SPACE:
                    path_finder.move()

        # Background
        _ = screen.fill("purple")

        # Items
        board.draw(screen)

        pg.display.flip()

        _ = clock.tick(60)  # Limits FPS to 60


if __name__ == "__main__":
    main()
